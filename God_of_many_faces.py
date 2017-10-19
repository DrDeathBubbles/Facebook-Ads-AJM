#This is a file for the creation of audicence from phonebooks
#And creating ads which use the photos of these phonebooks
#To make targeted ads

from Audience_tools import *
from Ads_tools import *
import glob
import csv


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


    #Sleep











#    Advertising_object = facebook_ads()
#    campaign = Advertising_object.create_campaign(851394958259883,'Many_faces')
    