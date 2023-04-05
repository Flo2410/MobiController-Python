import json

def main():
    f = open("protocol.json")
    data = json.load(f)

    for type in data:
        print(f"// {type}")
        for cmd in data.get(type):
            name = cmd.get("name").replace(" ", "_").upper()
            print(f"#define {name} {hex(cmd.get('min_id'))}")
        print("")

if __name__ == "__main__":
    main()