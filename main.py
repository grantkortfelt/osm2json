import json

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
