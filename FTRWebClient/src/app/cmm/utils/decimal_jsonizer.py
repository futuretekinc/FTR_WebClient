import json
import decimal

from flask import jsonify, make_response,after_this_request

def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return str(float(obj))
    raise TypeError

'''
USE -
json.dumps({},default=decimal_default)
'''

def fn_jsonify2(obj):
    try:
        return jsonify(obj)
    except Exception as e:
        print("fn_jsonify**")
        pass
    body = json.dumps(obj,default=decimal_default)
    d = json.loads(body)
    return jsonify(d)

def fn_jsonify(obj):
    try:
        return jsonify(obj)
    except Exception as e:
        pass
    return json.dumps(obj,default=decimal_default)
