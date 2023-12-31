import pandas as pd
import numpy as np
import render


def calc_metrics(metrics_dict, actuals):#, group_by_levels=None):
    '''Calculates metrics on provided actuals.
    Returns a list of metrics.
    parameters:
        metrics_dict: dict with metrics, expects each 'metric' to have
        keys of 'name' and 'func' with name of the metric to be appended onto end of each actual
        and 'func' which should take one argument of the actual being passed and return an identically shaped and indexed array or scalar
        actuals: a list of pd.series-like objects appropriately indexed. If func in metrics dict calls object methods on actuals, actuals must
        have that method be callable # TODO what does appropriately indexed mean??
        group_by_levels=None : for actuals of dtype dataframe or series with a multi-index that needs to be grouped before passing 
        into the metrics func
    '''
    metrics = pd.DataFrame(index=actuals.index)
    for metric in metrics_dict.values():
        if metric['group_levels']:
            grouped = actuals.groupby(level=metric['group_levels'],group_keys=False)
            if metric['other_args']:
                metrics[metric['name']] = metric['func'](grouped,**metric['other_args'])
            else:
                metrics[metric['name']] = metric['func'](grouped)
            #metrics.name = metric['name']
            #metrics = metrics.add_suffix(metric.get('name'))    
        else:
            if metric['other_args']:
                metrics[metric['name']] = metric['func'](actuals,**metric['other_args'])
            else:
                metrics[metric['name']] = metric['func'](actuals)
    
    if metrics.index.equals(actuals.index):
        print('Indexes are aligned')
    else:
        print('WARNING: Index of metrics is not equal to index of actuals. Alignment and calculations may not work as expected')
    return metrics

def simple_growth(input,g,nper):
    '''grow input exponentially at growth rate g for nper number of periods'''
    exps = np.arange(start=1,stop=nper+1,step=1)
    factors = np.cumprod((1+g),axis=0)
    result = input*factors
    return result

def level_mix_calc(df, levels): # conveniently calculate percentage mix
    '''calculates the percentage mix of a particular value in an index level of a df. 
    Returns a df'''
    base = df.groupby(level=levels).transform(lambda x: x.sum())
    mix = df / base
    return mix

def model_calc(model_dict, fcst_index):
    ''' takes in model dict. Returns a dataframe with index fcst_index,
    using models (function calls defined in model dict) to generate similarly indexed df'''
    placeholder = pd.DataFrame(index=fcst_index)
    model = pd.DataFrame() # doing it this way so that the model is only indexed insofar as there are model elements with that index. 
    # drawback is that we may end up with a model differently indexed from our actuals
    for account,values in model_dict.items():
        print(f'modeling account: {account} with value {values["model"]}')
        # build the components of model df bit by bit
        result_array = values['model']
        print(result_array)
        result_index = placeholder.xs(account,0,level='Account',drop_level=False).index
        result = pd.DataFrame(data=result_array,index=result_index)
        model = pd.concat([model,result],axis=0)
    return model




