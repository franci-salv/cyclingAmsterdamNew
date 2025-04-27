import csv

def load_city_coords(filepath):
    city_coords = {}
    with open(filepath, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            city = row['city'].strip().lower()
            lat = float(row['lat'])
            lon = float(row['lng'])
            city_coords[(city, row['country'].strip().lower())] = (lat, lon)  # optional: city + country key
    return city_coords

# Test manually
if __name__ == "__main__":
    filepath = r"...\worldcities.csv"  # Put your correct path here
    cities = load_city_coords(filepath)

    user_input = input("Enter a city: ").strip().lower()
    user_country = input("Enter a country: ").strip().lower()

    if (user_input, user_country) in cities:
        lat, lon = cities[(user_input, user_country)]
        print(f"Coordinates for {user_input.title()}, {user_country.title()}: {lat}, {lon}")
    else:
        print("City not found.")


