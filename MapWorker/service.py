import csv


def read_coords_from_csv(csv_filepath, layer_type):
    rows = []
    with open(csv_filepath, mode="r", encoding="utf-8") as file:
        rows = [row for row in csv.reader(file)]
    return {"layer_type": layer_type, "layer_data": rows}


def validate_csv_file(file_path):
    return True


# if layer_type == "markers":
#     column_names = ["lat1", "lon1", "popup", "marker_size", "marker_color"]
# elif layer_type == "polygons":
#     column_names = ["lat1", "lon1"]
# elif layer_type == "routes":
#     column_names = [
#         "lat1",
#         "lon1",
#         "lat2",
#         "lon2",
#         "popup1",
#         "popup2",
#         "line_width",
#         "line_color",
#     ]
# elif layer_type == "heatmap":
#     column_names = ["lat1", "lon1", "marker_size"]

# with open(csv_filepath, mode="r", encoding="utf-8") as file:
#     reader = csv.DictReader(file, fieldnames=column_names)
#     layer_data = [row for row in reader]
# return {"layer_type": layer_type, "layer_data": layer_data}
