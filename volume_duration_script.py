import os
import csv
import sys
import subprocess

def process_pcap(device_name, pcap_file):
    functionality, measurement = pcap_file.split("_")
    measurement = int(measurement.split(".")[0])  # Convert measurement to integer

    pcap_path = os.path.join(device_name, pcap_file)
    
    # Getting duration
    command = ['tshark', '-r', pcap_path, '-T', 'fields', '-e', 'frame.time_epoch']

    output = subprocess.check_output(command).decode().splitlines()
  
    duration = float(output[-1]) - float(output[0]) if output else 0

    # Getting volume
    volume = os.path.getsize(pcap_path) / 1024  # in KB

    # Getting packet count
    command = ['tshark', '-r', pcap_path, '-T', 'fields', '-e', 'frame.number']
    
    packet_count = len(subprocess.check_output(command).decode().splitlines())
    
    return {
        'device_name': device_name,
        'functionality_no': functionality,
        'measurement_no': measurement,
        'duration': duration,
        'volume_kb': volume,
        'packet_count': packet_count,
    }
  
def write_to_csv(rows, output_folder, device_name):
    os.makedirs(output_folder, exist_ok=True)
    file_name = os.path.join(output_folder, f"{device_name}.csv")

    # Sort rows by functionality_no and then by measurement_no before writing
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
    row = process_pcap(input_folder, pcap_file)
    all_rows.append(row)

write_to_csv(all_rows, 'volume_duration', input_folder)
