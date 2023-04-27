import json

def extract_codes(name, codes):
    print(f"enum class {name} {'{'}")

    for index, code in enumerate(codes):
        code_name = code.replace(" ", "_").replace("-", "_").upper()
        print(f"{code_name} = {hex(index)},")

    print("};\n")

def main():
    f = open("protocol.json")
    data = json.load(f)

    print("// --------------------------------------------------")
    print("// Begin generated code from protocol.json")
    print("// --------------------------------------------------")
    print("")

    for type in data:
        print(f"// {type}")
        print(f"enum class {type.upper()} {'{'}")
        for frame in data.get(type):
            frame_name = frame.get("name").replace(" ", "_").upper()
            print(f"{frame_name} = {hex(frame.get('min_id'))},")
        print("};\n")

    for frame in data.get([type for type in data][0]):
        frame_name = frame.get("name").replace(" ", "_").upper()

        for payload in frame.get("payload"):
            bits = payload.get("bits")
            codes = payload.get("codes")

            if bits != None:
                print(f"enum class {frame_name}_SUB_DEVICES {'{'}")
                
                for index, bit in enumerate(bits):
                    bit_name = bit.replace(" ", "_").replace("-", "_").upper()
                    print(f"{bit_name} = {hex(0x01 << index)},")

                print("};\n")

            if codes != None:
                payload_name = payload.get("name").replace(" ", "_").upper()
                extract_codes(payload_name, codes)
    
    for frame in data.get([type for type in data][1]):
        frame_name = frame.get("name").replace(" ", "_").upper()

        for payload in frame.get("payload"):
            codes = payload.get("codes")

            if codes != None:
                payload_name = payload.get("name").replace(" ", "_").upper()
                extract_codes(payload_name, codes)

    print("// --------------------------------------------------")
    print("// END generated code")
    print("// --------------------------------------------------")


if __name__ == "__main__":
    main()