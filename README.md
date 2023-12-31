# Project Name
Scraping, storing and processing
## Overview

The ZUS Coffee Melaka project is a web scraping and mapping solution for retrieving and visualizing ZUS Coffee outlet information in Melaka. The project consists of several components:

1. **Scraping (scrape.py):** This module includes functions to scrape data from the ZUS Coffee website, extracting outlet names and addresses. It also incorporates geocoding to obtain latitude and longitude coordinates for each outlet.

2. **Database Management (zus_melaka_app.py):** This module manages interactions with a SQLite database. It creates the necessary table, runs geocoding processes, and fetches data for display. The application leverages SQLite for data storage.

3. **Flask Endpoints (endpoint.py):** Defines Flask routes and endpoints to expose the scraped data through a web API. The endpoints provide access to outlet names, addresses, latitudes, and longitudes. Additionally, it includes a route for displaying a map of the outlets.

4. **Web API Endpoints (endpoint.py):** Offers a set of API endpoints that return JSON data for names, addresses, latitudes, longitudes, and all data.

5. **Map Visualization (endpoint.py, templates/map.html):** Utilizes Folium, a Python wrapper for Leaflet.js, to generate an interactive map showcasing ZUS Coffee outlets. The map includes catchment areas around each outlet and marks intersections.

6. **Index HTML (templates/index.html):** A simple HTML template for the main page, providing a link to view the map.

7. **Helper Functions (helper functions in scrape.py and zus_melaka.py):** Includes functions for calculating distances using Haversine formula and creating circle polygons for catchment areas.

## Built With

- [Flask](https://flask.palletsprojects.com/): Web framework for Python.
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/): Library for pulling data out of HTML and XML files.
- [Geopy](https://geopy.readthedocs.io/): Python client for several popular geocoding web services.
- [Shapely](https://shapely.readthedocs.io/): Python library for geometric operations using the GEOS library.
- [Folium](https://python-visualization.github.io/folium/): Python wrapper for Leaflet.js, a JavaScript library for interactive maps.

## Setup and Installation

Step 1: Create a Virtual Environment
Navigate to your project directory in the terminal and create a virtual environment. Replace venv with the desired name for your virtual environment:

**python3 -m venv venv**

Step 2: Activate the Virtual Environment
Activate the virtual environment. The activation command depends on your operating system:

**. venv/bin/activate**

After activation, your terminal prompt should change to indicate that you are now working within the virtual environment.

Step 3: Install Dependencies
With the virtual environment activated, install the project dependencies using pip. Assuming you have a requirements.txt file with your dependencies:

**pip3 install -r requirement.txt**

Step 4: Run Your Script or Application
Now, you can run your script or application within the virtual environment. For example:

**python3 endpoint.py**

Step 5: Deactivate the Virtual Environment
When you're done working on your project, deactivate the virtual environment:

**deactivate**

## Contributors

**Muhammad Luqmanul Hakim Bin Abd Yazib**
**017-5414912**

## License

This project is licensed under the MIT License.

