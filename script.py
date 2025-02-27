import pandas as pd
from pathlib import Path

# Define base directory
base_dir = Path("./multilevel-monitoring-of-activity-and-sleep-in-healthy-people-1.0.0/DataPaper")

def load_hrv_data(filepath):
    """Load heart rate variability (HRV) data from RR.csv."""
    if not filepath.exists():
        print(f"HRV data file not found: {filepath}")
        return None
    df = pd.read_csv(filepath)

    # Check column names
    print(f"HRV columns: {df.columns.tolist()}")  # Debugging
    
    if {"day", "time"}.issubset(df.columns):
        # Ensure 'day' and 'time' are strings before concatenation
        df['day'] = df['day'].astype(str)
        df['time'] = df['time'].astype(str)
        df['timestamp'] = pd.to_datetime(
    df['day'] + ' ' + df['time'], 
    format='%Y-%m-%d %H:%M:%S',  # Adjust based on your actual format
    errors='coerce'
)
    else:
        print("Error: Expected columns 'day' and 'time' not found in HRV data.")
        return None
    
    print(f"HRV data loaded successfully: {df.shape[0]} rows from {filepath.name}")
    return df

def load_sleep_logs(filepath):
    """Load sleep log data from a CSV file."""
    if not filepath.exists():
        print(f"Sleep log file not found: {filepath}")
        return None
    df = pd.read_csv(filepath)

    # Debug: Print column names
    print(f"Sleep log columns: {df.columns.tolist()}")  

    if {"Onset Date", "Onset Time"}.issubset(df.columns):
        # Convert both columns to strings before concatenation
        df['Onset Date'] = df['Onset Date'].astype(str)
        df['Onset Time'] = df['Onset Time'].astype(str)
        df['sleep_start'] = pd.to_datetime(df['Onset Date'] + ' ' + df['Onset Time'], errors='coerce')
    else:
        print("Error: Expected columns 'Onset Date' and 'Onset Time' not found in sleep data.")
        return None
    
    print(f"Sleep logs loaded successfully: {df.shape[0]} rows from {filepath.name}")
    return df

def preprocess_data(hrv_df, sleep_df):
    """Preprocess HRV and sleep log data for merging."""
    
    # Ensure required columns exist
    if {"Out Bed Date", "Out Bed Time"}.issubset(sleep_df.columns):
        # Convert to datetime
        sleep_df['Out Bed Date'] = sleep_df['Out Bed Date'].astype(str)
        sleep_df['Out Bed Time'] = sleep_df['Out Bed Time'].astype(str)
        sleep_df['sleep_end'] = pd.to_datetime(sleep_df['Out Bed Date'] + ' ' + sleep_df['Out Bed Time'], errors='coerce')
    else:
        print("Error: 'Out Bed Date' or 'Out Bed Time' missing from sleep data.")
        return None

    print(f"Preprocessed sleep logs: {sleep_df.shape[0]} rows")

    return sleep_df

if __name__ == "__main__":
    # Loop through each user folder
    for user_folder in base_dir.iterdir():
        if user_folder.is_dir():  # Ensure it's a directory
            hrv_file =  user_folder.joinpath("RR.csv")  # Corrected filename
            sleep_log_file = user_folder.joinpath("sleep.csv")  # Corrected filename

            if hrv_file.exists() and sleep_log_file.exists():
                print(f"\nProcessing data for {user_folder.name}...")

                # Load datasets
                hrv_data = load_hrv_data(hrv_file)
                sleep_logs = load_sleep_logs(sleep_log_file)

                # Preprocess and merge datasets
                merged_data = preprocess_data(hrv_data, sleep_logs)

                if merged_data is not None:
                    # Ensure output directory exists
                    output_dir = user_folder.joinpath("processed_data")
                    output_dir.mkdir(exist_ok=True)

                    # Save merged dataset
                    output_file = output_dir.joinpath("merged_hrv_sleep_data.csv")
                    merged_data.to_csv(output_file, index=False)
                    print(f"Merged data saved to {output_file}")
            else:
                print(f"Missing files for {user_folder.name}")