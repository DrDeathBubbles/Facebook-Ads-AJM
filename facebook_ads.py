
import os
import logging
from facebookads import FacebookAdsApi

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class facebook_ads:
    """
    A class for the creating of ad campaigns, adding adsets and ad creative
    """

    def __init__(self):
        """
        Initialising the FacebookAdsApi
        """
        try:
            app_id = os.environ['APPID']
            app_secret = os.environ['APPSECRET']
            access_token = os.environ['ACCESSTOKEN']

            FacebookAdsApi.init(app_id, app_secret, access_token)

        except KeyError as ke:
            logger.error('You need to set the following environment variable \n {}'.format(ke))
