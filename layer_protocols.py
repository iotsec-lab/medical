import os
import sys
import subprocess
import csv

ENCRYPTED_PROTOCOLS = {"https", "ftps", "tls", "ssh", "sftp", "ssl", "ipsec"}

def extract_protocols(pcap_path, max_layers=5):
    command = ['tshark', '-r', pcap_path, '-T', 'fields', '-e', 'frame.number', '-e', 'frame.protocols']
    output = subprocess.check_output(command).decode().splitlines()

    frames = []
    for line in output:
        frame_no, protocols = line.split("\t")
        layers = protocols.split(':')[:max_layers]  # Limit the layers to max_layers

        frame = {"frame_no": frame_no}
        for i, layer in enumerate(layers, start=1):
            frame[f"layer_{i}"] = layer
            frame[f"is_encrypted_{i}"] = layer in ENCRYPTED_PROTOCOLS

        frames.append(frame)
        
    return frames

def write_to_csv(frames, output_folder, csv_file_name, max_layers):
    if not frames:  # Check if frames is empty
        print(f"No data extracted from pcap file {csv_file_name}")
        return

    os.makedirs(output_folder, exist_ok=True)
    file_name = os.path.join(output_folder, f"{csv_file_name}.csv")

    # Define fieldnames based on max_layers
    fieldnames = ["frame_no"]
    for i in range(1, max_layers + 1):
        fieldnames.extend([f"layer_{i}", f"is_encrypted_{i}"])

    with open(file_name, "w") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        for frame in frames:
            writer.writerow(frame)

# Example usage
if len(sys.argv) < 2:
    print("Please provide the input folder name as a command line argument.")
    sys.exit(1)

input_folder = sys.argv[1]

pcap_files = [f for f in os.listdir(input_folder) if f.endswith(".pcap")]

for pcap_file in pcap_files:
    frames = extract_protocols(os.path.join(input_folder, pcap_file))
    csv_file_name = os.path.splitext(pcap_file)[0]  # Remove .pcap extension
    write_to_csv(frames, f'protocol_layers/{input_folder}', csv_file_name, max_layers=5)
