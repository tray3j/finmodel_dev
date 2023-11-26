import pandas as pd
import numpy as np
import render

class Account (pd.DataFrame):
    
    def init(self,name,data,index):
        self.name = name
        self.index = index
        self.data = data

class Model:

    def init(self, name, accounts):
        self.name = name
        self.Accounts = accounts


