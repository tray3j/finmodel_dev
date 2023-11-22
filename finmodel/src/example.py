
# A minimal, simplistic example
import pandas as pd
import numpy as np
from render import render_df

actl_periods = pd.PeriodIndex(pd.period_range(2019,2023,freq='A-DEC'))
fcst_periods = pd.PeriodIndex(pd.period_range(2024,2028,freq='A-DEC'))

# create two accounts: Gadgets and gizmos
gadgets = pd.Series(data=[60,70,85,100,125],index=actl_periods,name='gadgets')
gizmos = pd.Series(data=[200,210,217,228,239],index=actl_periods,name='gizmos')
# Enchancements: 1) have these items populate some global 'account' dict for accessing / consolidating
# 2) functionally generate instead of hardcoding (of course)
actuals = pd.concat([gadgets, gizmos],axis=0,keys=[gadgets.name, gizmos.name],names=['Account','Year'])
actuals.name='Sales'


# instantiate metrics dict which holds the logic for defining metrics

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

def level_mix_calc(df, levels): # conveniently calculate percentage mix
    '''calculates the percentage mix of a particular value in an index level of a df. 
    Returns a df'''
    base = df.groupby(level=levels).transform(lambda x: x.sum())
    mix = df / base
    return mix

metrics_dict = {
    'YoY Growth' : {
        'func': lambda x: x.pct_change(),
        'name': 'yoy_growth',
        'other_args' : None,
        'group_levels' : ['Account']
    },
    'Gizmo mix' : {
        'func': level_mix_calc,
        'other_args' : dict(levels=['Year']),
        'name': 'gizmo_mix',
        'group_levels' : None
    }
}

def simple_growth(input,g,nper):
    '''grow input exponentially at growth rate g for nper number of periods'''
    exps = np.arange(start=1,stop=nper+1,step=1)
    factors = np.power((1+g),exps)
    result = input*factors
    return result


growth = calc_metrics(metrics_dict=metrics_dict, actuals=actuals)

assumption_dict = {
    'gadget_growth': {
        'growth_func' : simple_growth, # TODO: remove, belongs in model step
        'growth' : growth.xs(key=('gadgets'))['yoy_growth'].mean()
    },

    'gizmo_growth': {
        'competition' : pd.Series([False, False, True, True, True],index=fcst_periods),
        'growth_func' : simple_growth, # TODO: remove, belongs in model step
        'no_competition_growth' : growth.query("Account == 'gizmos'").iloc[-2:]['yoy_growth'].mean(),
        'with_competition_growth' : "assumption_dict['gadget_growth']['growth']", # NEEDS REPLACEMENT AFTER THE FACT
        'rationale' : """Assumes the growth observed in the last two actual periods continues until competition enters. Then,
        grow at the same rate as gadgets have in the last two actual periods"""
    }
    
}
assumption_dict['gizmo_growth']['with_competition_growth'] = eval(assumption_dict['gizmo_growth']['with_competition_growth']) # is this legal?

model_dict = { # is this more appropriate as a function somehow?
    'gadgets': {
        'model' : simple_growth(input=actuals.xs('gadgets').iloc[-1],g=assumption_dict['gadget_growth']['growth'],nper=len(fcst_periods))
        },
    'gizmos': {
        'model' : simple_growth(input=actuals.xs('gizmos').iloc[-1],g=np.where(assumption_dict['gizmo_growth']['competition'],assumption_dict['gizmo_growth']['no_competition_growth'],assumption_dict['gizmo_growth']['with_competition_growth']),nper=len(fcst_periods))
        }
}

def model_calc(model_dict, fcst_index):
    ''' takes in model dict. Returns a dataframe with index fcst_index,
    using models (function calls defined in model dict) to generate similarly indexed df'''
    placeholder = pd.DataFrame(index=fcst_index)
    model = pd.DataFrame()
    for account,values in model_dict.items():
        print(f'modeling account: {account} with value {values["model"]}')
        # build the components of model df bit by bit
        result_array = values['model']
        result_index = placeholder.xs(account,0,level='Account',drop_level=False).index
        result = pd.DataFrame(data=result_array,index=result_index)
        model = pd.concat([model,result],axis=0)
    return model

model_index = pd.MultiIndex.from_product([actuals.index.get_level_values(0).unique().to_list(),fcst_periods],names=['Account','Year'])
model = model_calc(model_dict=model_dict, fcst_index=model_index)
model.columns = ['Sales'] # TODO make this not hardcoded

# We should wrap up these last few steps in a function
output = pd.concat([actuals.to_frame(),model],axis=0,keys=['Actual','Forecast'],names=['Source']).sort_index()#)

full_metrics_dict = metrics_dict
full_metrics_dict['YoY Growth']['group_levels'] = ['Account']
output_metrics = calc_metrics(metrics_dict=full_metrics_dict,actuals=output)
output = pd.concat([output,output_metrics],axis=1)



print(actuals)
print(growth)
render_df(pd.concat([actuals,growth],axis=0))
render_df(output)

