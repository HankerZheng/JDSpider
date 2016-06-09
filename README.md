About
====
This is a simple spider that can help get prices sepecific items and store<br>
the them in an EXCEL file. If the price has been changed, then the program<br>
would automatically send an e-mail to notify the user.<br>

Requirement
====
:-Python2.7-:<br>
:-Openpyxl-: Install `$pip install openpyxl`<br>

Setup
====
* Create a new file named "item_list.txt" and fill it with the item you care about.
    * One item per line;
    * A simicolon(with a whitespace on its right side) sperates the item name on the right side and item website on the right side
    * One example is showed below:
```
DUNU 2000 Gold; http://item.jd.com/1118888.html
GoPro HERO4 Silver Standard; http://item.jd.com/1328967.html
Timberland Barstow Wedge; http://item.jd.hk/1952761316.html
```

* Create a new file named "config.txt" with infomation listed below:
```javascript
{
    "data": {
        "items": "item_list.txt",
        "excel_file": "prices.xlsx",
        "url_prefix": "http://p.3.cn/prices/mgets?",
        "pduid": "800XXXX08"
    },
    "time": {
        "refresh": 1200,
        "exit": 2
    },
    "e-mail": {
        "from_addr": "user@host.com",
        "host": "smtp.host.com",
        "port": 25,
        "password": "password",
        "to_addr": [
            "receiver@host.com"
            ],
        "subject": "Price changed detected from JDSpider",
        "timeout": 2
    }
}
```
>`items`: File that stores the item information<br>
`excel_file`: Name of excel which collects the data<br>
`pduid`: Value of the COOKIE named __jdu from www.jd.com<br>
<br>
`refresh`: Time interval of two access in second<br>
<br>
`from_addr`: E-mail address of the sender<br>
`host`: SMTP host of the sender<br>
`port`: SMTP port<br>
`password`: Password of sender's e-mail<br>
`to_addr`: E-mail address of the receiver<br>
`subject`: Subject of the E-mail to be sent<br>
`timeout`: Time wait for the server to response<br>

Run Code
====
After all above have been set, RUN `$python JDSpider.py`
