# HTML to XML (XHTML) Batch Converter (No lxml)

This script converts `.html` files into well-formed `.xml` (XHTML-like) files.  
It uses [html5lib](https://pypi.org/project/html5lib/) as the parser, so no C/C++ build tools are required.

---

## Installation

1. Make sure you have Python 3.9+ installed.  
2. Clone or download this repository.  
3. Install the required dependencies:

```bash
python -m pip install -r requirements_no_lxml.txt
Usage
Convert all .html files inside a folder and output them as .xml:

bash
Kodu kopyala
python html_to_xml_batch_no_lxml.py "C:\Users\Desktop\XML\.html" -o "C:\Users\Desktop\XML\.xml_cikti"
-o specifies the output folder.

Add --flat if you want all XML files to be written into a single folder (instead of preserving the original directory structure).

Use --no-pretty to disable indentation/pretty-printing.

Example
Input: example.html
Output: example.xml (well-formed XML)

Notes
The parser automatically fixes broken or unclosed HTML tags.

The output is XHTML-compatible XML with proper tag closures.

Works completely offline, safe for company data.


---









ChatGPT’ye sor
