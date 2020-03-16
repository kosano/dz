from flask import Flask
from flask import request
from flask import render_template
from flask import flash
from flask import Response
import es
from flask_cors import *


app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
CORS(app, supports_credentials=True)

## 格式化搜索内容
def gsh(data):
    content = {}
    for k, v in data.items():
        if k == 'segmentAddr': content['segmentAddr(分词结果)'] = v; continue
        if k == 'formattedText': content['formattedText(标准化)'] = v; continue
        if k == 'structText':
            stext = ""
            for k2, v2 in v.items():
                stext += k2+'='+v2+', '
            content['structText(结构化)'] = stext[:-2]; continue
        if k == 'offlineLocation': content['offlineLocation(离线经纬度)'] = v; continue
        if k == 'offlineLocationLevel': content['offlineLocationLevel'] = v; continue
        if k == 'poiPredict': content['poiPredict(poi预测)'] = v; continue
        if k == 'poiCategory': content['poiCategory(poi分类)'] = v; continue
        if k == 'zipCode': content['zipCode(邮编)'] = v; continue
        if k == 'unifyPoiList': content['unifyPoiList'] = v; continue
        if k == 'poiCenter': content['poiCenter'] = v; continue
        if k == 'wgs84Location': content['wgs84Location'] = v; continue

    return content



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        ## 如果是 GET 请求就定位默认的经纬度
        return render_template('map3.html', context={'wgs84Location': '113.27,23.13'})
    else:
        poi = request.form.get('poi')
        if len(poi) < 1:
            flash('请输入你要搜索的POI！')
            return render_template('map3.html', context={'wgs84Location': '113.27,23.13'})
        adr = es.search(poi)
        data = adr['hits']['hits'][0]['_source']
        fc = request.form.get('fc')
        if fc == '1':
            data['segmentAddr'] = poi
        yc = request.form.get('yc')
        jgh = request.form.get('jgh')
        if len(jgh) < 1:
            del data['structText']
        jwd = request.form.get('jwd')
        bzh = request.form.get('bzh')
        gy = request.form.get('gy')
        fl = request.form.get('fl')
        zx = request.form.get('zx')
        yb = request.form.get('yb')
        ## 把从 es 服务器里搜索到的poi数据格式化
        context = gsh(data)
        return render_template('map3.html', context=context)



## 地图瓦片API 
@app.route("/tiles/<int:z>/<int:y>/<int:x>.png")
def getTiles(z, y, x):
    # return str(x)+"_"+str(y)+"_"+str(z)
    imgPath = "./static/{}/{}/{}.png".format(z, y, x)
    resp = None
    print(imgPath)
    with open(imgPath, 'rb') as f:
        img = f.read()
        resp = Response(img, mimetype="image/png")
        print(resp)
    return resp
 

 ## 经纬度转换格式
@app.route('/marker/<locations>')
def marker(locations):
    location = {}
    location['lat'] = locations.split(',')[0]
    location['lon'] = locations.split(',')[1]
    return render_template('map2.html', location=location)




if __name__ == '__main__':
    app.run('0.0.0.0', port=8080)