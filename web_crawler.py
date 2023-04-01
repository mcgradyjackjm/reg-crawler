import requests
from bs4 import BeautifulSoup
import sqlite3
import itertools
import string
import time

conn = sqlite3.connect('cars.db')
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS cars")

c.execute('''CREATE TABLE IF NOT EXISTS cars
            (registration TEXT, name TEXT, color TEXT)''')

def get_car_details(registration):
    url = f"https://car-check.co.uk/check/{registration}"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    title_tag = soup.find('title')
    title_text = title_tag.text
    split_title = title_text.split(" - ")

    if len(split_title) > 1:
        car_name = split_title[1]
    else:
        return None  # Return None if car_name is not found

    description_tag = soup.find('meta', attrs={'name': 'description'})

    if description_tag:
        description_text = description_tag['content']
        split_description = description_text.split(" ")

        if len(split_description) > 5:
            color = split_description[5]
        else:
            return None  # Return None if color is not found
    else:
        return None  # Return None if description_tag is not found

    return (registration, car_name, color)

# Generate all possible combinations of 3 letters
letters_combinations = [''.join(i) for i in itertools.product(string.ascii_uppercase, repeat=3)]

# Create a list of registrations with the MV07 prefix and the 3-letter combinations
registrations = [f"MV07{combination}" for combination in letters_combinations]

# Loop to print car details
for registration in registrations:
    car_details = get_car_details(registration)

    if car_details:  # Only print car details if the function returns a valid tuple
        print(car_details)
        c.execute("INSERT INTO cars VALUES (?, ?, ?)", car_details)
        conn.commit()
        time.sleep(2)  # Wait for 1 second before sending the next request

conn.close()