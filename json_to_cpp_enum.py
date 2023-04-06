import json

def main():
    f = open("protocol.json")
    data = json.load(f)

    for type in data:
        print(f"// {type}")
        print(f"enum class {type.upper()} {'{'}")
        for frame in data.get(type):
            name = frame.get("name").replace(" ", "_").upper()
            print(f"{name} = {hex(frame.get('min_id'))},")
        print("};\n")

    for frame in data.get([type for type in data][0]):
        name = frame.get("name").replace(" ", "_").upper()

        for payload in frame.get("payload"):
            bits = payload.get("bits")
            if bits == None:
                continue

            print(f"enum class {name}_SUB_DEVICES {'{'}")
            
            for index, bit in enumerate(bits):
                bit_name = bit.replace(" ", "_").replace("-", "_").upper()
                print(f"{bit_name} = {hex(0x01 << index)},")

            print("};\n")

if __name__ == "__main__":
    main()