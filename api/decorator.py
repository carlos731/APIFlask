from functools import wraps
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from flask import make_response, jsonify

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        # verificar se usuário é admin ou não para fazer essa operação.
        claims = get_jwt()  # recuperar o claims do login_views
        if claims['roles'] != 'admin':
            return make_response(jsonify(mensagem='Não é permitido esse recurso. Apenas administradores'), 403)
        else:
            return fn(*args, **kwargs)
    return wrapper