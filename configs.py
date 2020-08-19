from datetime import datetime, timedelta
from AWS.s3 import S3
import ast
import os


class Configs:

    #time stuff
    END_DATE = datetime.today().strftime('%Y-%m-%d')
    THIRTY_DAYS_FROM_TODAY = datetime.today() - timedelta(days=30)
    START_DATE = THIRTY_DAYS_FROM_TODAY.strftime('%Y-%m-%d')
    TODAY = datetime.today().strftime('%Y-%m-%d')

    @staticmethod
    def creds_helper(creds):
        """
        Just a quick way to grab env variables for diff banks
        """

        return ast.literal_eval(os.environ.get(creds))

    @staticmethod
    def s3_helper_uploader(bank, folder_location, dataframe):
        """
        Instead of rewriting this 6 times for each bank figure I just make a static
        function in the configs(for now). This will be used to just call the s3 class in AWS
        and send the data over to your AWS s3 bucket.
        :param bank: Banks name
        :param folder_location: Folder Locations name
        :param dataframe: Dataframe to upload
        :return: Hopefully a nice parquet file in your s3 bucket
        """

        try:
            s3 = S3(f"checking_savings_{Configs.TODAY}.parquet",
                    Configs.creds_helper("BUCKET_NAME")["BUCKET"],
                    Configs.creds_helper("AWS_KEYS")["ACCESS_KEY_ID"],
                    Configs.creds_helper("AWS_KEYS")["AWS_SECRET"],
                    str(bank),
                    str(folder_location),
                    dataframe)

            print("Uploading data to s3")

            s3.upload_file()

        except Exception as e:
            print("something went wrong! : " + str(e))
