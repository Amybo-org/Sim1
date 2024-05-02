# fermentation.py

import numpy as np
import csv

class Strain:
    def __init__(self, name, cell_OD, max_growth_rate, H2_req, CO2_req, nutrient_req):
        self.name = name
        self.cell_OD = float(cell_OD)
        self.max_growth_rate = float(max_growth_rate)
        self.H2_req = float(H2_req)
        self.CO2_req = float(CO2_req)
        self.nutrient_req = float(nutrient_req)
        self.count = 0  # Initialize count to 0
        self.OD = self.count * self.cell_OD  # Initialize OD

    def calculate_changes(self, H2_conc, CO2_conc, nutrient_conc, time_period):
        # Calculate the growth rate based on the concentrations of H2, CO2, and nutrients
        # Using Monod kinetics, assume growth rate is limited by the substrate with the lowest concentration
        min_conc = min(H2_conc / self.H2_req, CO2_conc / self.CO2_req, nutrient_conc / self.nutrient_req)

        # The actual growth rate is the minimum of the maximum growth rate and the Monod growth rate
        growth_rate = min(self.max_growth_rate, min_conc)

        # Calculate the change in cell count
        delta_count = growth_rate * self.count * time_period

        # Calculate the changes in the concentrations of H2, CO2, and nutrients
        # Assume that the strain consumes these substrates in proportion to its growth
        delta_H2 = max(-H2_conc, -delta_count * self.H2_req)
        delta_CO2 = max(-CO2_conc, -delta_count * self.CO2_req)
        delta_nutrient = max(-nutrient_conc, -delta_count * self.nutrient_req)

        # Update the cell count
        self.count += min(delta_H2 / self.H2_req, delta_CO2 / self.CO2_req, delta_nutrient / self.nutrient_req)

        # Update the optical density
        self.OD = max(0, self.count * self.cell_OD)

        # Return the changes in the concentrations of H2, CO2, and nutrients
        return delta_H2, delta_CO2, delta_nutrient

def load_strains_from_file(file_path):
    strains = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            name, cell_OD, max_growth_rate, H2_req, CO2_req, nutrient_req = row
            strain = Strain(name, float(cell_OD), float(max_growth_rate), float(H2_req), float(CO2_req), float(nutrient_req))
            strains.append(strain)
    return strains

def simulate_fermentation(strains, initial_count, initial_H2_conc=1.0, initial_CO2_conc=1.0, initial_nutrient_conc=1.0, time_period=100):
  # Set the initial count for each strain
  for strain in strains:
      strain.count = initial_count
  H2_conc = initial_H2_conc
  CO2_conc = initial_CO2_conc
  nutrient_conc = initial_nutrient_conc

  # Initialize a list to hold the total optical density over time
  total_OD = []

  # For each time period:
  for t in range(time_period):
    # Initialize the changes in the concentrations of H2, CO2, and nutrients
    delta_H2 = delta_CO2 = delta_nutrient = 0

    # Initialize the total optical density for this time period
    OD = 0

    # For each strain:
    for strain in strains:
      # Call the strain's calculate_changes method
      dH2, dCO2, dNutrient = strain.calculate_changes(H2_conc, CO2_conc, nutrient_conc, 1)

      # Sum the changes to get the overall culture values
      delta_H2 += dH2
      delta_CO2 += dCO2
      delta_nutrient += dNutrient

      # Add the strain's optical density to the total
      OD += strain.OD

    # Update the concentrations for the next time period
    H2_conc += delta_H2
    CO2_conc += delta_CO2
    nutrient_conc += delta_nutrient

    # Add the total optical density for this time period to the list
    total_OD.append(OD)

  # Return the total optical density over time
  print('Total OD: ', total_OD)
  return total_OD

print('Loading strains...')
strains = load_strains_from_file('data/strains_data.csv')
print('Loaded {} strains'.format(len(strains)))

print('Simulating fermentation...')
total_OD = simulate_fermentation(strains, initial_count=1000, initial_H2_conc=1.0, initial_CO2_conc=1.0, initial_nutrient_conc=1.0, time_period=100)
print('Simulation complete')