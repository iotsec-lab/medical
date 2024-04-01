import os
import csv
import sys
import subprocess

def is_lan_ip(host:str):
    if host.startswith("10") or host.startswith("192"):
        return True

    return False

def process_pcap(input_folder, pcap_file):
    functionality, measurement = pcap_file.split("_")
    measurement = int(measurement.split(".")[0])  # Convert measurement to integer
    pcap_path = os.path.join(input_folder, pcap_file)

    command = ['tshark', '-r', pcap_path, '-T', 'fields', '-e', 'frame.number', '-e', 'frame.len', 
           '-e', 'frame.protocols', '-e', 'tcp.srcport', '-e', 'udp.srcport', '-e', 'tcp.dstport', 
           '-e', 'udp.dstport', '-e', 'ip.src', '-e', 'ip.dst']

    output = subprocess.check_output(command).decode().splitlines()

    rows = []
    for line in output:
        packet_no, packet_size, protocol, tcp_srcport, udp_srcport, tcp_dstport, udp_dstport, src_host, dst_host = line.split("\t")
        source_port = tcp_srcport or udp_srcport or "N/A"
        destination_port = tcp_dstport or udp_dstport or "N/A"
        # print(protocol)
        if 'http' in protocol:
            protocol = 'http'
        elif 'tls' in protocol:
            protocol = 'tls'
        elif 'dns' in protocol:
            protocol = 'dns'
        elif 'tcp' in protocol:
            protocol = 'tcp'
        elif 'udp' in protocol:
            protocol = 'udp'
        else:
            print("Here" + protocol)
            protocol = "N/A"
        
        if is_lan_ip(src_host) and not is_lan_ip(dst_host):
            traffic_type = "outbound"
        elif not is_lan_ip(src_host) and is_lan_ip(dst_host):
            traffic_type = "inbound"
        else:
            traffic_type = "inbound"
        row = {
            'packet_no': packet_no,
            'packet_size': packet_size,
            'protocol': protocol or "N/A",
            'source_port': source_port,
            'destination_port': destination_port,
            'source_host': src_host or "N/A",
            'destination_host': dst_host or "N/A",
            'traffic_direction_type' : traffic_type
        }
        rows.append(row)
    
    return functionality, measurement, rows

def write_to_csv(functionality, measurement, rows, output_folder):
    if not rows:  # Check if rows is empty
        print(f"No data extracted from pcap file for functionality {functionality} and measurement {measurement}")
        return

    os.makedirs(output_folder, exist_ok=True)
    file_name = os.path.join(output_folder, f"{functionality}_{measurement}.csv")

    with open(file_name, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

# Example usage
if len(sys.argv) < 2:
    print("Please provide the input folder name as a command line argument.")
    sys.exit(1)

input_folder = sys.argv[1]
output_folder = f'per_packet_measurements/{input_folder}'

pcap_files = [f for f in os.listdir(input_folder) if f.endswith(".pcap")]
for pcap_file in pcap_files:
    functionality, measurement, rows = process_pcap(input_folder, pcap_file)
    write_to_csv(functionality, measurement, rows, output_folder)
