import os
import pandas as pd

class DataIngest:
    def __init__(self, folder_name='.', file_name='HPC_2k.log_structured.csv'):
        # Looks for the file in the current directory ('.')
        self.csv_path = os.path.join(folder_name, file_name)

    def transform_data(self, df):
        df_transformed = pd.DataFrame()

        # Mapping and cleaning the columns from your specific CSV
        df_transformed['line_id'] = df['LineId'].fillna(0).astype(int)
        df_transformed['node'] = df['Node'].fillna('Unknown')
        df_transformed['component'] = df['Component'].fillna('Unknown')
        df_transformed['state'] = df['State'].fillna('Unknown')
        df_transformed['timestamp'] = pd.to_datetime(df['Time'], unit='s')
        df_transformed['flag'] = pd.to_numeric(df['Flag']).fillna(0).astype(int)
        df_transformed['content'] = df['Content'].fillna('N/A')
        df_transformed['event_id'] = df['EventId'].fillna('N/A')
        df_transformed['event_template'] = df['EventTemplate'].fillna('N/A')
        return df_transformed

    def run_display(self):
        # 1. Check if file exists
        if not os.path.exists(self.csv_path):
            print(f"Error: Could not find file at {self.csv_path}")
            return

        # 2. Read the CSV
        df_raw = pd.read_csv(self.csv_path)
        print(f"--- File Loaded: {len(df_raw)} records found ---\n")

        # 3. Transform the data
        df_final = self.transform_data(df_raw)

        # 4. Display the data
        # pd.set_option ensures you see all columns in the terminal
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 1000)
        
        print(df_final.head(20))  # Displays the first 20 rows

if __name__ == '__main__':
    # Initialize and run only the display logic
    ingest = DataIngest()
    ingest.run_display()