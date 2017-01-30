from socket import *
from struct import *
import os
import re

BUF_SZE = 1024


def net0(host, port):
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((host, port))

    data = s.recv(BUF_SZE).decode("utf-8")
    print("[*]Data: ", data)

    # Find the numeric string between quotes
    search = re.search("'(\d+)'", data)
    num = int(search.group(1))
    print("[*]Num: ", str(num))

    # Convert the number to little endian format and send it back
    little = pack("<I", num)
    s.send(little)
    print("[*]Ans: ", s.recv(BUF_SZE).decode("utf-8"))
    s.close()


def net1(host, port):
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((host, port))
    data = s.recv(1024)

    # Convert the number from little endian format and send it back
    num = int(unpack("<I", data)[0])
    print("[*]Num: ", str(num))
    s.send((str(num) + os.linesep).encode("utf-8"))
    print("[*]Ans: ", s.recv(1024).decode("utf-8"))
    s.close()


def net2(host, port):
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((host, port))

    intsum = 0
    # Loop over the 4 unsigned integers being read in, and them to "sum"
    for i in range(4):
        data = s.recv(4)
        little_endian = int(unpack("<I", data)[0])
        print("[*]Data[", str(i), "]: ", str(little_endian))
        intsum += little_endian
    print("[*]Sum: " + str(intsum))

    # Handle integer overflow by doing a logical AND with 0xffffffff
    intsum &= 0xffffffff

    # Convert the sum back to little-endian, to send back over the wire
    sum_packed = pack("<I", intsum)
    s.send(sum_packed)
    print("[*]Ans: ", s.recv(1024).decode("utf-8"))
    s.close()


if __name__ == "__main__":
    name_port = {
        "net0": 2999,
        "net1": 2998,
        "net2": 2997
    }
    host = "192.168.1.37"  # Change me!
    for name, port in name_port.items():
        print(">>> ", name)
        locals()[name](host, port)
        print("<<<", os.linesep)
