import csv
import os
import re
import requests
import sqlite3
from bs4 import BeautifulSoup
from flask import Flask
from geopy.geocoders import Nominatim
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from math import radians, sin, cos, sqrt, atan2

app = Flask(__name__)  # Instantiate an app

# Function to scrape data from a page
def scrape_page(url):
    # Send an HTTP request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find all <span> tags within the specified class
        span_elements = soup.find_all('span', class_='entry-title')
        # Extract the text content of each <span> and store in a list
        names = [span.text.strip() for span in span_elements]
        # Find all <p> elements with addresses
        address_elements = soup.find_all('p')
        # Create a pattern only select addresses and ignore that is not related
        pattern = re.compile(r"^(?!.*(?:Company registration no:|COPYRIGHT)).*[A-Za-z][^\n\d]*\d.*$")
        # Initialize an empty list to store addresses that match the pattern
        matching_addresses = []

        # Checks if the addresses match a pattern.
        for i, address_element in enumerate(address_elements, start=1):
            address_text = address_element.get_text(strip=True)
            if pattern.match(address_text):
                matching_addresses.append(address_text)

        data = list(zip(names, matching_addresses))
        return data

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

# Function to run geocoding
def geocoding_location(cursor):
    geolocator = Nominatim(user_agent="zus_geocoder")

    # Check if columns exist in the table
    cursor.execute("PRAGMA table_info(ZUS_MELAKA_INFORMATION)")
    columns = [column[1] for column in cursor.fetchall()]

    # Add new columns if they don't exist
    if 'latitude' not in columns:
        cursor.execute("ALTER TABLE ZUS_MELAKA_INFORMATION ADD COLUMN Latitude REAL")
    if 'longitude' not in columns:
        cursor.execute("ALTER TABLE ZUS_MELAKA_INFORMATION ADD COLUMN Longitude REAL")

    # Fetch names from the database
    cursor.execute("SELECT Name, Address FROM ZUS_MELAKA_INFORMATION WHERE Latitude IS NULL AND Longitude IS NULL")
    rows = cursor.fetchall()

    for row in rows:
        name, address = row

        # Extract only the part of the address after the last hyphen
        name_parts = name.rsplit(' – ', 1)
        if len(name_parts) == 2:
            name = name_parts[1]
        
        # Append "MELAKA" to the end of the modified name
        name += " MELAKA"

        # Check if the name contains "Cheng" and modify it
        if "Cheng" in name:
            name = "Jalan Inang 1, melaka"

        # Check if the name contains "ElementX @ Hatten City" and modify it
        if "ElementX @ Hatten City" in name:
            name = "Jalan Melaka Raya, 23, MELAKA"

        location = geolocator.geocode(name)

        if location:
            latitude, longitude = location.latitude, location.longitude
            cursor.execute("UPDATE ZUS_MELAKA_INFORMATION SET Latitude=?, Longitude=? WHERE Address=?", (latitude, longitude, address))

def connect_to_database(db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    return connection, cursor

def close_database(connection):
    connection.commit()
    connection.close()

def check_and_run_process(db_path, table_name, required_columns, process_function):
    connection, cursor = connect_to_database(db_path)
    table_has_columns = check_table_columns(cursor, table_name, required_columns)
    close_database(connection)

    if not all(column in required_columns for column in ['Latitude', 'Longitude']) or not table_has_columns:
        process_function()

# Function to create database
def create_database():
    connection = sqlite3.connect("zus_melaka.db")
    cursor = connection.cursor()

    # Create table if not exists
    cursor.execute("CREATE TABLE IF NOT EXISTS ZUS_MELAKA_INFORMATION (Name TEXT, Address TEXT)")
    connection.commit()
    connection.close()

# Function to scrape name and addr
def scrape_name_addr(base_url, page_count, cursor):
    all_data = []

    for page_number in range(1, page_count + 1):
        page_url = f"{base_url}/page/{page_number}/"
        current_page_data = scrape_page(page_url)

        if current_page_data:
            all_data.extend(current_page_data)

    cursor.executemany("INSERT INTO ZUS_MELAKA_INFORMATION VALUES (?, ?)", all_data)


def check_table_columns(cursor, table_name, columns):
    # Execute a query to get information about the table columns
    cursor.execute(f"PRAGMA table_info({table_name})")
    
    # Fetch the column names from the result set
    existing_columns = [column[1] for column in cursor.fetchall()]
    
    # Check if all specified columns exist in the table
    for column in columns:
        if column not in existing_columns:
            return False
    
    return True

def save_data_to_csv(cursor, filename='output.csv'):
    # Fetch data from the database
    cursor.execute("SELECT Name, Address, Latitude, Longitude FROM ZUS_MELAKA_INFORMATION")
    data = cursor.fetchall()

    # Save data to CSV file
    if not os.path.exists(filename):
        with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['Name', 'Address', 'Latitude', 'Longitude']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            
            # Write the header
            writer.writeheader()
            
            # Write the data
            for row in data:
                writer.writerow({'Name': row[0], 'Address': row[1], 'Latitude': row[2], 'Longitude': row[3]})
    else:
        print(f"File '{filename}' already exists. Skipping creation.")

def run_process():
    create_database()
    connection = sqlite3.connect("zus_melaka.db")
    cursor = connection.cursor()

    base_url = 'https://zuscoffee.com/category/store/melaka'
    page_count = 2  # Adjust the number of pages as needed
    scrape_name_addr(base_url, page_count, cursor)
    geocoding_location(cursor)
    # Commit changes to the database
    connection.commit()
    # Save data to csv file
    save_data_to_csv(cursor, filename='output.csv')
    connection.close()

def check_table_columns(cursor, table_name, required_columns):
    # Get the columns present in the table
    cursor.execute(f"PRAGMA table_info({table_name})")
    existing_columns = [column[1] for column in cursor.fetchall()]

    # Check if all required columns are present
    return all(column in existing_columns for column in required_columns)

def calculate_distance(lat1, lon1, lat2, lon2):
    # Function to calculate distance between two points using Haversine formula
    # You can replace this with a more accurate method if needed
    from math import radians, sin, cos, sqrt, atan2

    R = 6371  # Radius of the Earth in kilometers

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance

def create_circle(lat, lon, radius=5):
    # Function to create a circle polygon for catchment area
    points = []

    for angle in range(0, 360, 5):
        dx = radius * cos(angle)
        dy = radius * sin(angle)

        points.append((lat + dx, lon + dy))

    return Polygon(points)
