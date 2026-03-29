# dataops-cloud-vehicle-locations
> Real-Time Location of all [CARTA](https://www.gocarta.org/) Buses and Shuttles

## background
Every second counts when you are trying to catch the bus.  We built this data pipeline to provide real-time data to both our operations center and the public.

## frequency
The pipeline runs approximately every 5 seconds.

## columns
| column | example | description |
| :--- | :--- | :--- |
| **vehicle_id** | `131` | The unique internal identifier for the specific physical bus. |
| **latitude** | `35.01519088745117` | The current North-South geographic coordinate of the vehicle. |
| **longitude** | `-85.32403106689453` | The current East-West geographic coordinate of the vehicle. |
| **reported** | `"2026-01-07T22:51:00-05:00"` | The standardized ISO 8601 date and time when the location was reported. |


## download links
- [metadata](https://gocarta.s3.us-east-2.amazonaws.com/public/data/cloud_vehicle_locations/v1/meta.json)
- [csv](https://gocarta.s3.us-east-2.amazonaws.com/public/data/cloud_vehicle_locations/v1/data.csv)
- [geojson](https://gocarta.s3.us-east-2.amazonaws.com/public/data/cloud_vehicle_locations/v1/data.points.geojson)
- [geoparquet](https://gocarta.s3.us-east-2.amazonaws.com/public/data/cloud_vehicle_locations/v1/data.parquet)
- [json](https://gocarta.s3.us-east-2.amazonaws.com/public/data/cloud_vehicle_locations/v1/data.json)
- [json lines](https://gocarta.s3.us-east-2.amazonaws.com/public/data/cloud_vehicle_locations/v1/data.jsonl)
- [shapefile](https://gocarta.s3.us-east-2.amazonaws.com/public/data/cloud_vehicle_locations/v1/data.points.shp.zip)

## preview links
- You can view the geojson on a map using [geojson.io](https://geojson.io/#data=data:text/x-url,https://gocarta.s3.us-east-2.amazonaws.com/public/data/cloud_vehicle_locations/v1/data.points.geojson).
- You can view the shapefile on a map using [shapefile.io](https://shapefile.io?url=https://gocarta.s3.us-east-2.amazonaws.com/public/data/cloud_vehicle_locations/v1/data.points.shp.zip).
- You can query the data with SQL using [duckdb](https://shell.duckdb.org/#queries=v0,CREATE-TABLE-dataset-AS-SELECT-*-FROM-'s3://gocarta/public/data/cloud_vehicle_locations/v1/data.parquet'~,Describe-dataset~).

## support
Post an issue [here](https://github.com/gocarta/dataops-cloud-vehicle-locations/issues) or email the package author at DanielDufour@gocarta.org.