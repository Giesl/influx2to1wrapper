# influx2to1wrapper
Python influxDB class, that can wrap new influx-client InfluxDBClient that overrides query and write_points to support backwards compatibiity.
For usage you must use token auth.

## query method
  Query method sends get request to /query endpoint and parse result into ResultSet from old influxdb package, so you can use it in you old code.

## write_points method
  Write_points method use same singature as old write_points form old influxdb package.
  Method uses new write_api and writes points to bucket (default retention policy is set to autogen, change it, if you have different).


This wrapper is based on https://docs.influxdata.com/influxdb/v2.7/query-data/influxql/


