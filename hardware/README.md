General Electric LINEAGE J85480S1 CPL Monitor Hardware
======================================================

The hardware consists in a Pi HAT interfacing the LINEAGE J85480S1 J1 connector
with the Raspi GPIO connector and (optionally) supplying power.

The HAT is designed for the 40-pin GPIO version (Raspberry Pi2 or Pi3).

![Monitoring Hat](/hardware/images/device-nocase-transparent-small.png?raw=true)


Bill Of Material
----------------

For one piece:

- 1x Raspberry Pi 2 Model B (the software and HAT work with any B Model layout)
- 1x 30p Female to Female Flat Ribbon Cable
- 1x HAT (see below)
- 1x Raspi + HAT Case (optional, see below)


HAT
---

### HAT Parts List

For one HAT:

- 1x HAT PCB
- 8x M2.5x6mm Screws
- 4x M25.12mm Spacers
- 1x 40p Female Header
- 1x 30p Male Header
- 1x 6p 1-row Male Header (optional, for power and J1 SPI pins)
- 2x Female DC Plug (optional, for 12V power supply)
- 2x 1N4002 Diode (optional, for 12V power supply)
- 1x LM2596-based DC-DC Step-Down Bucket Converter (optional, for 12V power input)

### HAT PCB

Everything you need to print your PCB are the files located
in the [```HAT```](HAT/) subdirectory.


Case
----

The case can be 3D-printed by using the files
located in the [```case```](case/) subdirectory.