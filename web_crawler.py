# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import sqlite3
import itertools
import string
import time

# Connect to the SQLite database
conn = sqlite3.connect('cars.db')
c = conn.cursor()

# Drop the 'cars' table if it already exists
c.execute("DROP TABLE IF EXISTS cars")

# Create the 'cars' table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS cars
            (registration TEXT, name TEXT, color TEXT)''')

# Define the function to get car details from a given registration number
def get_car_details(registration):
    # Construct the URL for the car-check website using the registration number
    url = f"https://car-check.co.uk/check/{registration}"

    # Keep trying to fetch car details until successful
    while True:
        # Send a GET request to the car-check website
        response = requests.get(url)

        # If the status code is 429 (Too Many Requests), wait for 300 seconds before retrying
        if response.status_code == 429:
            # Countdown the wait time, updating the remaining time in the same line
            wait_time = 300
            for remaining in range(wait_time, 0, -1):
                print(f"\r429 error for {registration}, waiting {remaining} seconds before retrying", end='', flush=True)
                time.sleep(1)
            # Print a newline character to move to the next line after the countdown
            print()
            continue

        # Parse the response HTML using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the 'details' div in the HTML
        details_div = soup.find('div', id='details')

        # If the 'details' div is found, extract car name and color
        if details_div:
            car_name_tag = details_div.find('span', text='Model')
            color_tag = details_div.find('span', text='Colour')

            # If both car_name_tag and color_tag are found, extract the text content
            if car_name_tag and color_tag:
                car_name = car_name_tag.find_next_sibling('span').text
                color = color_tag.find_next_sibling('span').text
            else:
                return None
        else:
            return None

        # Return a tuple with registration, car_name, and color
        return (registration, car_name, color)

# Generate all 3-letter combinations
letters_combinations = [''.join(i) for i in itertools.product(string.ascii_uppercase, repeat=3)]

# Create a list of registration numbers with the format MV07 + 3-letter combination
registrations = [f"MV07{combination}" for combination in letters_combinations]

# Iterate through the list of registration numbers
for registration in registrations:
    # Call the get_car_details function to fetch car details
    car_details = get_car_details(registration)

    # If car_details is not None, print the details and insert them into the 'cars' table
    if car_details:
        print(car_details)
        c.execute("INSERT INTO cars VALUES (?, ?, ?)", car_details)
        conn.commit()

        # Wait for 20 seconds before sending the next request to avoid rate-limiting
        time.sleep(20)

# Close the database connection
conn.close()
