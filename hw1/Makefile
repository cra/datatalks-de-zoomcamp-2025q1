init:
	echo "Make sure you set env vars"
	uv run ./10_create_schema.py
	uv run ./11_load_data.py

q1:
	docker run -it python:3.12.8 bash -c 'pip --version'

# q2:
#	echo 'postgres:5433'

q3:
	uv run ./20_trip_segmentation.py

q4:
	uv run ./30_longest_trips.py

q5:
	uv run ./40_biggest_pickup_zones.py

q6:
	uv run ./50_largest_tip.py

q7:
	terraform apply -help
	# init, apply -auto-approve, destroy

