# P4 Register Reader

P4 Register Reader is a debugging tool for reading registers inside of a P4 app.
It allows you to run 1 command and print the values in 1 or all registers.

### Getting Started

1. Save the p4registerreader.py file **in the same location as your topology file**

2. CD into the directory of the file

3. Run the following code to see instructions:

```
python p4registerreader.py
```

### Usage

**Read register on all switches**
```python
python p4registerreader.py a
```

**Read register on one switch**
```python
python p4registerreader.py [SWITCH NAME]
```

**Update Register Name and Size**
```python
python p4registerreader.py u
```