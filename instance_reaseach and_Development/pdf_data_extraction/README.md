# brownpaper_utility_bills_system
Research and project by INSTANCE Reasearch and Development for Brown Paper digital


# Create a Virtual Environment:

    python3 -m venv venv
    source venv/bin/activate  # For Linux/MacOS
    venv\Scripts\activate

# Installing Requirements
Use pip to install the following requiremnts.
Cerberus==1.3.7.
pypdf==5.1.0.

# Usage
from pypdf import PdfReader.

reader = PdfReader("example.pdf").
number_of_pages = len(reader.pages).
page = reader.pages[0].
text = page.extract_text().


