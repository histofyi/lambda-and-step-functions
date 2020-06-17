import json

class s3Provider():
    def __init__(self, bucket, client):
        self.__bucket = bucket
        self.__client = client

    def get_bucket(self):
        return self.__bucket

    def persist(self, key, data):
        self.__client.put_object(Body=data, Bucket=self.__bucket, Key=key)

    def fetch(self, key):
        obj = self.__client.get_object(Bucket=self.__bucket, Key=key)
        return obj['Body'].read().decode('utf-8')
