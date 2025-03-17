from skyfield.api import load
import requests

# Load TLE data (ISS)
satellites_url = "https://www.celestrak.com/NORAD/elements/stations.txt"
satellites = load.tle_file(satellites_url)

# Choose a satellite (e.g., ISS)
satellite = [sat for sat in satellites if sat.name == "ISS (ZARYA)"][0]

# Create a timescale for observation
ts = load.timescale()
t = ts.now()  # Current time

# Calculate the position of the satellite
geocentric = satellite.at(t)

# Get the latitude and longitude of the satellite
lat, lon = geocentric.subpoint().latitude.degrees, geocentric.subpoint().longitude.degrees

# Print the position
print(f"ISS Position at {t.utc_iso()}: Lat {lat}°, Lon {lon}°")

import matplotlib.pyplot as plt

# Plot the satellite's position
fig, ax = plt.subplots()
ax.scatter(lon, lat, color='red')  # Satellite position in red
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title('Satellite Position')

plt.show()

# Fetch the TLE data
response = requests.get(satellites_url)
# Load the satellites into Skyfield
satellites = load.tle_file(satellites_url)
satellite_names = [sat.name for sat in satellites]

# Create a timescale for observation
ts = load.timescale()
t = ts.now()  # Current time

# List to store satellite positions
positions = []

# Get the positions of all satellites
for sat in satellites:
    geocentric = sat.at(t)
    lat, lon = geocentric.subpoint().latitude.degrees, geocentric.subpoint().longitude.degrees
    positions.append((sat.name, lat, lon))

# Print satellite positions
for name, lat, lon in positions:
    print(f"{name} Position at {t.utc_iso()}: Lat {lat}°, Lon {lon}°")

# Create a plot
fig, ax = plt.subplots()
ax.set_title('Satellite Positions')

# Plot each satellite's position on the map
for name, lat, lon in positions:
    ax.scatter(lon, lat, label=name)

# Add labels and title
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

# Add a legend
ax.legend(loc='upper right')

# Show the plot
plt.show()

import time
try:
# Loop to update every 10 seconds
    # Loop to update every 10 seconds
 while True:
    # Fetch the current time
    t = ts.now()

    # List to store updated positions
    updated_positions = []

    # Get updated positions of all satellites
    for sat in satellites:
        geocentric = sat.at(t)
        lat, lon = geocentric.subpoint().latitude.degrees, geocentric.subpoint().longitude.degrees
        updated_positions.append((sat.name, lat, lon))

    # Clear the previous plot and plot updated positions
    plt.clf()  # Clear the previous plot

    # Plot each satellite's position
    for name, lat, lon in updated_positions:
        plt.scatter(lon, lat, label=name)

    # Set labels and title
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Real-Time Satellite Positions')

    # Add a legend
    plt.legend(loc='upper right')

    # Show the plot
    plt.pause(1)  # Pause to update the plot

    # Delay for 2 seconds before the next update
    time.sleep(2)

    plt.ioff()
    plt.show()
    print("Tracking ended.")
except KeyboardInterrupt:
    print("Tracking stopped by user.")

import geopy.distance

def calculate_distance(lat1, lon1, lat2, lon2):
    coords_1 = (lat1, lon1)
    coords_2 = (lat2, lon2)
    return geopy.distance.distance(coords_1, coords_2).km  # Distance in km

# Define a minimum distance (e.g., 500 km) for collision risk
min_distance_km = 500

# Compare each pair of satellites
for i in range(len(updated_positions)):
    for j in range(i+1, len(updated_positions)):
        name1, lat1, lon1 = updated_positions[i]
        name2, lat2, lon2 = updated_positions[j]

        # Calculate distance between the two satellites
        distance = calculate_distance(lat1, lon1, lat2, lon2)

        # If the distance is below the threshold, flag it as a collision risk
        if distance < min_distance_km:
            print(f"Collision Risk: {name1} and {name2} are {distance:.2f} km apart!")
            