import pandas as pd
import pytest
import os
from processs_load_data import load_data

def test_load_data():
    
    # Create a sample CSV file for testing
    data = {
        "lat": [10.0, 20.0, 30.0],
        "long": [100.0, 110.0, 120.0],
        "fna": ["A", "B", "C"]
    }
    df = pd.DataFrame(data)
    
    # Save to a temporary CSV file
    test_csv_path = "test_data.csv"
    df.to_csv(test_csv_path, sep=";", index=False)
    
    try:
        # Load the data using the function
        loaded_df = load_data(test_csv_path)

        # Check if the loaded data matches the original data
        expected_data = {
            "lat": [10.0, 20.0, 30.0],
            "long": [100.0, 110.0, 120.0],
            "fna": ["A", "B", "C"]
        }
        expected_df = pd.DataFrame(expected_data)

        # Assert that the loaded DataFrame matches the expected DataFrame
        pd.testing.assert_frame_equal(loaded_df.reset_index(drop=True), expected_df.reset_index(drop=True))

    finally:
        
        # Clean up the temporary file
        if os.path.exists(test_csv_path):
            os.remove(test_csv_path)
    


