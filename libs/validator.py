import functools
from flask import request, abort
import libs.http_status as status
from importlib import import_module
from marshmallow import ValidationError


class Validator(object):

    def __init__(self, validator, options=None, path='validators'):
        self.options = options
        self.validator = validator
        self.path = path
        self.partial = bool(self.options.partial) if self.options and self.options.partial else False

    def __call__(self, f):

        def wrapped_f(*args,  **kwargs):
            file_name = self.validator.split('.')[0]
            class_name = self.validator.split('.')[1]
            module_object = import_module(self.path + '.' + file_name)
            target_class = getattr(module_object, class_name)

            try:
                validator_instance = target_class()
                errors = validator_instance.validate(kwargs['data'], partial=self.partial)
                if errors:
                    kwargs['errors'] = errors
                else:
                    kwargs['data'] = validator_instance.load(kwargs['data'], partial=self.partial)
                    # kwargs['data'] = result

            except ValidationError as err:
                print(err.messages)
            return f(*args,  **kwargs)
        return wrapped_f


def require_json(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            abort(status.HTTP_BAD_REQUEST.get('code'))

        data = request.get_json()
        if not data:
            abort(status.HTTP_BAD_REQUEST.get('code'))
        kwargs['data'] = data

        return f(*args, **kwargs)

    return decorated_function
