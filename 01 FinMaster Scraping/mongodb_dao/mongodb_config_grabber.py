import requests
import sys
from pymongo import MongoClient
from dto.real_state_entry_dto import RealStateEntryDTO

class MongoConfigGrabber:

    def __init__(self):
        self.client = MongoClient('mongodb+srv://Sandra:<Sandra>@cluster0.xs4os.mongodb.net/real-state-db?retryWrites=true&w=majority')
        
        self.db = self.client['real-state-db']
        self.scrapping_urls_idealista=[]
        self.scrapping_urls_fotocasa=[]
    
    def get_scrapping_urls(self):
        scrapping_config_collection=self.db.scrapping_config
        for url in scrapping_config_collection.find({}):
            url_str = url["url"]
            if ("idealista" in url_str):
                self.scrapping_urls_idealista = self.scrapping_urls_idealista + [url_str]
            if ("fotocasa" in url_str):
                self.scrapping_urls_fotocasa = self.scrapping_urls_fotocasa + [url_str]

        print (self.scrapping_urls_idealista)
        
