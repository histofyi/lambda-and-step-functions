import boto3
import json
import urllib3
import os

http = urllib3.PoolManager()
s3 = boto3.client('s3')

bucket = os.environ['bucket']
key = "logs/input/rcsb_download.json"


def return_query_name(query_name):
  if query_name is None:
    query_name = 'default'
  return query_name


def fetch_query_file(query_name):
  key = 'config/queries/rcsb/{query_name}.json'.format(query_name = query_name)
  obj = s3.get_object(Bucket=bucket, Key=key)
  query = obj['Body'].read().decode('utf-8')
  return query


def fetch_rcsb_query(query_name):
    r = http.request('GET', 'https://search.rcsb.org/rcsbsearch/v1/query?json=' + fetch_query_file(query_name), headers={'Content-Type': 'application/json'})
    if r.status == 200:
        search_content = json.loads(r.data.decode('utf-8'))
        download_list = [entry['identifier'].lower() for entry in search_content['result_set']]
        return download_list, None, True
    else:
        return None, 'error', False


def lambda_handler(event, context):
    query_name = return_query_name(event['query_name'])
    data, errors, success = fetch_rcsb_query(query_name)
    if success:
        s3.put_object(Body=json.dumps(data), Bucket=bucket, Key=key)

        return {
          'success': True,
          'structures_found': len(data),
          'search_file': query_name
        }
