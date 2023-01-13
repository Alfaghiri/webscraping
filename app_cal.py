from bs4 import BeautifulSoup
from flask import Flask
from flask_cors import CORS
import requests
from datetime import datetime, timedelta
now = datetime.today().strftime('%d.%m.%Y')
todayDate = datetime.today()
print('Today Date:',todayDate)
# Increment today's date with 1 week to get the next Monday
nextsun = todayDate- timedelta(days=todayDate.weekday()+1)
prevsun = todayDate+ timedelta(days=-todayDate.weekday()-1, weeks=1)
print(prevsun)
d=7
dates=[]
for x in range(3):
    y=nextsun+timedelta(days=d)
    z=prevsun-timedelta(days=d)
    d+=7
    dates.append(y.strftime('%d.%m.%Y'))
    dates.append(z.strftime('%d.%m.%Y'))
print(dates)
app = Flask(__name__)
CORS(app)


def get_cal(url):
        cal_titel=[]
        cal_res=[]
        cal_starts=[]
        cal_ends=[]
        cal_keys={}
        cal_details=[]
        cal_des=[]
        all_cal=[]
        cal_result= requests.get(url)
        cal_doc=BeautifulSoup(cal_result.content,features='lxml')
        cal_time=cal_doc.select("span.cocal-ev-desc")
        cal_title=cal_doc.select("span.cocal-ev-title")
        cal_start=cal_doc.find_all("div",attrs={"class":["cocal-ev-horiz-container","cocal-ev-container"]})
        for time in cal_time:
            cal_des.append(time.get_text())
        for cal in cal_start:
            x=cal['data-event']
            y=list(x.split(","))
            y_start=y[1][14:18]
            mon_start=y[1][12:14]
            d_start=y[1][10:12]
            h_start=y[1][18:20]
            min_start=y[1][20:22]
            star=y_start+"-"+mon_start+"-"+d_start+"T"+h_start+":"+min_start
            y_end=y[2][12:16]
            mon_end=y[2][10:12]
            d_end=y[2][8:10]
            h_end=y[2][16:18]
            min_end=y[2][18:20]
            end=y_end+"-"+mon_end+"-"+d_end+"T"+h_end+":"+min_end
            cal_starts.append(star)
            cal_ends.append(end)
        for title in cal_title:
            cal_titel.append(title.get_text().strip())
        for index in range(len(cal_starts)):
            cal_keys['title']=cal_titel[index]
            cal_keys['start']=cal_starts[index]
            cal_keys['end']=cal_ends[index]
            cal_keys['id']=cal_des[index]
            x=cal_keys.copy()
            cal_res.append(x)
        
        return cal_res
#####################################################################

def get_all(urls):
    cal=[]
    for i in urls:
        x=get_cal(i)
        for index in x:
            cal.append(index)
    return cal
def get_urls(resNr):
    urls=[]
    for i in dates:
        url="https://online.uni-salzburg.at/plus_online/pl/ui/$ctx;design=ca2;header=max/wbKalender.cbRessourceKalender/NC_2599?pResNr="+resNr+"&pSerie=E&pDatumEnde=&pEndeNach=&pFrequenz=&pWochentag=&pZeitVon=&pZeitBis=&pDirektZumBuchen=F&pDisplayMode=w&pDatum=+"+i+"&pEndeArt=&pShowAsList=F&pZoom=100&pNurStandardGrp="
        urls.append(url)
    return urls
t01=get_urls("12590")
t02=get_urls("12591")
t03=get_urls("12592")

urll="https://online.uni-salzburg.at/plus_online/pl/ui/$ctx;design=ca2;header=max/wbKalender.cbRessourceKalender/NC_2599?pResNr=12590&pSerie=E&pDatumEnde=&pEndeNach=&pFrequenz=&pWochentag=&pZeitVon=&pZeitBis=&pDirektZumBuchen=F&pDisplayMode=w&pDatum=11.12.2022&pEndeArt=&pShowAsList=F&pZoom=100&pNurStandardGrp="
@app.route('/t01')
def t01cal():
    return get_all(t01)
@app.route('/t02')
def t02cal():
    return get_all(t02)
@app.route('/t03')
def t03cal():
    return get_all(t03)

if __name__== "__main__":
    app.run(debug=True)


