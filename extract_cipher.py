import os
import csv
import sys
import subprocess

def process_pcap(device_name, pcap_file):
    functionality, measurement = pcap_file.split("_")
    measurement = int(measurement.split(".")[0])  # Convert measurement to integer

    pcap_path = os.path.join(device_name, pcap_file)

    # Getting SSL/TLS cipher suite info if HTTPS traffic
    command = ['tshark', '-r', pcap_path, '-Y', 'ssl', '-T', 'fields', '-e', 'frame.number', '-e', 'tls.handshake.ciphersuite']
    print(command)
    output = subprocess.check_output(command).decode().splitlines()

    rows = []
    for line in output:
        frame_number, cipher_info = line.split()
        row = {
            'device_name': device_name,
            'functionality_no': functionality,
            'measurement_no': measurement,
            'frame_number': frame_number,
            'cipher_info': cipher_info if cipher_info != '' else 'N/A'
        }
        rows.append(row)

    return rows

def write_to_csv(rows, output_folder, device_name):
    os.makedirs(output_folder, exist_ok=True)
    file_name = os.path.join(output_folder, f"{device_name}.csv")

    # Sort rows by functionality_no and measurement_no before writing
    rows = sorted(rows, key=lambda x: (int(x['functionality_no']), int(x['measurement_no'])))

    with open(file_name, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

# Example usage
if len(sys.argv) < 2:
    print("Please provide the input folder name as a command line argument.")
    sys.exit(1)

input_folder = sys.argv[1]

all_rows = []
pcap_files = [f for f in os.listdir(input_folder) if f.endswith(".pcap")]
for pcap_file in pcap_files:
    rows = process_pcap(input_folder, pcap_file)
    all_rows.extend(rows)

write_to_csv(all_rows, 'cypher_suite', input_folder)
