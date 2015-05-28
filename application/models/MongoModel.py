from bson.objectid import ObjectId
from bson.json_util import loads
from application.errors import NoSuchFieldError, MissingRequiredFieldError, TypeCoercionError

class MongoModel:
    """Subclasses must have following class variables:
        * collection: pymongo collection reference
        * fields: list of fields on the document

        A field is represented by a dict:
        {
            'identifier': <key of field>,           # str
            'required': <required or not>,          # bool
            'type': <data type of field value>,     # str
            'default': *                            # optional
        }
    """

    def __init__(self, doc):
        """Constructor for MongoModel.
        Pass in dictionary of fields
        """
        for key, value in doc.iteritems():
            setattr(self, key, value)

        coercion = self.coerce_types()
        if coercion is not True:
            raise TypeCoercionError(coercion)

        missing_defaults = list(set(self.get_fields_with_defaults()) - set(doc.keys()))

        if missing_defaults:
            for default_key in missing_defaults:
                setattr(self, default_key, self.get_default_value(default_key))

    def update(self, doc):
        validation = self.validate_update(doc)
        if validation is True:
            for key, value in doc.iteritems():
                setattr(self, key, value)
        else:
            raise NoSuchFieldError(validation['fields'])

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
            if validation['invalid_cause'] is 'missing_required_fields':
                raise MissingRequiredFieldError(validation['fields'])

            elif validation['invalid_cause'] is 'no_such_fields':
                raise NoSuchFieldError(validation['fields'])


    @classmethod
    def destroy(cls, doc):
        collection.remove(doc)

    @classmethod
    def validate(cls, doc):
        missing_required_fields = list(set(cls.get_required_fields()) - set(doc.keys()))
        no_such_fields = list(set(doc.keys()) - set(cls.get_fields()))

        # check if all required fields are present
        if missing_required_fields:
            return {"invalid_cause": "missing_required_fields", "fields": missing_required_fields}
        elif no_such_fields:
            return {"invalid_cause": "no_such_fields", "fields": no_such_fields}
        else:
            print 'all good'
            return True

    def json_helper(self):
        return

    def validate_update(self, doc):
        no_such_fields = list(set(doc.keys()) - set(self.get_fields()))

        if no_such_fields:
            return {"invalid_cause": "no_such_fields", "fields": no_such_fields}
        else:
            print 'all good'
            return True


    @classmethod
    def get_required_fields(cls):
        return [field['identifier'] for field in cls.fields if 'required' in field and field['required'] and 'default' not in field]

    @classmethod
    def get_fields(cls):
        return [field['identifier'] for field in cls.fields]

    def get_fields_with_types(self):
        return [field['identifier'] for field in self.fields if 'type' in field]

    def get_field_type(self, field_id):
        for field in self.fields:
            if field['identifier'] is field_id and 'type' in field:
                return field['type']

    def get_fields_with_defaults(self):
        return [field['identifier'] for field in self.fields if 'default' in field and 'required' in field]

    def get_default_value(self, field_id):
        for field in self.fields:
            if field['identifier'] is field_id and 'default' in field:
                return field['default']

    def coerce_types(self):
        for field_id in self.get_fields_with_types():
            if hasattr(self, field_id):
                field_type = self.get_field_type(field_id)

                try:
                    field = {
                            dict: lambda field: loads(field),
                            str:  lambda field: str(field),
                            int:  lambda field: int(field)
                    }.get(field_type)(getattr(self, field_id))

                except (ValueError, TypeError) as e:
                    return {'error_type': type(e).__name__, 'field_id': field_id}

                setattr(self, field_id, field)

        return True

    def coerce_type(self, field_id):
        field = getattr(self, field_id)
        field_type = self.get_field_type(field_id)

        if field_type is dict:
            if type(field) is dict:
                return field
            else:
                return loads(field)
        elif field_type is str:
            if type(field) is str:
                return field
            else:
                return str(field)




