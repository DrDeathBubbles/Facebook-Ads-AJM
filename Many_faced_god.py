#This is a file for the creation of audicence from phonebooks
#And creating ads which use the photos of these phonebooks
#To make targeted ads

from Audience_tools import *
from Ads_tools import *
import glob
import csv
import time

path_to_data_files = '/Users/aaronmeagher/Work/testing_ads/'

if __name__ == "__main__":
    
    users = {}
    #Get users and create custom audiences
    files = glob.glob(path_to_data_files + '*.csv')
    for _file in files:
        dict_key = _file.lstrip(path_to_data_files).rstrip('.csv')
        temp =[]
        with open(_file,'r') as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                temp.extend(row)
        users[dict_key] = temp

    audience_map = {}
    audience = Audiences('act_851394958259883')
    for key in users.keys():
        audience_id = audience.creating_custom_audience(account_id ='act_851394958259883', 
        ca_name = key, ca_description = key)          

        audience.add_users_phone(users[key],audience_id)
        audience_map[key] = audience_id['id']


    #Sleep - needs to sleep for 2 hours

    a = facebook_ads()
    campaign = a.create_campaign(851394958259883,"DS_AJM_AUDIENCE_TEST_2", spend_cap = 10000)
    for key in audience_map.keys():
        targeting_params = a.targeting_parameters_custom_audience(audience_map[key])
        adset = a.ad_set_creation(851394958259883,'AJM_ADSET_TEST',campaign['id'],targeting_params)
        image = a.create_ad_image(851394958259883,path_to_data_files + key + '.png')
        ad_creative = a.create_ad_creative('This is the AdCreativeLinkData.Field.message',
        'websummit.com',image['hash'],294067420659309,851394958259883,'AJM_TEST_CREATIVE'
        )
        a.schedule_ads(851394958259883,'AJM_TEST',adset['id'],ad_creative['id']) 










#    Advertising_object = facebook_ads()
#    campaign = Advertising_object.create_campaign(851394958259883,'Many_faces')
    