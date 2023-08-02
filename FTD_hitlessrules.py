import os
import socket
import getpass
from netmiko import ConnectHandler

def resolve_fqdn(ftd_address):
    try:
        ip_address = socket.gethostbyname(ftd_address)
        return ip_address
    except socket.gaierror:
        return None

def get_ftd_credentials():
    ftd_address = input("Enter FTD IP or FQDN: ")

    if not resolve_fqdn(ftd_address):
        print("Resolving...")
        ftd_ip = resolve_fqdn(ftd_address)
        if ftd_ip:
            print(f"{ftd_address} == {ftd_ip}")
        else:
            print("Unable to resolve FQDN. Provide a valid IP address.")
            exit(1)
    else:
        ftd_ip = ftd_address
    
    #ftd_ip = input("Enter the FTD IP address: ")
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    return ftd_ip, username, password

def export_hitless_rules(ftd_ip, username, password, output_file):
    device = {
        "device_type": "cisco_ftd",
        "ip": ftd_ip,
        "username": username,
        "password": password,
    }

    try:
        with ConnectHandler(**device) as ssh_conn:
            # Send the command to display hitless rules from the access control policy
            output = ssh_conn.send_command("show access-list | include hitcnt=0")
    except Exception as e:
        print(f"Error connecting to FTD: {e}")
        return

    # Save the hitless rules output to a file
    with open(output_file, "w") as f:
        f.write(output)

    # Save the hitless rules output to the user-specified output file
    with open(output_file, "w") as f:
        f.write(output)

    print(f"Exported to {output_file}")

if __name__ == "__main__":
    ftd_ip, username, password = get_ftd_credentials()
    output_file = input("Enter output file name: ")
    export_hitless_rules(ftd_ip, username, password, output_file)
