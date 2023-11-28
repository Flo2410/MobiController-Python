# ----------------------------------------------------------------------------------------------------------------------------------------------
# File: updater.py
# Created Date: Tuesday, November 28th 2023, 9:24:09 am
# Author: Florian Hye
# Description: Update the firmware of the STM32 on the hardware controller of the Mobi.
# ----------------------------------------------------------------------------------------------------------------------------------------------

import subprocess
import sys
from logging import INFO
from min.minmon import MINMonitor
from min import MINFrame
from min.PayloadBuilder import PayloadBuilder
import requests
from packaging.version import parse as parse_version
from tempfile import TemporaryDirectory
from tqdm import tqdm
from argparse import ArgumentParser
from os import path

min_mon: MINMonitor = None
temp_dir: TemporaryDirectory = None


def get_installed_firmware_version():
    global min_mon

    min_mon.send_frame(62)  # min_id 62 -> Firmware Info
    receved_frame = None

    # wait for response
    while min_mon._recv_messages.qsize() <= 0:
        pass

    # read response
    while min_mon._recv_messages.qsize() > 0:
        receved_frame: MINFrame = min_mon.recv(block=False)
        # print(f"new Frame: ID: {receved_frame.min_id} len: {len(receved_frame.payload)} payload: 0x{receved_frame.payload.hex()}")

    pb = PayloadBuilder(receved_frame.payload)
    text = pb.read_string()
    version_text = text.split("\n")[1]
    version = version_text.split(":")[1].strip()
    return version


def get_current_version_from_github():
    res = requests.get(
        "https://api.github.com/repos/Flo2410/MobiController-Firmware/releases/latest"
    )

    data = res.json()
    version = data.get("tag_name")
    return version


import os
import requests


def download_current_firmware():
    global temp_dir
    url = "https://github.com/Flo2410/MobiController-Firmware/releases/latest/download/MobiController-Firmware.bin"
    file_name = "MobiController-Firmware.bin"
    temp_dir = TemporaryDirectory()
    file_path = os.path.join(temp_dir.name, file_name)

    res = requests.get(url, stream=True)
    total_size_in_bytes = int(res.headers.get("content-length", 0))
    block_size = 1024  # 1 Kibibyte

    progress_bar = tqdm(total=total_size_in_bytes, unit="iB", unit_scale=True)

    if res.ok:
        # print("saving to", os.path.abspath(file_path))
        with open(file_path, "wb") as f:
            for chunk in res.iter_content(chunk_size=block_size):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
                    progress_bar.update(len(chunk))

        progress_bar.close()
        return file_path
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(res.status_code, res.text))
        return None


def boot_into_bootloader():
    global min_mon

    min_mon.send_frame(60)  # min_id 60 -> Boot into bootloader for flashing
    return True

    # receved_frame = None

    # # wait for response
    # while min_mon._recv_messages.qsize() <= 0:
    #     pass

    # # read response
    # while min_mon._recv_messages.qsize() > 0:
    #     receved_frame: MINFrame = min_mon.recv(block=False)

    # pb = PayloadBuilder(receved_frame.payload)
    # status = pb.read_c_type("uint8_t")

    # if status == 0:
    #     return True
    # else:
    #     print(f"Error booting into bootloader! Got Statuscode: {status}")
    #     return False


def parse_args(parser: ArgumentParser):
    parser.add_argument(
        "-c", "--check", action="store_true", help="Only check the firmware version."
    )
    parser.add_argument(
        "-f", "--force", action="store_true", help="Forcefully update the version."
    )
    parser.add_argument(
        "-p",
        "--port",
        default="/dev/ttyACM0",
        type=str,
        help="Select the port the controller ist connected to. Default: /dev/ttyACM0",
    )
    parser.add_argument(
        "-b",
        "--binary",
        type=str,
        help="Flash a custom .bin file, instead of downloading it from GitHub.",
    )

    return parser.parse_args()


def main():
    global min_mon
    parser = ArgumentParser(
        prog="MobiController Firmware Updater",
        description="Update the firmware of the MobiController STM32.",
    )
    args = parse_args(parser)

    min_mon = MINMonitor(port=args.port, loglevel=INFO)

    firmware_bin_path = None

    if not args.binary:
        installed_version = get_installed_firmware_version()
        current_version = get_current_version_from_github()
        version_check = parse_version(installed_version) == parse_version(
            current_version
        )

        if not args.force or (args.check and args.force):
            if version_check:
                print("You allready have the current version installed!")
                bye()
                return

            print(
                f"There is a newer version available: {installed_version} -> {current_version}\n"
            )

        # if only checking -> exit
        if args.check:
            bye()
            return

        print(f"Upgrading the firmware to {current_version}")
    else:
        firmware_bin_path = path.abspath(args.binary)
        print(f"Flashing binary from: {firmware_bin_path}")

    do_upgrade = input("Do you want to upgrade? [y/N]: ").lower()
    if do_upgrade != "y" and do_upgrade != "j":
        bye()
        return

    if not args.binary:
        firmware_bin_path = download_current_firmware()

    if not firmware_bin_path:
        print("Error downloading the firmware!")
        bye()
        return

    staus = boot_into_bootloader()
    if not staus:
        bye()
        return

    # dfu-util -a 0 -D build/MobiController-Firmware.bin -s 0x08000000:leave
    subprocess.run(
        ["dfu-util", "-a", "0", "-w", "-D", firmware_bin_path, "-s", "0x08000000:leave"]
    )
    bye()


def bye():
    global min_mon, temp_dir

    min_mon.stop()
    if temp_dir:
        temp_dir.cleanup()
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        bye()
