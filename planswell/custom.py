import json
import os
import unicodedata
from facebookads.adobjects.adaccount import AdAccount
from facebookads import FacebookSession
from facebookads.api import FacebookAdsApi
from facebookads.adobjects.user import User
from facebookads.adobjects.customaudience import CustomAudience


this_dir = os.path.dirname('custom.py')
config_filename = os.path.join(this_dir, 'config.json')

config_file = open(config_filename)
config = json.load(config_file)

DAVE = 0
ABACUS = 4

my_app_id = config['app_id']
my_app_secret = config['app_secret']
my_access_token_1 = config['access_token']

session1 = FacebookSession(
    my_app_id,
    my_app_secret,
    my_access_token_1
)

api1 = FacebookAdsApi(session1)

FacebookAdsApi.set_default_api(api1)
me = User(fbid='me', api=api1)
my_accounts = list(me.get_ad_accounts())
print(my_accounts)
my_account = my_accounts[ABACUS]

my_account_id = my_account.get_id_assured()
print(my_account_id)


account = AdAccount(my_account_id)
custom_audiences = account.get_custom_audiences(fields=[
    CustomAudience.Field.name,
    CustomAudience.Field.id,
    CustomAudience.Field.approximate_count
])

our_audiences = []
for audience in custom_audiences:
	print(audience[CustomAudience.Field.name])
	print(audience[CustomAudience.Field.id])
	print(audience[CustomAudience.Field.approximate_count])
	print(" ")

# params = {
#     CustomAudience.Field.name: 'My test lookalike audience',
#     CustomAudience.Field.subtype: CustomAudience.Subtype.lookalike,
#     CustomAudience.Field.origin_audience_id: "23842584561250794",
#     CustomAudience.Field.lookalike_spec: {
#         'type': 'similarity',
#         'country': 'CA',
#     },
# }
# lookalike = account.create_custom_audience(params=params)
# print(lookalike)