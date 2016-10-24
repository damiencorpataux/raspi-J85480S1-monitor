CMTS CPL Monitor
================

A project for monitoring LINEAGE J85480S1 power-supplies, involving:
- LINEAGE J85480S1 and its J1 connector
- A Rapberrypi and its GPIO connector
- RPi.GPIO and Flask python libraries
- gunicorn and systemd


## Installation
```
git clone {repository-url} monitor
cd monitor
vi config.py  # optionally update with your preffered pinout, or not

python web.py  # test the service with built-in dev web server

sudo apt-get install gunicorn  # install gunicorn wsgi server
sudo ln -s `pwd`/systemd.service /etc/systemd/system/casa-monitor.service  # create systemd service
sudo systemctl start casa-monitor  # start the service
sudo systemctl status casa-monitor  # check the service state
curl localhost  # check the web-service output
sudo systemctl enable casa-monitor  # start the service upon boot
```

Testing with curl:
```
curl localhost
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
