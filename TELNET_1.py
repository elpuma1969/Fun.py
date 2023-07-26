import getpass
import telnetlib
import sys

HOST = "192.168.122.11"
user = input("Enter Telnet Username: ")
password = getpass.getpass()
tn = telnetlib.Telnet(HOST)

tn.read_until(b"Username: ")
tn.write(user.encode('ascii') + b"\n")
tn.read_until(b"Password: ")
tn.write(password.encode('ascii') + b"\n")

tn.write(b"terminal length 0\n")
tn.write(b"show ip int bri | in Vlan1\n")
tn.write(b"exit\n")

print(tn.read_all().decode('ascii'))
