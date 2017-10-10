
import os
import logging
import datetime

from facebookads import FacebookAdsApi
from facebookads.adobjects.campaign import Campaign
from facebookads.adobjects.targetingsearch import TargetingSearch
from facebookads.adobjects.targeting import Targeting
from facebookads.adobjects.adaccount import AdAccount
from facebookads.adobjects.adset import AdSet
from facebookads.adobjects.adimage import AdImage


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
        interests = [interest['id'] for interest in interests]
        targeting = {
            Targeting.Field.geo_locations: {
                Targeting.Field.countries: ['US']
            },
            Targeting.Field.interests: interests,

        }
        return targeting


    def ad_set_creation(self,act_id,ad_set_name,campaign_id,targeting):
        today = datetime.date.today()
        start_time = str(today + datetime.timedelta(weeks=1))
        end_time = str(today + datetime.timedelta(weeks=2))

        ad_account = AdAccount(fbid='act_{}'.format(act_id))

        params = {
            AdSet.Field.name: ad_set_name ,
            AdSet.Field.campaign_id: campaign_id,
            AdSet.Field.daily_budget: 1000,
            AdSet.Field.billing_event: AdSet.BillingEvent.impressions,
            AdSet.Field.optimization_goal: AdSet.OptimizationGoal.reach,
            AdSet.Field.bid_amount: 2,
            AdSet.Field.targeting: targeting,
            AdSet.Field.start_time: start_time,
            AdSet.Field.end_time: end_time,
            AdSet.Field.status: AdSet.Status.active,
        }
        adset = ad_account.create_ad_set(params=params)

        return adset

    def create_ad_image(self,act_id,image_path):
        image = AdImage(parent_id = 'act_{}'.format(act_id))
        image[AdImage.Field.filename] = image_path 
        image.remote_create()
        
        return image


if __name__ == '__main__':
    a = facebook_ads()
    campaign = a.create_campaign(851394958259883,'AJM_TEST_NES') 
    targeting = a.targeting_search('Xbox')
    targeting_params = a.targeting_parameters(targeting)
    adset = a.ad_set_creation(851394958259883,'AJM_ADSET_TEST',campaign['id'],targeting_params)
