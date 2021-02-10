import json
import tycho
import sys

data = " ".join(sys.argv[1:]).strip()

if len(data) == 0:
    print("No input given, please specify bytes to debug")
    sys.exit(1)

try:
    data = bytes.fromhex(data)
except:
    print("Failed to parse hex into bytes")
    sys.exit(2)

data_bytes = data
data = tycho.from_bytes(data)
print(json.dumps(data, indent=4))

