
# Voodoo GUI

Voodoo GUI is a simple Python library to create user interfaces like Streamlit but with an intuitive and simpler syntax.

## Installation

```bash
pip install voodoo-gui
```

## Usage

Example code to create a simple page:

```python
from voodoo.gui import Gui
import voodoo.gui.builder as vo

text = "Original text"

with vo.Page() as page:
    vo.text("# Getting started with voodoo GUI", mode="md")
    vo.text(f"My text: {text}")

    vo.input(f"{text}")

Gui(page).run(debug=True)
```

Then run:

```bash
python voodoopy_gui_example.py
```

Access the page on `localhost:3000`.
    