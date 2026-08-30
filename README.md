# piStationManager

A Raspberry Pi-based amateur radio station management system intended for contesting. 
Currently planned functions include SO2V assistance, antenna switching with hot-switching protection, and N1MM macro launching using UDP packets.

Please note that there are two versions of the program: ts590s and universal. The former is intended specifically for the Kenwood TS-590S and uses a direct serial interface that supports auto information (AI) for instantaneous CAT updates. The latter is a universal version that uses hamlib for CAT data, with no AI support. Future support for other AI-compatible radios (Kenwood, Elecraft, Yaesu) is possible.
