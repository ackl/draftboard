from flask import request, Blueprint, Response, make_response, jsonify
from flask.views import MethodView

from bson.json_util import dumps

class ApiController(MethodView):

    url = '/'

    def gen_response(self, payload):
        response = None

        if type(payload) is list:
            response = Response(dumps([obj.__dict__ for obj in payload]), mimetype='application/json')
        else:
            response = Response(dumps(payload.__dict__), mimetype='application/json')

        return make_response(response)

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
