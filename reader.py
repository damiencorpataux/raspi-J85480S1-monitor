# GPIO Reader component
#
#
# Wiring
# ------
#
# J1 Pin Name: J1 Pin number
#
# POWER_CAP_1: 1
# POWER_CAP_2: 2
# POWER_CAP_3: 3
# POWER_CAP_4: 4
# MOD_PRES_1: 5
# MOD_PRES_2: 6
# MOD_PRES_3: 7
# MOD_PRES_4: 8
# PFW_1: 9
# PFW_2: 10
# PFW_3: 11
# PFW_4: 12
# Fault: 17
# OTW: 25
# GND: 20 (or 22)
# 5V: 24 (max 750mA)
#
#
# Note: On the J1 connector, pin 1 is in the lower left corner,
#       pin 2 is on the upper left corner, etc...
#
#   246...
# +--------------
# | :::::::::::::::
# +------------------
#   1357...
#


import time, collections
import RPi.GPIO as GPIO

# GPIO to J1 Signal Names (Pin: Signal-Name dict)
pinout = {2: 'POWER_CAP_1',
          3: 'POWER_CAP_2',
          4: 'POWER_CAP_3',
          17: 'POWER_CAP_4',
          25: 'MOD_PRES_1', # 27 is always 1 (defect on that pi?)
          22: 'MOD_PRES_2',
          10: 'MOD_PRES_3',
          9: 'MOD_PRES_4',
          11: 'PFW_1',
          14: 'PFW_2',
          15: 'PFW_3',
          18: 'PFW_4',
          23: 'Fault',
          24: 'OTW'}

# Raw value to logical transform functions
to_human = {'POWER_CAP_1': lambda v: to_values['POWER_CAP'][bool(v)],
            'POWER_CAP_2': lambda v: to_values['POWER_CAP'][bool(v)],
            'POWER_CAP_3': lambda v: to_values['POWER_CAP'][bool(v)],
            'POWER_CAP_4': lambda v: to_values['POWER_CAP'][bool(v)],
            'MOD_PRES_1': lambda v: not v,
            'MOD_PRES_2': lambda v: not v,
            'MOD_PRES_3': lambda v: not v,
            'MOD_PRES_4': lambda v: not v,
            'PFW_1': lambda v: not v,
            'PFW_2': lambda v: not v,
            'PFW_3': lambda v: not v,
            'PFW_4': lambda v: not v,
            'Fault': lambda v: not v,
            'OTW': lambda v: not v}

to_values = {'POWER_CAP': {False: '1200W',
                           True: '2000W'}}

# Alarm table definition
to_alarms = {
    'OK': {
        'Fault': 1,
        'OTW': 1,
        'PFW': 1,
        'MOD_PRES': 0},
    'Thermal Shutdown ': {
        'Fault': 0,
        'OTW': 0,
        'PFW': 0,
        'MOD_PRES': 0},
    'Defective Fan': {
        'Fault': 0,
        'OTW': 1,
        'PFW': 0,
        'MOD_PRES': 0},
    'Blown AC Fuse in Unit': {
        'Fault': 0,
        'OTW': 1,
        'PFW': 0,
        'MOD_PRES': 0},
    'No AC <15mS (single unit) ': {
        'Fault': 1,
        'OTW': 1,
        'PFW': 0,
        'MOD_PRES': 0},
    'AC Present but not within limits': {
        'Fault': 1,
        'OTW': 1,
        'PFW': 0,
        'MOD_PRES': 0},
    'AC not present': {
        'Fault': 1,
        'OTW': 1,
        'PFW': 0,
        'MOD_PRES': 0},
    'Boost Stage Failure': {
        'Fault': 0,
        'OTW': 1,
        'PFW': 0,
        'MOD_PRES': 0},
    'Over Voltage Latched Shutdown': {
        'Fault': 0,
        'OTW': 1,
        'PFW': 0,
        'MOD_PRES': 0},
    'Over Current': {
        'Fault': 1,
        'OTW': 1,
        'PFW': 0,
        'MOD_PRES': 0},
    'Non-catastrophic Internal Failure': {
        'Fault': 0,
        'OTW': 1,
        'PFW': 1,
        'MOD_PRES': 0},
#    '1 Missing Module': {
#        'Fault': None,
#        'OTW': None,
#        'PFW': None,
#        'MOD_PRES': 1},
}


def init():
    """
    Initialize GPIO (pin mode, pull-ups, etc).
    """
    GPIO.setmode(GPIO.BCM)
    for pin in pinout.viewkeys():
	print 'Setting pin %s as INPUT with PULL-UP (50..65k)' % pin
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def cleanup():
    """
    Cleans up the GPIO state.
    """
    print GPIO.cleanup()


def read_raw():
    """
    Returns the raw measurements.
    """
    return {signal: GPIO.input(pin) for pin, signal in pinout.viewitems()}

def read_latch(n=8, interval=0.5):
    """
    Returns the raw measurements, latched.
    Multiple measurements are performed at regular interval, keeping worst values.
    """
    latch_hi = lambda values: int(any(values)) # returns 1 if any value is 1
    latch_low = lambda values: int(all(values)) # returns 0 if any value is 0
    latch_map = {'POWER_CAP': latch_low,
                 'MOD_PRES': latch_hi,
                 'PFW': latch_low,
                 'Fault': latch_low,
                 'OTW': latch_low}
    readings = []
    for i in range(n):
        readings.append(read_raw())
        time.sleep(interval)
    latched = collections.defaultdict(list)
    for reading in readings:
        for k, v in reading.viewitems():
            latched[k].append(v)
    for k, v in latched.viewitems():
        latched[k] = latch_map.get(k, latch_map.get(k[:-2]))(latched[k])
    return dict(latched)


def human(raw_values=None):
    """
    Returns the given raw measurement converted to human readable values.
    """
    # FIXME: PFW and Fault flap during a module failure
    #        (the pin state is reseted to not fault everytime the module is trying to restart, every presumably)
    #        shall we latch for a while somehow the value somehow ?
    return {signal: to_human[signal](value)
            for signal, value in (raw_values or read_raw()).viewitems()}

def alarms(raw_values=None):
    """
    Returns the given raw measurements converted to alarms,
    according the device documentation.
    """
    reading = raw_values or read_raw()
    return {module: {name: all([value == reading.get('%s_%s' % (signal, module),
                                                     reading.get(signal))
                                for signal, value in signals.viewitems()])
                     for name, signals in to_alarms.viewitems()}
            for module in [1, 2, 3, 4]}
