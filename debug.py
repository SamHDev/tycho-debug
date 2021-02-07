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
data = tycho.decode(data)


def print_byte(indent, byte: bytes or int, label):
    if isinstance(byte, int):
        byte = bytes([byte])

    for i in range(0, len(byte)):
        if i == 0:
            print_indent(indent, hex(byte[i])[2:].rjust(2, "0") + " - " + label)
        else:
            print_indent(indent, hex(byte[i])[2:].rjust(2, "0") + "")


def print_indent(indent, text):
    print((indent * "\t") + text)


def print_string(indent, value, length_text, offset=1):
    string_data = value.encode("utf-8")

    print_byte(indent, tycho.length.encode_length(len(string_data)), f"{length_text} {len(string_data)}")
    for char in value:
        print_byte(indent + offset, char.encode("utf-8"), f"\"{char}\"")


def print_element(indent, element, prefix=True):
    if isinstance(element, tycho.String):
        if prefix:
            print_byte(indent, 0x1D, "Value::String")
        string_data = element.value.encode("utf-8")

        print_byte(indent + 1, tycho.length.encode_length(len(string_data)), f"String has length {len(string_data)}")
        for char in element.value:
            print_byte(indent + 1, char.encode("utf-8"), f"\"{char}\"")

    elif isinstance(element, tycho.Char):
        if prefix:
            print_byte(indent, 0x1C, "Value::Char")
        char_data = element.value.encode("utf-8")
        print_byte(indent + 1, tycho.length.encode_length(len(element.value)),
                   f"Char has byte length {len(element.value)}")
        print_byte(indent + 1, char_data, f"\'{element.value}\'")

    elif isinstance(element, tycho.Bytes):
        if prefix:
            print_byte(indent, 0x1F, "Value::Bytes")
        print_byte(indent + 1, tycho.length.encode_length(len(element.value)),
                   f"Bytes array has length {len(element.value)}")
        print_byte(indent + 1, element.value, "Byte Array Data")

    elif isinstance(element, tycho.Boolean):
        if prefix:
            print_byte(indent, 0x10, "Value::Boolean")
        if element.value:
            print_byte(indent + 1, 0x01, "true")
        else:
            print_byte(indent + 1, 0x00, "false")

    elif isinstance(element, tycho.values.NumericalValue):
        if prefix:
            print_byte(indent, element.encode_prefix(), "Value::" + str(element.__class__.__name__))
        p = "u"
        if element.signed: p = "i"
        print_byte(indent + 1, element.encode_body(), f"{p}{element.byte_size * 8}({element.value})")

    elif isinstance(element, tycho.elements.Unit):
        if prefix:
            print_byte(indent, 0x00, "Unit")

    elif isinstance(element, tycho.elements.Option):
        if prefix:
            if element.value is None:
                print_byte(indent, 0x20, "Option::None")
            else:
                print_byte(indent, 0x21, "Option::Some")
        print_element(indent + 1, element.value)

    elif isinstance(element, tycho.elements.Array):
        if prefix:
            print_byte(indent, 0x30, "Array")
        print_byte(indent + 1, tycho.length.encode_length(len(element.value)), f"Array has length {len(element.value)}")
        i = 0
        for item in element.value:
            i += 1
            print_indent(indent + 1, f"(Element {i - 1})")
            print_element(indent + 2, item)

    elif isinstance(element, tycho.elements.Structure):
        if prefix:
            print_byte(indent, 0x40, "Structure")
        print_byte(indent + 1, tycho.length.encode_length(len(element.value)),
                   f"Structure has length {len(element.value)}")
        i = 0
        for key, item in element.value.items():
            i += 1
            print_indent(indent + 1, f"(Element {i - 1})")
            print_string(indent + 2, key, "Key has length")
            print_element(indent + 2, item)

    elif isinstance(element, tycho.elements.Variant):
        if prefix:
            print_byte(indent, 0x50, "Variant")
        print_string(indent + 1, element.name, "Variant name has length")
        print_element(indent + 1, element.value)

    elif isinstance(element, tycho.elements.Map):
        if prefix:
            print_byte(indent, 0x60 + element.key_type(1).encode_prefix(), "Map::" + element.key_type.__name__)

        i = 0
        for key, value in element.value.items():
            i += 1
            print_indent(indent + 1, f"(Element {i - 1})")
            print_element(indent + 1, key, prefix=False)
            print_element(indent + 2, value)

    elif isinstance(element, tycho.elements.List):
        if prefix:
            print_byte(indent, 0x70 + element.item_type(1).encode_prefix(), "List::" + element.item_type.__name__)

        i = 0
        for item in element.value:
            i += 1
            print_indent(indent + 1, f"(Element {i - 1})")
            print_element(indent + 1, item, prefix=False)

print_element(0, data)