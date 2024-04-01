import os
import pandas as pd
import sys
import csv

def calculate_protocol_percentages(input_folder, protocol):
    # Get a list of all CSV files in the input folder
    csv_files = [f for f in os.listdir(input_folder) if f.endswith(".csv")]
    functionalities = list(set([int(f.split("_")[0]) for f in csv_files]))
    functionalities = sorted(functionalities)
    print(functionalities)

    # Create a dictionary to store protocol percentages
    protocol_percentages = []
    device_name = input_folder.split("/")[1]

    for func in functionalities:
        current_protocol_percentage = [
            device_name,
            func
        ]
        for measurement_no in range(1,11):
            current_file = f"{func}_{measurement_no}.csv"
            df = pd.read_csv(os.path.join(input_folder, current_file))
            total_packets = len(df)            
            protocol_df = df[df['protocol'] == protocol]
            protocol_percentage = (len(protocol_df) / total_packets) * 100
            current_protocol_percentage.append(protocol_percentage)
        
        protocol_percentages.append(current_protocol_percentage)

    return protocol_percentages




def execute(input_folder, protocols):
    # Create the output folder if it doesn't exist
    device_name = input_folder.split("/")[1]
    os.makedirs(f"per_protocol_percentages/{device_name}", exist_ok=True)

    # Get a list of measurements
    measurements = [f'Measurement {i}' for i in range(1, 11)]
    header = ["device_name", "functionality_no"] + measurements

    # Iterate through protocol percentages and save each as a separate CSV
    for protocol in protocols:
        
        results = calculate_protocol_percentages(input_folder, protocol)
        print(results)
        # Sort by 'functionality_no' in ascending order
    
        with open(f"per_protocol_percentages/{device_name}/{protocol}_percentage.csv", 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            writer.writerows(results)
       


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the input folder name as a command line argument.")
        sys.exit(1)

    input_folder = sys.argv[1]
    with open(f"per_packet_measurements/{input_folder}/protocol_percentage.txt", 'r') as f:
        content = f.read()
        protocols  = content.split("\n")
        protocols = [p.split(":")[0] for p in protocols]
    del(protocols[-1])

    input_folder = "per_packet_measurements/" + input_folder

    print(input_folder)    

    execute(input_folder, protocols)
