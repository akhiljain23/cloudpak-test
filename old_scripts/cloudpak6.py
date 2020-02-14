import os
import datetime
import pandas
from cloudant.client import Cloudant
from cloudant import database



def generate_records(start_date, end_date):

    database_name = "blueprint_db"
    server_url = "http://127.0.0.1:5984"
    username = None 
    password = None
    design_doc = "_design/blueprintmetric"
    view_name = "blueprintcloudpakmetric"

    client = Cloudant(username, password, url=server_url, admin_party=True, connect=True)
    db_obj = database.CloudantDatabase(client, database_name)

    res = db_obj.get_view_result(design_doc, view_name, raw_result=True, include_docs=True, reduce=False)

    final_res = []
    for row in res['rows']:
        offering_installed_on = row['doc']['runtime_data'][0].get('created_on', 'Not Available')
        if offering_installed_on == "0001-01-01T00:00:00Z":
            offering_installed_on = ""
        offering_destroyed_on = row['doc']['runtime_data'][0].get('destroyed_on', 'Not Available')
        if offering_destroyed_on == "0001-01-01T00:00:00Z":
            offering_destroyed_on = ""
        cr_at = (row['doc']['created_at'])
        cr_at = datetime.datetime.strptime(cr_at[:10], '%Y-%m-%d')
        if cr_at >= start_date and cr_at <= end_date:
            entry = {
                "account":row['doc'].get('account', 'Not Available'),
                "workspace_id":row['doc'].get('_id', 'Not Available'),
                "workspace_status":row['doc'].get('status', 'Not Available'),
                "workspace_region" : row['doc'].get('location', 'Not Available'),
                "workspace_createdDate": row['doc'].get('created_at', 'Not Available'),
                "offering_installed_on" : offering_installed_on,
                "offering_destroyed_on" : offering_destroyed_on,
                "Offering_name" : row['doc']['catalog_ref'].get('item_name', 'Not Available'),
                "Offering_id" : row['doc']['catalog_ref'].get('item_id', 'Not Available'),
                "Offering_url" : row['doc']['catalog_ref'].get('item_url', 'Not Available'),
                "Offering_version" : row['doc']['catalog_ref'].get('offering_version', 'Not Available'),
                "cluster_id":row['doc']['shared_data'].get('cluster_id', 'Not Available'),
                "cluster_type" : row['doc']['shared_data'].get('cluster_type', 'Not Available'),
                "cluster_worker_count": row['doc']['shared_data'].get('worker_count', 'Not Available'),
                "cluster_worker_machine_type" : row['doc']['shared_data'].get('worker_machine_type', 'Not Available'),
                "cluster_created_on" : row['doc']['shared_data'].get('cluster_created_on', 'Not Available'),
                "cluster_region" : row['doc']['shared_data'].get('region', 'Not Available'),
                "deleted": row['doc'].get('deleted', 'true')
            }
            final_res.append(entry)
    dataframe = pandas.DataFrame(final_res)
    df = dataframe.sort_values("offering_installed_on", ascending=False)
    print(df)
    df.to_csv("CloudPak-{}.csv".format(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")), index=False)

    # Disconnect from the server
    client.disconnect()


if __name__ == "__main__":
    start_date = os.environ['START_DATE']
    end_date = os.environ['END_DATE']

    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    print("start date for getting records", start_date)
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    print("End date for getting records",end_date)

    secret = os.environ['abcdef']
    print(secret)
    print("Above is secret$$$$$$$$$$$$$$$$$$$")
    if secret == "secret":
        print("HOORAYYYYYYYYYYYYYYY")
    else:
        print("SADDDDDDDDDDDD")
    if end_date >= start_date:
        generate_records(start_date, end_date)
    else:
        print("Start date is greater than end date")
        

    
