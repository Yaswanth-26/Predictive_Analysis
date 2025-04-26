import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def get_most_common_crime(df):
    """Identify the most common crime type."""
    crime_counts = df['Crm Cd Desc'].value_counts()
    most_common_crime = crime_counts.idxmax()
    frequency = crime_counts.max()
    
    return most_common_crime, frequency

def analyze_crime_by_day(df, crime_types=None):
    """Analyze crime frequencies by day of the week."""
    if crime_types:
        filtered_data = df[df['Crm Cd Desc'].isin(crime_types)]
    else:
        filtered_data = df
        
    crime_by_day = filtered_data.groupby('Day of Week')['DR_NO'].count().reset_index()
    
    return crime_by_day

def analyze_economic_correlation(df, economic_data):
    """Analyze correlation between crime rates and economic factors."""
    # Group crime data by year and month to count occurrences
    crime_data = df.groupby(['occ_year', 'occ_month']).count()
    
    # Add crime count to economic data
    # This matches exactly how you did it in your notebook
    economic_data['Crime count'] = crime_data['DR_NO'].reset_index()['DR_NO']
    
    # Calculate correlation
    correlation = economic_data[['Unemployment Rate', 'Income Level', 
                              'GDP (Billion USD)', 'Poverty Rate', 
                              'Crime count']].corr()
    
    return correlation, economic_data

def analyze_demographic_patterns(df):
    """Analyze patterns in demographic data."""
    # Extract demographic data
    demographic_data = df[['Vict Age', 'Vict Sex', 'Crm Cd', 'Crm Cd Desc']]
    
    # Age distribution
    age_distribution = demographic_data['Vict Age'].value_counts().sort_index()
    
    # Gender distribution
    gender_distribution = demographic_data['Vict Sex'].value_counts()
    
    return {
        'age_distribution': age_distribution,
        'gender_distribution': gender_distribution
    }