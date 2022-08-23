import datetime
import os

from Scripts.App import AbusedIP
import pymongo as pymongo
import pandas as pd
pd.set_option('display.max_columns', 10)
from IP_Reputation.Scripts.init import *




class BackEnd(AbusedIP):

    def __init__(self, ipaddress):
        super().__init__()

        self.ipaddress = [ipaddress]
        self.clusuter = pymongo.MongoClient(mongo_connection) # MongoConnection String Here
        self.db = self.clusuter['AbuseDatabase']

        self.collection_AbuseIPs = self.db['AbuseIPs']
        self.collection_AbuseVT = self.db['AbuseVT']

        self.check_existance()

    def check_existance(self):
        ad = []
        vd = []
        for ip in self.ipaddress:
            abuse_data = self.collection_AbuseIPs.find_one({"ipAddress" : ip.strip()})
            virus_data = self.collection_AbuseVT.find_one({"ip" : ip.strip()})
            if abuse_data == None and virus_data == None:
                abuse_data,virus_data = self.upload_data(ip)
                self.metadata["State"] = "New IP"
            else:
                print("This IP Alreaday Exists")
                self.metadata["State"] = "Existing IP"
                self.metadata['AbuseIP_Data'] = {"Status" : 200, "Reason" : "Ok"}
                self.metadata['AbuseIP_Data']["Data"] = abuse_data
                self.metadata["VirusTotal_Data"] = {"Status" : 200, "Reason" : "Ok"}
                self.metadata["VirusTotal_Data"]['Data'] = virus_data

            if virus_data:

                for k, v in virus_data.items():
                    if type(v) == list:
                        links = []
                        for ele in v:
                            if type(ele) == dict:
                                if "url" in ele.keys():
                                    links.append(ele['url'])
                                else:
                                    links.append(ele[list(ele.keys())[-1]])
                            if type(ele) == list:
                                links.append(ele[0])
                        virus_data[k] = links
                self.metadata['VirusTotal_Data']['Data'] = virus_data


    def upload_data(self,ip):
        self.main(ip)
        virus_data = None
        abuse_data = self.metadata["AbuseIP_Data"]["Data"]
        if self.metadata["VirusTotal_Data"] != None:
            virus_data = self.metadata["VirusTotal_Data"]["Data"]
        if  virus_data :
            self.collection_AbuseIPs.insert_one(abuse_data)
            self.collection_AbuseVT.insert_one(virus_data)

        return abuse_data,virus_data



# print(BackEnd("8.8.8.8").metadata)
