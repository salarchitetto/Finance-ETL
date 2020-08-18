from datetime import datetime,timedelta
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
