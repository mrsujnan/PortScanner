import socket

def port_scan(targets, ports):
    print(f'Starting port scan for target(s): {targets}')
    for target in targets:
        for port in ports:
            port = int(port)
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)  # Set timeout for connection attempt
                result = sock.connect_ex((target, port))
                if result == 0:
                    print(f'Port {port} is open on {target}')
                sock.close()
            except KeyboardInterrupt:
                print("\nExiting...")
                return
            except socket.gaierror:
                print(f"Hostname {target} could not be resolved. Exiting...")
                return
            except socket.error:
                print(f"Couldn't connect to {target}:{port}. Exiting...")
                return

if __name__ == "__main__":
    targets = input("Enter the target IP addresses or hostnames (separated by comma): ").split(',')
    ports_input = input("Enter the ports to scan (separated by comma or range by -): ")
    ports = []
    if ',' in ports_input:
        ports = ports_input.split(',')
    elif '-' in ports_input:
        start_port, end_port = map(int, ports_input.split('-'))
        ports = range(start_port, end_port + 1)
    else:
        ports = [int(ports_input)]

    port_scan(targets, ports)
