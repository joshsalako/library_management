import fakeredis
import json

def get_redis_client():
    return fakeredis.FakeStrictRedis()

redis_client = get_redis_client()

def publish_message(channel, message):
    redis_client.publish(channel, json.dumps(message))

def subscribe_to_channel(channel):
    pubsub = redis_client.pubsub()
    pubsub.subscribe(channel)
    return pubsub
