import pymongo

from . import interfaces


class MongoDB:
    def __init__(self, uri, dbname="article-store", colname="manifests"):
        self._client = pymongo.MongoClient(uri)
        self._dbname = dbname
        self._colname = colname

    def db(self):
        return self._client[self._dbname]

    def collection(self):
        return self.db()[self._colname]


class SessionFactory:
    def __init__(self, mongodb_client):
        self._mongodb_client = mongodb_client

    def __call__(self):
        return Session(self._mongodb_client.collection())


class Session:
    def __init__(self, collection):
        self._collection = collection

    @property
    def articles(self):
        return ArticleStore(self._collection)


class ArticleStore:
    def __init__(self, collection):
        self._collection = collection

    def add(self, article):
        data = article.manifest
        if not data.get("_id"):
            data["_id"] = article.doc_id()
        self._collection.insert_one(data)