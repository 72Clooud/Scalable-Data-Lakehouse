import duckdb

from pathlib import Path

try:
    con = duckdb.connect('ecommerce.duckdb')

    data_path = Path('data/')

    if data_path.exists():
        data_files = [f for f in data_path.iterdir() if f.is_file() and f.suffix == '.csv']

        for file in data_files:
            table_name = f'raw_{file.stem}'
            sql = f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM read_csv_auto('{file}')"
            con.execute(sql) 
            print(f'Success: Load file {file.name} to table {table_name}')
    else:
        print(f"Directory {data_path} doesn't exist")

except Exception as e:
    print(f"error: {e}")
    raise e
finally:
    con.close()