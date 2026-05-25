
import json, sys, pyarrow as pa, pyarrow.parquet as pq
json_path = sys.argv[1]
parquet_path = sys.argv[2]
with open(json_path, 'r') as f:
    data = json.load(f)
# Convert list of dicts to Arrow table
table = pa.Table.from_pydict({k: [row[k] for row in data] for k in data[0].keys()})
pq.write_table(table, parquet_path)
