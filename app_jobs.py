import asyncio
import aiohttp
from bs4 import BeautifulSoup
from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
jobs_urls=[]
jobs_offset=17
for i in range(3):
    url="https://www.jobs.at/j?offset="+str(jobs_offset)+"&dateFrom=all&keyword=IT&location=Salzburg&radius=50&clearTerm=false&infiniteScroll=true"
    jobs_offset+=15
    jobs_urls.append(url)

####################################################################
jobs_res=[]
jobs_key={}
async def get_site_content(urls):
    for url in urls:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                jobs_titles=[]
                jobs_link=[]
                jobs_locs=[]
                jobs_company=[]
                jobs_details=[]
                jobs_images=[]
                text = await resp.read()
                jobs_doc=BeautifulSoup(text.decode('utf-8'), 'html.parser')
                jobs_title=jobs_doc.select("h2 a")
                jobs_comp=jobs_doc.select("a.c-job-company-link")
                jobs_loc=jobs_doc.select("a.js-locationLink")
                jobs_des=jobs_doc.select("p.c-job-teaser-text")
                jobs_img=jobs_doc.select("div.c-apply-box-company-logo img")
                for title in jobs_title:
                    jobs_titles.append(title.get_text().strip())
                    jobs_link.append(title["href"])
                for title in jobs_comp:
                    jobs_company.append(title.get_text().strip())
                for title in jobs_des:
                    jobs_details.append(title.get_text().strip())
                for title in jobs_loc:
                    jobs_locs.append(title.get_text().strip())
                for title in jobs_img:
                    jobs_images.append("https://www.jobs.at"+title['src'])
                for i in range(len(jobs_images)):
                    jobs_key['title']=jobs_titles[i]
                    jobs_key['image']=jobs_images[i]
                    jobs_key['comp']=jobs_company[i] 
                    jobs_key['link']=jobs_link[i] 
                    jobs_key['des']=jobs_details[i] 
                    x=jobs_key.copy()
                    jobs_res.append(x)    
####################################################################
loop = asyncio.get_event_loop()
loop.run_until_complete(get_site_content(jobs_urls))
loop.close()

@app.route('/')
def date():
    return jobs_res
if __name__== "__main__":
    app.run(debug=True)


