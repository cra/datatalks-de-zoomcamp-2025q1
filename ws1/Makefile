clean:
	rm ny_taxi_pipeline.duckdb

q1:
	uv run dlt --version

q2:
	@echo "1) make q2-load-data 2) make q2-describe" 

q2-one-shot:
	uv run ./q2_10_one-shot-data.py

q2-load-data:
	uv run ./q2_20_load_data.py

q2-describe:
	uv run ./q2_30_describe_tables.py

q3:
	uv run ./q3_num_rows.py

q4:
	uv run ./q4_trip_duration.py
