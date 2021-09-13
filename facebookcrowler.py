import random
import csv
import http.cookiejar
from os import link
import urllib.request
import requests
import bs4
import time

print("*****************************************Welcome to facebook crawler*************************************************")
print("*****************************************made for educational purpos*************************************************")
print("**************************Consider using static ip get one from your isp if not having*******************************")
print("********Delay - 10 sec to fetch data to each friend and user not having that data public will show as NULL***********")

def informationwriter(username, datafile):
    try:
        with open('facebookfriends.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([f"{username}", f"{datafile[0]}", f"{datafile[1]}",
                            f"{datafile[2]}", f"{datafile[3]}", f"{datafile[4]}"])
    except Exception as e:
        # print(e)
        print("Account may be deactivated")


def datacreator(datalist, soup):
    try:
        datalist.append(soup.find('div', {'id': 'work'}).text)
    except Exception as e:
        # print(e)
        datalist.append("NULL")
    try:
        datalist.append(soup.find('div', {'id': 'contact-info'}).text)
    except Exception as e:
        # print(e)
        datalist.append("NULL")
    try:
        datalist.append(soup.find('div', {'id': 'living'}).text)
    except Exception as e:
        # print(e)
        datalist.append("NULL")
    try:
        datalist.append(soup.find('div', {'id': 'education'}).text)
    except Exception as e:
        # print(e)
        datalist.append("NULL")
    try:
        datalist.append(soup.find('div', {'id': 'basic-info'}).text)
    except Exception as e:
        # print(e)
        datalist.append("NULL")
    return datalist

def delay():
    n = random.randint(7,12)
    return n


# cookies creator after login it will act as same browser till the program exits
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
urllib.request.install_opener(opener)
authentication_url = "https://m.facebook.com/login.php"
print('Please login opensource code password will be sent only to facebook server')
email = input("Please enter email id: ")
password = input("Please enter password: ")

payload = {

    'email': email,
    'pass': password
}


# data encoding to protect and read
data = urllib.parse.urlencode(payload).encode('utf-8')
req = urllib.request.Request(authentication_url, data)
resp = urllib.request.urlopen(req)
contents = resp.read()
totalfriends = int(input("Enter total number of friends"))
friends = totalfriends/10
n=0
while n<friends+2:
    url = f'https://mbasic.facebook.com/friends/center/friends/?ppk={n}'
    data = requests.get(url, cookies=cj)
    soup = bs4.BeautifulSoup(data.text, 'html.parser')
    z = 1
    for links in soup.find_all('a'):
        link = links.get("href")
        if z > 12 and z < 23:
            username = links.get_text()
            url = f"https://mbasic.facebook.com{link}"
            # print(url)
            data = requests.get(url, cookies=cj)
            soup = bs4.BeautifulSoup(data.text, 'html.parser')
            y = 1
            for links in soup.find_all('a'):
                link = links.get("href")
                url = f"https://mbasic.facebook.com{link}"
                if y == 3:
                    profileabout = f'{url}/about'
                    data = requests.get(profileabout, cookies=cj)
                    soup = bs4.BeautifulSoup(data.text, 'html.parser')
                    datalist = []
                    freshdata = datacreator(datalist, soup)
                    informationwriter(username, freshdata)
                    print('Done')
                y += 1
            d=delay()
            print(f'Delay {d} Sec')
            time.sleep(d)
        z += 1
    n+=1
    print('Delay 3 Sec')
    time.sleep(3)