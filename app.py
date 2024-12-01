import pandas as pd
import folium
from flask import Flask, render_template

# Initialize the Flask app
app = Flask(__name__)

# Function to load and process the data
def process_data():
    file_path = "Top 10 South India Temples - Only Lat Long.csv"
    df = pd.read_csv(file_path, encoding="latin1")

    # Clean and convert Latitude and Longitude
    def clean_coordinate(coord):
        coord = coord.replace("°", "").replace("N", "").replace("E", "").strip()
        return float(coord)

    df["Lattitude"] = df["Lattitude"].apply(clean_coordinate)
    df["Longitude"] = df["Longitude"].apply(clean_coordinate)
    return df

# Function to create the map
def create_map():
    df = process_data()
    first_temple = df.iloc[0]
    map_center = [first_temple["Lattitude"], first_temple["Longitude"]]
    mymap = folium.Map(location=map_center, zoom_start=6)

    # Add markers for each temple
    for _, row in df.iterrows():
        folium.Marker(
            location=[row["Lattitude"], row["Longitude"]],
            popup=row["Name"]
        ).add_to(mymap)

    # Save the map to an HTML file
    map_path = "templates/map.html"
    mymap.save(map_path)

# Route for the homepage
@app.route("/")
def index():
    return render_template("index.html")

# Route for the map page
@app.route("/map")
def map_view():
    create_map()  # Dynamically generate the map
    return render_template("map.html")

if __name__ == "__main__":
    app.run(debug=True)
