#Takes a tito export and filters based on ticket type, t
# he resulting emails of this filtering outputted to a csv
import pandas as pd
import sys
import csv
from hashed_phone_numbers_processing import *  

sys.path.insert(0,'/Users/aaronmeagher/Work/Facebook-Ads-API')

from upload_custom_audience import *

out = []

#with open('./que','r') as f:
#    data = csv.reader(f)
#    for row in data:
#        out.extend(row)

data = pd.read_csv('./Phone_book_test.csv')


users = data['raw'] 
users = users.dropna()
users = users.drop_duplicates()
audience_name = 'NEW_DS_phonebook_dropna_dropduplicates_raw'
#users = [out[i][0] for i in range(0,len(out)-1)]

#users = [hashing_phone_numbers(i) for i in users] 
fb_api_init()
audience_id = creating_custom_audience(account_id ='act_851394958259883', ca_name = audience_name,\
               ca_description = audience_name)          

add_users_phone(users,audience_id)


#audience_id = creating_custom_audience(account_id ='act_851394958259883', ca_name = 'DS_RISE_API_STRIPPED',\
#            ca_description = 'DS_RISE_API_STRIPPED' )          
#bins = 5000
#for i in range(0,len(users),bins):
#   
#
#    temp = add_users_phone(users[i:i+bins],audience_id)
#
#