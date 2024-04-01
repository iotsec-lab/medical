import os
import pandas as pd
import sys
import csv

from collections import Counter


def top3_frequent_values(input_list):
    
    counts = Counter(input_list)
    top3 = counts.most_common(3)
    total_count = len(input_list)
    result = [f"{value} ({(count / total_count) * 100:.2f}%)" for value, count in top3]
    return result


def calculate_top_ports(input_folder):
    top_inbound_src_ports = []
    top_inbound_dst_ports = []
    top_outbound_src_ports = []
    top_outbound_dst_ports = []

    csv_files = [f for f in os.listdir(input_folder) if f.endswith(".csv")]
    for cf in csv_files:
        with open(os.path.join(input_folder, cf), 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                
                if row[7] == 'inbound':
                    top_inbound_src_ports.append(row[3])
                    top_inbound_dst_ports.append(row[4])
                elif row[7] == 'outbound':
                    top_outbound_src_ports.append(row[3])
                    top_outbound_dst_ports.append(row[4])
    
    top_inbound_src_ports = top3_frequent_values(top_inbound_src_ports)
    top_inbound_dst_ports = top3_frequent_values(top_inbound_dst_ports)
    top_outbound_src_ports = top3_frequent_values(top_outbound_src_ports)
    top_outbound_dst_ports = top3_frequent_values(top_outbound_dst_ports)
    return top_inbound_src_ports, top_inbound_dst_ports, top_outbound_src_ports, top_outbound_dst_ports
    

def execute(input_folder):

    device_name = input_folder.split("/")[1]
    os.makedirs(f"top_ports/{device_name}/inbound", exist_ok=True)
    os.makedirs(f"top_ports/{device_name}/outbound", exist_ok=True)
    header = ["port_1", "port_2", "port_3"]

    top_inbound_src_ports, top_inbound_dst_ports, top_outbound_src_ports, top_outbound_dst_ports = calculate_top_ports(input_folder)
    
    with open(f"top_ports/{device_name}/inbound/src.csv", 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerow(top_inbound_src_ports)
    
    with open(f"top_ports/{device_name}/inbound/dst.csv", 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerow(top_inbound_dst_ports)
    
    
    with open(f"top_ports/{device_name}/outbound/src.csv", 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerow(top_outbound_src_ports)

    with open(f"top_ports/{device_name}/outbound/dst.csv", 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerow(top_outbound_dst_ports)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the input folder name as a command line argument.")
        sys.exit(1)
    
    input_folder = sys.argv[1]
    devices = ["babymonitor", "earwax", "earwax_wifi_data", "fitbitfitness", "guardianalertsystem", "kardiamobile", "ketoscanketonemeter", "withingsbpm", "wyzescale"]
    if input_folder == "all":
        for device in devices:
            folder = "per_packet_measurements/" + device
            execute(folder)

    else:

        input_folder = "per_packet_measurements/" + input_folder
        execute(input_folder)


