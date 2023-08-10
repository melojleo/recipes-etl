import pandas as pd
import requests
import json

# Function to fetch data from a JSON API endpoint
def get_data(url):

    normalized_data = []

    # Fetch JSON data from the URL
    response = requests.get(url)
    json_text = response.text

    # Split lines
    lines = json_text.strip().split('\n')

    # normalized_data
    for line in lines:
        json_data = json.loads(line)
        normalized_data.append(json_data)

    # Create a DataFrame 
    df = pd.DataFrame(normalized_data)
    
    # Extract recipes with chili ingredients
    chilies_variations = ["chilies", "chiles", "chili"]
    chilies_recipes = df[df['ingredients'].str.lower().str.contains('|'.join(chilies_variations))].reset_index()
    
    return chilies_recipes

# Function to convert to seconds
def convert_time_to_seconds(value):

    # Remove the "PT" 
    value = value.replace('PT', '')

    total_seconds = 0

    if 'H' in value and 'M' in value:
        parts = value.split('H')
        hours_multiplier = int(parts[0])

        minutes_part = parts[1].split('M')[0]
        minutes_multiplier = int(minutes_part)

        total_seconds += (hours_multiplier * 3600) + (minutes_multiplier * 60)
    elif 'H' in value:
        parts = value.split('H')
        hours_multiplier = int(parts[0])
        total_seconds += hours_multiplier * 3600
    elif 'M' in value:
        parts = value.split('M')
        minutes_multiplier = int(parts[0])
        total_seconds += minutes_multiplier * 60

    return total_seconds


# Function to add difficulty field
def add_difficulty_field(row):

    total_time = row['prepTimeInSeconds'] + row['cookTimeInSeconds']

    if total_time > 3600:
        return 'Hard'
    elif total_time >= 1800:
        return 'Medium'
    elif total_time < 1800 and total_time > 0:
        return 'Easy'
    else:
        return 'Unknown'


# Function to save DataFrame to CSV
def save_to_csv(df, filename, separator='|'):

    # Remove duplicates based on all columns
    df_no_duplicates = df.drop_duplicates()

    # Save DataFrame to CSV file 
    df_no_duplicates.to_csv(filename, sep='|', index=False)


# Function to calculate and save average total time
def calculate_and_save_average_total_time(df):

    # Sum 'cookTimeInSeconds' and 'prepTimeInSeconds' 
    df['total_time'] = df['cookTimeInSeconds'] + df['prepTimeInSeconds']
    
    # Filter out rows where 'difficulty' is not 'Unknown'
    filtered_df = df[df['difficulty'] != 'Unknown']
    
    # Calculate average 'total_time' grouped by 'difficulty'
    average_times = filtered_df.groupby('difficulty')['total_time'].mean()
    
    # Create a DataFrame with calculated averages
    results_df = pd.DataFrame({
        'difficulty': average_times.index,
        'average_total_time': average_times.values
    })
    
    # Save the results to Results.csv with 
    results_df.to_csv('Results.csv', sep='|', index=False)

# URL of the JSON file
url = "https://bnlf-tests.s3.eu-central-1.amazonaws.com/recipes.json"

# Get recipes with chili-related ingredients
chilies_df = get_data(url)

# Apply the 'convert_time_to_seconds' function to 'cookTime' and 'prepTime' columns
chilies_df['cookTimeInSeconds'] = chilies_df['cookTime'].apply(convert_time_to_seconds)
chilies_df['prepTimeInSeconds'] = chilies_df['prepTime'].apply(convert_time_to_seconds)

# Add the 'difficulty' field to the DataFrame
chilies_df['difficulty'] = chilies_df.apply(add_difficulty_field, axis=1)

# Save DataFrame to CSV file
save_to_csv(chilies_df, 'Chilies.csv')

# Calculate and save the average total time
calculate_and_save_average_total_time(chilies_df)
