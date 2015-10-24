from flask import Flask
from flask.ext.elasticsearch import FlaskElasticsearch
from flask.ext.cors import CORS
from flask import request
from flask import jsonify



app = Flask(__name__)
CORS(app)

app.config['ELASTICSEARCH_HOST'] = "vps207097.ovh.net:9200"
app.config['DEBUG'] = True

es = FlaskElasticsearch(app)
es.init_app(app)

@app.route('/search/')
def search():
	city = request.args.get('city', '')
	distance = request.args.get('distance', '')

	# city_search = es.search(index="fb_events", body={"size":1, "query": {'match': {'city': 'wroclaw'}}})
	# city_cord = city_search['geo_cord']

	query = {
  "query": {
    "filtered": {
    "query":  { "match": { "city": "wroclaw" }},
    "filter": { "geo_distance": { "distance": "400km", "geo_cord": {"lat": 15.2333,"lon": 52.70}}}
    }
  }
}
	res = es.search(index="fb_events", body=query)
	print res
	return jsonify(**res)





if __name__ == "__main__":
    app.run()