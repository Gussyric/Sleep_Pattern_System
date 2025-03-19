import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

# Define base directory
base_dir = Path("./multilevel-monitoring-of-activity-and-sleep-in-healthy-people-1.0.0/DataPaper")

def load_actigraph_data(filepath):
    """Load actigraph data from actigraph.csv."""
    if not filepath.exists():
        print(f"Actigraph data file not found: {filepath}")
        return None
    df = pd.read_csv(filepath)
    
    # Check column names for actigraph data
    print(f"Actigraph columns: {df.columns.tolist()}")  # Debugging

    if {"day", "time"}.issubset(df.columns):
        # Assume 'day' is always '1' and combine with a fixed date (e.g., '2025-03-17')
        df['timestamp'] = pd.to_datetime('2025-03-17 ' + df['time'].astype(str), format='%Y-%m-%d %H:%M:%S', errors='coerce')
        
        # Use 'Vector Magnitude' as an activity level
        df['activity_level'] = df['Vector Magnitude']  # Use Vector Magnitude for activity level
        
    else:
        print("Error: Expected columns 'day' and 'time' not found in actigraph data.")
        return None
    
    print(f"Actigraph data loaded successfully: {df.shape[0]} rows from {filepath.name}")
    return df

def visualize_actigraph_data(user_folder):
    """Visualize actigraph data."""
    # Filepath for actigraph data
    actigraph_filepath = user_folder / "actigraph.csv"
    
    if not actigraph_filepath.exists():
        print(f"Missing file in {user_folder}")
        return
    
    # Load actigraph data
    actigraph_df = load_actigraph_data(actigraph_filepath)
    if actigraph_df is None:
        return

    # --- 1. Actigraph Data (Activity Level) ---
    if not actigraph_df.empty:
        plt.figure(figsize=(10, 5))
        plt.plot(actigraph_df["timestamp"], actigraph_df["activity_level"], color="purple", label="Activity Level")
        plt.xlabel("Time")
        plt.ylabel("Activity Level")
        plt.title("Activity Level Over Time")
        plt.legend()
        plt.grid(True)
        plt.show()
    else:
        print("No valid data available to plot.")

if __name__ == "__main__":
    # Loop through each user folder
    for user_folder in base_dir.iterdir():
        if user_folder.is_dir():  # Ensure it's a directory
            actigraph_file = user_folder / "actigraph.csv"  # Corrected filename
            
            if actigraph_file.exists():
                print(f"\nProcessing data for {user_folder.name}...")

                # Visualize the actigraph data
                print(f"\nVisualizing data for {user_folder.name}...")
                visualize_actigraph_data(user_folder)
            else:
                print(f"Missing actigraph file for {user_folder.name}")