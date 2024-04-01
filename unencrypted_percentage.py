import os
import csv

def calculate_unencrypted_percentage_for_folder(folder_path):
    total_frames = 0
    unencrypted_frames = 0  # frames with dstport 80
    
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as csv_file:
                reader = csv.DictReader(csv_file)
                
                for row in reader:
                    dstport = row['dstport']
                    if dstport == "80":
                        unencrypted_frames += 1
                    total_frames += 1

    if total_frames == 0:  # avoid division by zero
        return 0
    return (unencrypted_frames / total_frames) * 100

def write_unencrypted_percentage_to_txt(folder_path):
    percentage = calculate_unencrypted_percentage_for_folder(folder_path)
    output_file_path = os.path.join(folder_path, "unencrypted_percentage.txt")
    with open(output_file_path, 'w') as output_file:
        output_file.write(f"Unencrypted Percentage: {percentage:.2f}%\n")

root_folder = "encryption_status"

for subfolder in os.listdir(root_folder):
    subfolder_path = os.path.join(root_folder, subfolder)
    if os.path.isdir(subfolder_path):
        write_unencrypted_percentage_to_txt(subfolder_path)

print("Completed processing all subfolders.")
