from bson.objectid import ObjectId

# Subclasses must have class variable collection
class MongoModel:

    def __init__(self, doc):
        for key, value in doc.iteritems():
            setattr(self, key, value)

    @classmethod
    def query(cls, query=None):
        if query is None:
            docs = cls.collection.find()
            return [cls(doc) for doc in docs]

        else:
            if '_id' in query:
                query['_id'] = ObjectId(query['_id'])

            doc = cls.collection.find_one(query)
            model = cls(doc)
            return model

    @classmethod
    def create(cls, doc):
        mongo_id = cls.collection.insert(doc)
        return cls.query({'_id': ObjectId(mongo_id)})

    @classmethod
    def destroy(cls, doc):
        collection.remove(doc)


    def update(self):
        self.collection.update({'_id': self._id}, self.__dict__)
        return self
