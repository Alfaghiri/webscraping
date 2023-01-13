import asyncio
import aiohttp
import html5lib
from flask import Flask
from flask_cors import CORS
from bs4 import BeautifulSoup
app = Flask(__name__)
CORS(app)
url_index=0
sale_urls =[]
sale_titels=[]
sale_utitels=[]
sale_images=[]
sale_links=[]
sale_key={}
sale_res=[]
for url in range(3):
    sale_urls.append("https://www.isic.at/de/verguenstigungen/?start="+str(url_index))
    url_index+=10
async def get_site_content():
    for url in sale_urls:  
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                text = await resp.read()
                sale_doc=BeautifulSoup(text.decode('utf-8'), 'html5lib')
                sale_titel=sale_doc.select("div#content h3")
                sale_utitel=sale_doc.select("div#content p")
                sale_image=sale_doc.select("div#content img")
                sale_link=sale_doc.select("a.more")
                for titel in sale_titel:
                    sale_titels.append(titel.get_text().strip())
                for utitel in sale_utitel:
                    sale_utitels.append(utitel.get_text().strip())
                for img in sale_image:
                    sale_images.append("https://www.isic.at"+img['data-src'])
                for link in sale_link:
                    sale_links.append("https://www.isic.at"+link['href'])
                
loop = asyncio.get_event_loop()
sites_soup = loop.run_until_complete(get_site_content())
""" print(sites_soup) """
loop.close()
for i in range(len(sale_links)):
    sale_key['titel']=sale_titels[i]
    sale_key['des']=sale_utitels[i]
    sale_key['image']=sale_images[i]
    sale_key['link']=sale_links[i]
    x=sale_key.copy()
    sale_res.append(x)
@app.route('/')
def res():
    return sale_res
if __name__== "__main__":
    app.run(debug=True)