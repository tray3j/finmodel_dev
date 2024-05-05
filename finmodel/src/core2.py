import pandas as pd
import numpy as np
from render import render_df 

def calculate_model(actuals,metric_func,assumptions,model_func,model_time_index):
    actuals = actuals
    metrics = metric_func(actuals)
    assumptions = assumptions
    model = model_func(actuals,metrics,assumptions)
    return model


def model_func(actuals,metrics,assumptions,model_time_index):
    placeholder_logic = None #TODO create model logic
    
    # basically replaces the time index present in actuals df with model defined time index
    index = actuals.index
    index = actuals.index.drop_level(model_time_index.name,)
    index = pd.concat([actuals],keys=model_time_index,names='time_index',levels=0,verify_integrity=True).index 
    
    model = pd.DataFrame(index=index,data=placeholder_logic)
    return model
