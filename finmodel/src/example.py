
# A minimal, simplistic example
import pandas as pd
import numpy as np
import core as cr
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

metrics_dict = {
    'YoY Growth' : {
        'func': lambda x: x.pct_change(),
        'name': 'yoy_growth',
        'other_args' : None,
        'group_levels' : ['Account']
    },
    'Gizmo mix' : {
        'func': cr.level_mix_calc,
        'other_args' : dict(levels=['Year']),
        'name': 'gizmo_mix',
        'group_levels' : None
    }
}


growth = cr.calc_metrics(metrics_dict=metrics_dict, actuals=actuals)
# growth here being the name of our metrics df

assumption_dict = {
    'gadget_growth': {
        'growth_func' : cr.simple_growth, # TODO: remove, belongs in model step
        'growth' : np.full(5,growth.xs(key=('gadgets'))['yoy_growth'].mean())
    }
} # split up because of inter-assumption dependencies #TODO better way to handle these dependcies?
assumption_dict['gizmo_growth'] = {
    'competition' : pd.Series([False, False, True, True, True],index=fcst_periods),
    'growth_func' : cr.simple_growth, # TODO: remove, belongs in model step
    'no_competition_growth' : growth.query("Account == 'gizmos'").iloc[-2:]['yoy_growth'].mean(),
    'with_competition_growth' : assumption_dict['gadget_growth']['growth'],
    'rationale' : """Assumes the growth observed in the last two actual periods continues until competition enters. Then,
    grow at the same rate as gadgets have in the last two actual periods"""
    }
    
model_dict = { # is this more appropriate as a function somehow?
    'gadgets': {
        'model' : cr.simple_growth(input=actuals.xs('gadgets').iloc[-1],g=assumption_dict['gadget_growth']['growth'],nper=len(fcst_periods))
        },
    'gizmos': {
        'model' : cr.simple_growth(input=actuals.xs('gizmos').iloc[-1],g=np.where(assumption_dict['gizmo_growth']['competition'],assumption_dict['gizmo_growth']['no_competition_growth'],assumption_dict['gizmo_growth']['with_competition_growth']),nper=len(fcst_periods))
        }
}

model_index = pd.MultiIndex.from_product([actuals.index.get_level_values(0).unique().to_list(),fcst_periods],names=['Account','Year'])
model = cr.model_calc(model_dict=model_dict, fcst_index=model_index)
model.columns = ['Sales'] # TODO make this not hardcoded

# We should wrap up these last few steps in a function
output = pd.concat([actuals.to_frame(),model],axis=0,keys=['Actual','Forecast'],names=['Source']).sort_index()#)

full_metrics_dict = metrics_dict
full_metrics_dict['YoY Growth']['group_levels'] = ['Account']
output_metrics = cr.calc_metrics(metrics_dict=full_metrics_dict,actuals=output)
output = pd.concat([output,output_metrics],axis=1)

render_df(output)

