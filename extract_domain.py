import os
import csv
import sys
import subprocess
import pandas
def load_unique_ips(device_name):
    data = pandas.read_csv(f'unique_ips/{device_name}.csv')
    return data['ip'].to_list()

def get_dns_response_ip_address(pcap_file, domain_name):
    try:
        # Run tshark command and capture output
        output = subprocess.check_output(['tshark', '-r', pcap_file, '-Y', f'dns.flags.response == 1 and dns.qry.name == {domain_name}', '-T', 'fields', '-e', 'dns.a'])

        # Return the resolved IP address
        output =  output.decode().strip()
        return output.split(',')
    except Exception as e:
        # Handle error if tshark command fails
        print(e)


def process_pcap(device_name, pcap_file):
    uniqe_ips = load_unique_ips(device_name)
    print(uniqe_ips)
    functionality, measurement = pcap_file.split("_")
    measurement = int(measurement.split(".")[0])  # Convert measurement to integer

    pcap_path = os.path.join(device_name, pcap_file)

    command = ['tshark', '-r', pcap_path, '-T', 'fields', '-e', 'frame.number', '-e', 'ip.dst', '-e', 'dns.qry.name', '-Y', 'dns']
    output = subprocess.check_output(command).decode().splitlines()

    rows = []
    for line in output:
        frame_no, _, domain_name = line.split('\t')
        ips = get_dns_response_ip_address(pcap_path, domain_name)
        for ip in ips:
            if ip in uniqe_ips:

                row = {
                    'frame_no': frame_no,
                    'ip': ip,
                    'domain': domain_name,
    
                }
                rows.append(row)
    

    return functionality, measurement, rows

def write_to_csv(functionality, measurement, rows, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    file_name = os.path.join(output_folder, f"{functionality}_{measurement}.csv")

    with open(file_name, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

# Example usage
if len(sys.argv) < 2:
    print("Please provide the input folder name as a command line argument.")
    sys.exit(1)

input_folder = sys.argv[1]
devices = ["babymonitor", "earwax", "earwax_wifi_data", "fitbitfitness", "guardianalertsystem", "kardiamobile", "ketoscanketonemeter", "withingsbpm", "wyzescale"]
if input_folder == "all":
    for device in devices:
        output_folder = f"domains/{device}"
        pcap_files = [f for f in os.listdir(device) if f.endswith(".pcap")]

        for pcap_file in pcap_files:
            functionality, measurement, rows = process_pcap(device, pcap_file)
            if rows:
                write_to_csv(functionality, measurement, rows, output_folder)
else:
    output_folder = f"domains/{input_folder}"
    pcap_files = [f for f in os.listdir(input_folder) if f.endswith(".pcap")]
    for pcap_file in pcap_files:
        functionality, measurement, rows = process_pcap(input_folder, pcap_file)
        if rows:
            write_to_csv(functionality, measurement, rows, output_folder)
