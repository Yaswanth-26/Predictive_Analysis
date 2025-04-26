import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

def prepare_data_for_prophet(df):
    """Prepare data for Prophet forecasting."""
    # Group by date and count occurrences
    prophet_data = df.groupby('Date Rptd').count().reset_index()[['Date Rptd', 'DR_NO']]
    
    # Rename columns to Prophet's required format
    prophet_data.rename(columns={'Date Rptd': 'ds', 'DR_NO': 'y'}, inplace=True)
    
    return prophet_data

def create_forecast_model(df, periods=365):
    """Create a Prophet forecast model."""
    # Prepare data
    prophet_data = prepare_data_for_prophet(df)
    
    # Create and fit model
    model = Prophet()
    model.fit(prophet_data)
    
    # Make future dataframe
    future = model.make_future_dataframe(periods=periods)
    
    # Forecast
    forecast = model.predict(future)
    
    return model, forecast

def plot_forecast(model, forecast):
    """Plot the forecast results."""
    fig = model.plot(forecast)
    plt.title('Crime Forecast')
    
    return fig

def plot_forecast_components(model, forecast):
    """Plot the forecast components."""
    fig = model.plot_components(forecast)
    
    return fig
