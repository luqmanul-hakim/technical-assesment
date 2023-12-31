import sqlite3

def index():
    connection = sqlite3.connect("zus_melaka.db")
    cursor = connection.cursor()
    cursor.execute("SELECT Name, Address, Latitude, Longitude FROM ZUS_MELAKA_INFORMATION")
    data = cursor.fetchall()
    connection.close()
    return data

def get_name():
    connection = sqlite3.connect("zus_melaka.db")
    cursor = connection.cursor()
    cursor.execute("SELECT Name FROM ZUS_MELAKA_INFORMATION")
    names = cursor.fetchall()
    connection.close()
    names_list = [name[0] for name in names]
    return names_list

def get_address():
    connection = sqlite3.connect("zus_melaka.db")
    cursor = connection.cursor()
    cursor.execute("SELECT Address FROM ZUS_MELAKA_INFORMATION")
    addresses = cursor.fetchall()
    connection.close()
    address_list = [address[0] for address in addresses]
    return address_list

def get_latitude():
    connection = sqlite3.connect("zus_melaka.db")
    cursor = connection.cursor()
    cursor.execute("SELECT Latitude FROM ZUS_MELAKA_INFORMATION")
    latitudes = cursor.fetchall()
    connection.close()
    latitude_list = [latitude[0] for latitude in latitudes]
    return latitude_list

def get_longitude():
    connection = sqlite3.connect("zus_melaka.db")
    cursor = connection.cursor()
    cursor.execute("SELECT Longitude FROM ZUS_MELAKA_INFORMATION")
    longitudes = cursor.fetchall()
    connection.close()
    longitude_list = [longitude[0] for longitude in longitudes]
    return longitude_list
