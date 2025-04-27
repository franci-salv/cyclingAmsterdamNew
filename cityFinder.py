import csv


filepath = r"C:\Users\franc\OneDrive\Bureaublad\Newer Beginnings\Amsterdam Cycling baby\worldcities.csv"
# Load the CSV into a dictionary: { city_name_lowercase: (lat, lon) }
def load_city_coords(filepath):
    city_coords = {}
    with open(filepath, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            city = row['city'].strip().lower()
            lat = float(row['lat'])
            lon = float(row['lng'])  # may be called 'lon' in your file
            city_coords[city] = (lat, lon)
    return city_coords


cities = load_city_coords(filepath)

#because it should fix my code I don't know
if __name__ == "__main__":
    cities = load_city_coords(filepath)

    user_input = input("Enter a city: ").strip().lower()

    if user_input in cities:
        lat, lon = cities[user_input]
        print(f"Coordinates for {user_input.title()}: {lat}, {lon}")
    else:
        print("City not found.")

