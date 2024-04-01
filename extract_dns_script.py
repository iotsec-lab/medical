import os
import csv
import sys
import subprocess

def process_pcap(device_name, pcap_file):
    functionality, measurement = pcap_file.split("_")
    measurement = int(measurement.split(".")[0])  # Convert measurement to integer

    pcap_path = os.path.join(device_name, pcap_file)

    command = ['tshark', '-r', pcap_path, '-Y', 'dns', '-T', 'fields', '-e', 'frame.number', '-e', 'frame.time_epoch']
    output = subprocess.check_output(command).decode().splitlines()

    rows = []
    for line in output:
        frame_no, time = line.split('\t')
        row = {
            'frame_no': frame_no,
            'time': time,
        }
        rows.append(row)

    return functionality, measurement, rows

def write_to_csv(functionality, measurement, rows, output_folder):
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
output_folder = f"dns_frames/{input_folder}"
pcap_files = [f for f in os.listdir(input_folder) if f.endswith(".pcap")]
for pcap_file in pcap_files:
    functionality, measurement, rows = process_pcap(input_folder, pcap_file)
    if rows:
        write_to_csv(functionality, measurement, rows, output_folder)
