import pandas as pd
import os 
from facebookads import FacebookAdsApi
#from facebookads.objects import CustomAudience, AdAccount, AdSet
from facebookads.adobjects.customaudience import CustomAudience
from facebookads.adobjects.adaccount import AdAccount
from facebookads.adobjects.adset import AdSet

import logging
import hashlib


logger = logging.getLogger(__name__)

class Audiences():
    """
    A class for the manipulation of custom audiences for facebook 
    """

    def __init__():
        try:
            app_id = os.environ["APPID"]
            app_secret = os.environ['APPSECRET']
            access_token = os.environ['ACCESSTOKEN']

            FacebookAdsApi.init(app_id, app_secret, access_token)
            logger.info('FB INIT')


        except KeyError as ke:
            logger.error('You need to set the following environ variables:\n'
                    'APPID, APPSECRET, ACCESSTOKEN {}'.format(ke)
                    )

        except ValueError as ve:
            logger.error(ve)


    def hashing(data):
        return [hashlib.sha224(k.encode('utf-8')).hexdigest() for k in data]



    def creating_custom_audience(**kwarg):    
        try:
            audience = CustomAudience(parent_id=kwarg['account_id'])
            audience[CustomAudience.Field.subtype] = CustomAudience.Subtype.custom
            audience[CustomAudience.Field.name] = kwarg['ca_name'] 
            audience[CustomAudience.Field.description] = kwarg['ca_description'] 
            audience_id = audience.remote_create()

        except KeyError as ke:
            logger.error('You need to supply the following keyword variables\n'
                    'account_id,ca_name,ca_descriptio {}'.format(ke))
            return 

        return audience_id


    def add_users(users,audience_id = ''):

        chunks = []
        for i in range(0,len(users),3000):
            chunks.append(users[i:i+3000])
        audience = CustomAudience(audience_id['id'])

        for group in chunks: 
            audience.add_users(CustomAudience.Schema.email_hash, group)
        return


    def add_users_phone(users,audience_id = ''):

        chunks = []
        for i in range(0,len(users),500):
            chunks.append(users[i:i+500])
        audience = CustomAudience(audience_id['id'])

        for group in chunks: 
            audience.add_users(CustomAudience.Schema.phone_hash, group)
        return

    def creating_look_alike(**kwarg):
        try:
            audience = CustomAudience(parent_id=kwarg['account_id'])
            audience[CustomAudience.Field.subtype] = CustomAudience.Subtype.lookalike
            audience[CustomAudience.Field.name] = kwarg['ca_name'] 
            audience[CustomAudience.Field.description] = kwarg['ca_description'] 
            audience['origin_audience_id'] = kwarg['oa_id'] 
            audience[CustomAudience.Field.lookalike_spec] = {'type':'similarity','country':kwarg['country']}
            audience_id = audience.remote_create() 

        except KeyError as ke:
            logger.error('You need to supply the following keyword variables\n'
                    'account_id,ca_name,ca_description,ca_id,country {}'.format(ke))
            return

        return audence_id



    def sharing_audience(**kwarg):
        audience = CustomAudience(parent_id = kwarg['account_id'])
        audience.share_audience(account_ids)
        return


    def custom_audiences_by_account(**kwarg):
        audience = CustomAudience(parent_id = kwarg['account_id'])

        return audience


    def read_custom_audiences_by_account(**kwarg):
        account = AdAccount(kwarg['account_id'])
        ca = account.get_custom_audiences(fields =[CustomAudience.Field.name])
        return ca



    def match_custom_audience(**kwargs):
        fb_api_init()
        out = []
        words = [x.lower() for x in kwargs['words']]
        account = AdAccount(kwargs['account_id'])
        ca = account.get_custom_audiences(fields =[CustomAudience.Field.name])

        for audience in ca:
            if any(word in [x.lower() for x in audience['name'].split(' ')]  for word in words):
                out.append(audience)

        return out 



if __name__ == '__main__':

    #data = pd.read_csv('/Users/aaronmeagher/Work/Facebook_experiments/Paddy_experiments/alpha_websummit/ad_input_data/tito.csv')

    #temp = data['Ticket Email']
    #temp = temp.append(data['Order Email'])
    #temp.dropna(inplace = True)
    #users = temp.unique()
    fb_api_init()

    #audience_id = creating_custom_audience(account_id ='act_851394958259883', ca_name = 'Tito_sep_15',\
     #       ca_description = 'The export from DK from Tito in sep 2015 ' ) 
#    Experiments = read_custom_audiences_by_account(account_id = 'act_872554132810632')
    #WS = read_custom_audiences_by_account(account_id = 'act_54708236')
    #add_users(users,audience_id)

    Test = match_custom_audience(account_id = 'act_851394958259883',
                                            words = ['thank', 'collision'])


    #   look_alike = creating_look_alike(account_id ='act_851394958259883', ca_name = 'Look_alike_audience_api_test', \
#            ca_description = 'This is a test of the look-alike audience creation tool ', oa_id = audience_id['id'],\
#            country='US')


#    audiences = []
#    while Experiments.load_next_page() == True:
#        print(Experiments)
#        audiences.append(Experiments)







