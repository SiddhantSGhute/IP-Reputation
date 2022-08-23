from configparser import ConfigParser

configParser = ConfigParser()
configParser.read("E:\OptiveProject\IP_Reputation\Scripts\Config.ini")

mongo_connection = configParser.get('MongoDB','connection')
abuse_key = configParser.get('Abuse','key')
virus_key = configParser.get('Virus','key')
mail_user = configParser.get('Mail','user')
mail_password = configParser.get('Mail','pass')
mail_smtp = configParser.get('Mail','smtp')
mail_default = configParser.get('Mail','default')


print(mail_password)