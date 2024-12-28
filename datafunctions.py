import numpy as np  
import pandas as pd

# Function to read and format the two datasets
def format_join(x,y):
    x['Day']=pd.to_datetime(x['Day'])
    y['Day']=pd.to_datetime(y['Day'])
    df=pd.merge(x,y,on=['Entity','Day'])
    return df