import getpass
import telnetlib

def telnet_to_device(ip, user, password):
    tn = telnetlib.Telnet(ip)

    tn.read_until(b"Username: ")
    tn.write(user.encode('ascii') + b"\n")

    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")

    # Wait for the prompt ending with "#"
    tn.read_until(b"#", timeout=5)  # Set a timeout for prompt detection
    tn.write(b"terminal length 0\n")

    # Wait for the prompt ending with "#"
    tn.read_until(b"#", timeout=5)
    tn.write(b"show ip int bri | in Vlan1\n")

    # Wait for the output to be received (prompt ending with "#")
    output = tn.read_until(b"#", timeout=10)

    # Close the Telnet connection
    tn.write(b"exit\n")
    tn.close()

    return output.decode('ascii')


if __name__ == "__main__":
    ip_addresses = ['192.168.122.12', '192.168.122.13', '192.168.122.110', '192.168.122.11']
    user = input("Enter Telnet Username: ")
    password = getpass.getpass()

    for ip in ip_addresses:
        try:
            print(f"Connecting to {ip}")
            output = telnet_to_device(ip, user, password)
            print(output)
        except Exception as e:
            print(f"Failed to connect to {ip}: {str(e)}")
