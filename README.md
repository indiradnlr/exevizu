# Exevizu Overview

**Exevizu** is a tool developed as an optional project for the 2019 Forensics course at EURECOM.

This python program displays a graphical representation of the binary code in the code section of a PE or an ELF file. Each sequence of four consecutive bits is represented by a line which direction depends on the value of the digit in hexadecimal basis. The colors of the lines give the order of the digits in the code section. You can use the mouse wheel to zoom and drag&drop to move inside the visualizer.



![Command Line Interface](https://i.imgur.com/De969MG.png)

![Result](https://i.imgur.com/bpeTkBM.png)
# Requirements

 - Python 2.7 (with Tkinter installed, normally included in standard distribution)
 - Modules listed in reqs.txt

# Installation

     git clone https://github.com/indiradnlr/exevizu.git
     cd exevizu/
     [sudo] pip install -r reqs.txt

# Usage

     python exevizu.py <path/to/file> [-h] [-sc START_COLOR] [-ec END_COLOR] [-om OMIT [OMIT ...]] [-nl] [-s]


e.g

     python exevizu.py pe-file.exe -om 0x0 0xe -sc '#887766' -ec '(46, 112, 201)'

## Arguments
### Required
| Argument | Description |
|--|--|
| \<path/to/file> | Path of the executable |

### Optional

| Argument | Description |
|--|--|
| -h, --help| Path of the executable |
| -sc ***START_COLOR***, --start-color ***START_COLOR***| Start color of gradient in HEX or RGB 255-tuple. e.g :'#42b0f4' or '(18,255,156)' |
|-ec ***END_COLOR***, --end-color ***END_COLOR***| End color of gradient in HEX or RGB 255-tuple. e.g :'#42b0f4' or '(18,255,156)' |
| -om ***OMIT*** [***OMIT*** ...], --omit ***OMIT*** [***OMIT*** ...]| List of hex values to omit during the computation of the graphical visualization. One value between 0x0 and 0xf at a time. e.g : 0x1 0xa 0xe|
|-nl, --no-legend| Disable legend display. |
|-s, --silent| Disable all output messages. |
