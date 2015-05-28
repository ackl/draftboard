from bson.objectid import ObjectId

# Subclasses must have class variable collection
class MongoModel:

    def __init__(self, doc):
        for key, value in doc.iteritems():
            setattr(self, key, value)

        missing_defaults = list(set(self.get_fields_with_defaults()) - set(doc.keys()))

        if missing_defaults:
            for default_key in missing_defaults:
                setattr(self, default_key, self.get_default_value(default_key))

    def get_fields_with_defaults(self):
        return [field['identifier'] for field in self.fields if 'default' in field]

    def get_default_value(self, field_id):
        for field in self.fields:
            if field['identifier'] is field_id and 'default' in field:
                return field['default']

    def update(self, doc):
        validation = self.validate_update(doc)
        if validation is True:
            for key, value in doc.iteritems():
                setattr(self, key, value)
        else:
            raise InsertError(validation['fields'])

        self.collection.update({'_id': self._id}, self.__dict__)
        return self

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
        validation = cls.validate(doc)
        if validation is True:
            print 'ok'
            mongo_id = cls.collection.insert(doc)
            return cls.query({'_id': ObjectId(mongo_id)})
        else:
            print 'not ok'
            if validation['invalid_because'] is 'missing_required_fields':
                raise MissingRequiredFieldsError(validation['fields'])

            elif validation['invalid_because'] is 'no_such_fields':
                raise InsertError(validation['fields'])


    @classmethod
    def destroy(cls, doc):
        collection.remove(doc)

    @classmethod
    def get_required_fields(cls):
        return [field['identifier'] for field in cls.fields if 'required' in field and field['required'] and 'default' not in field]

    @classmethod
    def get_fields(cls):
        return [field['identifier'] for field in cls.fields]

    @classmethod
    def validate(cls, doc):
        missing_required_fields = list(set(cls.get_required_fields()) - set(doc.keys()))
        no_such_fields = list(set(doc.keys()) - set(cls.get_fields()))

        #check if all required fields are present
        if missing_required_fields:
            return {"invalid_because": "missing_required_fields", "fields": missing_required_fields}
        elif no_such_fields:
            return {"invalid_because": "no_such_fields", "fields": no_such_fields}
        else:
            print 'all good'
            return True

    def validate_update(self, doc):
        no_such_fields = list(set(doc.keys()) - set(self.get_fields()))

        if no_such_fields:
            return {"invalid_because": "no_such_fields", "fields": no_such_fields}
        else:
            print 'all good'
            return True



class MongoModelError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

class InsertError(MongoModelError):
    def __init__(self, fields):
        self.message = 'The following fields could not be found on the model, but were in the call to the method: {0}'.format(', '.join(fields))

class MissingRequiredFieldsError(MongoModelError):
    def __init__(self, fields):
        self.message = 'The following fields are required by the model and have no default value, but were not in the call to the method: {0}'.format(', '.join(fields))
