import pandas as pd
from datafunctions import format_join
from models import trend_analysis,lag_analysis_region,lagged_effect_analysis
joineddf=format_join(pd.read_csv('data/daily-covid-19-vaccine-doses.csv'),pd.read_csv('data/daily-new-confirmed-covid-19-cases.csv'))
 
joineddf.rename(columns={
    'Entity': 'Region',
    'COVID-19 doses (daily, 7-day average, per million people)': 'Vaccines',
    'Daily new confirmed cases due to COVID-19 (rolling 7-day average, right-aligned)': 'Cases'
}, inplace=True)
trend_analysis(joineddf)
lag_analysis_region(joineddf)
lagged_effect_analysis(joineddf, lag_weeks=100) 

