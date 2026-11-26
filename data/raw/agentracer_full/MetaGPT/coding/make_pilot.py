import pyarrow.parquet as pq

table = pq.read_table("datasets/code/mbppplus-full.parquet")
pilot = table.slice(0, 5)
pq.write_table(pilot, "datasets/code/pilot-5.parquet")
print(f"Pilot: {pilot.num_rows} rows")
