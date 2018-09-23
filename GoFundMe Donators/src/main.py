"""Export GoFundMe campaign donators to CSV

# take campaign id from gofundme URL
$ campaign_id=seculartalk
$ python3 main.py $campaign_id
"""
import csv
import math
import sys
from urllib.parse import urljoin

import requests
from lxml import html


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
    return counter[0].text_content().strip().replace('Viewing ', '').replace(' Donations', '').split(' of ')[1]


def getPage(url):
    return requests.get(url).text


def getShowMoreDoc(url_id, num):
    url = "https://www.gofundme.com/mvc.php?route=donate/pagingDonationsFoundation&url={}&idx={}&type=recent"
    return html.fromstring(getPage(url.format(url_id, num)))


def floorNearestTen(num):
    return int(math.floor(num / 10.0)) * 10


def export_to_csv(csv_writer, supporters):
    for x in supporters:
        supporter = Supporter(x)
        name = supporter.getSupporterName()
        time = supporter.getSupporterTime()
        amount = supporter.getSupporterAmount()
        csv_writer.writerow((time, name, amount))


def main(url_id):
    base_url = urljoin('https://www.gofundme.com/', url_id)
    print(url_id)

    page = getPage(base_url)
    doc = html.fromstring(page)
    supporters_list = doc.cssselect('div .supporters-list')
    total = int(getTotalDonations(doc))
    print("This campaign received a total of {} donations so far".format(total))

    supporters = supporters_list[1].cssselect('.supporter-info')

    writer = csv.writer(sys.stdout)
    export_to_csv(writer, supporters)
    cur = 10
    while cur <= (floorNearestTen(total)):
        next_doc = getShowMoreDoc(url_id, cur)
        local_list = next_doc.cssselect('div .supporters-list')
        export_to_csv(writer, local_list[0].cssselect('.supporter-info'))
        cur = cur + 10


if __name__ == '__main__':
    main(sys.argv[1])
