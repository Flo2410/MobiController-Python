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

    for idx, type in enumerate(data):
        print("")

        if idx == 0:
            print("## Befehle (Commands)")
        else:
            print("## Antworten/Daten (Data)")

        print("")

        for frame in data.get(type):
            frame_name = frame.get("name").capitalize()

            print(f"### {frame_name}")
            print("")
            print("| Attribut | Wert |")
            print("| -------- | ---- |")

            for attr in frame:
                if attr != "payload":
                    print(f"| {attr} | {frame.get(attr)} |")

            if len(frame.get("payload")) == 0:
                print(f"| payload | empty |")
                print("")
                continue

            print("")
            print("#### Payload")
            print("{}".format("{: .no_toc }"))
            print("")
            print("| Attribut | Wert |")
            print("| -------- | ---- |")

            for payload_item in frame.get("payload"):
                for entry in payload_item:
                    if entry == "bits" or entry == "codes":
                        string = str(payload_item.get(entry)).replace("'", "")
                        print(f"| {entry} | {string} |")
                        continue

                    print(f"| {entry} | {payload_item.get(entry)} |")

                print("")

    # for frame in data.get([type for type in data][0]):
    #     frame_name = frame.get("name").replace(" ", "_").upper()

    #     for payload in frame.get("payload"):
    #         bits = payload.get("bits")
    #         codes = payload.get("codes")

    #         if bits != None:
    #             print(f"enum class {frame_name}_SUB_DEVICES {'{'}")

    #             for index, bit in enumerate(bits):
    #                 bit_name = bit.replace(" ", "_").replace("-", "_").upper()
    #                 print(f"{bit_name} = {hex(0x01 << index)},")

    #             print("};\n")

    #         if codes != None:
    #             payload_name = payload.get("name").replace(" ", "_").upper()
    #             extract_codes(payload_name, codes)

    # for frame in data.get([type for type in data][1]):
    #     frame_name = frame.get("name").replace(" ", "_").upper()

    #     for payload in frame.get("payload"):
    #         codes = payload.get("codes")

    #         if codes != None:
    #             payload_name = payload.get("name").replace(" ", "_").upper()
    #             extract_codes(payload_name, codes)


if __name__ == "__main__":
    main()
