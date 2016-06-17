import flask, reader

app = flask.Flask(__name__)
reader.init()

@app.route('/')
def read():
    """Returns the reader data"""
    return flask.jsonify(reader.read())


# CLI invocation handler
if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0',
                port=80,
                debug=app.config.get('DEBUG'),
                use_reloader=True)
    finally:
        print 'Cleaning GPIO state...'
        reader.cleanup()
