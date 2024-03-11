import requests
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

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

def train_passover_classifier(features, labels):
    """
    Trains a random forest classifier for predicting passovers.

    Parameters:
        features (list): List of feature vectors.
        labels (list): List of binary labels indicating passover events (1 for passover, 0 for no passover).

    Returns:
        RandomForestClassifier: Trained classifier model.
    """
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

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
        inclination = float(line2[2])
        ascending_node = float(line2[3])

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
    """
    Main function to fetch data, train passover classifier, and visualize objects.
    """
    # Fetch orbital data for active debris and stations
    categories = ["active", "stations"]
    all_objects = []

    for category in categories:
        objects = get_celestrak_data(category)
        all_objects.extend(objects)

    print("List of active space debris and satellites:")
    for obj in all_objects:
        print(obj["name"])

    # Feature engineering and labeling for passover prediction
    # Assume features and labels are preprocessed accordingly

    # Train passover classifier
    passover_classifier = train_passover_classifier(features, labels)

    # Make predictions for passovers
    passover_predictions = passover_classifier.predict(features)

    # Visualize objects on a map
    visualize_objects(all_objects)

if __name__ == "__main__":
    main()
