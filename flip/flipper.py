import csv
import requests

def do(config):
    while True:
        with open('inventory.csv') as csvfile:
            inventory = []
            for index, row in enumerate(csv.reader(csvfile, delimiter=',', quotechar='"')):
                if index > 0:
                    inventory.append({
                        'account': row[0],
                        'name': row[1],
                        'quantity': row[2],
                        'price': row[3]
                    })
        for item in inventory:
            if item['name'] not in ['gp']:
                r = requests.get(config['base_url']+'items/search/'+item['name'], headers=config['headers'])
                if r.status_code == 200:
                    return True, r.text
                else:
                    return False, r.text
