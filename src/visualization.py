import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_crime_trends(df):
    """Plot overall crime trends by year."""
    crime_per_year = df.groupby('occ_year')['DR_NO'].sum()
    
    plt.figure(figsize=(10, 6))
    crime_per_year.plot(kind='bar', color='skyblue')
    plt.xlabel('Year')
    plt.ylabel('Total Number of Crimes')
    plt.title('Total Number of Crimes Per Year')
    plt.xticks(rotation=45)
    
    return plt.gcf()

def plot_seasonal_patterns(df):
    """Plot seasonal patterns in crime data."""
    crime_by_month = df.groupby('occ_month').count().reset_index()
    
    plt.figure(figsize=(10, 6))
    plt.title('Seasonal pattern in crime data')
    sns.barplot(data=crime_by_month, x='occ_month', y='Crm Cd Desc')
    plt.xlabel('Month')
    plt.ylabel('Number of Crimes')
    plt.xticks(range(12), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 
                          'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    
    return plt.gcf()

def plot_crime_by_region(df):
    """Plot crime rates by region."""
    crime_by_region = df.groupby('AREA NAME')['DR_NO'].count().reset_index()
    crime_by_region = crime_by_region.sort_values(by='DR_NO', ascending=False)
    
    plt.figure(figsize=(10, 6))
    plt.title('Crime Rates by Region')
    sns.barplot(data=crime_by_region, x='AREA NAME', y='DR_NO')
    plt.ylabel('Number of Crimes')
    plt.xticks(rotation=45)
    
    return plt.gcf()

def plot_economic_correlation(correlation):
    """Plot correlation between economic factors and crime rates."""
    plt.figure(figsize=(10, 6))
    sns.heatmap(data=correlation, annot=True)
    plt.title('Correlation Between Economic Factor and Crime Rate')
    
    return plt.gcf()