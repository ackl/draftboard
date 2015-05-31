class MongoModelError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

class NoSuchFieldError(MongoModelError):
    def __init__(self, fields):
        self.message = 'The following fields could not be found on the model, but were in the call to the method: {0}'.format(', '.join(fields))

class MissingRequiredFieldError(MongoModelError):
    def __init__(self, fields):
        self.message = 'The following fields are required by the model and have no default value, but were not in the call to the method: {0}'.format(', '.join(fields))

class InvalidFieldValueError(MongoModelError):
    def __init__(self, fields):
        self.message = 'The following fields were given invalid values: {0}'.format(', '.join(fields))

class TypeCoercionError(MongoModelError):
    def __init__(self, args):
        self.message = '{0} | The following field could not be converted into the required type: {1}'.format(args['error_type'], args['field_id'])
