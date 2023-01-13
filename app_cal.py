import asyncio
import aiohttp
import html5lib
from flask import Flask
from flask_cors import CORS
from bs4 import BeautifulSoup
app = Flask(__name__)
CORS(app)

async def get_site_content():
        async with aiohttp.ClientSession() as session:
            async with session.get("https://online.uni-salzburg.at/plus_online/pl/ui/$ctx;design=ca2;header=max/wbraum.editRaum?chksum=0&pMaskAction=R&pRaumNr=9834") as resp:
                text = await resp.read()
                cal_doc=BeautifulSoup(text.decode('utf-8'), 'html5lib')
                cal=cal_doc.select('span.Mask')
                for i in cal:
                    print(i)
                
loop = asyncio.get_event_loop()
sites_soup = loop.run_until_complete(get_site_content())
""" print(sites_soup) """
loop.close()

@app.route('/')
def res():
    return "1"
if __name__== "__main__":
    app.run(debug=True)