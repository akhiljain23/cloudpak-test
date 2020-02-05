import os
import datetime
from cloudant.client import Cloudant
from cloudant import design_document
from cloudant import database
from cloudant import view

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
#print(client.list_views())
my_database1 = client["blueprint_db"]
db_obj = database.CloudantDatabase(client, "blueprint_db")
#print(db_obj.design_documents())
print(db_obj.list_design_documents())

ddoc = design_document.DesignDocument(db_obj, "_design/workspace")
ddoc.fetch()
#ddoc.add_view("sampleView", "")
print(ddoc)
print(ddoc.list_views())

view_obj = view.View(ddoc, "workspacecountbyaccount")
print(dir(view_obj))
#print(view_obj.custom_result())
#with view_obj.custom_result(include_docs=True) as rslt:
#    for doc in rslt:
#        print(doc)

result = db_obj.get_view_result('_design/workspace', 'workspacecountbyaccount',
    raw_result=True)
print(result)

res = db_obj.get_view_result('_design/workspace', 'workspacecountbyaccount',
    raw_result=True, include_docs=True, skip=100, limit=100, reduce=False)
res = db_obj.get_view_result('_design/workspace', 'workspacecountbyaccount',
    raw_result=True, include_docs=True, reduce=False)
final_res = []
for row in res['rows']:
    cr_at = (row['doc']['created_at'])
    print(cr_at[:11])
    cr_at = datetime.datetime.strptime(cr_at[:10], '%Y-%m-%d')
    if cr_at >= startDate and cr_at <= endDate:
        final_res.append(row['doc'])
print(final_res)
print(len(final_res))





a = "1994-01-23"
date_time_obj = datetime.datetime.strptime(a, '%Y-%m-%d')
print(date_time_obj)

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
