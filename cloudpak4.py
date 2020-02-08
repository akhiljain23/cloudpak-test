import os
import datetime
import pandas
from cloudant.client import Cloudant
from cloudant import database

# print(os.environ)
startDate = os.environ['START_DATE']
endDate = os.environ['END_DATE']
catalogOfferingType = os.environ['CATALOG_OFFERING_TYPE']

startDate = datetime.datetime.strptime(startDate, '%Y-%m-%d')
endDate = datetime.datetime.strptime(endDate, '%Y-%m-%d')

if endDate > startDate:
    print(startDate, endDate, catalogOfferingType)

client = Cloudant(None, None, url="http://127.0.0.1:5984", admin_party=True, connect=True)
session = client.session()
db_obj = database.CloudantDatabase(client, "blueprint_db")

offering_mapping = {
    "helm" : "blueprinthelmmetric",
    "cloudpak": "blueprintcloudpakmetric",
    "terraform" : "blueprintterraformmetric"
}

res = db_obj.get_view_result('_design/blueprintmetric', offering_mapping[catalogOfferingType],
    raw_result=True, include_docs=True, reduce=False)
final_res = []
for row in res['rows']:
    cr_at = (row['doc']['created_at'])
    print(cr_at[:11])
    cr_at = datetime.datetime.strptime(cr_at[:10], '%Y-%m-%d')
    if cr_at >= startDate and cr_at <= endDate:
        entry = {
            "account":row['doc']['account'],
            "workspace_id":row['doc']['_id'],
            "workspace_status":row['doc']['status'],
            "workspace_createdDate": row['doc']['created_at'],
            "offering_installed_on" : row['doc']['runtime_data'][0]['created_on'],
            "offering_destroyed_on" : row['doc']['runtime_data'][0]['destroyed_on'],
            "Offering_name" : row['doc']['catalog_ref']['item_name'],
            "Offering_id" : row['doc']['catalog_ref']['item_id'],
            "Offering_url" : row['doc']['catalog_ref']['item_url'],
            "cluster_id":row['doc']['shared_data']['cluster_id'],
            "cluster_type" : row['doc']['shared_data']['cluster_type'],
            "cluster_worker_count": row['doc']['shared_data']['worker_count'],
            "cluster_worker_machine_type" : row['doc']['shared_data']['worker_machine_type'],
            "cluster_created_on" : row['doc']['shared_data']['cluster_created_on']
        }
        final_res.append(entry)
dataframe = pandas.DataFrame(final_res)
print(dataframe)
open('qwerty.csv', 'a').close()
dataframe.to_csv("qwerty.csv", index=False)

# Disconnect from the server
client.disconnect()
