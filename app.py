from flask import Flask,request,render_template,jsonify,session
import pandas as pd
import googlemaps
import time

app = Flask(
    __name__,
    static_folder='static',
    static_url_path='/'
)
app.secret_key="any string but secret"
apiKey='AIzaSyD16pHbSZFQnQzL2HtWdsai4QOzr0bWLGU'
gmaps = googlemaps.Client(key=apiKey)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/donate')
def link():
    return render_template('donate.html')

@app.route('/contact')
def link2():
    return render_template('contact.html')

@app.route('/flowchart')
def link3():
    return render_template('smithmap.html')


@app.route('/map')
def map():
    
    city = request.args.get('cities')
    keyword = request.args.get('keyword')
    radius = request.args.get('radius')
    #################################開始在GOOGLE-MAP中搜尋######################################
    ids = []
    #定義輸出結果項目
    myFields=['place_id','name','rating','user_ratings_total','formatted_address','international_phone_number','opening_hours','geometry']

    results = []
    geocode_result = gmaps.geocode(city)
    loc = geocode_result[0]['geometry']['location']
    query_result = gmaps.places_nearby(keyword=keyword,location=loc,radius=radius)
    results.extend(query_result['results'])
    while query_result.get('next_page_token'):
        time.sleep(2)
        query_result = gmaps.places_nearby(page_token=query_result['next_page_token'])
        results.extend(query_result['results'])    
    resultInfo = city+"為中心半徑"+str(radius)+"公尺內的"+keyword+"店家數量:"+str(len(results))+"間"
   
    if not results:
        s="搜尋範圍內無符合條件店家,請擴大搜尋範圍重新搜尋"
        return render_template('map.html', myResult=s, Resultlist = "")
    else:
        for place in results:
            ids.append(place['place_id'])
                
        stores_info = []
        # 去除重複id
        ids = list(set(ids)) 
        for id in ids:
            stores_info.append(gmaps.place(place_id=id, fields= myFields, language='zh-TW')['result'])

    #########################################對搜尋結果做處理############################################################
        #去除搜尋結果中店名有汽車玻璃的店家
        if (keyword == "玻璃"):
            stores_info2 =[]
            for i in range(0,len(results)):
                if (not("汽車" in stores_info[i]['name'])):
                    stores_info2.append(stores_info[i])
                    output = pd.DataFrame.from_dict(stores_info2)
        else:
            output = pd.DataFrame.from_dict(stores_info)
       
        #對'user_ratings_total'進行降冪排序
        output = output.sort_values(by='user_ratings_total', ascending=False)

    #####################################################################################################      
        #output.to_csv(keyword+'.csv',index=False, encoding='utf-8-sig')  
   
        d1 = output.to_dict('records')
  
        #print(d1)
        return render_template('map.html', myResult=resultInfo, Resultlist = d1, Source=city)