
import os
import logging

from facebookads import FacebookAdsApi
from facebookads.adobjects.campaign import Campaign
from facebookads.adobjects.targetingsearch import TargetingSearch
from facebookads.adobjects.targeting import Targeting

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




    def create_campaign(self,act_id,campaign_name):
 
        campaign = Campaign(parent_id='act_{}'.format(act_id))
        campaign.update({
            Campaign.Field.name:campaign_name ,
            Campaign.Field.objective: Campaign.Objective.link_clicks,
        })

        campaign.remote_create(params={
            'status': Campaign.Status.paused,
        })
        return campaign        

    def targeting_search(self,ad_interest):
        params = {
            'q': ad_interest,
            'type': 'adinterest'
        }
        resp = TargetingSearch.search(params=params)
        return resp

    def targeting_parameters(self,interests):
        targeting = {
            Targeting.Field.geo_locations: {
                Targeting.Field.countries: ['US']
            },
            Targeting.Field.interests: interests,

        }
