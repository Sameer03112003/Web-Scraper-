# Web-Scraper-

# Web Scraping and Database Storage

This project demonstrates how to scrape meta information from various websites and store the extracted data into a MySQL database. The primary goals include extracting meta titles, meta descriptions, social media links, technologies used, payment gateways, website language, and categorizing the websites.

# Features

- Web Scraping: Uses `requests` and `BeautifulSoup` for scraping data from web pages.
- Database Storage: Connects to a MySQL database to store the scraped data.
- Tech Stack Detection: Identifies technologies used on the websites, including CMS, JavaScript libraries, and frameworks.
- Social Media Links Extraction: Collects social media links from the web pages.
- Payment Gateway Detection: Identifies common payment gateways used on the websites.

## Prerequisites

- Python 3.x
- MySQL Server

### Python Libraries

- `requests`
- `bs4` (BeautifulSoup)
- `mysql.connector`

You can install the required Python libraries using:

bash
pip install requests beautifulsoup4 mysql-connector-python
Also install by running  
pip install -r requirement.txt

# MySQL Setup

Ensure you have MySQL installed and running. You need to create a database named `scrap` and configure a user with the necessary privileges.

## Getting Started

### 1. Clone the repository

### 2. Configure MySQL Connection

Update the MySQL connection settings in the script with your credentials:

python
db_connection = mysql.connector.connect(
    host="localhost",
    user="your-username",
    password="your-password",
    database="scrap"
)


### 3. Run the Script

Execute the script to start scraping and storing data:

bash
python scrape.py

The script will:

1. Connect to the MySQL database.
2. Check and create the necessary table if it doesn't exist.
3. Scrape data from a predefined list of websites.
4. Store the scraped data into the database.

## Functions Overview

### `scrape_website(url)`

Scrapes the given URL to extract meta information, social media links, technologies used, payment gateways, and website language.

### `create_table_if_not_exists(db_connection)`

Creates the `websites` table in the MySQL database if it doesn't already exist.

### `store_in_database(data, db_connection)`

Stores the scraped data into the MySQL database.

## Example Usage

Here's an example of how you can scrape a single website and print the results:

python
url = "(https://www.flipkart.com)"
data = scrape_website(url)
print(data)


This README file provides a comprehensive guide on setting up and running the web scraping project. It includes instructions on dependencies, configuration, and execution, along with an overview of the main functions used in the script.
