import unittest
from fermentation import Strain, simulate_fermentation

class TestFermentation(unittest.TestCase):
  def setUp(self):
    self.strain = Strain('test_strain', 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8)

  def test_strain_creation(self):
    self.assertEqual(self.strain.name, 'test_strain')
    self.assertEqual(self.strain.biomass_OD, 0.1)
    self.assertEqual(self.strain.H2_yield, 0.2)
    self.assertEqual(self.strain.CO2_yield, 0.3)
    self.assertEqual(self.strain.NH3_yield, 0.4)
    self.assertEqual(self.strain.H2_consumption, 0.5)
    self.assertEqual(self.strain.CO2_consumption, 0.6)
    self.assertEqual(self.strain.NH3_consumption, 0.7)
    self.assertEqual(self.strain.biomass_consumption, 0.8)

  def test_simulate_fermentation(self):
    strains = [self.strain]
    total_OD = simulate_fermentation(strains, initial_count=1000, initial_H2_conc=1.0, initial_CO2_conc=1.0, initial_NH3_conc=1.0, time_period=10, time_periods=5)
    self.assertEqual(total_OD, 1000)

if __name__ == '__main__':
  unittest.main()