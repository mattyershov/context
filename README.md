# context

Contest Extension (context for short) is a Raspberry Pi-based amateur radio station management system intended for contesting.

While most modern HF radios feature a large color display that can show almost unlimited information about the radio, many older radios, such as the Elecraft K3 and Kenwood TS-590, use a monochrome segmented LCD display that shows only limited information. Context attempts to solve this problem by serving as an extension to such a radio. It displays essential information for contesting, including frequency displays and T/R focus indicators for VFOs A and B, and status of select radio settings. The program interfaces with a Contour Design ShuttleProV2 for control of frequency, radio settings, and macros.

The program is intended to run on a Raspberry Pi and touchscreen display. The radio uses one serial/USB port to connect to a logging computer and another to connect to the Pi.

Planned features include control of antenna switches (similar to a MOAS) and support for more radios. Please keep in mind that context will only support radios capable of sending unsolicited CAT data, as polling results in sluggish CAT updates.