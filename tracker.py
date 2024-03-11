import requests
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import tkinter as tk

# Global variable for category selection
category_var = None

def get_celestrak_data(category):
    """
    Fetches orbital data from Celestrak API for a given category.

    Parameters:
        category (str): The category of objects to fetch ("active" or "stations").

    Returns:
        list: List of dictionaries containing orbital data for objects in the specified category.
    """
    url = f"https://www.celestrak.com/NORAD/elements/{category}.txt"
    response = requests.get(url)
    data = response.text.splitlines()
    objects = []

    for i in range(0, len(data), 3):
        name = data[i].strip()
        line1 = data[i+1].strip()
        line2 = data[i+2].strip()
        objects.append({"name": name, "line1": line1, "line2": line2})

    return objects

def visualize_objects(objects):
    """
    Visualizes the objects on a map.

    Parameters:
        objects (list): List of dictionaries containing orbital data for objects.
    """
    latitudes = []
    longitudes = []

    for obj in objects:
        line2 = obj["line2"].split()
        if len(line2) < 4:  # Check if line2 has at least 4 elements (including latitude and longitude)
            continue  # Skip this object if it doesn't have enough elements in line2

        # Check if latitude and longitude can be converted to floats
        try:
            inclination = float(line2[2])
            ascending_node = float(line2[3])
        except ValueError:
            continue  # Skip this object if latitude or longitude cannot be converted to float

        if inclination < 90:
            latitude = 90 - inclination
        else:
            latitude = inclination - 90

        longitude = ascending_node

        latitudes.append(latitude)
        longitudes.append(longitude)

    plt.figure(figsize=(10, 6))
    plt.scatter(longitudes, latitudes, marker='.', color='blue')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Visualization of Objects')
    plt.grid(True)
    plt.show()

def fetch_and_visualize_objects():
    """
    Fetches the selected category of objects and visualizes them on a map.
    """
    global category_var
    category = category_var.get()
    objects = get_celestrak_data(category)
    visualize_objects(objects)

def main():
    global category_var

    root = tk.Tk()
    root.title("Space Debris Tracker")

    category_label = tk.Label(root, text="Select category:")
    category_label.pack()

    category_var = tk.StringVar()
    category_var.set("active")  # Default value

    category_dropdown = tk.OptionMenu(root, category_var, "active", "stations")
    category_dropdown.pack()

    fetch_button = tk.Button(root, text="Fetch and Visualize Objects", command=fetch_and_visualize_objects)
    fetch_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
