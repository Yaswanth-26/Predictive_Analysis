import sys
import os
from pathlib import Path

# Get the absolute path to the project directory
project_dir = str(Path(__file__).parent.absolute())

# Add the project directory to Python's path
if project_dir not in sys.path:
    sys.path.append(project_dir)
    print(f"Added {project_dir} to Python path")

# Now import the modules from src
try:
    from src.data_processing import load_data, clean_data, normalize_data, load_economic_data
    from src.visualization import plot_crime_trends, plot_seasonal_patterns, plot_crime_by_region, plot_economic_correlation
    from src.analysis import get_most_common_crime, analyze_crime_by_day, analyze_economic_correlation
    from src.forecasting import create_forecast_model, plot_forecast
    print("All modules imported successfully!")
except ImportError as e:
    print(f"Import error: {e}")
    print("Current sys.path:", sys.path)


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_forecast_components(model, forecast):
    """Plot the forecast components."""
    fig = model.plot_components(forecast)
    return fig


def main():
    # Get the absolute path to your project directory
    project_dir = Path(__file__).parent.absolute()
    
    # Create absolute paths to your data files
    crime_file_path = os.path.join(project_dir, "data", "raw", "Crime_Data_from_2020_to_Present.csv")
    economic_file_path = os.path.join(project_dir, "data", "raw", "economic factors.csv")
    
    # Ensure the directories exist
    os.makedirs(os.path.join(project_dir, "data", "processed"), exist_ok=True)
    os.makedirs(os.path.join(project_dir, "results"), exist_ok=True)
    
    # Check if the files exist
    if not os.path.exists(crime_file_path):
        print(f"Error: Crime data file not found at {crime_file_path}")
        return
    
    if not os.path.exists(economic_file_path):
        print(f"Error: Economic data file not found at {economic_file_path}")
        return
        
    print(f"Found crime data at: {crime_file_path}")
    print(f"Found economic data at: {economic_file_path}")
    df = load_data(crime_file_path)
    
    # Clean and preprocess crime data
    df_clean = clean_data(df)
    
    # Save processed crime data
    df_clean.to_csv("data/processed/cleaned_crime_data.csv", index=False)
    
    # Basic analysis
    most_common_crime, frequency = get_most_common_crime(df_clean)
    print(f"Most common crime: {most_common_crime} with {frequency} occurrences")
    
    # Generate visualizations
    plt.figure(figsize=(15, 10))
    
    plt.subplot(2, 2, 1)
    plot_crime_trends(df_clean)
    
    plt.subplot(2, 2, 2)
    plot_seasonal_patterns(df_clean)
    
    plt.subplot(2, 2, 3)
    plot_crime_by_region(df_clean)
    
    plt.tight_layout()
    plt.savefig("results/crime_analysis_summary.png")
    
    # Economic data analysis
    economic_file_path = "data/raw/economic factors.csv"
    economic_data = load_economic_data(economic_file_path)
    
    # Analyze correlation between crime and economic factors
    correlation, updated_economic_data = analyze_economic_correlation(df_clean, economic_data)
    
    # Plot economic correlation
    econ_fig = plot_economic_correlation(correlation)
    econ_fig.savefig("results/economic_correlation.png")
    
    # Save updated economic data with crime counts
    updated_economic_data.to_csv("data/processed/economic_with_crime.csv", index=False)
    
    # Time series forecasting
    model, forecast = create_forecast_model(df_clean)
    forecast_fig = plot_forecast(model, forecast)
    forecast_fig.savefig("results/crime_forecast.png")
    
    components_fig = plot_forecast_components(model, forecast)
    components_fig.savefig("results/forecast_components.png")

if __name__ == "__main__":
    main()