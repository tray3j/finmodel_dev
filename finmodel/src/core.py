import pandas as pd
import numpy as np
import render





class Actuals(pd.DataFrame):
    '''Class for holding a actuals data with related features. 
    Inherits pd.DataFrame. minimally requires an index and accounts.
    Implies the size and shape of data needed for model.
    Data is loaded with the .load() method ''' 
    
    def init(self,accounts,index):
        self.index = index
        self.accounts = accounts
        self.data = None

    def load(self,df):
        self.accounts = df.columns
        # TODO should accounts be instantiated here or in the init method?
        if (df.index == self.index and self.data == None): # checks if actuals is empty
            self = df
        else:
            self.loc[df.index,df.columns] = df


class Metrics(pd.DataFrame):
    '''Class for holding metric calculations and results'''

    def init(self, metrics_dict, actuals):
        self.columns = metrics_dict.keys()
        


class Model:
# TODO Have barely started this
    def init(self, name, actuals):
        self.name = name
        self.Accounts = actuals.accounts



