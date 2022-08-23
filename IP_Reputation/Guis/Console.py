import sys
sys.path.append(r"E:\OptiveProject")

from colorama import Fore
import traceback
from Guis.Perform import Processor


class CmdGui(Processor):

    def __init__(self):
        super().__init__()

    def showCommands(self):
        print(Fore.LIGHTRED_EX + '-'*100 +'\nWhat action would you like to take:\n',
              '[S]ingle IP Reputation?\n', '[M]ultiple IPs Reputation?\n', '[F]ile Of IPs?\n', 'E[x]it?\n')

    def get_action(self):
        text = "> "
        action = input(Fore.YELLOW + text + Fore.GREEN)
        return action.strip().lower()

    def singleIP(self):
        self.ipaddress = []
        while True:
            single_ip = input("Please Enter Valid IP Address OR E[x]it : ").lower()
            if single_ip == 'x' or single_ip == 'exit':
                break
            check = self.check_single_ip(single_ip)
            if check:
                self.ipaddress.append(check)
                break

    def multipleIPs(self):
        self.ipaddress = []
        self.source = "Multiple"
        while True:
            multi_ip = input("Please Enter Valid IP Address Comma Separated OR E[x]it : ").strip()
            if multi_ip != "":
                multi_ip = multi_ip.split(',')
                multi_ip = [ip.strip().lower() for ip in multi_ip]
                if multi_ip[0] == 'x' or multi_ip[0] == 'exit':
                    break
                for ip in multi_ip:
                    check = self.check_single_ip(ip)
                    if check:
                        self.ipaddress.append(check)
                break

    def fileIPs(self):
        pass

    def exit_app(self):
        print("Exiting.....")
        return False

    def main(self):
        with open("LOGO.txt","r") as f:
            logo = f.read()
            f.close()
        print(Fore.LIGHTGREEN_EX + logo)
        try:
            is_on = True

            while is_on:
                self.showCommands()
                action = self.get_action()
                if action == "s" or action == 'single':
                    self.singleIP()
                    self.perform_main()

                elif action == "m" or action == 'multiple':
                    self.multipleIPs()
                    self.perform_main()

                elif action == 'f' or action == 'file':
                    self.fileIPs()
                    self.perform_main()


                elif action == 'x' or action == 'exit':
                    is_on = self.exit_app()
                    break

                else:
                    print("You Chose Invalide Option Please Choose Given Option In [S|M|F]\n")



        except Exception as e:
            print(e)
            traceback.print_exc()


CmdGui().main()

