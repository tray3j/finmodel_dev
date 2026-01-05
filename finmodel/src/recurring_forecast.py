import pandas as pd
import numpy as np
import path
import datetime as dt


'''
RECURRING FORECAST SCRIPT

This script is intended to take a table with columns (columns VAR) and take in assumptions which are stored in YAML or some
other markup langaage

The  key features implemented are:

- Renewing the current set of contracts with a given set of assumptions on new dates and amount changes

- Calculates a churn overlay on the contracts, using a combination of individual name contracts, which are
concatenated in the same shape as normal contracts, as well as the unnamed assumptions which get loaded
as placeholder contract-like entries for matched periods, and then become renewed in perpetuity and their
amounts increased the same as ARR to effectively neutralize the ARR which will in reality become churn

- Takes a forecasted table of bookings (implemented in a separate script) and then adds them to the 
future contract backlog...

- The backlog of future contracts is then added to ARR  

Each component of recurring revenue alters the state of the contracts table state by appending records,
and each feature is implemented with an individual function in this module. Each function takes in the
contracts variable, a month as a period, and assumptions as parameters.

Once complete, the script will return a contracts table object which can be analyzed with power BI
or excel 

in addition, it will generate an ARR rollforard table, a contracted ARR rollforward table (which is ARR 
+ Backlog contracts), and a recurring billings table which are calculated based on the bookings table


'''

DATE_COLUMNS = []

def load_actual_contracts(None):
    pass

def load_forecasted_bookings(None):
    pass

def load_assumptions(None):
    pass

def load_contract_backlog(None):
    pass

def price_increase_setter(None):
    pass

def renew_contracts(
    contracts: pd.DataFrame,
    assumptions: pd.DataFrame,
    period: dt.Date,):

    renewal_term_assmumption = assumptions['Renewal Terms']
    
    contracts_renewing = contracts.loc[contracts['contract_end' == period]].copy()
    # may have to loop through each column in this next step, not sure if you can add the date to all of them in one shot
    contracts_renewing.loc[:,DATE_COLUMNS] = contracts_renewing.loc[:,DATE_COLUMNS] + renewal_term_assmumption
    contracts_renewing['Renewed From'] = contracts_renewing['Contract ID']
    contracts_renewing['Contract ID'] = contracts_renewing['Contract ID'].str.concat('_renewal')
    contracts_renewing['ARR Category'] = 'Renewal'
    price_increases = contracts_renewing.copy()
    price_increases['ARR'] = price_increase_setter(contracts_renewing)
    price_increases['ARR Category'] = 'Price Increase'
    price_increases['Contract ID'] = contracts_renewing['Renewed From'].str.concat('_price_increase')

    contracts.append(contracts_renewing)
    contracts.append(price_increases)
    return contracts


def churn_forecaster(
    contracts: pd.DataFrame,
    named_churn_list: pd.DataFrame,
    unnamed_churn_assumptions: pd.DataFrame,
    period: dt.Date
    )

    eligible_contracts = contracts.loc[contracts['contract_end'] == period].copy()
    contracts['']

def 



