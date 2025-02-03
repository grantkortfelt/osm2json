import json
import tkinter as tk
from tkinter import filedialog, messagebox

# Function to convert a polygon file (.poly) to GeoJSON format (.json)
def poly2json(infile, outfile=None):
    coordinates = []
    # read input file's coordinates
    with open(infile, "r") as fp:
        for line in fp:
            if line.strip().startswith("END"):
                break
            if line.strip() and not line.strip().startswith(("polygon", "END")):
                parts = line.strip().split()
                if len(parts) == 2:
                    lat, lon = map(float, parts)
                    coordinates.append((lat, lon))
    # create GeoJSON object with the coordinates
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [coordinates]
                },
                "properties": {}
            }
        ]
    }
    # write GeoJSON object to output file if provided
    if outfile:
        with open(outfile, "w") as fp:
            json.dump(geojson, fp, indent=4)
    return geojson


def open_file_dialog():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(title="Select .poly file to convert", filetypes=[("Polygon files", "*.poly")])
    if file_path:
        try:
            geojson = poly2json(file_path)
            save_file_dialog(geojson)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

def save_file_dialog(geojson):
    file_path = filedialog.asksaveasfilename(title="Save .json file", defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, "w") as fp:
            json.dump(geojson, fp, indent=4)

open_file_dialog()