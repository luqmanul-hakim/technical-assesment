import csv
import folium
from flask import Flask, jsonify, render_template
from scrape import check_and_run_process, run_process, create_circle
from zus_melaka_app import get_address, get_latitude, get_longitude, get_name, index

app = Flask(__name__)

@app.route('/name')
def name():
    return jsonify({"names": get_name()})

@app.route('/address')
def address():
    return jsonify({"addresses": get_address()})

@app.route('/latitude')
def latitude():
    return jsonify({"latitudes": get_latitude()})

@app.route('/longitude')
def longitude():
    return jsonify({"longitudes": get_longitude()})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/all')
def get_all():
    return jsonify({"index": index()})

@app.route('/map_data')
def map_data():
    # Fetch data from the csv file
    filename = "output.csv"
    keys = {'Name', 'Latitude', 'Longitude'}
    records = []

    with open(filename, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            records.append({key: row[key] for key in keys})
    
    for record in records:
        record['Float_latitude'] = float(record['Latitude'])
        record['Float_longitude'] = float(record['Longitude'])
    
    # Create a Folium map centered at the first outlet
    my_map = folium.Map(location=[records[0]['Float_latitude'], records[0]['Float_longitude']], zoom_start=12)
    
    # Add circles for catchment areas and check for intersections
    for i, record1 in enumerate(records):
        catchment1 = create_circle(record1['Float_latitude'], record1['Float_longitude'])
        
        for j, record2 in enumerate(records):
            if i != j:
                catchment2 = create_circle(record2['Float_latitude'], record2['Float_longitude'])
                
                if catchment1.intersects(catchment2):
                    folium.Marker(
                        location=[record2['Float_latitude'], record2['Float_longitude']],
                        popup=f"Intersects with {record1['Name']}",
                        icon=folium.Icon(color='red')
                    ).add_to(my_map)

        folium.Circle(
            location=[record1['Float_latitude'], record1['Float_longitude']],
            radius=5000,
            color='blue',
            fill=True,
            fill_opacity=0.2
        ).add_to(my_map)

    # Save the map as an HTML file
    my_map.save('templates/map.html')

    return render_template('map.html')

if __name__ == '__main__':
    db_path = "zus_melaka.db"
    table_name = "ZUS_MELAKA_INFORMATION"
    required_columns = ["Latitude", "Longitude"]

    check_and_run_process(db_path, table_name, required_columns, run_process)
    app.run(debug=True)
