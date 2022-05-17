import requests
import sys
from pymongo import MongoClient
from dto.real_state_entry_dto import RealStateEntryDTO

class MongoDBDataRecorder:

    def __init__(self, dto_dictionary):        
        try:
            self.dto_dictionary = dto_dictionary
            self.client =  MongoClient('mongodb+srv://Sandra:Sandra@cluster0.xs4os.mongodb.net/real-state-db?retryWrites=true&w=majority')
            self.db = self.client['real-state-db']

        except Exception:
            print("Unable to connect to the server.")
            
    def post_data(self):
        scrapped_data_collection=self.db.Remax
        for key, dto_list in self.dto_dictionary.items():
            print("------- saving data from url " + key)
            for dto in dto_list:
                print("saving " + dto.id)
                dto_mongodb=dto.__dict__
                scrapped_data_collection.save(dto_mongodb)
                
    def post_detalle(self):
        scrapped_data_collection=self.db.RemaxDetalle
        for key, dto_list in self.dto_dictionary.items():
            #print("------- saving data from url " + key)
            for dto in dto_list:
                print("saving :" + dto.id)
                dto_mongodb=dto.__dict__
                scrapped_data_collection.save(dto_mongodb)                