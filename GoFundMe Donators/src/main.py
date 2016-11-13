import os.path
from urllib.parse import urljoin
from lxml import html
import requests, math

def getText(element):
    return element.get('text')

class Supporter():
    def __init__(self, element):
        self.element = element
    def getSupporterName(self):
        info = self.element.cssselect('.supporter-info .row .column .supporter-name')
        return info[0].text
    def getSupporterTime(self):
        info = self.element.cssselect('.supporter-info .row .column .supporter-time')
        return info[0].text
    def getSupporterAmount(self):
        info = self.element.cssselect('.supporter-info .row .column .supporter-amount')
        return info[0].text

def getTotalDonations(doc):
    counter = doc.cssselect('.donations-control-footer .mb')
    return counter[0].text.strip().replace('Viewing ', '').replace(' Donations', '').split(' of ')[1]

def getPage(url):
    return requests.get(url).text

def getShowMoreDoc(url_id, num):
    return html.fromstring(getPage("https://www.gofundme.com/mvc.php?route=donate/pagingDonationsFoundation&url=" + url_id + "&idx=" + str(num) + "&type=recent"))

def floorNearestTen(num):
    return int(math.floor(num / 10.0)) * 10

# Change the base_url to change the campaign being targeted
base_url = 'https://www.gofundme.com/seculartalk'
url_id = base_url.replace('https://', '').replace('http://', '').replace('www.', '').replace('gofundme.com/', '').split('/')[0];
print(url_id)
page = getPage(base_url)
doc = html.fromstring(page)
supporters_list = doc.cssselect('div .supporters-list')
print("This campaign received a total of " + getTotalDonations(doc) + " donations so far")

total = int(getTotalDonations(doc))

cur = 10

supporters = supporters_list[0].cssselect('.supporter-info')
    
while cur <= (floorNearestTen(total)):
    nextDoc = getShowMoreDoc(url_id, cur);

    local_list = nextDoc.cssselect('div .supporters-list')
    
    for x in local_list[0].cssselect('.supporter-info'):
        supporter = Supporter(x)
        name = supporter.getSupporterName()
        time = supporter.getSupporterTime()
        amount = supporter.getSupporterAmount()
        print(name + " donated " + amount + " " + time)
        
    cur=cur+10

# Deprecated in favor of a system that prints results as they are gathered 
'''
for e in supporters:
    supporter = Supporter(e)
    name = supporter.getSupporterName()
    time = supporter.getSupporterTime()
    amount = supporter.getSupporterAmount()
    print(name + " donated " + amount + " " + time)
    '''












