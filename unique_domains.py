import os
import csv

def extract_unique_domains_from_csv(csv_file_path):
    unique_domains = set()
    
    with open(csv_file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        
        for row in reader:
            domain_name = row['domain_name']
            if domain_name:
                unique_domains.add(domain_name)
                
    return unique_domains

def write_unique_domains_to_txt(unique_domains, output_file_path):
    print(output_file_path)
    with open(output_file_path, 'w') as output_file:
        for domain in sorted(unique_domains):
            output_file.write(f"{domain}\n")

def process_folder_for_unique_domains(folder_path):
    unique_domains = set()

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            unique_domains.update(extract_unique_domains_from_csv(file_path))
    print(unique_domains)
    output_file_path = os.path.join(folder_path, "all_unique_domains.txt")
    write_unique_domains_to_txt(unique_domains, output_file_path)

# Main script
root_folder = "domains"

for subfolder in os.listdir(root_folder):
    subfolder_path = os.path.join(root_folder, subfolder)
    print(subfolder)
    if os.path.isdir(subfolder_path):
        process_folder_for_unique_domains(subfolder_path)

print("Completed processing all subfolders.")
