import unittest
import sys
import os
import csv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from fermentation import Strain, simulate_fermentation

class TestFermentation(unittest.TestCase):
  def setUp(self):
    self.strain = Strain('test_strain', 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8)

  def test_strain_creation(self):
    with open('data/strains_data.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip the header row
        for row in reader:
            if row[0] == 'test_strain':  # Find the row for 'test_strain'
                self.assertEqual(self.strain.name, row[0])
                self.assertEqual(self.strain.biomass_OD, float(row[1]))
                self.assertEqual(self.strain.Y_H2, float(row[2]))
                self.assertEqual(self.strain.Y_CO2, float(row[3]))
                self.assertEqual(self.strain.Y_NH3, float(row[4]))
                self.assertEqual(self.strain.H2_consumption, float(row[5]))
                self.assertEqual(self.strain.CO2_consumption, float(row[6]))
                self.assertEqual(self.strain.NH3_consumption, float(row[7]))
                self.assertEqual(self.strain.biomass_consumption, float(row[8]))
                break

  def test_simulate_fermentation(self):
    strains = [self.strain]

    # Test that total_OD increases with each iteration
    total_OD = simulate_fermentation(strains, initial_count=1000, initial_H2_conc=10.0, initial_CO2_conc=10.0, initial_NH3_conc=10.0, time_period=10, time_periods=5)
    for i in range(1, len(total_OD)):
      self.assertGreater(total_OD[i], total_OD[i-1])

    # Test that total_OD stays constant when time period is 0
    total_OD = simulate_fermentation(strains, initial_count=1000, initial_H2_conc=1.0, initial_CO2_conc=1.0, initial_NH3_conc=1.0, time_period=0, time_periods=5)
    for i in range(1, len(total_OD)):
      self.assertEqual(total_OD[i], total_OD[i-1])

if __name__ == '__main__':
  unittest.main()