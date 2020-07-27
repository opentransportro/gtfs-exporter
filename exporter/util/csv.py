import pandas as pd

def remove_column(file: str, column: str):
    try:
        pd.read_csv(file).set_index(column).to_csv(file, index=None)
    except:
        pass
