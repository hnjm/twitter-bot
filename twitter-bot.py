import time
import tweepy
import requests
from bs4 import BeautifulSoup

from bot_keys import *

yesterdaysDebt = 21485032298997

while True:

    # Current Time
    ct = time.strftime("%H:%M:%S",time.localtime())
    
    if (ct[3] == "0" and ct[4] == "0" and ct[6] == "0" and ct[7] == "0"):
        print("Checking...\t Time: " + ct)
        time.sleep(1)


    if (ct[0] == "1" and ct[1] == "2" and ct[3] == "3" and ct[4] == "0" and ct[6] == "0" and ct[7] == "0"):

        print("It\'s 12:30... Preparing Tweet...")
        
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        api = tweepy.API(auth)

        print("Getting Data...")
        
        f = requests.get('https://www.commodity.com/debt-clock/us/')
        soup = BeautifulSoup(f.text, 'lxml')

        allHtml = list(soup.children)[1]

        a = list(allHtml.children)[1]
        b = list(a.children)[0]
        c = list(b.children)[4]
        d = list(c.children)[0]
        e = list(d.children)[0]
        f = list(e.children)[0]
        g = list(f.children)[0]
        h = list(g.children)[0]
        i = list(h.children)[7]
        j = list(i.children)[3]

        # This is the debt scraped from the website
        debt = j.get_text()
        debtInt = int(debt.replace(',',''))

        difference = debtInt - yesterdaysDebt 
                
        percent = '%f' % (difference / debtInt)
        
        adjective = ""

        # Conditionally set the wording depending on whether or not
        # it's an increase or decrease
        if (difference >= 0):
            adjective = " An increase of "
        else:
            adjective = " A decrease of "


        # update_status is the API call that sends new tweets    
        api.update_status("Today\'s National Debt is $" + str(debt) + adjective + percent + "% from yesterday.")

        print("Tweet Sent!")

        yesterdaysDebt = debt;

        time.sleep(1)
