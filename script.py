import pandas as pd
import os

# Define file paths
data_dir = "data/"
hrv_file = os.path.join(data_dir, "hrv_data.csv")
sleep_log_file = os.path.join(data_dir, "sleep_logs.csv")

def load_hrv_data(filepath):
    """Load heart rate variability (HRV) data from a CSV file."""
    try:
        df = pd.read_csv(filepath)
        print(f"HRV data loaded successfully: {df.shape[0]} rows")
        return df
    except FileNotFoundError:
        print("HRV data file not found.")
        return None

def load_sleep_logs(filepath):
    """Load sleep log data from a CSV file."""
    try:
        df = pd.read_csv(filepath)
        print(f"Sleep logs loaded successfully: {df.shape[0]} rows")
        return df
    except FileNotFoundError:
        print("Sleep log file not found.")
        return None

def preprocess_data(hrv_df, sleep_df):
    """Clean and merge HRV and sleep datasets."""
    if hrv_df is None or sleep_df is None:
        print("Error: One or both datasets are missing.")
        return None
    
    # Convert timestamps to datetime format
    hrv_df['timestamp'] = pd.to_datetime(hrv_df['timestamp'])
    sleep_df['sleep_start'] = pd.to_datetime(sleep_df['sleep_start'])
    sleep_df['sleep_end'] = pd.to_datetime(sleep_df['sleep_end'])
    
    # Merge datasets based on closest timestamps
    merged_df = pd.merge_asof(hrv_df.sort_values('timestamp'), 
                              sleep_df.sort_values('sleep_start'),
                              left_on='timestamp', right_on='sleep_start',
                              direction='backward')
    
    print(f"Merged dataset contains {merged_df.shape[0]} rows.")
    return merged_df

if __name__ == "__main__":
    # Load datasets
    hrv_data = load_hrv_data(hrv_file)
    sleep_logs = load_sleep_logs(sleep_log_file)
    
    # Preprocess and merge datasets
    merged_data = preprocess_data(hrv_data, sleep_logs)
    
    if merged_data is not None:
        # Ensure output directory exists
        os.makedirs(data_dir, exist_ok=True)
        
        # Save merged dataset
        output_file = os.path.join(data_dir, "merged_hrv_sleep_data.csv")
        merged_data.to_csv(output_file, index=False)
        print(f"Merged data saved to {output_file}")
