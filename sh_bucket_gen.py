import click
import boto3
import make_bucket
import validate_name
from decouple import config

PROD_ID=config('PROD_ACCOUNT')
DEFUALT_LOG_BUCKET=config('DEFUALT_LOG_BUCKET')

def validate_bucketname(ctx, param, value):
    bucket=value
    if validate_name.assert_prefix(bucket) == True:
        return bucket
    else:
        raise click.BadParameter('bad prefix no `c4ads-sh` at start')

@click.command()
@click.option("--bucket",'bucket', prompt="bucket-name", callback=validate_bucketname, help="Bucket name for SH data.")
@click.option("--profile",default="prod",help="AWS profile to use. Should be prod.")
@click.option("--log_bucket", default=DEFUALT_LOG_BUCKET, help="server access logging bucket")
def main(bucket, profile, log_bucket):

    session = boto3.Session(profile_name=profile)
    s3_client = session.client('s3')
    sts = session.client("sts")
    account_id = sts.get_caller_identity()["Account"]
    if account_id != PROD_ID:
        click.confirm('You are not in prod account. Be sure you have a logging bucket set up. Continue?', abort = True)

    # actions
    make_bucket.create_bucket(bucket, s3_client)
    make_bucket.put_bucket_encryption(bucket, s3_client)
    make_bucket.block_public_access(bucket, s3_client)
    make_bucket.put_bucket_tagging(bucket, s3_client)
    make_bucket.enableAccessLogging(bucketName=bucket,storageBucket=log_bucket,s3_client=s3_client)

    click.echo(f'using profile {profile}')
    click.echo(f'bucket name is {bucket}')
    click.echo('s3 path is s3://{}'.format(bucket))

if __name__ == '__main__':
    main()

