from influxdb.resultset import ResultSet
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import requests


class InfluxClientWrapper(InfluxDBClient):

    def query(self, query: str, params=None, bind_params=None, epoch=None, expected_response_code=200, database=None,
              raise_errors=True, chunked=False, chunk_size=0, method=u'GET'):
        url = f"{self.url}/query"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Token {self.token}"
        }

        new_params = {
            "orgID": self.org,
            "db": database,
            "rp": "autogen",
            "q": query
        }

        params = params.update(new_params)

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == expected_response_code:
            # Expected response:
            # [
            #     {'results': [
            #         {'statement_id': 0,
            #          'series': [
            #              {'name': 'status',
            #               'columns': ['time', 'last'],
            #               'values': [
            #                   ['2023-07-17T11:04:58.224984832Z', 36]
            #               ]
            #               }
            #          ]
            #          }
            #     ]
            #     }
            # ]
            data = response.json()

            if len(data) > 0:
                try:
                    return ResultSet(data["results"][0])
                except KeyError:
                    print("KEY ERROR WHEN QUERY TO /query ENDPOINT")
                    return None
            return None
        else:
            print(f"Error: {response.status_code} - {response.text}")
        return None

    def write_points(self,
                     points,
                     time_precision=None,
                     database=None,
                     retention_policy=None,
                     tags=None,
                     batch_size=None,
                     protocol='json',
                     consistency=None,
                     **kwargs
                     ):
        bucket = f"{database}/autogen"

        # mapping of old tags annotations (influx 1.x)
        point: dict
        for point in points:
            if type(point) is dict and "tags" not in point.keys():
                point["tags"] = tags
            elif type(point) is dict and "tags" in point.keys():
                point["tags"].update(tags)

        with self.write_api(write_options=SYNCHRONOUS) as write_api:
            write_api.write(bucket=bucket, record=points)
