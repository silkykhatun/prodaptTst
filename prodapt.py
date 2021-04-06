import pandas as pd

def normalize_dfs(df):
    date_head = {'timestamp': "transaction_date", 'date': "transaction_date", 'date_readable': "transaction_date"}
    type_head = {'type': "transaction_type", 'transaction': "transaction_type"}
    amount_head_list = ['amounts', 'amount', 'euro', 'cents']
    to_head_list = ['to']
    from_head_list = ['from']
    df = df.rename(columns=date_head)
    df = df.rename(columns=type_head)
    df = df.rename(columns={'amounts': 'amount'})
    
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    
    amnt_set = set(df.columns) & set(amount_head_list)
    if len(amnt_set) > 1:
        res= [col  for col in df.columns if col in amnt_set]
        df['amount'] = df[res].astype(str).agg('.'.join, axis=1).astype(float)
        df = df.drop(columns=res)
    
    return df
	
def combine_all(paths):
    dfs = [pd.read_csv(path) for path in paths]
    normalized = [normalize_dfs(df) for df in dfs]
    return pd.concat(normalized).reset_index(drop=True)
	
op = combine_all(['bank1.csv', 'bank2.csv', 'bank3.csv'])
op.to_csv(r'bank.csv')