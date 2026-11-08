# Kuromi's Little Library

A Kuromi-inspired Library Management System built with Python and PyQt6.

## Features
- Dashboard statistics for books, students, and active loans
- Add, edit, delete, and search book records
- Register, edit, delete, and search student records
- Issue and return books with due dates
- JSON data persistence
- Input validation and confirmation dialogs
- Purple, lavender, pink, and charcoal styling

## Requirements
- Python 3.10 or newer
- PyQt6

## Install and run
Open Terminal in this folder and run:

```bash
python3 -m pip install -r requirements.txt
python3 main.py
```

The app creates `library_data.json` automatically when records are saved. Keep this file in the same folder as `main.py` and `library_logic.py` so your records remain available next time.

## Important
This is a learning project. Read the code, test each feature, and be ready to explain how the buttons, layouts, JSON storage, and event handlers work during your viva. Replace the sample student name and number in the window title with your own details if needed.
