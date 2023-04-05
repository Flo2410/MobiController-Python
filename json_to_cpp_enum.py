import json

def main():
    f = open("protocol.json")
    data = json.load(f)

    for type in data:
        print(f"// {type}")
        print(f"enum {type.upper()} {'{'}")
        for frame in data.get(type):
            name = frame.get("name").replace(" ", "_").upper()
            print(f"{name} = {hex(frame.get('min_id'))},")
        print("};\n")

if __name__ == "__main__":
    main()