from flask import request

def wants_json():
    return request.accept_mimetypes.accept_json and \
not request.accept_mimetypes.accept_html
