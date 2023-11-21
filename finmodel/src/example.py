
# A minimal, simplistic example
import pandas as pd
import numpy as np

actl_periods = pd.PeriodIndex(pd.period_range(2019,2023,freq='A-DEC'))
fcst_periods = pd.PeriodIndex(pd.period_range(2024,2028,freq='A-DEC'))

# create two accounts: Gadgets and gizmos
gadgets = pd.Series(data=[60,70,85,100,125],index=actl_periods,name='gadgets')
gizmos = pd.Series(data=[200,210,217,228,239],index=actl_periods,name='gizmos')
# Enchancements: 1) have these items populate some global 'account' dict for accessing / consolidating
# 2) functionally generate instead of hardcoding (of course)
actuals = pd.concat([gadgets, gizmos],axis=0,keys=[gadgets.name, gizmos.name],names=['Account','Year'])

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
    exps = np.arange(start=0,stop=nper+1,step=1)
    factors = np.power((1+g),exps)
    result = input*factors
    return result


growth = calc_metrics(metrics_dict=metrics_dict, actuals=actuals)

assumption_dict = {
    'gadget_growth': {
        'growth_func' : simple_growth,
        'growth' : growth.xs(key=('gadgets'))['yoy_growth'].mean()
    },

    'gizmo_growth': {
        'competition' : pd.Series([False, False, True, True, True],index=fcst_periods),
        'growth_func' : simple_growth,
        'no_competition_growth' : growth.query("Account == 'gizmos'").iloc[-2:]['yoy_growth'].mean(),
        'with_competition_growth' : "assumption_dict['gadget_growth']['growth']", # NEEDS REPLACEMENT AFTER THE FACT
        'rationale' : """Assumes the growth observed in the last two actual periods continues until competition enters. Then,
        grow at the same rate as gadgets have in the last two actual periods"""
    }
    
}
assumption_dict['gizmo_growth']['with_competition_growth'] = eval(assumption_dict['gizmo_growth']['with_competition_growth']) # is this legal?

print(actuals)
print(growth)
print(assumption_dict)

