import os
import pandas as pd
import sys
import csv
import numpy as np

from collections import Counter
def is_lan_ip(host:str):
    if host.startswith("10") or host.startswith("192"):
        return True

    return False


def unique_ips(input_folder):
    
    ips = []

    csv_files = [f for f in os.listdir(input_folder) if f.endswith(".csv")]
    for cf in csv_files:
        with open(os.path.join(input_folder, cf), 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                
                if row[7] == 'outbound':
                    if not is_lan_ip(row[6]):
                        ips.append(row[6])
    
    ips =  list(set(ips))
    nr = np.asarray(ips)
    return nr.reshape(len(ips), 1).tolist()
                   
    
def execute(input_folder):
    # Create the output folder if it doesn't exist
    device_name = input_folder.split("/")[1]
    os.makedirs(f"unique_ips", exist_ok=True)


    header = ["ip"]
   
    ips = unique_ips(input_folder)
    
    with open(f"unique_ips/{device_name}.csv", 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(ips)
    

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the input folder name as a command line argument.")
        sys.exit(1)

    input_folder = sys.argv[1]
    input_folder = "per_packet_measurements/" + input_folder

    execute(input_folder)


