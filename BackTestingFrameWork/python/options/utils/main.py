import pandas as pd
import numpy as np

class Utilities:
    def __init__(self):
        pass

    def groupDf(self,
                    columnName = None,
                    data = None,
                    frequency = None
                    ):
        return data.groupby(pd.Grouper(key = str(columnName), freq = str(frequency)))
    
    def groupDataFrameDictionary(self,
                           data = None):
        return {date: dataframe for date, dataframe in data}