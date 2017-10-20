
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
from facebookads.adobjects.adcreative import AdCreative
from facebookads.adobjects.adcreativelinkdata import AdCreativeLinkData
from facebookads.adobjects.adcreativeobjectstoryspec \
    import AdCreativeObjectStorySpec
from facebookads.adobjects.ad import Ad

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




    def create_campaign(self,act_id,campaign_name,spend_cap=10000):
        """
        Creates named campaign within the advertising account with spendcap.a

        referenced by act_id. The name of the campaign to
        be genereated is the campaing_name.

        Returns

        <Campaign> {
        "id": "6090107330196",
        "name": "AJM_TEST_NES",
        "objective": "LINK_CLICKS"
        }

        """
 
        campaign = Campaign(parent_id='act_{}'.format(act_id))
        campaign.update({
            Campaign.Field.spend_cap:spend_cap,
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

    def targeting_parameters_custom_audience(self,audience_id):
        """
        Creates the targeting for a specific custom audience
        """
        targeting = {
            Targeting.Field.custom_audiences:[{'id':audience_id}]  
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
    
    def create_ad_creative(self,message,link,image_hash,page_id,act_id,adcreative_name):
        link_data = AdCreativeLinkData()
        link_data[AdCreativeLinkData.Field.message] = message 
        link_data[AdCreativeLinkData.Field.link] = link 
        link_data[AdCreativeLinkData.Field.image_hash] = image_hash 

        object_story_spec = AdCreativeObjectStorySpec()
        object_story_spec[AdCreativeObjectStorySpec.Field.page_id] = page_id 
        object_story_spec[AdCreativeObjectStorySpec.Field.link_data] = link_data

        creative = AdCreative(parent_id='act_{}'.format(act_id))
        creative[AdCreative.Field.name] = 'AdCreative for Link Ad'
        creative[AdCreative.Field.object_story_spec] = object_story_spec
        creative.remote_create()

        return(creative)

    def schedule_ads(self,act_id, ad_name,ad_set_id, creative_id):
        ad = Ad(parent_id='act_{}'.format(act_id))
        ad[Ad.Field.name] = ad_name
        ad[Ad.Field.adset_id] = ad_set_id 
        ad[Ad.Field.creative] = {
            'creative_id': creative_id,
        }
        ad.remote_create(params={
            'status': Ad.Status.paused,
        })

        return ad


if __name__ == '__main__':
    a = facebook_ads()
    campaign = a.create_campaign(851394958259883,'AJM_TEST_NES') 
    targeting = a.targeting_search('Xbox')
    #targeting_params = a.targeting_parameters(targeting)
    targeting_params = a.targeting_parameters_custom_audience(6085957639596)
    adset = a.ad_set_creation(851394958259883,'AJM_ADSET_TEST',campaign['id'],targeting_params)
    image = a.create_ad_image(851394958259883,'/Users/aaronmeagher/Desktop/San_Juan.jpg')
    ad_creative = a.create_ad_creative('This is the AdCreativeLinkData.Field.message',
    'websummit.com',image['hash'],294067420659309,851394958259883,'AJM_TEST_CREATIVE'
    )
    a.schedule_ads(851394958259883,'AJM_TEST',adset['id'],ad_creative['id'])
