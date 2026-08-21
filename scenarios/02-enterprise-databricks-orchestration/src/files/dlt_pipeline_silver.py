import dlt

@dlt.table(name="silver_trans")
def bronze_transactions():
    df = dlt.read("bronze_trans")
    return df
