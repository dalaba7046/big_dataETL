from flask import Flask,jsonify,request
from flask_pymongo import PyMongo
from flask_restful import reqparse, abort, Api, Resource


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/591spider"
app.config['MONGODB_USERNAME']='rb'
app.config['MONGODB_PASSWORD'] = 'Pn123456'
mongo = PyMongo(app)
xinbei = mongo.db.xin_bei
taipei=mongo.db.tai_bei
output = []
output2=[]
for s in xinbei.find():
    output.append({'linkman' : s['linkman'], 'nick_name' : s['nick_name'],'house_attr':s['house_attr'],'kind_name':s['kind_name'],'house_phone':s['house_phone'],'house_gender':s['house_gender']})
for t in taipei.find():
    output2.append({'linkman' : s['linkman'], 'nick_name' : s['nick_name'],'house_attr':s['house_attr'],'kind_name':s['kind_name'],'house_phone':s['house_phone'],'house_gender':s['house_gender']})


#api=Api(app)
#parser = reqparse.RequestParser()
#
#parser.add_argument('id')
#parser.add_argument('linkman')
#parser.add_argument('house_attr')
#parser.add_argument('house_gender')
#parser.add_argument('house_phone')
#parser.add_argument('kind_name')
#parser.add_argument('nick_name')
#
#response = {"code": 200, "msg": "success"}
#
#class xinbei(Resource):
#    def db_init(self):
#        mongo = PyMongo(app)
#        xinbei = mongo.db.xin_bei
#        return mongo, xinbei
#    def get(self):
#        mongo, xinbei = self.db_init()
#        results = []
#        for elem in xinbei.find():
#            if elem['house_gender'] == house_gender:
#                results.append(elem)
#        data = {}
#        
#        data['source'] = '新北市'
#        data['house_gender'] = house_gender
#        data['Octorber'] = ten_count
#        data['November '] = eleven_count
#        response["data"] = data
#        return response


#所有資料
@app.route("/",methods=['GET'])
def get_all():
  return jsonify({'result' : output})
#設計查詢【男生可承租】且【位於新北】的租屋物件
@app.route("/xinbei",methods=['GET'])
def xinbei():
    if 'house_gender'  in request.args:
        house_gender = request.args['house_gender']
    else:
        return '沒找到'
    results = []
    for elem in output:
        if elem['house_gender'] == house_gender:
            results.append(elem)
    return jsonify(results)
#設計所有【非屋主自行刊登】的租屋物件
@app.route("/nick_name",methods=['GET'])
def nick_name():
    results = []
    for elem in output:
        if elem['nick_name'] !='屋主':
             results.append(elem)
    for elems in output2:
        if elems['nick_name'] !='屋主':
             results.append(elem)
    return jsonify(results)   
#設計以【聯絡電話】查詢租屋物件
@app.route("/phone",methods=['GET'])
def phone():
    results = []
    for elem in output:
        if elem['house_phone']  is not None:
             results.append(elem)
    for elems in output2:
        if elems['house_phone']  is not None:
             results.append(elem)
    return jsonify(results)



app.run()