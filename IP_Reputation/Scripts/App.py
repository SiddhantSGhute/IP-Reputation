"""
Project Details :
Create VirusTotal and AbuseIPDb public accounts and retrieve respective API keys.
Get IP’s with "abuseConfidenceScore" greater than 95 from AbuseIPDb. Store the list of IPs and the corresponding data in a excel file.
Download and host a mongo server in Local or Cloud.
With the collected list of IPs, perform IP reputation check in VirusTotal and post “Country, Detected URLs, detected_downloaded_samples, undetected_downloaded_samples, undetected_urls in MongoDB under Collection ‘AbuseVT’
Send an automated mail to ‘Akhashavannan.Manivannan@optiv.com' with the AbuseIPDB result excel attached. Also post the VirusTotal results in email body in a presentable table format.
Feel free to add creativity and enrichments to the above requirement.


Helpful URLs:-



https://www.abuseipdb.com/
https://docs.abuseipdb.com/#introduction
https://developers.virustotal.com/v3.0/reference
https://www.virustotal.com/gui/home/upload
https://www.mongodb.com/
"""
import datetime
import time
import requests
from IP_Reputation.Scripts.init import *

class AbusedIP():

    def __init__(self):
        today = datetime.datetime.today()
        self.year, self.month, self.day, self.hour, self.minute = today.year, today.month, today.day, today.hour, today.minute

        self.metadata = dict()
        self.confidence_Score_threshold = 95
        self.abuse_key = abuse_key
        self.virus_key = virus_key



    def confidence_structural_data(self, data):
        structural_data = dict()
        keys = ['ipAddress', 'abuseConfidenceScore', 'countryCode', 'totalReports', 'domain', 'hostnames', 'ipVersion',
                'isPublic', 'isWhitelisted', 'isp', 'lastReportedAt', 'numDistinctUsers', 'usageType']
        for key in keys:
            if key in data.keys():
                structural_data[key] = data[key]
            else:
                structural_data[key] = [None]

        return structural_data

    def confidence_Score(self, ip):

        url = 'https://api.abuseipdb.com/api/v2/check'
        querystring = {
            'ipAddress': ip,
            'maxAgeInDays': '90'
        }

        headers = {
            'Accept': 'application/json',
            'Key': self.abuse_key
        }
        response = requests.get(url=url, params=querystring, headers=headers)
        self.metadata["AbuseIP_Data"] = {
            "Status": response.status_code,
            "Reason": response.reason
        }
        if response.status_code != 200:
            print({"Error": f"{response.reason} With Code {response.status_code}"})
            return None
        data = self.confidence_structural_data(response.json()['data'])

        return data

    def reputation_structural_data(self, data, ip):
        structural_data = dict()
        structural_data['ip'] = ip
        keys = ['country', 'detected_urls', 'undetected_urls', 'detected_downloaded_samples',
                'undetected_downloaded_samples']
        for key in keys:
            if key in data.keys():
                if not data[key]:
                    structural_data[key] = [None]
                else:
                    structural_data[key] = data[key]
            else:
                structural_data[key] = [None]

        return structural_data

    def reputation_score(self, ip):

        url = 'https://www.virustotal.com/vtapi/v2/ip-address/report'
        querystring = {
            'apikey': self.virus_key,
            'ip': ip
        }
        response = requests.get(url=url, params=querystring)
        self.metadata["VirusTotal_Data"] = {
            "Status": response.status_code,
            "Reason": response.reason
        }
        if response.status_code != 200:
            print({"Error": f"{response.reason} With Code {response.status_code}"})
            return None
        response_data = response.json()

        data = self.reputation_structural_data(response_data, ip)

        time.sleep(16)
        return data

    def main(self, ip=None):
        global virus_data
        virus_data = None
        if ip:
            self.metadata['IP'] = ip
            abuse_data = self.confidence_Score(ip)
            self.metadata['AbuseIP_Data']["Data"] = abuse_data

            if abuse_data:
                abuse_score = abuse_data['abuseConfidenceScore']
                if abuse_score >= self.confidence_Score_threshold:
                    self.metadata["Uploaded"] = True
                    virus_data = self.reputation_score(ip)
                    self.metadata["VirusTotal_Data"]['Data'] = virus_data
                else:
                    self.metadata["Uploaded"] = False
                    self.metadata["VirusTotal_Data"] = None


# abuseip = AbusedIP()  # Initiate
# process = abuseip.main("8.8.8.8") # Search For The IP
# metadata = abuseip.metadata # Returns The Data
# print(metadata)
