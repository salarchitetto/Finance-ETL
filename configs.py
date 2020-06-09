from datetime import datetime
import ast
import os


class Configs:
    # Acorns

    # CapitalOne

    # Mohela

    # Nelnet

    # PNC
    PNC_LINK = "https://www.pnc.com"

    # Slavic

    # Vanguard

    # static sleep time
    TIME_TO_SLEEP = 5

    TODAYS_DATE = datetime.today().strftime('%Y-%m-%d')

    @staticmethod
    def creds_helper(creds):
        """
        Just a quick way to grab env variables for diff banks
        """
        return ast.literal_eval(os.environ.get(creds))
