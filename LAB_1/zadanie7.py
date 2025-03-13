import unittest

class TemperatureConverter:
    @staticmethod
    def celsius_to_fahrenheit(celsius):
        return celsius * 9/5 + 32

    @staticmethod
    def fahrenheit_to_celsius(fahrenheit):
        return (fahrenheit - 32) * 5/9

    @staticmethod
    def celsius_to_kelvin(celsius):
        return celsius + 273.15

    @staticmethod
    def kelvin_to_celsius(kelvin):
        return kelvin - 273.15



class TestTemperatureConverter(unittest.TestCase):
    def test_celsius_to_fahrenheit(self):
        self.assertAlmostEqual(TemperatureConverter.celsius_to_fahrenheit(25), 77)
        self.assertAlmostEqual(TemperatureConverter.celsius_to_fahrenheit(-40), -40)
        self.assertAlmostEqual(TemperatureConverter.celsius_to_fahrenheit(0), 32)

    def test_fahrenheit_to_celsius(self):
        self.assertAlmostEqual(TemperatureConverter.fahrenheit_to_celsius(77), 25)
        self.assertAlmostEqual(TemperatureConverter.fahrenheit_to_celsius(-40), -40)
        self.assertAlmostEqual(TemperatureConverter.fahrenheit_to_celsius(32), 0)

    def test_celsius_to_kelvin(self):
        self.assertAlmostEqual(TemperatureConverter.celsius_to_kelvin(25), 298.15)
        self.assertAlmostEqual(TemperatureConverter.celsius_to_kelvin(-273.15), 0)
        self.assertAlmostEqual(TemperatureConverter.celsius_to_kelvin(0), 273.15)

    def test_kelvin_to_celsius(self):
        self.assertAlmostEqual(TemperatureConverter.kelvin_to_celsius(298.15), 25)
        self.assertAlmostEqual(TemperatureConverter.kelvin_to_celsius(0), -273.15)
        self.assertAlmostEqual(TemperatureConverter.kelvin_to_celsius(273.15), 0)

if __name__ == '__main__':
    unittest.main()