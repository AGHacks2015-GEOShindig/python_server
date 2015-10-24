# encoding: UTF-8
from flask import Flask
from flask.ext.elasticsearch import FlaskElasticsearch
from flask.ext.cors import CORS
from flask import request
from flask import jsonify
from pprint import pprint



app = Flask(__name__)
CORS(app)

app.config['ELASTICSEARCH_HOST'] = "vps207097.ovh.net:9200"
app.config['DEBUG'] = True

es = FlaskElasticsearch(app)
es.init_app(app)

@app.route('/search/')
def search():
    distance = request.args.get('distance')
    city = request.args.get('city')

    print city
    print distance

    if not distance:
        distance = "5"
    if not city: 
        city = u'kraków'

    city_search = es.search(index="fb_events", body={"size":1, "query": {'match': {'city': city}}})
    pprint(city_search)
    city_cord = city_search['hits']['hits'][0]['_source']['place']['location']['geo_cord']
    pprint(city_search)
    city_cord = city_cord.split(',')
    print city_cord
    distance += "km"
    query = {
        "size":100, "query": {
            "filtered": {
                "query":  { "match": { "city": city }},
                "filter": { "geo_distance": { "distance": distance, "geo_cord": {"lat": city_cord[0],"lon": city_cord[1]}}}
            }
       }
    }
    res = es.search(index="fb_events", body=query)
    return jsonify(res['hits'])

@app.route('/mobile/')
def mobile():
    distance = request.args.get('distance')
    lat = request.args.get('lat')
    lon = request.args.get('lon')


    if not distance:
        distance = "50"
    if not lat: 
    	lat = `19.9609909`
    	lon = `50.0536804`

        

    #city_search = es.search(index="fb_events", body={"size":1, "query": {'match': {'city': city}}})
    #pprint(city_search)
    #city_cord = city_search['hits']['hits'][0]['_source']['place']['location']['geo_cord']
    #pprint(city_search)
    #city_cord = city_cord.split(',')
    #print city_cord
    distance += "km"
    query = {
        "size":100, "query": {
            "filtered": {
                "filter": { "geo_distance": { "distance": distance, "geo_cord": {"lat": lat,"lon": lon}}}
            }
       }
    }
    res = es.search(index="fb_events", body=query)
    return jsonify(res['hits'])




if __name__ == "__main__":
    app.run()