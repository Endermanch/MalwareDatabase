# росия🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢🤢
import sys
import re 
import urllib.request
import urllib.error
import urllib.parse
import random 
import hashlib 
import requests 
import os
import argparse
import pyvirtualdisplay
from selenium import webdriver
import datetime


timestamp_now = datetime.datetime.now().strftime('%Y-%m-%d')

print("""\n
# Daily Dose of Malware (DDoM)
#
# Original author: https://github.com/notnop
# Rewritten by Enderman and Matt in Python 3!
#
# %%%%&&&&..............%%%/       Malware is art! 
# %%%%&&&&.........&&&..%%%%%      Don't let it become a filthy criminal's tool!
# %%%%&&&&.........&&&..%%%%%%%
# %%%%&&&&.........&&&..%%%%%%%    https://malwarewatch.org
# %%%%&&&&.........,,,..%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
# %%%%  _________________ .%%%%
# %%%%  _________________ .%%%%
# %%%%  _________________ .%%%%
# %%%%  _________________ .%%%%
# %%%%  _________________ .%%%%
# %%%%  _________________ .%%%%
# %&&%                    ,%&&%
# %&&%%%%%%%%%%%%%%%%%%%%%%%&&%
# %&&%%%%%%%%%%%%%%%%%%%%%%%&&%\n""")
# Flags
parser = argparse.ArgumentParser(description='DDoM v2.0')
parser.add_argument("-c", "--count", nargs=1, type=int, help="Defines the number of malware samples you want, up to 5000. If the argument is omitted, sets to 100 by default.",
                required=False, default=argparse.SUPPRESS, metavar="SAMPLES")
parser.add_argument("-r", "--rename", help="[Not recommended] Makes the samples executable. Don't use this unless you're confident you won't execute them on your host.",
                required=False, action="store_const", const=True)              
parser.add_argument("-y", "--yes-to-all", help="Skips the confirmation prompt.",
                required=False, action="store_const", const=True)

def confirmation(question, default="no"):    
    valid = {"yes": True, "y": True, "ye": True,
                "no": False, "n": False} 
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    validInputEntered = False
    while not validInputEntered:
        data = input("{}{}".format(question, prompt)).lower()
        if data in valid:
            validInputEntered = True
            return valid[data]
        if data == "":
            validInputEntered = True
            return default



args = parser.parse_args()
print(args)
if not "count" in args:
    print("[*]  Argument was omitted - going with 100 samples by default")
    scount = 100
else:
    scount = args.count[0]

# Global variables

final_list = []  # Malware address collector
headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'
} 

print("""\nYou'll get latest {} samples from:
\t# http://malc0de.com
\t# http://vxvault.net
\t# http://tracker.h3x.eu
""".format(scount))

confirmed = confirmation("Confirm and start downloading {} samples?".format(scount), "no")
if not confirmed:
    sys.exit(0)

print("\nSearching...")

