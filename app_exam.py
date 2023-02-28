"""
@authors:
Abdul Wahhab Alfaghiri Al Anzi   01524445
Nouzad Mohammad                  00820679
"""
import asyncio
import aiohttp
from flask import Flask
from flask_cors import CORS
from bs4 import BeautifulSoup
import time
from datetime import datetime
app = Flask(__name__)
CORS(app)
now = datetime.today().strftime('%Y-%m-%d')
start=time.time()
exam_url1="https://online.uni-salzburg.at/plus_online/ee/rest/slc.xm.exd/exExamOffer?$filter=exExamDateFrom-gte="+now+"&$orderBy=exExamDate=ascnf&$skip=0&$top=100&orgId=20781"
exam_url="https://online.uni-salzburg.at/plus_online/ee/rest/slc.xm.exd/exExamOffer?$filter=exExamDateFrom-gte="+now+"&$orderBy=exExamDate=ascnf&$skip=0&$top=100&orgId=14078"
print(exam_url)
exams=[]
async def get_site_content(exam_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(exam_url) as resp:
            text = await resp.read()
            j=0
            z=0
            exam_titels=[]
            exam_rooms=[]
            exam_sems=[]
            exam_dates=[]
            exam_starts=[]
            exam_ends=[]
            exam_regs=[]
            exam_key={}
            exam_doc=BeautifulSoup(text.decode('utf-8'), 'xml')
            exam_titel=exam_doc.select("examOffers courseName value")
            exam_room=exam_doc.select("examOffers appointments displayName")
            exam_sem=exam_doc.select("examOffers courseSemesterShortName value")
            exam_date=exam_doc.select("examOffers examDate value")
            exam_start=exam_doc.select("examOffers examStart value")
            exam_end=exam_doc.select("examOffers examEnd value")
            exam_reg=exam_doc.select("examOffers deRegistrationEnd value")
            exam_check=exam_doc.select("examOffers")
            print(len(exam_start))
            for exam in exam_titel:
                exam_titels.append(exam.get_text().strip())
            for i in range(len(exam_check)):
               if(len(exam_check[i].select('appointments'))>0):
                  exam_rooms.append(exam_room[j].get_text().strip()) 
                  j+=1
               else:
                  exam_rooms.append('Ort noch nicht festgelegt')
            for i in range(len(exam_check)):
               if(len(exam_check[i].select('examEnd'))>0):
                  exam_ends.append(exam_end[z].get_text().strip()) 
                  z+=1
               else:
                  exam_ends.append('00:00:00')  
            for exam in exam_sem:
                exam_sems.append(exam.get_text().strip())
            for exam in exam_date:
                exam_dates.append(exam.get_text().strip())
            for exam in exam_start:
                exam_starts.append(exam.get_text().strip())
            for exam in exam_reg:
                exam_regs.append(exam.get_text().strip())
            for i in range(len(exam_rooms)):
                exam_key['titel']=exam_titels[i]
                exam_key['room']=exam_rooms[i]
                exam_key['sem']=exam_sems[i]
                exam_key['date']= get_date(exam_dates[i])
                exam_key['start']=exam_starts[i]
                exam_key['end']=exam_ends[i]
                exam_key['endreg']=get_regdate( exam_regs[i])
                x=exam_key.copy()
                exams.append(x)               
    return
def get_date(date):
    y=list(date.split("-"))
    return y[2]+"."+y[1]+"."+y[0]
def get_regdate(date):
    x=list(date.split("T"))
    y=get_date(x[0])
    z=x[1]
    return y +" um "+z
loop = asyncio.get_event_loop()
sites_soup = loop.run_until_complete(get_site_content(exam_url))
sites_soup = loop.run_until_complete(get_site_content(exam_url1))
loop.close()
####################################################################
end=time.time()
total_time=end-start
print(total_time,now)
@app.route('/')
def date():
    return exams
if __name__== "__main__":
    app.run(debug=True)


