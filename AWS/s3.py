import boto3
from botocore.exceptions import ClientError
import awswrangler as wr


class S3:
    """
    Couple of functions for s3 access and what not
    """

    def __init__(self, file_name, bucket, access_key, secret, bank, sub_bucket, df=None):
        self.file_name = file_name
        self.bucket = bucket
        self.access_key = access_key
        self.secret = secret
        self.bank = bank
        self.sub_bucket = sub_bucket
        self.df = df

    def upload_file(self):
        """
        Upload a file to an S3 bucket
        """

        try:
            # login to s3 client
            s3_client = boto3.Session(aws_access_key_id=self.access_key,
                                      aws_secret_access_key=self.secret)

            wr.s3.to_parquet(self.df, f"s3://{self.bucket}/{self.bank}/{self.sub_bucket}/{self.file_name}",
                             boto3_session=s3_client)
            print(f"Written to S3 folder: {self.sub_bucket}")

        except ClientError as e:
            print(f"Error uploading: {self.file_name}: " + str(e))

    def load_file(self):
        """
        For testing. Checking to see if the file actually came through into
        the specified bucket

        *read multiple files = f"s3://{self.bucket}/{self.bank}/{self.sub_bucket}/ *

        :return: Dataframe
        """

        # login to s3 client
        s3_client = boto3.Session(aws_access_key_id=self.access_key,
                                  aws_secret_access_key=self.secret)
        try:
            df = wr.s3.read_parquet(f"s3://{self.bucket}/{self.bank}/{self.sub_bucket}/", boto3_session=s3_client)
            return df
        except ClientError as e:
            print(f"Error reading from {self.bucket}" + str(e))

    def get_s3_keys(self):
        """Get a list of keys in an S3 bucket."""

        keys = []
        client = boto3.client('s3', self.access_key,
                              self.secret)

        resp = client.list_objects_v2(Bucket=self.bucket)
        for obj in resp['Contents']:
            keys.append(obj['Key'])

        return keys
