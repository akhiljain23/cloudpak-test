import os
import datetime
from cloudant.client import Cloudant

# print(os.environ)
startDate = os.environ['START_DATE']
endDate = os.environ['END_DATE']
catalogOfferingType = os.environ['CATALOG_OFFERING_TYPE']

startDate = datetime.datetime.strptime(startDate, '%Y-%m-%d')
endDate = datetime.datetime.strptime(endDate, '%Y-%m-%d')

if endDate > startDate:
    print(startDate, endDate, catalogOfferingType)

client = Cloudant("admin", "admin", url="http://127.0.0.1:5984", connect=True)

session = client.session()
print('Username: {0}'.format(session['userCtx']['name']))
print('Databases: {0}'.format(client.all_dbs()))

a = "1994-01-23"
date_time_obj = datetime.datetime.strptime(a, '%Y-%m-%d')

b = "2020-01-29T07:00:42+0000"
date_time_obj2 = datetime.datetime.strptime(b, '%Y-%m-%dT%H:%M:%S+%f')

all_dbs = client.all_dbs()
docs = []
for db in all_dbs:
    if db == "blueprint_db":
        my_database = client[db]
        for document in my_database:
            docs.append(document)
print(len(docs))



# Disconnect from the server
client.disconnect()
