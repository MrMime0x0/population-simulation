import sqlite3
import random
import matplotlib.pyplot as plt

# Parameters for the simulation
initial_population = 1000
birth_rate = 0.03  # 3% birth rate
death_rate = 0.02  # 2% death rate
years_to_simulate = 10

# Initialize the SQLite3 database
conn = sqlite3.connect('population.db')
cursor = conn.cursor()

# Create table for logging population data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS population_log (
        year INTEGER PRIMARY KEY,
        population INTEGER,
        births INTEGER,
        deaths INTEGER
    )
''')
conn.commit()

def simulate_population(initial_population, birth_rate, death_rate, years):
    population = initial_population
    for year in range(1, years + 1):
        births = int(population * birth_rate)
        deaths = int(population * death_rate)
        population = population + births - deaths
        
        # Insert data into the database
        cursor.execute('''
            INSERT INTO population_log (year, population, births, deaths)
            VALUES (?, ?, ?, ?)
        ''', (year, population, births, deaths))
        conn.commit()

        print(f"Year {year}: Population = {population}, Births = {births}, Deaths = {deaths}")

def fetch_population_data():
    cursor.execute('SELECT year, population, births, deaths FROM population_log')
    data = cursor.fetchall()
    return data

def plot_population_data(data):
    years = [row[0] for row in data]
    population = [row[1] for row in data]
    births = [row[2] for row in data]
    deaths = [row[3] for row in data]

    plt.figure(figsize=(10, 6))
    plt.plot(years, population, label='Population', marker='o')
    plt.plot(years, births, label='Births', marker='o')
    plt.plot(years, deaths, label='Deaths', marker='o')

    plt.xlabel('Year')
    plt.ylabel('Count')
    plt.title('Population Simulation Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()

# Run the simulation
simulate_population(initial_population, birth_rate, death_rate, years_to_simulate)

# Fetch and plot the data
data = fetch_population_data()
plot_population_data(data)

# Close the database connection
conn.close()
