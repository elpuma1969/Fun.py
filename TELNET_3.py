import os
import getpass
import telnetlib

if __name__ == "__main__":
    ip_addresses = ['192.168.122.12', '192.168.122.13', '192.168.122.110', '192.168.122.11']
    user = input("Enter Telnet Username: ")
    password = getpass.getpass()

    # Create a folder named "BACKUP_SCH" if it doesn't exist
    backup_folder = "BACKUP_SCH"
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    for ip in ip_addresses:
        try:
            print(f"Connecting to {ip}")
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

            # Use the IP address as the identifier for the backup file name
            identifier = ip

            # Create a backup file with the IP address as the title
            backup_filename = os.path.join(backup_folder, f"{identifier}.txt")
            with open(backup_filename, "w") as backup_file:
                backup_file.write(output.decode('ascii'))

            print(f"Backup for {identifier} saved in {backup_filename}")
        except Exception as e:
            print(f"Failed to connect to {ip}: {str(e)}")
