import requests
import matplotlib.pyplot as plt

def get_celestrak_data(category):
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

def filter_objects(objects, criteria):
    filtered_objects = []
    for obj in objects:
        if criteria in obj["name"].lower():
            filtered_objects.append(obj)
    return filtered_objects

def visualize_objects(objects):
    latitudes = []
    longitudes = []

    for obj in objects:
        line2 = obj["line2"].split()
        inclination = float(line2[2])
        ascending_node = float(line2[3])
        orbital_period = float(line2[7])

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

def main():
    categories = ["active", "stations"]
    all_objects = []

    for category in categories:
        objects = get_celestrak_data(category)
        all_objects.extend(objects)

    print("List of active space debris and satellites:")
    for obj in all_objects:
        print(obj["name"])

    criteria = input("Enter criteria to filter objects (leave blank for no filter): ").lower()
    filtered_objects = filter_objects(all_objects, criteria)

    if filtered_objects:
        print("\nFiltered objects:")
        for obj in filtered_objects:
            print(obj["name"])
    else:
        print("\nNo objects found with the given criteria.")

    visualize = input("Do you want to visualize the objects on a map? (yes/no): ").lower()
    if visualize == "yes":
        visualize_objects(all_objects)

if __name__ == "__main__":
    main()
