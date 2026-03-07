import pandas as pd

def load_csv(path):
    """Load CSV into DataFrame"""
    df = pd.read_csv(path)
    return df