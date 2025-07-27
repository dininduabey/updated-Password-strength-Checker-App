## Password Strength Checker GUI
A modern and secure Password Strength Analyzer built using Python and Tkinter, with features like password hashing (bcrypt), strength scoring, and exporting results to a .txt file.

# Features
1. Password Strength Analysis
2. Analyzes passwords based on:
  Length
  Character variety (uppercase, lowercase, digits, special chars)
  Repeated or sequential patterns
  Presence in common password lists
  Dictionary word checks
  Keyboard patterns (e.g., qwerty, 12345)
3. Secure Hashing with bcrypt
Automatically hashes passwords using the industry-standard bcrypt library.
4. Export Reports
Save detailed password analysis reports to .txt files.
5. Password Visibility Toggle
Option to show/hide the password input field.
6. Graphical User Interface (GUI)
Built with Tkinter for an intuitive desktop experience.

## Requirements
Python 3.x
Libraries:
bcrypt
tkinter (usually comes with Python)
Install Dependencies
```
pip install bcrypt
```

▶️ How to Run
Locally (Development)
```
cd password_strength_checker
python password_checker.py
```

As a Standalone Executable (.exe)
You can compile this project into a standalone executable using PyInstaller.

1. Install PyInstaller
```
pip install pyinstaller
```
2. Build the Executable
```
pyinstaller --noconfirm --onefile --windowed password_checker.py
```

The output .exe will be in the dist/ folder.

3. Include Required Files
Make sure these files are present in the same directory as the .exe:

common.txt
dictionary.txt (optional)
Alternatively, embed them during build:
```
pyinstaller --noconfirm --onefile --windowed --add-data "common.txt;." password_checker.py
```
Usage Tips
1. Use strong, unique passwords (long, complex, and random).
2. Avoid predictable patterns like 123456, password, or qwerty.
3. Always check your password against known weak lists.
4. Export the report to review or audit later.
