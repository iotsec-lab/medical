import os
import csv
import sys
import subprocess

def process_pcap(device_name, pcap_file):
    pcap_path = os.path.join(device_name, pcap_file)

    command = ['tshark', '-r', pcap_path, '-T', 'fields', '-e', 'frame.number', '-e', 'ip.proto', '-e', 'tcp.dstport']
    output = subprocess.check_output(command).decode().splitlines()

    rows = []
    for line in output:
        frame_no, ip_proto, dstport = line.split('\t')

        # Here we're assuming that HTTPS (port 443) means encrypted and HTTP (port 80) means unencrypted.
        # Other protocols/ports can be added as needed.
        encrypted = "Encrypted" if dstport == "443" else "Unencrypted" if dstport == "80" else "Unknown"

        row = {
            'frame_no': frame_no,
            'ip_proto': ip_proto,
            'dstport': dstport,
            'encrypted': encrypted,
        }
        rows.append(row)

    return rows

def write_to_csv(rows, output_folder, pcap_file):
    os.makedirs(output_folder, exist_ok=True)
    file_name = os.path.join(output_folder, f"{pcap_file}.csv")

    with open(file_name, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

# Example usage
if len(sys.argv) < 2:
    print("Please provide the input folder name as a command line argument.")
    sys.exit(1)

input_folder = sys.argv[1]
output_folder = f"encryption_status/{input_folder}"
pcap_files = [f for f in os.listdir(input_folder) if f.endswith(".pcap")]

for pcap_file in pcap_files:
    rows = process_pcap(input_folder, pcap_file)
    if rows:
        write_to_csv(rows, output_folder, pcap_file)
