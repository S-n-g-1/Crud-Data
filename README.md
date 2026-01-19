# Inventory App (Python + GTK + SQLite)

This is a desktop application built with Python, PyGObject (GTK 3), and SQLite.

## Requirements

- Python 3.8+
- GTK 3 Runtime (Linux usually has it; Windows/macOS need installation via MSYS2 or Brew)
- PyGObject

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
   ```

2. Install dependencies:
   ```bash
   pip install pygobject pyinstaller
   ```

   *Note: On some systems, you may need to install system-level GTK development libraries first.*
   * Ubuntu/Debian: `sudo apt install libgirepository1.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-3.0`
   * Fedora: `sudo dnf install gobject-introspection-devel cairo-gobject-devel gtk3-devel`

## Running the App

```bash
python main.py
```

## Building with PyInstaller

To create a standalone executable:

1. Run the build command:
   ```bash
   pyinstaller --name="InventoryApp" --windowed --add-data="style.css:." main.py
   ```
   
   *Note: On Windows, use `;` instead of `:` for `--add-data` (e.g., `--add-data="style.css;."`).*

2. The executable will be in the `dist/InventoryApp/` folder.

## Project Structure

- `main.py`: Main application logic and GUI.
- `database.py`: SQLite database operations.
- `style.css`: GTK CSS styling.
