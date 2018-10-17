#!/usr/bin/env python3
import json
import uuid
from staclint.stac_validator import StacValidate
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import request
from flask import url_for
from zappa.async import get_async_response
from zappa.async import task


app = Flask(__name__)


@task(capture_response=True)
def run_validate(stac_file, version):
    return StacValidate(stac_file.strip(), version, verbose=True).message

@app.route('/async-response/<response_id>')
def response(response_id):
    response = get_async_response(response_id)
    if response is None:
        abort(404)

    if response['status'] == 'complete':
        return jsonify(response['response'])

    # sleep(5)

    return "Not yet ready. Redirecting.", 302, {
        'Content-Type': 'text/plain; charset=utf-8',
        'Location': url_for('response', response_id=response_id, backoff=5),
        'X-redirect-reason': "Not yet ready.",
    }

@app.route('/', methods=['GET', 'POST'])
def validate():

    if request.method == 'GET':
        return "I'm alive!"

    # Find input params
    data = request.json

    json_STAC = data.get('json')
    url_STAC = data.get('url')
    version = data.get('schemaVersion', None)

    if type(json_STAC) is dict:
        local_stac = f"/tmp/{str(uuid.uuid4())}.json"

        with open(local_stac, "w") as f:
            json.dump(json_STAC, f)

        stac_file = local_stac
    else:
        stac_file = url_STAC

    response = run_validate(stac_file.strip(), version)
    print('response.response_id: {}'.format(response.response_id))

    if isinstance(response, dict):
        return jsonify(response)

    return redirect(url_for('response', response_id=response.response_id))


if __name__ == '__main__':
    app.run()
