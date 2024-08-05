import pandas as pd
import numpy as np

class ReadData:
    def __init__(self, file_path = None):

        if file_path is None:
            print("No file path provided.")
            return
        
        file_extension = file_path.split('.')[-1].lower()

        try:
            if file_extension == 'json':
                self.df = pd.read_json(file_path)
                print("JSON file loaded successfully.")
            elif file_extension == 'csv':
                self.df = pd.read_csv(file_path)
                print("CSV file loaded successfully.")
            elif file_extension == 'feather':
                self.df = pd.read_feather(file_path)
                print("Feather file loaded successfully.")
            elif file_extension == 'parquet':
                self.df = pd.read_parquet(file_path)
                print("Parquet file loaded successfully.")
            elif file_extension in ['xls', 'xlsx']:
                self.df = pd.read_excel(file_path)
                print("Excel file loaded successfully.")
            else:
                print("Unsupported file format.")
        except FileNotFoundError:
            print(f"{file_extension.capitalize()} file not found.")
        except ValueError as e:
            print(f"Error reading {file_extension.capitalize()} file: {e}")
        except Exception as e:
            print(f"Error occurred while loading {file_extension.capitalize()} file: {e}")

        if self.df is None:
            raise ValueError("No valid file path provided or files could not be loaded.")

        try:
            self.df['expiry'] = pd.to_datetime(self.df['expiry'])
            self.df['date'] = pd.to_datetime(self.df['date'])
            # set_time_to_end_of_day this function sets the expiry to the eod of the expiry date
            self.df['expiry'] = self.df['expiry'].apply(self.set_time_to_end_of_day)
            self.df['time_to_maturity'] = (self.df['expiry']-self.df['date']).dt.total_seconds()/(3600*24)
            self.df['nearest_atm'] = self.df['spot'].apply(self.closest_strike_price)
            self.df['strike_price_diff'] = np.abs(self.df['strike_price'] - self.df['spot'])
        except Exception as e:
            raise KeyError("Something went wrong in class initialisation of Interview Test")

