General Electric LINEAGE J85480S1 CPL Monitor
=============================================

A project for monitoring LINEAGE J85480S1 power-supplies, involving:
- LINEAGE J85480S1 and its J1 connector
- A Rapberrypi and its GPIO connector
- A Pi HAT (see specification in hardware/README.md)
- RPi.GPIO and Flask python libraries
- gunicorn and systemd

![Monitoring Device](/hardware/images/device-transparent-small.png?raw=true)


Hardware Specifications
-----------------------

Please refer to the [hardware README](hardware/).


Software Installation (Debian)
------------------------------

### Install and configure the web-service
```
sudo apt-get install python python-dev python-pip git
git clone {repository-url} cmts-cpl-monitor
cd cmts-cpl-monitor
sudo pip install -r requirements.txt
vi config.py         # optionally update with your preferred pinout, or not
python web.py        # test the service with built-in dev web server
curl localhost:5000  # check the web-service output
```

### Install and configure gunicorn
```
sudo apt-get install gunicorn           # install gunicorn wsgi server
sudo cp `pwd`/systemd.service /etc/systemd/system/cmts-cpl-monitor.service  # create systemd service
sudo systemctl start cmts-cpl-monitor   # start the service
sudo systemctl status cmts-cpl-monitor  # check the service state
curl localhost                          # check the web-service output
sudo systemctl enable cmts-cpl-monitor  # start the service upon boot
```

### Testing with curl
```
curl localhost[:5000]
```
displays:
```
{
  "alarms": {
    "1": {
      "AC Present but not within limits": false, 
      "AC not present": false, 
      "Blown AC Fuse in Unit": false, 
      "Boost Stage Failure": false, 
      "Defective Fan": false, 
      "No AC <15mS (single unit) ": false, 
      "Non-catastrophic Internal Failure": false, 
      "OK": true, 
      "Over Current": false, 
      "Over Voltage Latched Shutdown": false, 
      "Thermal Shutdown ": false
    }, 
    "2": {
      "AC Present but not within limits": false, 
      "AC not present": false, 
      "Blown AC Fuse in Unit": false, 
      "Boost Stage Failure": false, 
      "Defective Fan": false, 
      "No AC <15mS (single unit) ": false, 
      "Non-catastrophic Internal Failure": false, 
      "OK": true, 
      "Over Current": false, 
      "Over Voltage Latched Shutdown": false, 
      "Thermal Shutdown ": false
    }, 
    "3": {
      "AC Present but not within limits": false, 
      "AC not present": false, 
      "Blown AC Fuse in Unit": false, 
      "Boost Stage Failure": false, 
      "Defective Fan": false, 
      "No AC <15mS (single unit) ": false, 
      "Non-catastrophic Internal Failure": false, 
      "OK": false, 
      "Over Current": false, 
      "Over Voltage Latched Shutdown": false, 
      "Thermal Shutdown ": false
    }, 
    "4": {
      "AC Present but not within limits": true, 
      "AC not present": true, 
      "Blown AC Fuse in Unit": false, 
      "Boost Stage Failure": false, 
      "Defective Fan": false, 
      "No AC <15mS (single unit) ": true, 
      "Non-catastrophic Internal Failure": false, 
      "OK": false, 
      "Over Current": true, 
      "Over Voltage Latched Shutdown": false, 
      "Thermal Shutdown ": false
    }
  }, 
  "human": {
    "Fault": false, 
    "MOD_PRES_1": true, 
    "MOD_PRES_2": true, 
    "MOD_PRES_3": false, 
    "MOD_PRES_4": true, 
    "OTW": false, 
    "PFW_1": false, 
    "PFW_2": false, 
    "PFW_3": false, 
    "PFW_4": true, 
    "POWER_CAP_1": "2000W", 
    "POWER_CAP_2": "2000W", 
    "POWER_CAP_3": "2000W", 
    "POWER_CAP_4": "2000W"
  }, 
  "raw": {
    "Fault": 1, 
    "MOD_PRES_1": 0, 
    "MOD_PRES_2": 0, 
    "MOD_PRES_3": 1, 
    "MOD_PRES_4": 0, 
    "OTW": 1, 
    "PFW_1": 1, 
    "PFW_2": 1, 
    "PFW_3": 1, 
    "PFW_4": 0, 
    "POWER_CAP_1": 1, 
    "POWER_CAP_2": 1, 
    "POWER_CAP_3": 1, 
    "POWER_CAP_4": 1
  }
}
```


Datasheets
----------

* [LINEAGE Compact Power Line Shelves Model J85480S1](http://apps.geindustrial.com/publibrary/checkout/J85480S1?TNR=Data%20Sheets%7CJ85480S1%7Cgeneric)
* [LINEAGE Compact Power Line CP2000AC54 Front-End Power Supply](http://apps.geindustrial.com/publibrary/checkout/CP2000AC54?TNR=Data%20Sheets%7CCP2000AC54%7CPDF&filename=CP2000AC54.pdf)
* [LINEAGE Compact Power Line 48V DC Critical Power Solution](http://apps.geindustrial.com/publibrary/checkout/CPB-CPL?TNR=Brochures%7CCPB-CPL%7CPDF&filename=CPB-CPL%203-17-16.pdf)


Credits
-------

* **Jon Martin** <<jon.martin@citycable.ch>>
* **Pascal Pellet** <<pascal.pellet@lausanne.ch>>
* **Jérôme Siegfried** <<jerome.siegfried@lausanne.ch>>
