
import threading
import socket
import json

json_file_path = "portdictionary.json"

with open(json_file_path, "r") as file:
    portdict = json.load(file)

count=0
worked=False


def port_scan(target, port, portdict, timeout=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((target, port))
        global worked
        worked=True
        global count
        if result == 0:
            count+=1
            if port in portdict:
                print(f'Port {port} : {portdict[str(port)]} is open on {target}')
            else:
                print(f"Port {port} is Open on {target}")
        
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

        
def scanport(target, port_range, portdict, threads=10, timeout=1):
    print(threads)
    print(f'Starting port scan for target: {target}')
    print(f'Scanning ports {port_range[0]} to {port_range[1]} with {threads} threads')
    for port in range(port_range[0], port_range[1] + 1):
        threading.Thread(target=port_scan, args=(target, port, portdict, timeout)).start()


if __name__ == "__main__":
    targets = input("Enter the target IP addresses or hostnames (separated by ','): ").split(',')
    ports_input = input("Enter the ports to scan (separated by ',' or range by '-'): ")
    thread = input("Enter the number of threads(default is 10)")
    if ',' in ports_input:
        ports = ports_input.split(',')
    elif '-' in ports_input:
        start_port, end_port = map(int, ports_input.split('-'))
        ports = range(start_port, end_port + 1)
    else:
        ports = [int(ports_input)]
    if thread == '':
        thread = 10
    else:
        thread = int(thread)
    for target in targets:
        scanport(target, (min(ports), max(ports)), portdict, thread)
        if worked:
            if count==0:
                print(f"No ports are open on {target}")
            else:
                print(f"Totally {count} ports are open on {target}")
    
    
