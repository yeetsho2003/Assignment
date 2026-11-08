"""Kuromi's Little Library - a small PyQt6 library management system.
Run with: python main.py
"""
import sys
from datetime import date
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem,
    QStackedWidget, QMessageBox, QDialog, QFormLayout, QSpinBox,
    QComboBox, QHeaderView, QFrame, QDateEdit
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from library_logic import load_data, save_data, next_id

PURPLE = "#24172f"
PANEL = "#332342"
LAVENDER = "#b99add"
PINK = "#f3b6d5"
TEXT = "#fff5ff"
MUTED = "#c9b8d5"

STYLE = f"""
QMainWindow, QWidget {{ background: {PURPLE}; color: {TEXT}; font-family: 'Arial'; font-size: 13px; }}
QFrame#sidebar {{ background: #1b1225; border-right: 1px solid #513b60; }}
QLabel#brand {{ color: {PINK}; font-size: 23px; font-weight: bold; padding: 12px; }}
QLabel#pageTitle {{ color: {PINK}; font-size: 25px; font-weight: bold; }}
QLabel#muted {{ color: {MUTED}; }}
QFrame#card {{ background: {PANEL}; border: 1px solid #59436a; border-radius: 14px; }}
QPushButton {{ background: {LAVENDER}; color: #24172f; border: 0; border-radius: 9px; padding: 10px 14px; font-weight: bold; }}
QPushButton:hover {{ background: {PINK}; }}
QPushButton#nav {{ background: transparent; color: {TEXT}; text-align: left; padding: 13px; }}
QPushButton#nav:hover, QPushButton#nav:checked {{ background: #49345a; color: {PINK}; }}
QPushButton#danger {{ background: #a94f78; color: white; }}
QLineEdit, QComboBox, QSpinBox, QDateEdit {{ background: #21172c; color: {TEXT}; border: 1px solid #705783; border-radius: 7px; padding: 8px; }}
QTableWidget {{ background: #2b2036; alternate-background-color: #382947; gridline-color: #59436a; border: 1px solid #59436a; border-radius: 9px; }}
QHeaderView::section {{ background: #59436a; color: white; padding: 8px; border: none; font-weight: bold; }}
QTableWidget::item:selected {{ background: #76568e; }}
"""

