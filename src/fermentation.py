# fermentation.py

import numpy as np
import csv

class Strain:
    def __init__(self, name, cell_OD, max_growth_rate, H2_half_velocity, CO2_half_velocity, NH3_half_velocity):
        self.name = name  # Strain name
        self.cell_OD = float(cell_OD)  # Each cell's contribution to the optical density
        self.max_growth_rate = float(max_growth_rate) 
        self.H2_half_velocity = float(H2_half_velocity)  # H2 half-velocity constant
        self.CO2_half_velocity = float(CO2_half_velocity)  # CO2 half-velocity constant
        self.NH3_half_velocity = float(NH3_half_velocity)  # NH3 half-velocity constant
        self.biomass = 0  # Initialize biomass to 0

    def calculate_growth_rate(self, H2_conc, CO2_conc, NH3_conc):
        # Calculate the growth rate using the Monod equation
        H2_growth_rate = self.max_growth_rate * H2_conc / (self.H2_half_velocity + H2_conc)
        CO2_growth_rate = self.max_growth_rate * CO2_conc / (self.CO2_half_velocity + CO2_conc)
        NH3_growth_rate = self.max_growth_rate * NH3_conc / (self.NH3_half_velocity + NH3_conc)

        # The overall growth rate is the minimum of the growth rates for each substrate
        return min(H2_growth_rate, CO2_growth_rate, NH3_growth_rate)

    def calculate_changes(self, H2_conc, CO2_conc, NH3_conc, time_period):
        # Calculate the growth rate
        growth_rate = self.calculate_growth_rate(H2_conc, CO2_conc, NH3_conc)

        # Calculate the changes in the concentrations of H2, CO2, and NH3
        delta_H2 = -growth_rate * self.biomass / H2_conc
        delta_CO2 = -growth_rate * self.biomass / CO2_conc
        delta_NH3 = -growth_rate * self.biomass / NH3_conc

        # Update the biomass
        self.biomass += growth_rate * time_period

        # Return the changes in the concentrations of H2, CO2, and NH3
        return delta_H2, delta_CO2, delta_NH3

def load_strains_from_file(file_path):
  strains = []
  with open(file_path, 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
      name, cell_OD, max_growth_rate, H2_half_velocity, CO2_half_velocity, NH3_half_velocity = row
      strain = Strain(name, float(cell_OD), float(max_growth_rate), float(H2_half_velocity), float(CO2_half_velocity), float(NH3_half_velocity))
      strains.append(strain)
  return strains

def simulate_fermentation(strains, initial_count, initial_H2_conc=1.0, initial_CO2_conc=1.0, initial_NH3_conc=1.0, time_period=100, time_periods=100):
  # Set the initial count for each strain
  for strain in strains:
      strain.count = initial_count
  H2_conc = initial_H2_conc
  CO2_conc = initial_CO2_conc
  NH3_conc = initial_NH3_conc

  # Initialize a list to hold the total optical density over time
  total_OD = []

  # For each time period:
  for t in range(time_periods):
    # Initialize the changes in the concentrations of H2, CO2, and NH3
    delta_H2 = delta_CO2 = delta_NH3 = 0

    # Initialize the total optical density for this time period
    OD = 0

    # For each strain:
    for strain in strains:
      # Call the strain's calculate_changes method
      dH2, dCO2, dNH3 = strain.calculate_changes(H2_conc, CO2_conc, NH3_conc, time_period)

      # Sum the changes to get the overall culture values
      delta_H2 += dH2
      delta_CO2 += dCO2
      delta_NH3 += dNH3

      # Add the strain's optical density to the total
      OD += strain.OD

    # Update the concentrations for the next time period
    H2_conc += delta_H2
    CO2_conc += delta_CO2
    NH3_conc += delta_NH3

    # Add the total optical density for this time period to the list
    total_OD.append(OD)

  # Return the total optical density over time
  print('Total OD: ', total_OD)
  return total_OD

print('Loading strains...')
strains = load_strains_from_file('data/strains_data.csv')
print('Loaded {} strains'.format(len(strains)))

print('Simulating fermentation...')
total_OD = simulate_fermentation(strains, initial_count=1000, initial_H2_conc=1.0, initial_CO2_conc=1.0, initial_NH3_conc=1.0, time_period=10, time_periods=5)
print('Simulation complete')