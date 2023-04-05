import json

def main():
    f = open("protocol.json")
    data = json.load(f)

    for type in data:
        print(f"// {type}")
        for frame in data.get(type):
            name = f"{type.replace('s', '').upper()}_"
            name += frame.get("name").replace(" ", "_").upper()
            print(f"#define {name} {hex(frame.get('min_id'))}")
        print("")

if __name__ == "__main__":
    main()