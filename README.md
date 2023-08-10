# Recipe ETL Application README

This repository contains a Python script that performs ETL (Extract, Transform, Load) operations on recipe data. The script downloads a JSON file containing recipes, processes the data, and generates CSV files with relevant information. Below are the instructions to run the script and details about its functionality.

## Instructions

1. **Clone the Repository:** Start by cloning this repository to your local machine:

   ```bash
   git clone https://github.com/your-username/hf_bi_python_excercise.git

2. **Navigate to the Directory:** Move into the recipes-etl directory:

   ```bash
   cd recipes-etl\hf_bi_python_excercise

3. **Install Dependencies:**  Install the required packages. It's recommended to use a virtual environment:

   ```bash
   python -m venv venv
    # On Linux, use:source venv/bin/activate  
   venv\Scripts\activate
   pip install -r .\requirements.txt

4. **Run the Script:**  Execute the script to perform ETL operations:

   ```bash
   python .\main.py


## Functionality


The Python script performs the following tasks:


1. **Fetch Data:** Fetches recipe data from a JSON API endpoint
2. **Extract Recipes:** Extracts recipes containing variations of the word "chili" in their ingredients.
3. **Add Difficulty Level:** Adds a difficulty level field to each extracted recipe based on total preparation and cooking time.
4. **Save Extracted Recipes:** Saves the extracted chili recipes to a CSV file named Chilies.csv.
5. **Calculate Average Time:** Calculates the average total time for recipes of different difficulty levels and saves the results to Results.csv.

## Unit Tests

The repository includes unit tests to ensure the functionality of the script. To run the tests, navigate to the recipes-etl directory and execute:
    
```bash
python .\hf_bi_python_excercise\test_module.py
