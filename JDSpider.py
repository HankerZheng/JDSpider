#coding=UTF-8
"""
Function: Get prices of specific items from JD database.
          Store the prices into Excel file
"""

import json
import re
import time
import urllib2
import logging
logging.basicConfig(level=logging.INFO,  
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',  
                    datefmt='%a, %d %b %Y %H:%M:%S',  
                    filename='./local.log',  
                    filemode='w')

from notifier import SendEMail
from excel_operations import ExcelOperation
from load_config import configs



_XLS_NAME = configs["data"]["excel_file"]   # name of EXCEL file that stores all the prices info
_ITEM_LIST_FILE = configs["data"]["items"]  # the file store item list_REFRESH_TIME = 1200        # 20 min per price
_URL_PREFIX = configs["data"]["url_prefix"]
_PDUID = configs["data"]["pduid"]

_WAIT_TIME = configs["time"]["exit"]            # wait 2s for the program to terminate
_REFRESH_TIME = configs["time"]["refresh"]

_RE_SKUID = re.compile('.+/(\d+).html')



def parse_items(input_file_name):
    """
    Parse item information from input_file_name.
    The format in input_file_name is
            *ITEM_NAME*; *ITEM_URL*
    Return 2 lists
    The first list is itemname_list
    The second list is skuid_list
    """
    with open(input_file_name) as f:
        itemname_list = [line.split('; ')[0] for line in f]
        f.seek(0)
        skuid_list = [_RE_SKUID.match(line.split('; ')[1]).group(1) for line in f]
    return [itemname_list, skuid_list]

def get_prices(skuids):
    """
    Append skuids after _URL_PREFIX and read the JSON
    Deserialize the JSON input and get the prices array.
    """
    # Create Query URL
    J_ID = ['J_'+skuid for skuid in skuids]
    append_id = ','.join(J_ID)
    request_url = _URL_PREFIX + 'pduid=' + _PDUID + '&skuids=' + append_id
    # Access to URL
    my_json = urllib2.urlopen(request_url).read()
    # Create return list
    p_prices = [float(item['p']) for item in json.loads(my_json)]
    return p_prices


class SpiderEngine(object):
    def __init__(self):
        # Get item_list
        info_list = parse_items(_ITEM_LIST_FILE)
        self.itemnames = info_list[0]  # the list of item_names
        self.skuids = info_list[1]     # the list of item_ids

    def update(self):
        info_list = parse_items(_ITEM_LIST_FILE)
        self.itemnames = info_list[0]  # the list of item_names
        self.skuids = info_list[1]     # the list of item_ids        

    def run(self):
        count = 0
        if not self.notifier_test():
            return
        while True:
            lt = time.localtime()
            # Start Collecting Data @ 2016-06-08 15:17
            logging.info("Start Collecting Data @ " + time.strftime('%Y-%m-%d %H:%M:%S', lt) )
            # Keyboard to terminate this program
            try:
                # get prices and warp them in name_price_dict
                prices = get_prices(self.skuids)
                name_price_dict = {name:price for (name, price) in zip(self.itemnames, prices)}
                # write data into excel file
                current_time = time.time()
                excel = ExcelOperation(_XLS_NAME, name_price_dict, current_time)
                changed_prices = excel()
                # price change notifier
                if changed_prices:
                    logging.info("Price change detected:" % changed_prices)
                    for item_name, content in changed_prices.iteritems():
                        logging.info("(%s)'s price"%item_name + 'has changed %s'% content)
                    self.notifier(changed_prices)

                count += 1
                # wait for another round
                logging.info("Finish the %d round of data collection" % count)
                time.sleep(_REFRESH_TIME)
            except KeyboardInterrupt:
                logging.info('Exit...')
                time.sleep(_WAIT_TIME)
                break
            self.update()

    def notifier_test(self):
        """
        Test the notifier function at the beginning of the program
        """
        email_test = SendEMail("initial test", configs["e-mail"], "test email")
        try:
            email_test()
        except ValueError, e:
            logging.error("Fail to pass the notifier test %s" % e)
            return False
        return True


    def notifier(self, changed_prices):
        res = []
        with open(_ITEM_LIST_FILE) as f:
            for line in f:
                if line.split('; ')[0] in changed_prices.keys():
                    res.append(line)

        logging.info("Start initialize E-mail...")
        res = [line.strip() + changed_prices[line.split('; ')[0]] for line in res]
        content = '    ' + '\n    '.join(res)
        email = SendEMail(content,  configs["e-mail"], configs["e-mail"]["subject"])
        try:
            email()
        except ValueError, e:
            logging.error("%s" % e)
        logging.info("E-mail has been sent successfully...")

if __name__ == '__main__':
    app = SpiderEngine()
    # app.notifier({"DUNU 2000 Gold":100.0, "HLA T-Shirt HNTBD2N301A":99.0})
    app.run()