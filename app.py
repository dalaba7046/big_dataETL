from flask import Flask,jsonify,request
from flask_pymongo import PyMongo
from flask_restful import reqparse, abort, Api, Resource


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/591spider"
app.config['MONGODB_USERNAME']='rb'
app.config['MONGODB_PASSWORD'] = 'Pn123456'
mongo = PyMongo(app)
#xinbei = mongo.db.xin_bei
#taipei=mongo.db.tai_bei
#output = []
#output2=[]
#for s in xinbei.find():
#    output.append({'linkman' : s['linkman'], 'nick_name' : s['nick_name'],'house_attr':s['house_attr'],'kind_name':s['kind_name'],'house_phone':s['house_phone'],'house_gender':s['house_gender']})
#for t in taipei.find():
#    output2.append({'linkman' : t['linkman'], 'nick_name' : t['nick_name'],'house_attr':t['house_attr'],'kind_name':t['kind_name'],'house_phone':t['house_phone'],'house_gender':t['house_gender']})



#所有資料
@app.route("/api",methods=['GET'])
def get_all():
    xinbei = mongo.db.xin_bei
    taipei=mongo.db.tai_bei
    output = []
    for s in xinbei.find():
        output.append({'地區':'新北','刊登者' : s['linkman'], '身分' : s['nick_name'],'型態':s['house_attr'],'類別':s['kind_name'],'電話':s['house_phone'],'限定性別':s['house_gender']})
    for t in taipei.find():
        output.append({'地區':'台北','刊登者' : t['linkman'], '身分' : t['nick_name'],'型態':t['house_attr'],'類別':t['kind_name'],'電話':t['house_phone'],'限定性別':t['house_gender']})
    return jsonify({'result' : output})

#設計查詢【男生可承租】且【位於新北】的租屋物件
@app.route("/api/<house_gender>",methods=['GET'])
def search(house_gender): 
    xinbei = mongo.db.xin_bei
    res=xinbei.find({'house_gender': house_gender})
    output=[]
    for q in res:
        output.append({'刊登者' : q['linkman'], '身分' : q['nick_name'],'型態':q['house_attr'],'類別':q['kind_name'],'電話':q['house_phone'],'限定性別':q['house_gender']})
    return jsonify({'result':output})
#設計所有【非屋主自行刊登】的租屋物件
@app.route("/api/nick_name",methods=['GET'])
def nick_name():
   xinbei = mongo.db.xin_bei
   taipei = mongo.db.tai_bei
   
   output = []
   for elem in xinbei.find():
        if elem['nick_name'] !='屋主':
             output.append({'刊登者' : elem['linkman'], '身分' : elem['nick_name'],'型態':elem['house_attr'],'類別':elem['kind_name'],'電話':elem['house_phone'],'限定性別':elem['house_gender']})
   for elems in taipei.find():
        if elems['nick_name'] !='屋主':
             output.append({'刊登者' : elem['linkman'], '身分' : elem['nick_name'],'型態':elem['house_attr'],'類別':elem['kind_name'],'電話':elem['house_phone'],'限定性別':elem['house_gender']})

   return jsonify({'result':output})
#設計以【聯絡電話】查詢租屋物件
@app.route("/api/<phone>",methods=['GET'])
def phone(phone):
    xinbei = mongo.db.xin_bei
    taipei = mongo.db.tai_bei
    res=xinbei.find({'house_phone': phone})
    res2=taipei.find({'house_phone': phone})
    output = []
    for elem in res:
        output.append(elem)
    for elems in res2:
        output.append(elem)
    return jsonify({'result':output})

@app.route('/api/<area>/<nick_name>/<linkman>', methods=['GET'])
def search_all(area,nick_name,linkman):
    xinbei = mongo.db.xin_bei
    taipei = mongo.db.tai_bei
    output = []
    for s in xinbei.find():
            output.append({'地區':'新北','刊登者' : s['linkman'], '身分' : s['nick_name'],'型態':s['house_attr'],'類別':s['kind_name'],'電話':s['house_phone'],'限定性別':s['house_gender']})
    for t in taipei.find():
            output.append({'地區':'台北','刊登者' : t['linkman'], '身分' : t['nick_name'],'型態':t['house_attr'],'類別':t['kind_name'],'電話':t['house_phone'],'限定性別':t['house_gender']})
    res=[]
    for q in output:
        if q['地區'] == area and q['身分'] == nick_name and q['刊登者'] == linkman:
            res.append(q)
    return jsonify({'result':res})

app.run()
