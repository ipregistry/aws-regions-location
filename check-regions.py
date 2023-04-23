import requests
import csv

# Load AWS regions from the URL
url = "https://ip-ranges.amazonaws.com/ip-ranges.json"
response = requests.get(url)
data = response.json()

aws_regions = set()
for ip_range in data["prefixes"]:
    if "network_border_group" in ip_range and ip_range["network_border_group"] != "GLOBAL":
        aws_regions.add(ip_range["network_border_group"])

for ip_range in data["ipv6_prefixes"]:
    if "network_border_group" in ip_range and ip_range["network_border_group"] != "GLOBAL":
        aws_regions.add(ip_range["network_border_group"])

# Load AWS regions from the CSV file
csv_regions = set()
with open("aws-regions-location.csv", "r") as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip header line
    for row in csvreader:
        csv_regions.add(row[0])

# Check if all regions in the URL are present in the CSV file
missing_regions = aws_regions - csv_regions

if missing_regions:
    raise ValueError(f"The following regions are missing from the CSV file: {', '.join(missing_regions)}")
else:
    print("All regions from the URL are present in the CSV file.")