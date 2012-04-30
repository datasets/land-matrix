import csv
import logging
import datastore.client

url = 'http://datahub.io/dataset/land-matrix/resource/f46a9192-cf2b-410e-b4f7-dc80538e5541'
client = datastore.client.DataStoreClient(url)
fp = 'data/database.csv'

def upload():
    # use Deal Number as unique id 
    def add_id(dict_):
        dict_['id'] = dict_['Deal Number']
        return dict_
    # in general should not need to delete since have unique id
    client.delete()
    client.upsert(map(add_id, csv.DictReader(open(fp), delimiter=';')))

if __name__ == '__main__':
    # show progress info
    logging.basicConfig(level=logging.DEBUG)
    upload()

