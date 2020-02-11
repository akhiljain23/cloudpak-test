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
        print(row['doc']['_id'])
        cr_at = (row['doc']['created_at'])
        print(cr_at[:11])
        cr_at = datetime.datetime.strptime(cr_at[:10], '%Y-%m-%d')
        if cr_at >= start_date and cr_at <= end_date:
            entry = {
                "account":row['doc']['account'],
                "workspace_id":row['doc']['_id'],
                "workspace_status":row['doc']['status'],
                "workspace_region" : row['doc']['location'],
                "workspace_createdDate": row['doc']['created_at'],
                "offering_installed_on" : row['doc']['runtime_data'][0]['created_on'],
                "offering_destroyed_on" : row['doc']['runtime_data'][0]['destroyed_on'],
                "Offering_name" : row['doc']['catalog_ref']['item_name'],
                "Offering_id" : row['doc']['catalog_ref']['item_id'],
                "Offering_url" : row['doc']['catalog_ref']['item_url'],
                "Offering_version" : row['doc']['catalog_ref']['offering_version'],
                "cluster_id":row['doc']['shared_data']['cluster_id'],
                "cluster_type" : row['doc']['shared_data']['cluster_type'],
                "cluster_worker_count": row['doc']['shared_data']['worker_count'],
                "cluster_worker_machine_type" : row['doc']['shared_data']['worker_machine_type'],
                "cluster_created_on" : row['doc']['shared_data']['cluster_created_on'],
                "cluster_region" : row['doc']['shared_data']['region']
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

    if end_date >= start_date:
        generate_records(start_date, end_date)
    else:
        print("Start date is greater than end date")
        

    
