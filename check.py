#!/usr/bin/python

"""
Nagios check for Casa C10G PSM.
"""


import sys, collections, argparse, requests

def getopts():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="C10G monitoring web-service URL", type=str)
    args = parser.parse_args()
    return args

def output(code, message):
    state = {0: 'OK',
             1: 'WARNING',
             2: 'CRITICAL',
             3: 'UNKNOWN'}
    try:
        print '%s: %s' % (state[code], message)
        sys.exit(code)
    except Exception:
        output(3, 'Internal check error')

def check():
    opts = getopts()
    try:
        response = requests.get(opts.url)
        data = response.json()
    except requests.exceptions.ConnectionError as e:
        output(2, 'Monitoring URL is not reachable ({0})'.format(e.request.url))
    except requests.exceptions.RequestException as e:
        output(3, e)
    except ValueError as e:
        output(2, 'Monitoring data could not be read as json ({0}...)'.format('x'))#response.text[:50]))
    except Exception as e:
        output(2, 'Unknown check error ({0}: {1})'.format(e.__class__, e.message))
    if all([alarms['OK'] for module, alarms in data['alarms'].viewitems()]):
        output (0, 'All green')
    else:
        active_alarms = collections.defaultdict(list)
        for module, alarm in [(module, alarm)
                              for module, alarms in data['alarms'].viewitems()
                              for alarm, active in alarms.viewitems()
                              if active and alarm != 'OK']:
            active_alarms[module].append(alarm)
        if data['human']['Fault']:
            active_alarms['Chassis'].append('Fault indicator active')
        string = ('Alarm on modules: {0}\n'.format(', '.join(active_alarms.viewkeys())) +
                  '\n'.join(['Module {0}: {1}'.format(module, ', '.join(alarms))
                             for module, alarms in active_alarms.viewitems()]))
        code = 1 if len(active_alarms.viewkeys()) <= 2 else 2
        output(code, string)

if __name__ == '__main__':
    check()