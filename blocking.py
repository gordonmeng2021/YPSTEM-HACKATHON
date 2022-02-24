import time
from datetime import datetime as dt
import PyQt5  
#Hostpath
hostsPath = r"C:\Windows\System32\drivers\etc\hosts"
redirect = "127.0.0.1"

#blocked websites
website_list = []

#Block website

def block(website,start_time,end_time):
    website_list.append(website)

    while True:
        if dt(dt.now().year, dt.now().month, dt.now().day, start_time) < dt(dt.now().year, dt.now().month, dt.now().day, end_time):
            with open(hostsPath, 'r+') as file:
                content = file.read()
                for site in website_list:
                    if site in content:
                        pass
                    else:
                        file.write(redirect + " " + site + "\n")
            
            print("Successfuly blocked! Focus!")
            break
        else:

            with open(hostsPath, 'r+') as file:
                content = file.readlines()
                file.seek(0)

                for line in content:     

                    if not any(website in line for website in website_list):
                        file.write(line)  
                
                file.truncate()
                print("Unlocked")
                break




def unblock():
    with open(hostsPath, 'r+') as file:
        lines = file.readlines()

        while len(lines) > 21:
            file.truncate()
            print("Unlocked")
            break
            
def unblock_1():
    with open(hostsPath, 'r+') as file:
                content = file.readlines()
                file.seek(150)
                file.truncate()
               
                print("Unlocked")
               
unblock_1()






