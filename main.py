# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "boto3",
#     "datablob",
#     "simple-env",
#     "tzdata",
# ]
# ///
import datablob
from datetime import datetime, timedelta
import simple_env as se
import time

import boto3
from boto3.dynamodb.conditions import Key, Attr

from zoneinfo import ZoneInfo

start_time = time.perf_counter()

AWS_DYNAMODB_TABLE_NAME = se.get("AWS_DYNAMODB_TABLE_NAME")
DATAOPS_TIMEZONE = se.get("DATAOPS_TIMEZONE")
AWS_BUCKET_NAME = se.get("AWS_BUCKET_NAME")
AWS_BUCKET_PATH = se.get("AWS_BUCKET_PATH")
AWS_DYNAMODB_REGION = se.get("AWS_DYNAMODB_REGION")
DATAOPS_QUICK_MODE = se.get("DATAOPS_QUICK_MODE")

# make sure we don't run faster than 0.5 seconds per loop
MIN_ITERATION_TIME = 0.5

timezone = ZoneInfo(DATAOPS_TIMEZONE)
timezone_utc = ZoneInfo("UTC")

VEHICLE_IDS = list(sorted(se.get("VEHICLE_IDS").strip().split(",")))

vehicle_ids = [(vid, vid.strip().zfill(4)) for vid in VEHICLE_IDS]

dynamodb = boto3.resource("dynamodb", region_name=AWS_DYNAMODB_REGION)
table = dynamodb.Table(AWS_DYNAMODB_TABLE_NAME)

while True:
    try:
        start_iteration_time = time.perf_counter()

        rows = []

        for vehicle_id, vid in vehicle_ids:
            # Querying the partition key for the newest single item
            response = table.query(
                KeyConditionExpression=Key("vehicleId").eq(vid),
                FilterExpression=Attr("age").eq("Fresh"),
                ScanIndexForward=False,  # Sorts descending (newest first)
                Limit=1,  # Only grab the top result
            )

            items = response.get("Items", [])

            if not items:
                # print(f"[dataops-cloud-vehicle-locations] no data found for vehicle: {vid}")
                continue

            item = items[0]

            timestamp = float(item["timestamp"])

            received_utc = datetime.fromtimestamp(timestamp, tz=timezone_utc)

            # 3. Create initial Reported datetime using Received's UTC date
            reported_time_obj = datetime.strptime(item["time"], "%H:%M:%S").time()
            reported_utc = datetime.combine(
                received_utc.date(), reported_time_obj, tzinfo=timezone_utc
            )

            # If reported is > 60 seconds after received, it belongs to the previous day
            if reported_utc > (received_utc + timedelta(minutes=1)):
                reported_utc -= timedelta(days=1)

            row = {
                "vehicle_id": vehicle_id,
                "latitude": float(item["latitude"]),
                "longitude": float(item["longitude"]),
                "reported": reported_utc.astimezone(timezone).isoformat(),
            }

            rows.append(row)

        client = datablob.DataBlobClient(
            bucket_name=AWS_BUCKET_NAME, bucket_path=AWS_BUCKET_PATH
        )

        if DATAOPS_QUICK_MODE == True:
            # do a quick geojson upload
            geojson = client.convert_rows_to_geojson_points(
                rows, longitude_key="longitude", latitude_key="latitude"
            )
            client.upload_geojson_points("cloud_vehicle_locations", "1", geojson)
        else:
            # do a full upload, including metadata
            client.update_dataset(
                name="cloud_vehicle_locations",
                version="1",
                data=rows,
                description="Real-Time Location of CARTA Fixed-Route Buses and Shuttles.",
                latitude_key="latitude",
                longitude_key="longitude",
                xlsx=False,
            )

        print(f"[dataops-cloud-vehicle-locations] updated {len(rows)} rows")

        end_time = time.perf_counter()
        iteration_time = end_time - start_iteration_time

        if iteration_time < MIN_ITERATION_TIME:
            time.sleep(MIN_ITERATION_TIME - iteration_time)

        execution_time = end_time - start_time
        print("execution_time:", execution_time)
        if execution_time >= 60:
            print("time is up")
            exit()

    except Exception as e:
        print(e)
