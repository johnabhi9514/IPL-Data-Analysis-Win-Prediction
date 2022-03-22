import pandas as pd
import numpy as np

class grapf():
    def __init__(self):
        self.data = 'IPL Matches 2008-2020.csv'

    def tosswinner(self):
        self.df = pd.read_csv(self.data ,index_col=False)
        return self.df
