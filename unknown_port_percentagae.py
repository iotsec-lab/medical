import os
import csv

def calculate_unknown_port_percentage_for_folder(folder_path):
    total_frames = 0
    unknown_port_frames = 0  # frames where dstport is not 80 or 443
    
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as csv_file:
                reader = csv.DictReader(csv_file)
                
                for row in reader:
                    dstport = row['dstport']
                    if dstport not in ["80", "443"]:
                        unknown_port_frames += 1
                    total_frames += 1

    if total_frames == 0:  # avoid division by zero
        return 0
    return (unknown_port_frames / total_frames) * 100

def write_unknown_port_percentage_to_txt(folder_path):
    percentage = calculate_unknown_port_percentage_for_folder(folder_path)
    output_file_path = os.path.join(folder_path, "unknown_port_percentage.txt")
    with open(output_file_path, 'w') as output_file:
        output_file.write(f"Unknown Port Percentage: {percentage:.2f}%\n")

# Main script
root_folder = "encryption_status"

for subfolder in os.listdir(root_folder):
    subfolder_path = os.path.join(root_folder, subfolder)
    if os.path.isdir(subfolder_path):
        write_unknown_port_percentage_to_txt(subfolder_path)

print("Completed processing all subfolders.")
