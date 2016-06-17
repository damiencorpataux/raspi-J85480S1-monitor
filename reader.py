# GPIO Reader component
#
#
# Wiring
# ------
#
# J1 Pin Name: J1 Pin number: GPIO Pin number
#
# MOD_PRES1: 5: 11
# MOD_PRES2: 6: 2
# MOD_PRES3: 7: 3
# MOD_PRES4: 8: 4
# PFW_1: 9: 15
# PFW_2: 10: 18
# PFW_3: 11: 7
# PFW_4: 12: 8
# Fault: 17: 9
# OTW: 25: 10
#
#
# Note: On ht eJ1 connector, pin 1 is in the lower left corner,
#       pin 2 is on the upper left corner, etc...
#
#   246...
# +--------------
# | :::::::::::::::
# +------------------
#   1357...
#


import RPi.GPIO as GPIO

map = {11: ('MOD_PRES1', lambda v: not v),
       22:  ('MOD_PRES2', lambda v: not v),
       23:  ('MOD_PRES3', lambda v: not v),
       4:  ('MOD_PRES4', lambda v: not v),
       15: ('PFW_1',     lambda v: not v),
       18: ('PFW_2',     lambda v: not v),
       7:  ('PFW_3',     lambda v: not v),
       8:  ('PFW_4',     lambda v: not v),
       9:  ('Fault',     lambda v: not v),
       10: ('OTW',       lambda v: not v)}

def init():
    # NOTE: The GPIO.BOARD option specifies that you are referring to the pins by the number of the pin the the plug - i.e the numbers printed on the board (e.g. P1) and in the middle of the diagrams below.
    #       The GPIO.BCM option means that you are referring to the pins by the "Broadcom SOC channel" number, these are the numbers after "GPIO"
    #       Unfortunately the BCM numbers changed between versions of the Pi1 Model B.
    GPIO.setmode(GPIO.BCM)
    # FIXME: faaaack GPIO has pull-ups:
    #        GPIO.setup(butPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button pin set as input w/ pull-up
    #        https://learn.sparkfun.com/tutorials/raspberry-gpio/python-rpigpio-example
    for pin in map.viewkeys():
	print 'Setting pin %s as INPUT' % pin
        GPIO.setup(pin, GPIO.IN)

def read():
    # FIXME: PFW and Fault flap during a module failure
    #        (the pin state is reseted to not fault everytime the module is trying to restart, every presumably)
    #        shall we latch for a while somehow the value somehow ?
    return {x[0]: x[1](GPIO.input(pin)) for pin, x in map.viewitems()}

def cleanup():
        print GPIO.cleanup()
