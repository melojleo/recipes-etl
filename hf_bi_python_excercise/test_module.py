import pandas as pd
import requests
import json
import unittest
from unittest.mock import patch
from main import (
    get_data, convert_time_to_seconds, add_difficulty_field,
    save_to_csv, calculate_and_save_average_total_time
)

class TestYourModule(unittest.TestCase):

    @patch('requests.get')  
    def test_get_data(self, mock_get):
        # Example data to simulate JSON response
        json_data = [
            {"name": "Easter Leftover Sandwich", "ingredients": "12 whole Hard Boiled Eggs\n1/2 cup Mayonnaise\n3 Tablespoons Grainy Dijon Mustard\n Salt And Pepper, to taste\n Several Dashes Worcestershire Sauce\n Leftover Baked Ham, Sliced\n Kaiser Rolls Or Other Bread\n Extra Mayonnaise And Dijon, For Spreading\n Swiss Cheese Or Other Cheese Slices\n Thinly Sliced Red Onion\n Avocado Slices\n Sliced Tomatoes\n Lettuce, Spinach, Or Arugula"},
            {"name": "Pasta with Pesto Cream Sauce", "ingredients": "3/4 cups Fresh Basil Leaves\n1/2 cup Grated Parmesan Cheese\n3 Tablespoons Pine Nuts\n2 cloves Garlic, Peeled\n Salt And Pepper, to taste\n1/3 cup Extra Virgin Olive Oil\n1/2 cup Heavy Cream\n2 Tablespoons Butter\n1/4 cup Grated Parmesan (additional)\n12 ounces, weight Pasta (cavitappi, Fusili, Etc.)\n2 whole Tomatoes, Diced"},
            {"name": "Herb Roasted Pork Tenderloin with Preserves", "ingredients": "2 whole Pork Tenderloins\n Salt And Pepper, to taste\n8 Tablespoons Herbs De Provence (more If Needed\n1 cup Preserves (fig, Peach, Plum)\n1 cup Water\n1 Tablespoon Vinegar"}
            
        ]
        
        json_text = '\n'.join(json.dumps(data) for data in json_data)

        # Configure the mock to return the simulated response
        mock_response = mock_get.return_value
        mock_response.text = json_text

        # Call the get_data function
        url = "https://bnlf-tests.s3.eu-central-1.amazonaws.com/recipes.json"
        result = get_data(url)

        # Define the expected result based on simulated data
        expected_result = pd.DataFrame(json_data, columns=['name', 'ingredients'])

        # Extract chili-related recipes manually from the expected result
        chilies_variations = ["chilies", "chiles", "chili"]
        expected_chilies_recipes = expected_result[expected_result['ingredients'].str.lower().str.contains('|'.join(chilies_variations))].reset_index()

        # Compare the expected result with the actual result (chilies recipes only)
        self.assertTrue(result.equals(expected_chilies_recipes))
        
    def test_conversion(self):
        data = {
            'cookTime': ['PT10M', 'PT5M', 'PT20M', 'PT15M', 'PT3H', 'PT20M', '100M', '7H', '1H30M'],
            'prepTime': ['PT5M', 'PT10M', 'PT15M', 'PT1H', 'PT30M', 'PT10M', '1H', '5H', '1H30M']
        }

        expected_cookTimeInSeconds = [600, 300, 1200, 900, 10800, 1200, 6000, 25200, 5400]
        expected_prepTimeInSeconds = [300, 600, 900, 3600, 1800, 600, 3600, 18000, 5400]

        chilies_df = pd.DataFrame(data)
        chilies_df['cookTimeInSeconds'] = chilies_df['cookTime'].apply(convert_time_to_seconds)
        chilies_df['prepTimeInSeconds'] = chilies_df['prepTime'].apply(convert_time_to_seconds)

        self.assertEqual(chilies_df['cookTimeInSeconds'].tolist(), expected_cookTimeInSeconds)
        self.assertEqual(chilies_df['prepTimeInSeconds'].tolist(), expected_prepTimeInSeconds)
    
    def test_easy(self):
        row = {'prepTimeInSeconds': 300, 'cookTimeInSeconds': 600}
        self.assertEqual(add_difficulty_field(row), 'Easy')

    def test_medium(self):
        row = {'prepTimeInSeconds': 900, 'cookTimeInSeconds': 1200}
        self.assertEqual(add_difficulty_field(row), 'Medium')

    def test_hard(self):
        row = {'prepTimeInSeconds': 2400, 'cookTimeInSeconds': 1500}
        self.assertEqual(add_difficulty_field(row), 'Hard')

    def test_unknown(self):
        row = {'prepTimeInSeconds': 0, 'cookTimeInSeconds': 0}
        self.assertEqual(add_difficulty_field(row), 'Unknown')
        
    def test_save_csv(self):
        # Created example Df
        data = {'col1': [1, 2, 3],
                'col2': ['A', 'B', 'C']}
        df = pd.DataFrame(data)

        # Save to CVS
        filename = 'test_output.csv'
        save_to_csv(df, filename)

        # Read the CSV
        df_read = pd.read_csv(filename, sep='|')

        # Check both dataframes
        self.assertTrue(df.equals(df_read))

    def test_calculate_and_save_average_total_time(self):
        data = {
            'difficulty': ['Hard', 'Medium', 'Easy', 'Unknown', 'Hard', 'Medium', 'Easy', 'Hard'],
            'cookTimeInSeconds': [3600, 1800, 900, 0, 2700, 2400, 1200, 3600],
            'prepTimeInSeconds': [1800, 1200, 600, 0, 1800, 2400, 600, 1800]
        }

        df = pd.DataFrame(data)
        
        calculate_and_save_average_total_time(df)
        
        results_df = pd.read_csv('Results.csv', sep='|')
        
        expected_results = {
            'difficulty': ['Easy', 'Hard', 'Medium'],
            'average_total_time': [1650.0, 5100.0, 3900.0]  
        }
        
        expected_results_df = pd.DataFrame(expected_results)
        
        pd.testing.assert_frame_equal(results_df, expected_results_df)

if __name__ == '__main__':
    unittest.main()







    