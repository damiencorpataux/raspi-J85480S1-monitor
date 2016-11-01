"""
LINEAGE J85480S1 CPL Monitor, GPIO Reader configuration.
"""

# GPIO to J1 Signal Names (Pin: Signal-Name dict)
pinout = {17: 'POWER_CAP_1',
          18: 'POWER_CAP_2',
          27: 'POWER_CAP_3',
          22: 'POWER_CAP_4',
          23: 'MOD_PRES_1',
          24: 'MOD_PRES_2',
          25: 'MOD_PRES_3',
          5: 'MOD_PRES_4',
          6: 'PFW_1',
          12: 'PFW_2',
          13: 'PFW_3',
          19: 'PFW_4',
          20: 'OTW',
          16: 'Fault'}