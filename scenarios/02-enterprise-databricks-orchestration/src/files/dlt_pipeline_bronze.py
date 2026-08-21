import dlt

@dlt.table(name="bronze_trans")
def bronze_transactions():
    df = spark.createDataFrame([('Alice', 1), ('Bob', 2), ('Charlie', 3)], ['name', 'id'])
    return df
