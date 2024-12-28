import numpy as np
import pandas as pd
from datafunctions import format_join
joines_df=format_join(pd.read_csv('daily-covid-19-vaccine-doses.csv'),pd.read_csv('daily-new-confirmed-covid-19-cases.csv'))
print(joines_df.head())