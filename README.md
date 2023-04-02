
# Car Reg Plate Checker

This is a Python project that scrapes car registration details from the website [https://car-check.co.uk/](https://car-check.co.uk/) for registration plates beginning with a certain value, in this case "MV07". The scraped data is stored in an SQLite database named "cars.db". 

## Requirements

- Python 3.x
- requests module
- BeautifulSoup module
- sqlite3 module

## Installation

1. Clone the repository to your local machine:

git clone https://github.com/your_username/reg-crawler.git

2. Install the required modules:
pip install requests
pip install beautifulsoup4

## Usage

1. Open the command prompt and navigate to the project directory:
cd reg-crawler

2. Run the script:

python web_crawler.py

3. The script will generate all possible combinations of 3 letters and add the prefix "MV07" to each combination to generate a list of car registration plates. It will then scrape the website for car details for each registration plate in the list, including the car name and color. The data is stored in an SQLite database named "cars.db". 

## Customization

You can modify the script to search for car registration plates beginning with a different prefix by changing the value of `prefix` variable in the `registrations` list.

prefix = "MV07"
letters_combinations = [''.join(i) for i in itertools.product(string.ascii_uppercase, repeat=3)]
registrations = [f"{prefix}{combination}" for combination in letters_combinations]

You can also modify the delay time between requests to avoid triggering security mechanisms. The time.sleep() method is used to wait for a specified number of seconds between requests. By default, the delay time is set to 2 seconds.

time.sleep(2)  # Wait for 2 seconds before sending the next request
