import datetime
import os
from Scripts.Mail import SendMail
import pandas as pd
from colorama import Fore
import regex as re
from Database.AbuseVT import BackEnd
import pprint
import streamlit as st


class Processor():
    IP = None

    def __init__(self):
        self.today = datetime.datetime.today()
        self.year, self.month, self.day, self.hour, self.minute, self.second = self.today.year, self.today.month, self.today.day, self.today.hour, self.today.minute, self.today.second
        self.source = 'Single'
        self.ipaddress = []
        self.AbuseData = []
        self.VirusData = []
        self.html = None
        self.state = True
        self.abuse_limit = 1000
        self.virus_limit = 500
        self.common_path = r"E:\OptiveProject\Database\AbuseDatabase"
        os.makedirs(f"{self.common_path}\AbuseDatabase", exist_ok=True)
        os.makedirs(f"{self.common_path}\VirusDatabase", exist_ok=True)
        self.abuse_filename = f"{self.common_path}\AbuseDatabase\AbuseIP_{self.year}{self.month}{self.day}_{self.hour}{self.minute}{self.second}.csv"
        self.virus_filename = f"{self.common_path}\VirusDatabase\VirusTotal_{self.year}{self.month}{self.day}_{self.hour}{self.minute}{self.second}.csv"

    def check_limit(self, init: bool):
        filename = fr"{self.common_path}\Consumption.txt"
        if init:
            if os.path.isfile(filename):
                with open(filename, 'r') as f:
                    date, abuse, virus = [i.strip() for i in f.readlines()]
                    print(date, abuse, virus)
                    if date == f"{self.year}{self.month}{self.day}":
                        self.abuse_limit = int(abuse)
                        self.virus_limit = int(virus)
                    f.close()
            else:
                with open(filename, 'w') as f:
                    f.writelines([f"{self.year}{self.month}{self.day}\n", "1000\n", "500"])
                    f.close()
        else:
            with open(filename, 'w') as f:
                f.writelines([f"{self.year}{self.month}{self.day}\n", f"{self.abuse_limit}\n", f"{self.virus_limit}"])
                f.close()

    def check_state(self):
        global reason
        reason = 'Ok'
        abuse_state = self.metadata.get("AbuseIP_Data")
        virus_state = self.metadata.get("VirusTotal_Data")
        if virus_state:
            reason = virus_state['Reason']
            virus_state = virus_state['Status']
            if virus_state == 200:
                self.virus_limit -= 1

        else:
            virus_state = 200

        if abuse_state['Status'] != 200:
            self.state = False
            print(Fore.RED + f"Error Status & Reason:{abuse_state['Status']} {abuse_state['Reason']} ")

        else:
            self.abuse_limit -= 1
            if virus_state != 200:
                self.state = False
                print(Fore.RED + f"Error Status & Reason:{virus_state} {reason} ")

    def check_single_ip(self, ip):
        pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
        ip = pattern.search(ip)
        if ip:
            ip = ip[0]
            ip = [i if int(i) < 255 else None for i in ip.split('.')]
            if None in ip:
                return None
            ip = ".".join(ip)
            return ip

        return None

    def processIP(self):
        if self.ipaddress:
            for ip in self.ipaddress:
                print(Fore.RED + f"IP : {ip}" + Fore.GREEN)
                self.backend = BackEnd(ip)
                self.metadata = self.backend.metadata
                self.check_state()
                if not self.state:
                    break
                abuse_data = self.metadata['AbuseIP_Data']['Data']
                virus_data = self.metadata['VirusTotal_Data']
                if virus_data:
                    virus_data = virus_data['Data']
                    self.VirusData.append(virus_data)

                self.threshold = self.backend.confidence_Score_threshold
                self.AbuseData.append(abuse_data)
                pprint.pprint(abuse_data)
                if virus_data:
                    pprint.pprint(f"{virus_data}")
                print("-" * 50)

    def saveAbuse(self):
        if self.AbuseData:
            df = pd.DataFrame(self.AbuseData)
            df.to_csv(self.abuse_filename, index=False)

    def organinse(self, x):
        if len(x) > 1:
            return f"{x[0]} and more {len(x) - 1} found".title()
        elif len(x) < 1:
            return f"No Data Found"
        else:
            return x

    def createHtml(self):
        headers = ['detected_urls', 'undetected_urls', 'detected_downloaded_samples', 'undetected_downloaded_samples']
        if self.VirusData:
            df = pd.DataFrame(self.VirusData)
            df.to_csv(self.virus_filename, index=False)

            for col in df.columns:
                if col in headers:
                    df[col] = df[col].apply(lambda x: self.organinse(x))
            if not df.empty:
                df = df.drop(['_id'], axis="columns")
                df = df.head().to_html()
                self.html = df


    def send(self,choice = None,email_ids = None):
        if choice:
            pass
        else:
            choice = input("Send This Mail [Y|N]? OR E[x]it?").strip().lower()
        if choice == "y":
            if email_ids:
                email_ids = [i.strip() for i in email_ids]
            else:
                email_ids = input("Enter Single/Multiple Email ID Comma Separated : ").strip().split(',')
                email_ids = [i.strip() for i in email_ids]
            files = [self.abuse_filename, self.virus_filename]
            # print(f"Html : {self.html}")
            SendMail(htmldata=f"{self.html}", email_ids=email_ids, filepaths=files)
        else:
            pass

    def reset(self):
        self.today = datetime.datetime.today()
        self.year, self.month, self.day, self.hour, self.minute, self.second = self.today.year, self.today.month, self.today.day, self.today.hour, self.today.minute, self.today.second
        self.source = 'Single'
        self.ipaddress = []
        self.AbuseData = []
        self.VirusData = []
        self.html = None
        self.state = True
        self.abuse_filename = f"{self.common_path}\AbuseDatabase\AbuseIP_{self.year}{self.month}{self.day}_{self.hour}{self.minute}{self.second}.csv"
        self.virus_filename = f"{self.common_path}\VirusDatabase\VirusTotal_{self.year}{self.month}{self.day}_{self.hour}{self.minute}{self.second}.csv"

    def perform_main(self):
        self.check_limit(True)
        self.processIP()
        self.saveAbuse()
        self.createHtml()
        self.send()
        self.reset()
        self.check_limit(False)
        print(Fore.RED + f"Abuse Limit : {self.abuse_limit}\t\tVirus Limit : {self.virus_limit}")
