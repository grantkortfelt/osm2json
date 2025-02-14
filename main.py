import json
import tkinter as tk
from tkinter import filedialog, messagebox


class File:
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return self.path


class Poly(File):
    def __init__(self, path):
        super().__init__(path)

    def to_json(self):
        coordinates = []
        with open(self.path, "r") as fp:
            for line in fp:
                if line.strip().startswith("END"):
                    break
                if line.strip() and not line.strip().startswith(("polygon", "END")):
                    parts = line.strip().split()
                    if len(parts) == 2:
                        lat, lon = map(float, parts)
                        coordinates.append((lat, lon))
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
        return geojson
    
    def open_file_dialog(self):
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        file_path = filedialog.askopenfilename(title="Select .poly file to convert", filetypes=[("Polygon files", "*.poly")])
        if file_path:
            try:
                geojson = Poly.to_json(self)
                Poly.save_file_dialog(self, geojson)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

    def save_file_dialog(self, geojson):
        file_path = filedialog.asksaveasfilename(title="Save .json file", defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "w") as fp:
                json.dump(geojson, fp, indent=4)
            messagebox.showinfo("Success", f"File saved as {file_path}")


a = Poly("zealandia.poly")
a.open_file_dialog()