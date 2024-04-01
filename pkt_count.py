import os
import csv
import sys

def count_packets(device_name):
    pcap_folder = device_name
    pcap_files = [f for f in os.listdir(pcap_folder) if f.endswith(".pcap")]

    packet_counts = {}
    measurements = set()

    for pcap_file in pcap_files:
        functionality, measurement = pcap_file.split("_")
        measurement = int(measurement.split(".")[0])  # Convert measurement to integer
        measurements.add(measurement)

        command = f"tshark -r {os.path.join(pcap_folder, pcap_file)} | wc -l"
        output = os.popen(command).read().strip()
        packet_count = int(output)

        key = (device_name, functionality)
        if key not in packet_counts:
            packet_counts[key] = {}
        packet_counts[key][measurement] = packet_count

    return packet_counts, measurements

def write_to_csv(packet_counts, measurements, device_names):
    folder_name = "packet_counts"
    os.makedirs(folder_name, exist_ok=True)
    file_name = "_".join(device_names) + "_packet_counts.csv"
    file_path = os.path.join(folder_name, file_name)

    # Sort measurements in ascending order
    sorted_measurements = sorted(measurements)

    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)
        headers = ["device_name", "functionality_no"]
        headers += [f"Measurement {i}" for i in sorted_measurements]  # Incremental measurement column names
        writer.writerow(headers)

        # Sort packet_counts by functionality number
        sorted_packet_counts = sorted(packet_counts.items(), key=lambda x: int(x[0][1]))

        for (device_name, functionality), counts in sorted_packet_counts:
            row = [device_name, functionality]
            for measurement in sorted_measurements:
                row.append(counts.get(measurement, 0))
            writer.writerow(row)

# Example usage
if len(sys.argv) < 2:
    print("Please provide at least one device name as a command line argument.")
    sys.exit(1)

device_names = sys.argv[1:]
all_packet_counts = {}
all_measurements = set()

for device_name in device_names:
    packet_counts, measurements = count_packets(device_name)
    all_packet_counts.update(packet_counts)
    all_measurements.update(measurements)

write_to_csv(all_packet_counts, all_measurements, device_names)
