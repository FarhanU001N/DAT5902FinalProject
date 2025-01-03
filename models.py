import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
from datafunctions import format_join
from sklearn.linear_model import LinearRegression

joineddf=format_join(pd.read_csv('daily-covid-19-vaccine-doses.csv'),pd.read_csv('daily-new-confirmed-covid-19-cases.csv'))
 
joineddf.rename(columns={
    'Entity': 'Region',
    'COVID-19 doses (daily, 7-day average, per million people)': 'Vaccines',
    'Daily new confirmed cases due to COVID-19 (rolling 7-day average, right-aligned)': 'Cases'
}, inplace=True)

def trend_analysis(data):
    selected_regions = ['Africa', 'Asia', 'North America', 'South America', 'Europe']
    filtered_data = data[data['Region'].isin(selected_regions)]

    if filtered_data.empty:
        print("No data available for selected regions.")
        return

    plt.figure(figsize=(12, 6))

    for region in selected_regions:
        subset = filtered_data[filtered_data['Region'] == region]
        
        if subset.empty:
            print(f"No data available for region: {region}")
            continue
        
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
        plt.legend(loc="upper left")
        plt.show()


def lag_analysis_region(data, selected_regions=None, max_lag_months=30):
    if selected_regions is None:
        selected_regions = ['Africa', 'Asia', 'North America', 'South America', 'Europe', 'Oceania']
    
    lags = range(0, max_lag_months + 1)
    region_correlations = {}

    # Filter data for selected regions
    filtered_data = data[data['Region'].isin(selected_regions)]

    # Check if the filtered data is empty
    if filtered_data.empty:
        print("No data available for the selected regions.")
        return {}

    # Loop through each region
    for region in selected_regions:
        subset = filtered_data[filtered_data['Region'] == region].sort_values('Day')
        if subset.empty:
            region_correlations[region] = [np.nan] * (max_lag_months + 1)
            continue
        
        vaccines = subset['Vaccines'].values
        cases = subset['Cases'].values

        if len(vaccines) == 0 or len(cases) == 0:
            region_correlations[region] = [np.nan] * (max_lag_months + 1)
            continue

        # Calculate correlations for weekly lags
        correlations = []
        for lag in lags:
            lag_days = lag * 30  # Make the lag months
            if lag_days > 0 and lag_days < len(vaccines):
                correlations.append(np.corrcoef(vaccines[:-lag_days], cases[lag_days:])[0, 1])
            elif lag_days == 0:
                correlations.append(np.corrcoef(vaccines, cases)[0, 1])
            else:
                correlations.append(np.nan)  # Append NaN for invalid lags

        region_correlations[region] = correlations

    return region_correlations

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

def lagged_effect_analysis(data, lag_weeks=100):
    # Convert lag from weeks to days (assuming 7 days per week)
    lag_days = lag_weeks * 7 
    
    # Sort data by date
    data = data.sort_values(['Region', 'Day']).reset_index(drop=True)
    data = data[data['Region'].isin(['Africa', 'Asia', 'North America', 'South America', 'Europe','Oceania'])]
    def apply_lag(group):
        group = group.copy()
        group['Lagged Cases'] = group['Cases'].shift(-lag_days)
        return group
    
    lagged_data = data.groupby('Region').apply(apply_lag).reset_index(drop=True)
    
    # Drop rows with NaN values after shifting
    lagged_data = lagged_data.dropna(subset=['Vaccines', 'Lagged Cases'])
    # Linear regression to quantify relationship
    X = lagged_data['Vaccines'].values.reshape(-1, 1)
    y = lagged_data['Lagged Cases'].values
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    
    # Add regression line to the scatter plot
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=lagged_data['Vaccines'], y=lagged_data['Lagged Cases'], color='blue', label='Actual Data')
    plt.plot(lagged_data['Vaccines'], y_pred, color='red', label='Regression Line')
    plt.title(f"Vaccination Effect on COVID-19 Cases ({lag_weeks}-Week Lag)")
    plt.xlabel("Vaccines (7-day avg per million)")
    plt.ylabel(f"COVID-19 Cases (Lagged by {lag_weeks} weeks)")
    plt.legend()
    plt.grid()
    plt.show()
    
    # Print regression summary
    print(f"Regression Summary for {lag_weeks}-Week Lag:")
    print(f"Intercept: {model.intercept_:.2f}")
    print(f"Coefficient: {model.coef_[0]:.2f}")
    print(f"R-squared: {model.score(X, y):.2f}")



#trend_analysis(joineddf)
#lag_analysis_region(joineddf)
#lagged_effect_analysis(joineddf, lag_weeks=100) 
#hypothesis_testing(joineddf)
