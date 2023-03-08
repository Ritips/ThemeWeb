import argparse
import requests
import csv


parser = argparse.ArgumentParser()
parser.add_argument("--multiply", default=5, type=int)
parser.add_argument("--larger", default=0, type=int)
parser.add_argument("host", type=str)
parser.add_argument("port", type=str)
args = parser.parse_args()


response = requests.get("http://" + args.host + ':' + args.port)
if not response:
    print('Fuck yourself')
    exit()

json_object = response.json()

with open("anomalies.csv", 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter=';')
    for key in sorted(json_object):
        sum_each_second_zero = sum_each_second_one = 0
        values = json_object[key]

        values_to_check = []
        for val in values:
            if val % args.multiply and val >= args.larger:
                values_to_check.append(val)

        min_a = min(values_to_check)
        max_a = max(values_to_check)
        for i in range(0, len(values_to_check), 2):
            sum_each_second_zero += values_to_check[i]
        for i in range(1, len(values_to_check), 2):
            sum_each_second_one += values_to_check[i]
        o = f'{key}penis{min_a}penis{max_a}penis{sum_each_second_zero}penis{sum_each_second_one}'
        w.writerow(o.split("penis"))

