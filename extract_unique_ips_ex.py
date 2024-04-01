import os
import csv
import sys
import subprocess
import requests
import pandas
import json

def find_object_by_key_value(json_array, key, value):
    for obj in json_array:
        if obj.get(key) == value:
            return obj
    return None

def get_domain(ip, device_name):
    csv_files = [f for f in os.listdir(f'domains/{device_name}') if f.endswith(".csv")]
    for csv_file in csv_files:
        df = pandas.read_csv(os.path.join(f'domains/{device_name}', csv_file))
        df = df.loc[df['ip'] == ip]
        try:
            if not df.empty:
                return df['domain'].values[0]
        except Exception as e:
            print(ip, e)
            exit()

def get_location_batch(ips):
    url = "http://ip-api.com/batch"
    ips = list(ips)
    ip_chunks = [ips[i:i+100] for i in range(0, len(ips), 100)]
    results = []

    for chunk in ip_chunks:
        data = json.dumps(chunk)
        response = requests.post(url, data=data)
        results.extend(response.json())

    return results



def get_location(ip_address, all_ips_location):
    data = find_object_by_key_value(all_ips_location, "query", ip_address)
    keys = ['status', 'country', 'countryCode', 'region', 'regionName', 'city', 'zip', 
            'lat', 'lon', 'timezone', 'isp', 'org', 'as', 'query']
    data = {key: data.get(key, '') for key in keys}
    return data
    # response = requests.get(f'http://ip-api.com/json/{ip_address}')
    # data = None
    # try:

    #     data = response.json()
    # except Exception as e:
    #     print(response.text)
    #     print(ip_address)
    # keys = ['status', 'country', 'countryCode', 'region', 'regionName', 'city', 'zip', 
    #         'lat', 'lon', 'timezone', 'isp', 'org', 'as', 'query']
    # data = {key: data.get(key, '') for key in keys}
    # return data

def extract_ips(input_folder):
    pcap_files = [f for f in os.listdir(input_folder) if f.endswith(".pcap")]

    all_ips = set()
    ip_count = dict()
    for pcap_file in pcap_files:
        pcap_path = os.path.join(input_folder, pcap_file)

        # Extract source and destination IP addresses
        command = ['tshark', '-r', pcap_path, '-T', 'fields', '-e', 'ip.src', '-e', 'ip.dst']
        output = subprocess.check_output(command).decode().splitlines()

        # Add all unique IP addresses to the set
        for line in output:
            ips = line.split("\t")
            for ip in ips:
                if ip not in ip_count:
                    ip_count[ip] = 1
                else:
                    ip_count[ip] += 1
            all_ips.update(ips)
   

    return all_ips, ip_count

def write_ips(ips,ip_count, output_folder, device_name):
    os.makedirs(output_folder, exist_ok=True)
    file_name = os.path.join(output_folder, f"{device_name}.csv")

    rows = []
    all_ips_locations = get_location_batch(ips)
    for ip in ips:
        
        row = get_location(ip, all_ips_locations)
        
        row['count'] = ip_count[ip]
        row['domain'] = get_domain(ip, device_name)
        # print("row", get_domain(ip, device_name))
        rows.append(row)
        # except Exception as e:
        #     print("error", ip, e, ip_count)
    
    with open(file_name, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


# Example usage
# if len(sys.argv) < 2:
#     print("Please provide the input folder name and device name as command line arguments.")
#     sys.exit(1)

# input_folder = sys.argv[1]
input_folder = 'wyzescale'

ips, ip_count = extract_ips(input_folder)

write_ips(ips, ip_count, 'ip_analysis', input_folder)
