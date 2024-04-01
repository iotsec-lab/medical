import os
import pandas as pd
import sys
import csv
def calculate_traffic_percentages(input_folder):
    
   
    csv_files = [f for f in os.listdir(input_folder) if f.endswith(".csv")]
    functionalities = list(set([int(f.split("_")[0]) for f in csv_files]))
    functionalities = sorted(functionalities)
    print(functionalities)
   
    inbound_percentages = []
    outbound_percentages = []
    device_name = input_folder.split("/")[1]

    for func in functionalities:
        current_inbound_percentages = [
            device_name,
            func
        ]
        current_outbound_percentages = [
            device_name,
            func
        ]
        for measurement_no in range(1,11):
            current_file = f"{func}_{measurement_no}.csv"
            df = pd.read_csv(os.path.join(input_folder, current_file))
            total_packets = len(df)            
            inbound_df = df[df['traffic_direction_type'] == "inbound"]
            outbound_df = df[df['traffic_direction_type'] == "outbound"]
            
            inbound_percentage = (len(inbound_df) / total_packets) * 100
            outbound_percentage = (len(outbound_df) / total_packets) * 100

            current_inbound_percentages.append(inbound_percentage)
            current_outbound_percentages.append(outbound_percentage)
            
        
        inbound_percentages.append(current_inbound_percentages)
        outbound_percentages.append(current_outbound_percentages)

    return inbound_percentages, outbound_percentages

    

def execute(input_folder):
    # Create the output folder if it doesn't exist
    device_name = input_folder.split("/")[1]
    os.makedirs(f"traffic_percentages/{device_name}", exist_ok=True)

    # Get a list of measurements
    measurements = [f'Measurement {i}' for i in range(1, 11)]
    header = ["device_name", "functionality_no"] + measurements

    # Iterate through protocol percentages and save each as a separate CSV
    
        
    inbound, outbound = calculate_traffic_percentages(input_folder)
    print(inbound)
       
        # Sort by 'functionality_no' in ascending order
    
    with open(f"traffic_percentages/{device_name}/inbound.csv", 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(inbound)
    
    with open(f"traffic_percentages/{device_name}/outbound.csv", 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(outbound)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the input folder name as a command line argument.")
        sys.exit(1)

    input_folder = sys.argv[1]

    execute(input_folder)


