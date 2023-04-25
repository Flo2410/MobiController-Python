# ----------------------------------------------------------------------------------------------------------------------------------------------
# File: cli.py
# Created Date: Thursday, April 6th 2023, 4:06:36 pm
# Author: Florian Hye
# Description: CLI for the Mobi-Contoller 
# ----------------------------------------------------------------------------------------------------------------------------------------------

from min.min import  MINFrame
from min.minmon import MINMonitor
from logging import INFO
import sys
from threading import Thread, Event
from numpy import uint8, float32, ndarray, uint
import numpy as np
import struct
from min.PayloadBuilder import PayloadBuilder
import json

kthread = None
min_mon: MINMonitor = None
proto_file = None

class KeyboardThread(Thread):

    def __init__(self, input_cbk = None, name='keyboard-input-thread'):
        self.input_cbk = input_cbk
        self._stop_event = Event()
        super(KeyboardThread, self).__init__(name=name)
        self.start()

    def run(self):
        while not self._stop_event.is_set():
            self.input_cbk(input("")) #waits to get input + Return
min_mon: MINMonitor = None



def encode_uint(number: uint) -> ndarray:
    return bytes(struct.pack('<H', number))


def encode_float(number: float) -> np.ndarray:
    # convert the float to a uint8 array using tobytes()
    return np.frombuffer(float32(number).tobytes(), dtype=uint8)


def parse_int(string: str) -> uint8:
    try:
        if string.startswith("0x"):
            return int(string, 16)
        elif string.startswith("0b"):
            return int(string, 2)
        else:
            return int(string)
    except ValueError:
        return 0

def parse_payload(arr: list[str]) -> list[uint8]:
    out = []
    for num in arr:
        # check if is int or float:
        if "." in num: # is float
            out.extend(encode_float(num))
        else:
            out.extend(encode_uint(parse_int(num)))
    return out

def convert_subdevice_mask_to_index(mask: uint8) -> uint8:
    for i in range(8):
        current_mask = 0x01 << i
        if (mask & current_mask) == current_mask:
            return i
        
def decode_frame(frame: MINFrame):
    global proto_file
    # print(f"new Frame: ID: {frame.min_id} len: {len(frame.payload)} payload: 0x{frame.payload.hex()}")

    proto_data: list = proto_file.get("data")

    for data in proto_data:
        if data.get("min_id") == frame.min_id:
            print(data.get("name"), end=": ")

            pb = PayloadBuilder(frame.payload)

            for value in data.get("payload"):
                read_value = pb.read_c_type(value.get('c_type'))

                # check for "bits"
                bits = value.get("bits")
                if bits != None:
                    print(f"{bits[convert_subdevice_mask_to_index(read_value)]}")
                    continue
                
                # check for "code". used by status code 
                codes = value.get("codes")
                if codes != None:
                    read_value = f"{read_value} -> {codes[read_value]}"

                print(f"{value.get('name')} - {value.get('c_type')}: {read_value}")
            break;

    # proto_data_imu = [x for x in proto_data if x.get("name") == "imu"][0]

    
def keyboard_callback(inp: str):
    global kthread, min_mon

    if kthread._stop_event.is_set():
        return
    
    if inp == "exit":
        bye()
        return
    
    #evaluate the keyboard input
    arr = inp.split(" ")
    min_id = parse_int(arr.pop(0))

    payload = parse_payload(arr)
    # print(f"min_id: {hex(min_id)}, data: {payload}")
    
    min_mon.send_frame(min_id, bytes(payload))


def main():
    global kthread, min_mon, proto_file

    print("MobiController CLI\n")

        # load the proto json file
    with open("protocol.json") as file:
        proto_file = json.loads(file.read())

    
    min_mon = MINMonitor(port="/dev/ttyACM1", loglevel=INFO)
            
    #start the Keyboard thread
    kthread = KeyboardThread(keyboard_callback)

    while True:
        while min_mon._recv_messages.qsize() > 0:
            receved_frame: MINFrame = min_mon.recv(block=False)
            # print(f"new Frame: ID: {receved_frame.min_id} len: {len(receved_frame.payload)} payload: 0x{receved_frame.payload.hex()}")
            decode_frame(receved_frame)
                
    
def bye():
    global min_mon, kthread

    min_mon.stop()
    kthread._stop_event.set()
    print("BYE!")
    sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        bye()
  

