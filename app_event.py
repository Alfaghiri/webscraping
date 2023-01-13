import asyncio
import aiohttp
import html5lib
from flask import Flask
from flask_cors import CORS
from bs4 import BeautifulSoup
import time
app = Flask(__name__)
CORS(app)
start=time.time()
event_url = 'https://www.salzburg-altstadt.at/de/veranstaltungskalender'
event_res=[]
event_images=[]
event_dates=[]
event_startdate=[]
event_enddate=[]
event_links=[]
event_details=[]
event_keys={}
event_desc=[]
async def get_links(link):
    async with aiohttp.ClientSession() as session:
                    async with session.get(link) as resp:
                        text1 = await resp.read()
                        event_docc=BeautifulSoup(text1.decode('utf-8'), 'html5lib')
                        tagdetails=event_docc.select_one("div.wysiwyg p")
                        for e in tagdetails.find_all('br'):
                            e.extract()
                        for tagdet in tagdetails:
                            event_details.append(tagdet.get_text())
async def get_site_content():
    async with aiohttp.ClientSession() as session:
        async with session.get(event_url) as resp:
            text = await resp.read()
            event_doc=BeautifulSoup(text.decode('utf-8'), 'html5lib')
            event_titel=event_doc.select("div.event-teaser__title a")
            event_date=event_doc.select("div.event-teaser__date time")
            event_image=event_doc.select("picture")
            for img in event_image:
                event_images.append("https://www.salzburg-altstadt.at"+img['data-default-src'])
            del event_images[0]
            del event_images[0]
            for dat in event_date:
                event_dates.append(dat.get_text().strip())
            for idx, ele in enumerate(event_dates):
                 event_dates[idx] = ele.replace('\n', ' ')
            event_startdate=event_dates[::2]
            event_enddate=event_dates[1::2]
            print(event_startdate)
            for tag in event_titel:
                event_links.append("https://www.salzburg-altstadt.at"+tag['href'])
            for link in event_links:
                await get_links(link)
            event_index=0
            substring = '\n'
            new_list = [item for item in event_details if substring not in item]            
            for tag in event_titel:
                event_keys['name']=tag.get_text().strip()
                event_keys['link']=("https://www.salzburg-altstadt.at"+tag['href'])
                event_keys['image']=event_images[event_index]
                for i in range(len(event_startdate)):
                    event_keys['startdate']=event_startdate[i]
                    event_keys['enddate']=event_enddate[i]
                    
                event_keys['desc']=new_list[event_index]
                event_index+=1
                x=event_keys.copy()
                event_res.append(x)
    return event_res
loop = asyncio.get_event_loop()
sites_soup = loop.run_until_complete(get_site_content())
""" print(sites_soup) """
loop.close()
end=time.time()
total_time=end-start
print(total_time)
@app.route('/')
def res():
    return event_res
if __name__== "__main__":
    app.run(debug=True)