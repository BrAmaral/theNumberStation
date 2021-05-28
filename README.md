# theNumberStation

**theNumberStation** is a Python program that implements the One-Time Pad concept described by Gilbert Vernam and Joseph Mauborgne. In theory, the cipher is unbrekable if the following rules are respected:

- The One-Time Pad should consist of random characters;
- The One-Time Pad should have the same length as the message;
- The One-Time Pad must be used only once per message;
- There must be only 2 copies of the One-Time Pad (when used by physical means);
- The One-Time Pad must be destroyed immediately after use.

The program was made for fun, and was heavily inspired by the game "Call of Duty Black Ops" and number stations that operated during the Cold War. **I don't recommend that you encrypt real sensitive information using theNumberStation**.

### Requirements

You must have python 3.x installed in your machine. Please visit https://www.python.org/ for instructions, if necessary.

Also, when installing, check the **add Python to the PATH variable** box (if you are installing it in **Windows**).

### Basic usage

Execute the code on a terminal with:

```bash
python3 theNumberStation.py
```



### References

- https://cryptomuseum.com/crypto/otp/index.htm
