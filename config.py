import redis
# import pymongo
# import elasticsearch

username = "admin"
password = "password"

redis_con = redis.Redis(host='localhost', port=6379, db=0)

# mongo_con = pymongo.MongoClient().adminka
# elastic_con = elasticsearch.Elasticsearch()
