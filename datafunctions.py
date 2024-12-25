import numpy as np  
import pandas as pd

# Function to read and format the two datasets
def read_format_join(xname,yname):
    x=pd.read_csv(xname)
    y=pd.read_csv(yname)
    x['day']=pd.to_datetime(x['day'])
    y['day']=pd.to_datetime(y['day'])
    df=pd.merge(x,y,on=['entity','day'])
    return df