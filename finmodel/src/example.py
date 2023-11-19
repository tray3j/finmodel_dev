
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
accounts = [gadgets, gizmos]

# instantiate metrics dict which holds the logic for defining metrics
metrics_dict = {
    'YoY Growth' : {
        'func': lambda x: x.pct_change(),
        'name': '_yoy_growth'
    }
}

def calc_metrics(metrics_dict, actuals):
    '''Calculates metrics on provided actuals.
    Returns a list of metrics.
    parameters:
        metrics_dict: dict with metrics, expects each 'metric' to have
        keys of 'name' and 'func' with name of the metric to be appended onto end of each actual
        and 'func' which should take one argument of the actual being passed and return an identically shaped and indexed array or scalar

        actuals: a list of pd.series-like objects appropriately indexed. If func in metrics dict calls object methods on actuals, actuals must
        have that method be callable # TODO what does appropriately indexed mean??
    '''
    metrics = []
    for metric in metrics_dict.values():
        for actual in actuals:
            metric_name = actual.name + metric.get('name')
            metric_output = metric['func'](actual)
            metric_output.name = metric_name
            metrics.append(metric_output)
    return metrics

growth = calc_metrics(metrics_dict=metrics_dict, actuals=accounts)

print(accounts)
print(growth)

