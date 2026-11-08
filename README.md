# context
## Overview
Contest Extension (Context for short) is a Raspberry Pi- and Arduino-based amateur radio station management system intended for contesting.

While most modern HF radios feature a large color display that can show almost unlimited information about the radio, many older radios, such as the Elecraft K3 and Kenwood TS-590, use a monochrome segmented LCD display that shows only limited information. Context attempts to solve this problem by serving as an extension to such a radio. It displays essential information for contesting, including frequency displays and T/R focus indicators for VFOs A and B, and status of select radio settings. The program interfaces with a Contour Design ShuttleProV2 for control of frequency, radio settings, and macros.

## Planned Features
- Antenna switching and phasing control using RS485
- Rotor control
- Ability to link multiple panels
- Audio processing
- UDP logger integration

## Disclaimer
Context is a bespoke open-source project, and prioritizes performance and capability at the expense of ease of setup. I designed it to work well with my station and operating style, but adapting it to a different station would require rewriting much of the code—mainly CAT commands, Qt GUI config, and antenna selections. Have fun!
