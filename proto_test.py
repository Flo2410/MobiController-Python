from min.min import  MINFrame
from min.minmon import MINMonitor
from min.PayloadBuilder import PayloadBuilder
from logging import INFO
import json
from numpy import uint8

min_mon: MINMonitor = None
proto_file = None

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
                bits = value.get("bits")
                if bits != None:
                    print(f"{bits[convert_subdevice_mask_to_index(pb.read_c_type(value.get('c_type')))]}")
                    continue

                print(f"{value.get('name')} - {value.get('c_type')}: {pb.read_c_type(value.get('c_type'))}")
            break;

    # proto_data_imu = [x for x in proto_data if x.get("name") == "imu"][0]

    

def main():
    global min_mon, proto_file

    print("Protokoll Test\n")

    # load the proto json file
    with open("protocol.json") as file:
        proto_file = json.loads(file.read())

    min_mon = MINMonitor(port="/dev/ttyACM1", loglevel=INFO)

    builder = PayloadBuilder()
    # builder.append_uint8(0b01001000)
    builder.append_uint16(1000)

    # imu 
    # min_mon.send_frame(0x20, builder.get_payload())

    # temp
    min_mon.send_frame(36, builder.get_payload())

    # builder.append_uint8(1)
    # min_mon.send_frame(38, builder.get_payload())

    while True:
        while min_mon._recv_messages.qsize() > 0:
            receved_frame: MINFrame = min_mon.recv(block=False)
            decode_frame(receved_frame)
   

def bye():
    global min_mon
    min_mon.stop()
    print("BYE!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        bye()
  