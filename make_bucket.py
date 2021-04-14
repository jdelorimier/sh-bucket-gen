import logging
import boto3
from botocore.exceptions import ClientError
import copy

def create_bucket(bucket_name,s3_client,region=None):
    """Create an S3 bucket in a specified region

    https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-creating-buckets.html

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """
    # Create bucket
    try:
        if region is None:
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            # s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def delete_bucket(bucket_name,s3_client):
    s3_client.delete_bucket(
        Bucket=bucket_name)

def put_bucket_encryption(bucket_name,s3_client):
    s3_client.put_bucket_encryption(
        Bucket=bucket_name,
        ServerSideEncryptionConfiguration={
            'Rules': [
                {
                    'ApplyServerSideEncryptionByDefault': {
                        'SSEAlgorithm': 'AES256',
                    },
                },
            ]
        }
    )

def block_public_access(bucket_name, s3_client):
    s3_client.put_public_access_block(
        Bucket=bucket_name,
        PublicAccessBlockConfiguration={
            'BlockPublicAcls': True,
            'IgnorePublicAcls': True,
            'BlockPublicPolicy': True,
            'RestrictPublicBuckets': True
        }
    )

def put_bucket_tagging(bucket_name,s3_client):
    s3_client.put_bucket_tagging(
        Bucket=bucket_name,
        Tagging={
            'TagSet': [
                {
                    'Key': 'Project',
                    'Value': 'sh'
                },
                {
                    'Key': 'CreatedBy',
                    'Value': 'james'
                },
            ]
        }
    )   

def enableAccessLogging(bucketName, storageBucket,s3_client):
    # https://stackoverflow.com/questions/56649516/how-to-enable-s3-server-access-logging-using-the-boto3-sdk
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
    #Give the group log-delievery WRITE and READ_ACP permisions to the
    #target bucket

    targetPrefix='{bucket}/{bucket}--'.format(bucket=bucketName)

    s3_client.put_bucket_logging(
        Bucket=bucketName,
        BucketLoggingStatus={
            'LoggingEnabled': {
                'TargetBucket': storageBucket,
                'TargetPrefix': targetPrefix,
                'TargetGrants': [
                {
                    'Grantee': {
                        'Type': 'Group',
                        'URI': 'http://acs.amazonaws.com/groups/s3/LogDelivery',
                    },
                    'Permission': 'READ',
                }
            ]
            }
        }
    )