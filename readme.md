# Tycho Debugger
A simple python script to debug [Tycho binary format](https://github.com/samhdev/tycho).

Uses the [tycho python library](https://github.com/samhdev/tycho-py)
### Installing
```
git clone https://github.com/samhdev/tycho-debug
cd tycho-debug
pip install -r requirements.txt
python debug.py <bytes in hex>
```

### Example
```
python debug.py 40 03 03 66 6f 6f 1e 0b 48 65 6c 6c 6f 20 57 6f 72 6c 64 03 62 61 72 11 0a 03 62 61 7a 10 01
------------------------------------------------------------------------------------------------------------
40 - Structure
	03 - Structure has length 3
	(Element 0)
		03 - Key has length 3
			66 - "f"
			6f - "o"
			6f - "o"
		1d - Value::String
			0b - String has length 11
			48 - "H"
			65 - "e"
			6c - "l"
			6c - "l"
			6f - "o"
			20 - " "
			57 - "W"
			6f - "o"
			72 - "r"
			6c - "l"
			64 - "d"
	(Element 1)
		03 - Key has length 3
			62 - "b"
			61 - "a"
			72 - "r"
		01 - Value::Unsigned8
			0a - u8(10)
	(Element 2)
		03 - Key has length 3
			62 - "b"
			61 - "a"
			7a - "z"
		10 - Value::Boolean
			01 - true
```
