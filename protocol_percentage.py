import os
import csv

def get_protocol_percentage_from_csv(csv_path):
    """Extract protocol percentage from a single CSV file."""
    protocol_count = {}
    total_packets = 0

    with open(csv_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            protocol = row['protocol']
            protocol_count[protocol] = protocol_count.get(protocol, 0) + 1
            total_packets += 1

    # Calculate the percentage for each protocol
    protocol_percentage = {}
    for protocol, count in protocol_count.items():
        protocol_percentage[protocol] = (count / total_packets) * 100
    
    return protocol_percentage

def calculate_protocol_percentage_in_folder(folder_path):
    """Calculate protocol percentage for all CSV files in a folder."""
    total_protocol_percentage = {}

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            csv_path = os.path.join(folder_path, file_name)
            protocol_percentage = get_protocol_percentage_from_csv(csv_path)
            
            # Aggregate results
            for protocol, percentage in protocol_percentage.items():
                total_protocol_percentage[protocol] = total_protocol_percentage.get(protocol, 0) + percentage

    # Get average percentages
    num_csv_files = len([f for f in os.listdir(folder_path) if f.endswith('.csv')])
    for protocol in total_protocol_percentage:
        total_protocol_percentage[protocol] /= num_csv_files

    return total_protocol_percentage

def write_protocol_percentage_to_txt(protocol_percentage, output_file_path):
    """Writes the protocol percentage to a txt file."""
    with open(output_file_path, 'w') as txt_file:
        for protocol, percentage in sorted(protocol_percentage.items(), key=lambda x: x[1], reverse=True):
            txt_file.write(f"{protocol}: {percentage:.2f}%\n")

# Main script
base_folder_path = "per_packet_measurements"

for folder_name in os.listdir(base_folder_path):
    folder_path = os.path.join(base_folder_path, folder_name)
    if os.path.isdir(folder_path):
        protocol_percentage = calculate_protocol_percentage_in_folder(folder_path)
        output_path = os.path.join(folder_path, "protocol_percentage.txt")
        write_protocol_percentage_to_txt(protocol_percentage, output_path)

print("Protocol percentages have been written to the respective subfolders.")
