import duckdb
import rich
from q2_20_load_data import pipeline


if __name__ == '__main__':
    dbname = f"{pipeline.pipeline_name}.duckdb"
    searchpath_sql = f"SET search_path = '{pipeline.dataset_name}'"
    print(f"connecting to {dbname} and executing\n{searchpath_sql}")
    conn = duckdb.connect(dbname)
    conn.sql(searchpath_sql)
    rich.print(conn.sql("DESCRIBE"))
