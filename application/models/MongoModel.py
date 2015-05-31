from bson.objectid import ObjectId
from bson.json_util import loads
from application.errors import NoSuchFieldError, MissingRequiredFieldError, TypeCoercionError, InvalidFieldValueError

class MongoModel(object):
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

        Field values of a derived class may have extra
        validation performed by implementing a
        validate_extra method.
    """

    def __init__(self, doc):
        """Constructor for MongoModel.
        Pass in dictionary where keys are fields
        identifiers and values are field values.
        """
        for key, value in doc.iteritems():
            setattr(self, key, value)

        self._id = str(self._id)

        coercion = self.coerce_types()
        if coercion is not True:
            raise TypeCoercionError(coercion)

        missing_defaults = list(set(self.get_fields_with_defaults()) - set(doc.keys()))

        if missing_defaults:
            for default_key in missing_defaults:
                setattr(self, default_key, self.get_default_value(default_key))

    def update(self, doc=None):
        """Synchronise a model's attributes to the
        corresponding mongodb document.
        """
        if doc is not None:
            validation = self.validate_update(doc)
            if validation is True:
                for key, value in doc.iteritems():
                    setattr(self, key, value)
            else:
                raise NoSuchFieldError(validation['fields'])

        self.collection.find_one_and_update(
                {'_id': ObjectId(self._id)}, {'$set': self.generate_update_doc()}, upsert=True)

        self._id = str(self._id)
        return self

    @classmethod
    def query(cls, query=None):
        """Query the mongo collection and return the
        corresponding model(s).
        If no query params are provided, a list of all
        models in the collection is returned.
        """
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
        """Create a new model and write it to the
        mongo collection by passing in a dictionary.
        """
        validation = cls.validate(doc)
        if validation is True:
            mongo_id = cls.collection.insert(doc)
            return cls.query({'_id': ObjectId(mongo_id)})
        else:
            if validation['invalid_cause'] is 'missing_required_fields':
                raise MissingRequiredFieldError(validation['fields'])

            elif validation['invalid_cause'] is 'no_such_fields':
                raise NoSuchFieldError(validation['fields'])

            elif validation['invalid_cause'] is 'invalid_field_value':
                raise InvalidFieldValueError(validation['fields'])


    @classmethod
    def destroy(cls, doc):
        """Remove a model's document from the mongo collection."""
        collection.remove(doc)

    @classmethod
    def validate(cls, doc):
        """Base validation for creating a MongoModel.
        A check is performed on the fields keys as well as a
        type check on field values if the derived class implements
        a validate_extra method.
        """
        missing_required_fields = list(set(cls.get_required_fields()) - set(doc.keys()))
        no_such_fields = list(set(doc.keys()) - set(cls.get_fields()))

        # check if all required fields are present
        if missing_required_fields:
            return {"invalid_cause": "missing_required_fields", "fields": missing_required_fields}
        elif no_such_fields:
            return {"invalid_cause": "no_such_fields", "fields": no_such_fields}
        else:
            return True

    def validate_update(self, doc):
        """Validate an update dictionary before writing to
        the collection.
        """
        no_such_fields = list(set(doc.keys()) - set(self.get_fields()))

        if no_such_fields:
            return {"invalid_cause": "no_such_fields", "fields": no_such_fields}
        else:
            return True


    @classmethod
    def get_required_fields(cls):
        """Returns a list of identifiers for the model's required
        fields that have no default value provided.
        """
        return [field['identifier'] for field in cls.fields if 'required' in field and field['required'] and 'default' not in field]

    @classmethod
    def get_fields(cls):
        """Returns a list of all field identifiers for the model.
        """
        return [field['identifier'] for field in cls.fields]

    def get_fields_with_types(self):
        """Returns a list of all field identifiers for the model where
        the field has a specified type.
        """
        return [field['identifier'] for field in self.fields if 'type' in field]

    def get_field_type(self, field_id):
        """Returns the type (if specified on the model) of the field with
        an identifier matching the field_id argument.
        """
        for field in self.fields:
            if field['identifier'] is field_id and 'type' in field:
                return field['type']

    def get_fields_with_defaults(self):
        """Returns a list of all field identifiers for the model where
        the field has a default value.
        """
        return [field['identifier'] for field in self.fields if 'default' in field and 'required' in field]

    def get_default_value(self, field_id):
        """Returns the default value (if specified on the model) of the field
        with an identifier matching the field_id argument.
        """
        for field in self.fields:
            if field['identifier'] is field_id and 'default' in field:
                return field['default']

    def coerce_types(self):
        """Attempt to cast all field values to the required type, usually
        after creating or updating a model with data from a JSON string.
        """
        for field_id in self.get_fields_with_types():
            if hasattr(self, field_id):
                field_type = self.get_field_type(field_id)
                field = getattr(self, field_id)

                if type(field) is not field_type:
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
        """Attempt to cast a field value to the required type, usually
        after creating or updating a model with data from a JSON string.
        """
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
        elif field_type is int:
            if type(field) is int:
                return field
            else:
                return int(field)

    def generate_update_doc(self):
        """Helper method to generate a valid update object
        to write to the class's mongo collection.
        """
        update = self.__dict__
        update['_id'] = ObjectId(update['_id'])
        return update

    def generate_json(self):
        """Helper method to generate the data for a JSON
        response to a request on the ApiController.
        """
        return self.__dict__




