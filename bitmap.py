import struct

def char(c):
    #1 byte
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    #2 bytes
    return struct.pack('=h', w)

def dword(d):
    #4 bytes
    return struct.pack('=l', d)

class Header:
    def __init__(self):
        self._signature = ['B','M']
        self._file_size = 0
        self._reserved = 0
        self._data_offset = 0

    def configure_header(fileSize, dataOffset):
        self._file_size = fileSize
        self._data_offset = dataOffset

    def header_values():
        return (
            char(self._signature[0]),
            char(self._signature[1]),
            dword(self._file_size),
            dword(self._reserved),
            dword(self._data_offset)
        )

class InfoHeader:


class Pixels:
