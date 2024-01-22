import boto3
from datetime import datetime, timedelta


def get_latest_lambda_metrics(log_group_name):
    aws_access_key_id = ''
    aws_secret_access_key = ''
    region_name = 'ap-south-1'  # Replace with your AWS region

    client = boto3.client('logs', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)

    filter_pattern = 'REPORT RequestId'

    filter_parameters = {
        'logGroupName': log_group_name,
        'startTime': int((datetime.now() - timedelta(days=1)).timestamp()) * 1000,  # 24 hours ago
        'limit': 1,
        'filterPattern': filter_pattern
    }

    response = client.filter_log_events(**filter_parameters)

    # Extract the relevant information from the latest log entry
    if 'events' in response and response['events']:
        latest_event = response['events'][0]
        log_message = latest_event['message']

        log_list = log_message.split('\t')

        key_value_pairs = [item.split(': ', 1) for item in log_list if ':' in item]

        log_data = dict(key_value_pairs)

    return log_data

log_group_name = '/aws/lambda/ffmpeg'  

data = get_latest_lambda_metrics(log_group_name)