class RecordDialog(QDialog):
    def __init__(self, title, fields, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumWidth(360)
        form = QFormLayout(self)
        self.inputs = {}
        for key, label, kind, options in fields:
            if kind == "combo":
                widget = QComboBox(); widget.addItems(options)
            elif kind == "spin":
                widget = QSpinBox(); widget.setRange(0, 9999); widget.setValue(1)
            else:
                widget = QLineEdit(); widget.setPlaceholderText(label)
            self.inputs[key] = widget
            form.addRow(label, widget)
        buttons = QHBoxLayout()
        save = QPushButton("Save ♡"); cancel = QPushButton("Cancel")
        save.clicked.connect(self.accept); cancel.clicked.connect(self.reject)
        buttons.addWidget(save); buttons.addWidget(cancel); form.addRow(buttons)

    def values(self):
        result = {}
        for key, widget in self.inputs.items():
            if isinstance(widget, QComboBox): result[key] = widget.currentText()
            elif isinstance(widget, QSpinBox): result[key] = widget.value()
            else: result[key] = widget.text().strip()
        return result

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kuromi's Little Library | Yeetsho Choden | 08230237")
        self.resize(1120, 720)
        self.data = load_data()
        root = QWidget(); outer = QHBoxLayout(root); outer.setContentsMargins(0,0,0,0); outer.setSpacing(0)
        sidebar = QFrame(); sidebar.setObjectName("sidebar"); sidebar.setFixedWidth(215)
        side = QVBoxLayout(sidebar)
        brand = QLabel("♡ KUROMI'S\n   LIBRARY ♡"); brand.setObjectName("brand"); side.addWidget(brand)
        side.addWidget(QLabel("A little place for big stories"))
        self.stack = QStackedWidget()
        self.pages = {}
        for name, symbol in [("Dashboard", "✦"), ("Books", "▣"), ("Students", "♙"), ("Loans", "♡")]:
            button = QPushButton(f"{symbol}   {name}"); button.setObjectName("nav"); button.setCheckable(True)
            button.clicked.connect(lambda checked=False, n=name: self.show_page(n))
            side.addWidget(button); self.pages[name] = self.make_page(name)
            self.stack.addWidget(self.pages[name])
            if name == "Dashboard": self.nav_dashboard = button
        side.addStretch()
        note = QLabel("Made with ♡ and a little mischief"); note.setObjectName("muted"); note.setWordWrap(True); side.addWidget(note)
        outer.addWidget(sidebar); outer.addWidget(self.stack, 1)
        self.setCentralWidget(root)
        self.show_page("Dashboard")

    def make_page(self, name):
        page = QWidget(); layout = QVBoxLayout(page); layout.setContentsMargins(28,25,28,25); layout.setSpacing(15)
        title = QLabel(name); title.setObjectName("pageTitle"); layout.addWidget(title)
        subtitle = QLabel({"Dashboard":"Welcome to your cute little library!", "Books":"Keep track of every lovely book.", "Students":"Manage library members.", "Loans":"Issue books and record returns."}[name]); subtitle.setObjectName("muted"); layout.addWidget(subtitle)
        if name == "Dashboard":
            cards = QGridLayout()
            self.stat_labels = {}
            for i, (key, label) in enumerate([("books","Total books"),("students","Students"),("loans","Active loans")]):
                frame = QFrame(); frame.setObjectName("card"); box = QVBoxLayout(frame)
                number = QLabel("0"); number.setStyleSheet(f"font-size:30px;color:{PINK};font-weight:bold")
                caption = QLabel(label); caption.setObjectName("muted"); box.addWidget(number); box.addWidget(caption)
                self.stat_labels[key] = number; cards.addWidget(frame,0,i)
            layout.addLayout(cards)
            welcome = QFrame(); welcome.setObjectName("card"); v = QVBoxLayout(welcome)
            v.addWidget(QLabel("☾  Welcome to Kuromi's reading corner!"))
            v.addWidget(QLabel("Use the menu to add books, register students, and manage book loans."))
            layout.addWidget(welcome); layout.addStretch()
        else:
            searchrow = QHBoxLayout(); search = QLineEdit(); search.setPlaceholderText(f"Search {name.lower()}...")
            search.textChanged.connect(lambda text, n=name: self.populate_table(n, text))
            searchrow.addWidget(search); layout.addLayout(searchrow)
            actions = QHBoxLayout()
            add = QPushButton("＋ Add new"); edit = QPushButton("Edit selected"); delete = QPushButton("Delete selected")
            delete.setObjectName("danger")
            add.clicked.connect(lambda checked=False, n=name: self.add_record(n))
            edit.clicked.connect(lambda checked=False, n=name: self.edit_record(n))
            delete.clicked.connect(lambda checked=False, n=name: self.delete_record(n))
            actions.addWidget(add); actions.addWidget(edit); actions.addWidget(delete)
            if name == "Loans":
                issue = QPushButton("Issue a book"); issue.clicked.connect(self.issue_book); actions.addWidget(issue)
                ret = QPushButton("Return selected"); ret.clicked.connect(self.return_book); actions.addWidget(ret)
            layout.addLayout(actions)
            table = QTableWidget(); table.setAlternatingRowColors(True); table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
            table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers); table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            layout.addWidget(table, 1); page.table = table
        return page

    def show_page(self, name):
        names = ["Dashboard", "Books", "Students", "Loans"]
        self.stack.setCurrentIndex(names.index(name))
        for button in self.findChildren(QPushButton):
            if button.objectName() == "nav": button.setChecked(button.text().endswith(name))
        self.refresh()

    def records(self, name):
        return self.data[{"Books":"books", "Students":"students", "Loans":"loans"}[name]]

    def columns(self, name):
        return {"Books":["id","title","author","category","quantity"], "Students":["student_id","name","class","section","contact"], "Loans":["loan_id","book_title","student_name","issue_date","status"]}[name]

    def populate_table(self, name, query=""):
        table = self.pages[name].table; rows = self.records(name); cols = self.columns(name)
        filtered = [r for r in rows if query.lower() in " ".join(str(v) for v in r.values()).lower()]
        table.setColumnCount(len(cols)); table.setHorizontalHeaderLabels([c.replace("_"," ").title() for c in cols]); table.setRowCount(len(filtered))
        for i, row in enumerate(filtered):
            for j, col in enumerate(cols): table.setItem(i,j,QTableWidgetItem(str(row.get(col,""))))
        table.resizeRowsToContents()

    def refresh(self):
        self.stat_labels["books"].setText(str(len(self.data["books"])))
        self.stat_labels["students"].setText(str(len(self.data["students"])))
        self.stat_labels["loans"].setText(str(sum(1 for x in self.data["loans"] if x.get("status")=="Issued")))
        for name in ("Books","Students","Loans"):
            self.populate_table(name)
        save_data(self.data)

    def selected_index(self, name):
        row = self.pages[name].table.currentRow()
        if row < 0: QMessageBox.information(self, "Select a row", "Please select a record first."); return None
        visible = [r for r in self.records(name)]
        item = self.pages[name].table.item(row,0)
        key = self.columns(name)[0]
        return next((i for i,r in enumerate(visible) if str(r.get(key,"")) == item.text()), None)

    def add_record(self, name):
        if name == "Books":
            fields=[("title","Book title","text",None),("author","Author","text",None),("category","Category","combo",["Fiction","Education","Science","Technology","History","Other"]),("quantity","Quantity","spin",None)]
        elif name == "Students":
            fields=[("student_id","Student ID","text",None),("name","Full name","text",None),("class","Class","text",None),("section","Section","combo",["A","B","C","D"]),("contact","Contact number","text",None)]
        else:
            QMessageBox.information(self,"Loans","Use Issue a book to create a loan."); return
        dialog=RecordDialog(f"Add {name[:-1]}",fields,self)
        if dialog.exec():
            values=dialog.values()
            if any(not str(v).strip() for v in values.values()): QMessageBox.warning(self,"Missing details","Please complete all fields."); return
            if name == "Books": values["id"]=next_id(self.data["books"],"id")
            else:
                if any(s["student_id"]==values["student_id"] for s in self.data["students"]): QMessageBox.warning(self,"Duplicate ID","That student ID already exists."); return
            self.records(name).append(values); self.refresh()

    def edit_record(self, name):
        if name == "Loans": QMessageBox.information(self,"Edit","Use Return selected to update a loan."); return
        index=self.selected_index(name)
        if index is None:return
        old=self.records(name)[index]
        if name=="Books": fields=[("title","Book title","text",None),("author","Author","text",None),("category","Category","combo",["Fiction","Education","Science","Technology","History","Other"]),("quantity","Quantity","spin",None)]
        else: fields=[("student_id","Student ID","text",None),("name","Full name","text",None),("class","Class","text",None),("section","Section","combo",["A","B","C","D"]),("contact","Contact number","text",None)]
        dialog=RecordDialog("Edit record",fields,self)
        for key,widget in dialog.inputs.items():
            value=old.get(key,"")
            if isinstance(widget,QComboBox): widget.setCurrentText(str(value))
            elif isinstance(widget,QSpinBox): widget.setValue(int(value))
            else: widget.setText(str(value))
        if dialog.exec():
            values=dialog.values()
            if any(not str(v).strip() for v in values.values()): QMessageBox.warning(self,"Missing details","Please complete all fields."); return
            if name=="Books": values["id"]=old["id"]
            elif values["student_id"] != old["student_id"] and any(s["student_id"]==values["student_id"] for s in self.data["students"]): QMessageBox.warning(self,"Duplicate ID","That student ID already exists."); return
            self.records(name)[index]=values; self.refresh()

    def delete_record(self,name):
        index=self.selected_index(name)
        if index is None:return
        if QMessageBox.question(self,"Confirm delete","Delete the selected record?") == QMessageBox.StandardButton.Yes:
            self.records(name).pop(index); self.refresh()

    def issue_book(self):
        if not self.data["books"] or not self.data["students"]:
            QMessageBox.warning(self,"Cannot issue","Add at least one book and one student first."); return
        dialog=QDialog(self); dialog.setWindowTitle("Issue a book ♡"); form=QFormLayout(dialog)
        available_books=[b for b in self.data["books"] if int(b["quantity"])>0]
        book=QComboBox(); book.addItems([f"{b['title']} (ID {b['id']})" for b in available_books])
        student=QComboBox(); student.addItems([f"{s['name']} ({s['student_id']})" for s in self.data["students"]])
        due=QDateEdit(); due.setCalendarPopup(True); due.setDate(QDate.currentDate().addDays(14))
        form.addRow("Book",book); form.addRow("Student",student); form.addRow("Due date",due)
        ok=QPushButton("Issue book"); ok.clicked.connect(dialog.accept); form.addRow(ok)
        if not book.count(): QMessageBox.warning(self,"Out of stock","All books are currently unavailable."); return
        if dialog.exec():
            b=available_books[book.currentIndex()]
            s=self.data["students"][student.currentIndex()]
            b["quantity"]=int(b["quantity"])-1
            self.data["loans"].append({"loan_id":next_id(self.data["loans"],"loan_id"),"book_title":b["title"],"student_name":s["name"],"issue_date":date.today().isoformat(),"due_date":due.date().toString("yyyy-MM-dd"),"status":"Issued"})
            self.refresh()

    def return_book(self):
        index=self.selected_index("Loans")
        if index is None:return
        loan=self.data["loans"][index]
        if loan["status"]!="Issued": QMessageBox.information(self,"Already returned","This book has already been returned."); return
        if QMessageBox.question(self,"Return book",f"Mark '{loan['book_title']}' as returned?") == QMessageBox.StandardButton.Yes:
            loan["status"]="Returned"
            book=next((b for b in self.data["books"] if b["title"]==loan["book_title"]),None)
            if book: book["quantity"]=int(book["quantity"])+1
            self.refresh()

if __name__ == "__main__":
    app=QApplication(sys.argv); app.setStyle("Fusion"); app.setStyleSheet(STYLE)
    window=MainWindow(); window.show(); sys.exit(app.exec())
