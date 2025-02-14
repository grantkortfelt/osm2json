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
    
    def convert(self):
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


class Json(File):
    def __init__(self, path):
        super().__init__(path)

    def to_poly(self):
        with open(self.path, "r") as fp:
            data = json.load(fp)
        coordinates = data["features"][0]["geometry"]["coordinates"][0]
        with open(self.path.replace(".json", ".poly"), "w") as fp:
            fp.write("polygon\n")
            for lat, lon in coordinates:
                fp.write(f"{lat} {lon}\n")
            fp.write("END\n")
        return self.path.replace(".json", ".poly")
    
    def convert(self):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(title="Select .json file to convert", filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                poly_path = Json.to_poly(self)
                Json.save_file_dialog(self, poly_path)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
    
    def save_file_dialog(self, poly_path):
        file_path = filedialog.asksaveasfilename(title="Save .poly file", defaultextension=".poly", filetypes=[("Polygon files", "*.poly")])
        if file_path:
            with open(file_path, "w") as fp:
                with open(poly_path, "r") as p:
                    fp.write(p.read())
            messagebox.showinfo("Success", f"File saved as {file_path}")