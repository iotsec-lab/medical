import os
import csv

def extract_unique_cities_from_csv(csv_path):
    """Extracts unique cities from a single CSV file."""
    cities = set()

    with open(csv_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            cities.add(row['city'])
    
    return cities

def gather_all_unique_cities(folder_path):
    """Gathers unique cities from all CSV files in the specified folder."""
    all_cities = set()

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            csv_path = os.path.join(folder_path, file_name)
            all_cities.update(extract_unique_cities_from_csv(csv_path))

    return all_cities

def write_unique_cities_to_txt(cities, output_file_path):
    """Writes the set of unique cities to a txt file."""
    with open(output_file_path, 'w') as txt_file:
        for city in sorted(cities):
            txt_file.write(f"{city}\n")

# Main script
folder_path = "5_ip_analysis"

unique_cities = gather_all_unique_cities(folder_path)
output_path = os.path.join(folder_path, "unique_cities.txt")
write_unique_cities_to_txt(unique_cities, output_path)

print(f"All unique cities have been written to {output_path}")
