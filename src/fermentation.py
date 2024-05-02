# fermentation.py
# See https://en.wikipedia.org/wiki/Monod_equation for an explanation of the Monod equation

import csv

class Strain:
    def __init__(self, name, biomass_OD, max_growth_rate, H2_half_velocity, CO2_half_velocity, NH3_half_velocity, Y_H2, Y_CO2, Y_NH3):
        self.name = name  # Strain name
        self.biomass_OD = float(biomass_OD)  # Each unit biomass' contribution to the optical density
        self.max_growth_rate = float(max_growth_rate) 
        self.H2_half_velocity = float(H2_half_velocity)
        self.CO2_half_velocity = float(CO2_half_velocity)
        self.NH3_half_velocity = float(NH3_half_velocity)
        self.biomass = 0  # Initialize biomass to 0
        self.Y_H2 = float(Y_H2)  # Yield coefficient for H2
        self.Y_CO2 = float(Y_CO2)  # Yield coefficient for CO2
        self.Y_NH3 = float(Y_NH3)  # Yield coefficient for NH3
        
    @property
    # Define the strain's optical density contribution
    def OD(self):
        return self.biomass_OD * self.biomass

    def calculate_growth_rate(self, H2_conc, CO2_conc, NH3_conc):
        # Calculate the growth rate using the Monod equation
        return self.max_growth_rate * H2_conc / (self.H2_half_velocity + H2_conc) * CO2_conc / (self.CO2_half_velocity + CO2_conc) * NH3_conc / (self.NH3_half_velocity + NH3_conc)

    def calculate_changes(self, H2_conc, CO2_conc, NH3_conc, time_period):
        # Calculate the growth rate
        growth_rate = self.calculate_growth_rate(H2_conc, CO2_conc, NH3_conc)

        # Calculate the changes in the concentrations of H2, CO2, and NH3
        delta_H2 = -growth_rate * time_period * self.biomass / self.Y_H2
        delta_CO2 = -growth_rate * time_period * self.biomass / self.Y_CO2
        delta_NH3 = -growth_rate * time_period * self.biomass / self.Y_NH3

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
      name, biomass_OD, max_growth_rate, H2_half_velocity, CO2_half_velocity, NH3_half_velocity, Y_H2, Y_CO2, Y_NH3 = row
      strain = Strain(name, float(biomass_OD), float(max_growth_rate), float(H2_half_velocity), float(CO2_half_velocity), float(NH3_half_velocity), float(Y_H2), float(Y_CO2), float(Y_NH3))
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

def main():
  print('Loading strains...')
  strains = load_strains_from_file('data/strains_data.csv')
  print('Loaded {} strains'.format(len(strains)))

  print('Simulating fermentation...')
  total_OD = simulate_fermentation(strains, initial_count=1000, initial_H2_conc=1.0, initial_CO2_conc=1.0, initial_NH3_conc=1.0, time_period=10, time_periods=5)
  print('Simulation complete')

if __name__ == '__main__':
  main()