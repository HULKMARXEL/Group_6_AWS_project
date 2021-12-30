import boto3

def forecast_data(identifier):
    forecast = boto3.client('forecast', region_name='us-east-1')

    dataset = forecast.create_dataset(
        DatasetName= 'dataset_' + identifier.replace("-", "_"),
        Domain='CUSTOM',
        DatasetType='TARGET_TIME_SERIES',
        DataFrequency='min',
        Schema={
            "Attributes": [
                {
                    "AttributeName": "item_id",
                    "AttributeType": "string"
                },
                {
                    "AttributeName": "timestamp",
                    "AttributeType": "timestamp"
                },
                {
                    "AttributeName": "target_value",
                    "AttributeType": "float"
                }
            ]
        }
    )

    dataset_group = forecast.create_dataset_group(
        DatasetGroupName='dataset_group_' + identifier.replace("-", "_"),
        Domain='CUSTOM',
        DatasetArns=[
            dataset['DatasetArn']
        ]
    )

    dataset_import = forecast.create_dataset_import_job(
        DatasetImportJobName='dataset_import_' + identifier.replace("-", "_"),
        DatasetArn=dataset['DatasetArn'],
        DataSource={
            'S3Config': {
                'Path': 's3://group-6-marxel-train-data/' + identifier + '.csv',
                'RoleArn': 'arn:aws:iam::535906493048:role/service-role/AmazonForecast-ExecutionRole-1640867055574'
            }
        }
    )
