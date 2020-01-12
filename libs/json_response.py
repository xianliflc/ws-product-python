def build_response(data, errors=None, code=200):

    if not (errors is None):
        return {
            'success': False,
            'error': errors
        }, code

    elif not (data is None):
        return {
            'success': True,
            'data': data
        }, code
    else:
        return None, code


def response(data, code):
    return build_response(data, None, code)


def error(errors, code):
    return build_response(None, errors, code)
