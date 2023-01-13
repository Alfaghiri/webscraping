from bs4 import BeautifulSoup
from flask import Flask
from flask_cors import CORS
import requests
app = Flask(__name__)
CORS(app)
event_url="https://www.meinbezirk.at/event/salzburg/list"
event_result = requests.get(event_url)
event_doc=BeautifulSoup(event_result.text,"html.parser")
event_titel=event_doc.select("div.column h3.event-card-headline a")
event_date=event_doc.select("div.column ul.event-card-date-location")
event_des=event_doc.select("div.column div.event-card-text p")
event_image=event_doc.select("div.column img.imagecontainer")
event_res=[]
event_images=[]
event_titels=[]
event_dates=[]
event_startdate=[]
event_enddate=[]
event_links=[]
event_details=[]
event_keys={}
event_index=0

for tag in event_titel:
    event_titels.append(tag.get_text().strip())
    event_links.append(tag['href'])
for date in event_date:
    x=date.select_one("li")
    event_dates.append(x.get_text().strip())
for img in event_image:
    event_images.append(img['data-src'])
for des in event_des:
    event_details.append(des.get_text().strip())
print(len(event_titels))
print(len(event_dates))
print(len(event_images))
print(len(event_details))
for i in range(len(event_titels)):
    event_keys['titel']=event_titels[i]
    event_keys['link']=event_links[i]
    event_keys['image']=event_images[i]
    event_keys['des']=event_details[i]
    event_keys['date']=event_dates[i]
    x=event_keys.copy()
    event_res.append(x)
@app.route('/')
def res():
    return event_res
if __name__== "__main__":
    app.run(debug=True)


