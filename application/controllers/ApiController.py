from flask import request, Blueprint, Response, make_response, jsonify
from flask.views import MethodView

from bson.json_util import dumps

class ApiController(MethodView):

    url = '/'

    def gen_response(self, payload):
        response = None

        if type(payload) is list:
            json_list = []

            for obj in payload:
                json_list.append(self.generate_json(obj))

            response = Response(dumps(json_list), mimetype='application/json')

        else:
            json_dict = self.generate_json(payload)
            response = Response(dumps(json_dict), mimetype='application/json')

        return make_response(response)

    def generate_json(self, obj):
        json_dict = obj.__dict__
        json_extra = obj.json_helper()

        if json_extra is not None:
            for key, value in json_extra.iteritems():
                json_dict[key] = value

        return json_dict


    def error_response(self, e):
        return jsonify({
            'error_type': type(e).__name__,
            'error_message': str(e)
        }), 400


    def get_endpoint(self):
        return str(request.url_rule).split('/')[-1]

    @classmethod
    def register(cls, mod):
        symfunc = cls.as_view(cls.__name__)

        for endpoint, options in cls.url_rules.iteritems():
            url_rule = options
            methods = ('GET',)
            defaults = {}

            if len(options) == 2:
                url_rule, methods = options
            elif len(options) == 3:
                url_rule, methods, defaults = options

            mod.add_url_rule(url_rule, methods=methods, defaults=defaults, view_func=symfunc)