# Malc0de
def malc0de(samples):
    global final_list

    url_list = []

    if samples <= 50:
        pages = 1
    else:
        pages = (samples // 50) + 1

    # Browsing pages
    for i in range(0, pages):
        address = "https://malc0de.com/database/?&page=" + str(i)

        try:
            #req = requests.get(address, headers=headers)
            #con = urllib.request.urlopen(req, timeout=60).read()
            req = requests.get(address, headers=headers)
            con = req.content.decode("utf-8")
            b = re.findall("<td>[\d]{4}-[\d]{2}-[\d]{2}<\/td>\n.+\n", con)
            if b:
                for i in b:
                    date = re.search("<td>([\d]{4}-[\d]{2}-[\d]{2})<\/td>", i)
                    malware = re.search("\t<td>(.+)<\/td>", i)
                    if date and malware:
                        malware = re.sub("<br\/>", "", malware.group(1))
                        url_list.append(malware)
        except Exception as e:
            print("Malc0de: " + str(e))

    final_list += url_list

    print("[*]  Malc0de - Done ", len(url_list))
	
# VXVault
def vxvault(nr_samples):
    global final_list

    url_list = []
    address = "http://vxvault.net/ViriList.php?s=0&m=" + str(nr_samples)

    try:
        #req = urllib.request.Request(address, None, headers)
        #con_page = urllib.request.urlopen(req).read()
        req = requests.get(address, headers=headers)
        con_page = req.content.decode("utf-8")
        # Find all malware addresses
        page = con_page.split("\r")
        for i in page:
            match = re.search(
                "href='ViriFiche\.php\?ID=[\d]+'>(.+)</a></TD>", i)
            if match:
                temp_mal_address = match.group(1)
                if not re.search("[\d]{1,2}-[\d]{1,2}", temp_mal_address):

                    # Add malware addresses
                    url_list.append(temp_mal_address)

        final_list += url_list

    except Exception as e:
        #print("vxvault: " + str(e))
        raise e

    print("[*]  VXVault - Done ", len(url_list))

def h3x_get(nr_samples):
    lst = []

    address = "http://tracker.h3x.eu/"
    req = urllib.request.Request(address, None, headers)
    con_page = urllib.request.urlopen(req).readlines()

    # Print con_page

    for linie in con_page:
        address = re.findall("href='/site/([A-Za-z0-9%\._-]+)", linie.decode("utf-8"))
        lst += address
        if len(lst) >= nr_samples:
            return lst
    return lst


def h3x_clean(x=1000):
    global final_list
    list = h3x_get(x)
    new_list = []

    # Cleaning
    for i in list:
        i = re.sub("%3A", ":", i)
        i = re.sub("%2F", "/", i)
        new_list.append(i)

    final_list += new_list

    print("[*]  tracker.h3x - Done ", len(new_list))


def google(export_bool=False, output_bool=False):
    
    dorks = {"Pony": ["intitle:Authorization inurl:panel*/admin.php intext:Authorization. Sign in.",
                      "intitle:Authorization inurl:panel*/*admin.php",
                      "intitle:Authorization inurl:*admin.php Authorization. User Password Save password. Login. TF."],
             "WannaCry": "intitle:\"index of\" \"@Please_Read_Me@.txt",
             "Stealer": "intitle:\"(c) Bilal Ghouri\"",
             "LokiBot": "inurl:PvqDq929BSx_A_D_M1n_a.php intitle:Auth",
             "1ms0rry": "intitle:1ms0rry MINERPANEL",
             "SpyEye": "intitle:FRMCP intext:Please, enter password"}

    

    info = {}
    links_list = []

    directory = "google" + timestamp_now
    # now Firefox will run in a virtual display.
    # you will not see the browser.
    print("[*]  Google - Starting Firefox...")
    print("[*]  Google - NOTE: Do not control Firefox while it is running!")
    browser = webdriver.Firefox()
    for i in dorks.keys():  # for every dork in dictionary
        if i == "Pony":  # for Pony is more than one dork
            for j in dorks[i]:
                browser.get('http://www.google.com/search?q=' + j + "&t=h_&ia=web")
                links = browser.find_elements_by_xpath("//h3//a[@href]")
                for elem in links:
                    link = elem.get_attribute("href")
                    links_list.append(link)
            info.update({i: links_list})
            links_list = []

        else:
            browser.get('http://www.google.com/search?q=' + dorks[i] + "&t=h_&ia=web")
            links = browser.find_elements_by_xpath("//h3//a[@href]")
            for elem in links:
                link = elem.get_attribute("href")
                links_list.append(link)

            info.update({i: links_list})
            links_list = []

    for i in info:
        print("-----------------------------")
        print(i)
        for j in info[i]:
            print(j)
        print("-----------------------------")

    browser.quit()

# Collect samples address:
malc0de(scount)
vxvault(scount)
h3x_clean(scount)
try:
    google()
except Exception as e:
    print(str(e))


final_list = list(set(final_list))
print("\nUnique addresses: ", len(final_list))

print("\nDownloading...")


# Generate random string
charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"


def get_random_word(a):
    word = ''
    for i in range(a):
        word += random.choice(charset)
    return word


# MD5 file
def md5Checksum(filePath):
    fh = open(filePath, 'rb')
    m = hashlib.md5()
    while True:
        data = fh.read(8192)
        if not data:
            break
        m.update(data)
    return m.hexdigest()


def download_file(address, dldagent={'User-Agent': "Chromium"},
                  destination_folder=os.getcwd() + "\\Samples\\",
                  logs="error.log"):

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Filename
    filename = destination_folder + str(get_random_word(8)) + '.exe'

    # Try to download sample
    try:

        # Check if URL start with "http://
        if address[:7] != "http://":
            address = "http://" + address

        # Construct URL and set timeout
        req = urllib.request.Request(address, None, dldagent)
        u = urllib.request.urlopen(req, timeout=4).read()  # timeout 5 seconds

        # Write to file
        f = open(filename, 'wb')
        f.write(u)
        f.close()

        # Write information to the log file
        with open(destination_folder + logs, "a") as handle:
            md5hash = md5Checksum(filename)
            handle.write(md5hash + "\t" + filename + "\t" + address + "\n")
            handle.close

        print("[*]  Downloaded: " + filename)

    except Exception as e:
        with open(destination_folder + logs, "a") as handle:
            handle.write("Error: " + address + "\t" + str(e) + "\n")
            handle.close()
        pass


for mal in final_list:
    download_file(mal)