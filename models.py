import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
from datafunctions import format_join
joineddf=format_join(pd.read_csv('daily-covid-19-vaccine-doses.csv'),pd.read_csv('daily-new-confirmed-covid-19-cases.csv'))
 
joineddf.rename(columns={
    'Entity': 'Region',
    'COVID-19 doses (daily, 7-day average, per million people)': 'Vaccines',
    'Daily new confirmed cases due to COVID-19 (rolling 7-day average, right-aligned)': 'Cases'
}, inplace=True)

def trend_analysis(data):
    selected_regions = ['Africa', 'Asia', 'North America', 'South America', 'Europe']
    filtered_data = data[data['Region'].isin(selected_regions)]
    
    plt.figure(figsize=(12, 6))
    
    for region in selected_regions:
        subset = filtered_data[filtered_data['Region'] == region]
        
        # Create the primary y-axis for cases
        fig, ax1 = plt.subplots(figsize=(12, 6))
        ax1.plot(subset['Day'], subset['Cases'], color='tab:blue', label=f'{region} Cases')
        ax1.set_xlabel("Date")
        ax1.set_ylabel("COVID-19 Cases (7-day avg)", color='tab:blue')
        ax1.tick_params(axis='y', labelcolor='tab:blue')
        ax1.grid()

        # Create the secondary y-axis for vaccines
        ax2 = ax1.twinx()
        ax2.plot(subset['Day'], subset['Vaccines'], color='tab:green', label=f'{region} Vaccines')
        ax2.set_ylabel("Vaccines (7-day avg per million)", color='tab:green')
        ax2.tick_params(axis='y', labelcolor='tab:green')
        
        # Title and legend
        plt.title(f"Trends in Vaccination and COVID-19 Cases: {region}")
        fig.tight_layout()
        plt.legend(loc="upper left")
        plt.show()

def lag_analysis(data, max_lag=30):
    lags = range(0, max_lag + 1)
    correlations = []

    # Sort data by day
    data = data.sort_values('Day')

    # Get global values for vaccines and cases
    vaccines = data['Vaccines'].values
    cases = data['Cases'].values

    # Calculate correlations for each lag
    for lag in lags:
        if lag > 0:
            correlations.append(np.corrcoef(vaccines[:-lag], cases[lag:])[0, 1])
        else:
            correlations.append(np.corrcoef(vaccines, cases)[0, 1])

    # Plot cross-correlation
    plt.figure(figsize=(10, 6))
    plt.plot(lags, correlations, marker='o', color='b', label='Global Correlation')
    plt.title("Global Cross-Correlation Between Vaccines and Cases")
    plt.xlabel("Lag (Days)")
    plt.ylabel("Correlation")
    plt.grid()
    plt.legend()
    plt.show()

    return correlations
def hypothesis_testing(data):
    regions = data['Region'].unique()
    high_vaccine_regions = []
    low_vaccine_regions = []
    
    for region in regions:
        subset = data[data['Region'] == region]
        avg_vaccines = subset['Vaccines'].mean()
        if avg_vaccines > data['Vaccines'].mean():
            high_vaccine_regions.append(region)
        else:
            low_vaccine_regions.append(region)
    
    # Compare cases
    high_cases = data[data['Region'].isin(high_vaccine_regions)]['Cases']
    low_cases = data[data['Region'].isin(low_vaccine_regions)]['Cases']
    t_stat, p_value = ttest_ind(high_cases, low_cases, equal_var=False)
    
    print(f"T-statistic: {t_stat}, P-value: {p_value}")
    if p_value < 0.05:
        print("Significant difference between high and low vaccination regions.")
    else:
        print("No significant difference between high and low vaccination regions.")



trend_analysis(joineddf)
lag_analysis(joineddf)
hypothesis_testing(joineddf)
