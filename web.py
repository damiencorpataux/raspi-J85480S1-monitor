# CMTS CPL Monitor, Web interface
#
# Usage:
#   sudo python web.py


import flask, reader

app = flask.Flask(__name__)
reader.init()

@app.route('/')
def read():
    """Returns the reader data"""
    raw_values = (reader.read_latch()
                  if 'latch' in flask.request.args.keys()
                  else reader.read_raw())
    return flask.jsonify(raw=raw_values,
                         human=reader.human(raw_values),
                         alarms=reader.alarms(raw_values))


# CLI invocation handler
if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0',
                port=80,
                debug=app.config.get('DEBUG'),
                threaded=False,
                use_reloader=True)
    finally:
        print 'Cleaning GPIO state...'
        reader.cleanup()
