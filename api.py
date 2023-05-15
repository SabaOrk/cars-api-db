import requests
from conf import API_URL
import json
import sqlite3
import os

"""
მომაქვს მანქანების ჩამონათვალი რაღაც ბრაზილიური API-დან
ბმული: https://deividfortuna.github.io/fipe/
"""


def get_listing():
    headers = {'content-type': 'application/json'}

    res = requests.get(API_URL, headers=headers)
    if res.status_code == 200:
        return res.json()
    else:
        return []


"""
ვპრინტავ მანქნების სიას
"""

for car in get_listing():
    print(f"name: {car['nome']}, code: {car['codigo']}")


"""
JSON ფაილში ჩაწერა
"""

json_object = json.dumps({"cars": get_listing()}, indent=4)

with open('cars.json', 'w') as f:
    f.write(json_object)


def save_to_db(list):
    """
    ინფორმაციის ბაზაში ჩაწერა sqlite-ის გამოყენებით
    table: cars (name, code)
    """

    if os.path.exists("cars.sqlite"):
        conn = sqlite3.connect('cars.sqlite')
    else:
        conn = sqlite3.connect('cars.sqlite')

    c = conn.cursor()
    c.execute('''CREATE TABLE cars
                    (name text, code integer)''')
    conn.commit()

    for car in list:
        c.execute("INSERT INTO cars VALUES (?, ?)", (car['nome'], int(car['codigo'])))

    conn.commit()
    conn.close()


save_to_db(get_listing())
