import os
import fa

class facebook_ads:
    """
    A class for the creating of ad campaigns, adding adsets and ad creative
    """

    def __init__:
        """
        Initialising the FacebookAdsApi
        """
        try:
            app_id = os.environ['APPID']
            app_secret = os.environ['APPSECRET']
            access_token = os.environ['ACCESSTOKEN']