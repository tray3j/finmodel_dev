
# A minimal, simplistic example
import pandas as pd
import numpy as np

# create series of sales figures over a quarterly range. These are the ACTUALS
sales = pd.Series([50,60,75,90,125,135,140,163])
ind = pd.PeriodIndex(pd.period_range('2019Q1',periods=8,freq="Q-NOV")) 
sales.index=ind
print(sales)

# Calculate the growth, Which is a metric
growth = sales.pct_change(4) # 4 because this is an annual growth rate. TODO make dynamic
print(growth)

# now we define what periods we would like to forecast
fcst_periods = pd.PeriodIndex(pd.period_range('2021Q1',periods=8,freq='Q-NOV'))

# make an ASSUMPTION(average actual growth) about our DRIVER's(growth) behavior in the forecast periods 
fcst_growth = pd.Series([growth.mean() for i in range(8)],index=fcst_periods)
print(fcst_growth)

# now use the DRIVER to calculate the FORECAST
base_index = fcst_periods 
base = pd.Series(sales.values,fcst_periods)
fcst_sales = (1+fcst_growth) * base


model = pd.concat([sales,fcst_sales])
print(model)