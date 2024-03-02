# parse-probing
A study of internal representations of models trained to parse PEGs.

# File Structure
`.`  
`├── README.md`  
`├── brack`: Data for the language `brack`  
`|-- data.py`: Dataset class (PL `DataModule`) for any of the languages  
`├── dataset.ipynb`: Dataset generation code  
`├── dyck1`: Data for the language `dyckone`  
`├── dyck3`: Data for the language `dyckthree`  
`├── enumerate`: Enumerated strings of a fixed length for each language.  
`│   ├── brack10.txt`  
`│   ├── dyckone20.txt`  
`│   ├── dyckthree9.txt`  
`│   ├── expr6.txt`  
`│   ├── star20.txt`  
`│   └── triple12.txt`  
`├── expr`: Data for the language `expr`  
`├── generate`: Code to enumerate strings for each language, either randomly or deterministically  
`│   ├── g1.py`  
`│   ├── g2.py`  
`│   ├── g3.py`  
`│   ├── g4.py`  
`│   ├── g5.py`  
`│   ├── g6.py`  
`│   └── generate-slow`: Slower methods to either enumerate strings or generate grammars  
`│       ├── generate.sh`: Iterate over all strings of a fixed length and parse them  
`│       ├── generation.hs`: Same  
`│       ├── generation.py`: Randomly create grammars (these grammars tend to be infeasible and hard to control)  
`│       └── peg.hs`: Code to define and parse PEGs  
`├── star`: Data for the language `star`  
`├── stats.py`: Code to find statistics of string length  
`└── triple`: Data for the language `triple`  