
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
accounts = pd.concat([gadgets, gizmos],axis=0,keys=[gadgets.name, gizmos.name],names=['Account','Year'])
print(accounts.info())
# instantiate metrics dict which holds the logic for defining metrics
metrics_dict = {
    'YoY Growth' : {
        'func': lambda x: x.pct_change(),
        'name': 'yoy_growth'
    }
}

def calc_metrics(metrics_dict, actuals, group_by_levels=None):
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
    metrics = []
    for metric in metrics_dict.values():
        if group_by_levels:
            grouped = actuals.groupby(level=group_by_levels,group_keys=False)
            metrics = grouped.apply(metric['func'])
            metrics.name = metric['name']
            #metrics = metrics.add_suffix(metric.get('name'))    
        else:
            for actual in actuals:
                metric_name = actual.name + metric.get('name')
                metric_output = metric['func'](actual)
                metric_output.name = metric_name
                metrics.append(metric_output)    
    
    if metrics.index.equals(actuals.index):
        print('Indexes are aligned')
    else:
        print('WARNING: Index of metrics is not equal to index of actuals. Alignment and calculations may not work as expected')
    return metrics

growth = calc_metrics(metrics_dict=metrics_dict, actuals=accounts,group_by_levels=['Account'])

print(accounts)
print(growth)

