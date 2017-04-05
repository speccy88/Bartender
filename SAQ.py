import urllib
from lxml import html
import requests
#from PIL import Image
import re
import io

class Bottle():
    def __init__(self, code_saq=None, url=None, to_file=False):
        self.code_saq = code_saq
        
        # Search with the SAQ code
        if code_saq:
            search_url = "http://www.saq.com/webapp/wcs/stores/servlet/SearchDisplay?storeId=20002&catalogId=50000&langId=-2&pageSize=20&beginIndex=0&searchCategory=Entete&searchTerm="
            page = requests.get(search_url+code_saq)
            self.tree = html.fromstring(page.text)
            
        # Raise an error if nothing to search
        if not code_saq or url:
            raise("WTF")
        
        # Write to file for easier XPATH inspection
        if to_file:
            with open("output.html", "w") as text_file:
                text_file.write(page.text.encode('utf8'))
        
        ### get some data about the bottle ###
        
        # get the name of the bottle
        self.nameUnicode = self.tree.xpath('//*[@id="content"]/div[2]/div/div[2]/div[2]/div[1]/div[1]/div[1]/h1')[0].text
        self.name = self.nameUnicode.encode('utf8')
        
        # get the alcohol percentage
        percent_raw = self.tree.xpath('//*[@id="details"]')[0].text_content().encode("utf8")
        percent_find = re.findall(r'([0-9]+)..%', percent_raw)
        self.percent = percent_find[len(percent_find)-1]+"%"
        
        # get the CUP and SAQ code
        code_raw = self.tree.xpath('//*[@id="content"]/div[2]/div/div[2]/div[2]/div[1]/div[1]/div[2]')[0].text_content().encode("utf8")
        codes = re.findall(r'[0-9]+', code_raw)
        self.code_cup = codes[1]
        self.code_saq = codes[0]

        # get the price
        price_raw = self.tree.xpath('//*[@id="content"]/div[2]/div/div[2]/div[2]/div[2]/div[1]/div[1]/p')[0].text_content().encode("utf8")
        price_find = re.search(r'([0-9]+),([0-9]+)', price_raw)
        self.price = price_find.group()+"$"
        
        # get the product picture
        image_url_raw = self.tree.xpath('//*[@id="content"]/div[2]/div/div[2]/div[2]/div[1]/div[2]')[0].text_content()
        self.image_url = "http:"+re.search(r'src="(//s7d9.*)" alt', image_url_raw).group(1)    
        self.image_file = io.StringIO(urllib.urlopen(self.image_url).read())
        #self.image = Image.open(image_file)
        #self.image.save("static/"self.code_saq+".png", "PNG")
        #self.image.show()
        
    def __str__(self):
        return "Bottle (CUP={} - SAQ={}) name: {} percent: {} price: {}".format(self.code_cup, self.code_saq, self.name, self.percent, self.price)

        
if __name__=="__main__": 
    code_list = ["00255091",
               "00268714",
               "00323972",
               "00117101",
               "00195370",
               "10757154"]          

    for code in code_list:
        print(Bottle(code))