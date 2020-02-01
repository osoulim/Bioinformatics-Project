from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QFileDialog, QStatusBar, QMessageBox
from PyQt5.QtCore import Qt
from main import generate_tree, generate_tree_from_file, find_all, find_repeats, find_lcs, find_palindrom

app = QApplication([])
window = QWidget()
window.setWindowTitle("Bioinformatic Project")

### START UI
# Buttons
file_button = QPushButton('Load File')
generate_button = QPushButton('Generate')
query_button = QPushButton('Search')
longest_button = QPushButton('Find Repeat')
lcs_button = QPushButton('Find LCS')
palindrom_button = QPushButton('Find Palindrom')
save_button = QPushButton('Save ')

# Text Edits
strings_text = QTextEdit()
strings_text.setPlaceholderText("Sequences Here")

query_line = QLineEdit()
query_line.setPlaceholderText("Query here")

longest_line = QLineEdit()
longest_line.setPlaceholderText("k number")

lcs_line = QLineEdit()
lcs_line.setPlaceholderText("k number")

# Labels
file_label = QLabel("Load_file")
longest_label = QLabel("Longest repeat")
lcs_label = QLabel("LCS")

# Layouts
strings_layout = QVBoxLayout()

strings_bottom_layout = QHBoxLayout()
strings_bottom_layout.addWidget(file_button)
# strings_bottom_layout.addWidget(file_label)
strings_bottom_layout.addWidget(generate_button)

strings_layout.addWidget(strings_text)
strings_layout.addLayout(strings_bottom_layout)

longest_layout = QVBoxLayout()
longest_layout.addWidget(longest_line)
longest_layout.addWidget(longest_button)

lcs_layout = QVBoxLayout()
lcs_layout.addWidget(lcs_line)
lcs_layout.addWidget(lcs_button)

palindrom_layout = QVBoxLayout()
palindrom_layout.addWidget(palindrom_button)

features_layout = QVBoxLayout()
features_layout.addLayout(longest_layout)
features_layout.addLayout(lcs_layout)
features_layout.addLayout(palindrom_layout)


temp_layout = QHBoxLayout()
temp_layout.addLayout(strings_layout)
temp_layout.addLayout(features_layout)

query_layout = QHBoxLayout()
query_layout.addWidget(query_line)
query_layout.addWidget(query_button)


main_layout = QVBoxLayout()
main_layout.addLayout(temp_layout)
main_layout.addLayout(query_layout)

result_label = QTextEdit()
result_label.setPlaceholderText("Result Will be here")
result_label.setEnabled(False)
result_label.setStyleSheet("color: black")
result_label.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
main_layout.addWidget(result_label)

status_layout = QHBoxLayout()
status_bar = QLabel("Ready")
status_bar.setStyleSheet("color: blue")
status_layout.addWidget(status_bar)
status_layout.addWidget(save_button)

main_layout.addLayout(status_layout)

window.setLayout(main_layout)
window.show()
### END UI

### GLOBAL variables
suffix_tree = None
file_name = ""
ans = ""
positions = ""


### UI Functionalities

#File button
def open_file_name_dialog():
    global file_name
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fileName, _ = QFileDialog.getOpenFileName(window, "QFileDialog.getOpenFileName()", "","All Files (*);;fasta files (*.fasta)", options=options)
    file_name = fileName if fileName else ""
    status_bar.setText("File load successfully")

file_button.clicked.connect(open_file_name_dialog)

#Generate buttom
def on_generate_button_click():
    global file_name, suffix_tree
    if file_name:
        suffix_tree = generate_tree_from_file(file_name)
    else:
        tmp = strings_text.toPlainText().strip().replace(">\n", "").split("\n")
        texts = [x for x in tmp if x != '']
        if len(texts) == 0:
            return QMessageBox.warning(window, "Error!", "Neither file or text not provided", QMessageBox.Ok, QMessageBox.Ok)
        suffix_tree = generate_tree(texts)
    status_bar.setText("Tree generated successfully")

generate_button.clicked.connect(on_generate_button_click)

#Query button
def on_query_button_click():
    global suffix_tree, positions
    if suffix_tree == None:
        return QMessageBox.warning(window, "Error!", "Tree did not be generated!", QMessageBox.Ok, QMessageBox.Ok)
    query = query_line.text().strip()
    if query == "":
        return QMessageBox.warning(window, "Error!", "Enter Query!", QMessageBox.Ok, QMessageBox.Ok)
    positions = find_all(suffix_tree, query)
    result_label.setText(str(positions))
        

query_button.clicked.connect(on_query_button_click)

#Longest button
def on_longest_button_click():
    global suffix_tree, ans, positions
    if suffix_tree == None:
        return QMessageBox.warning(window, "Error!", "Tree did not be generated!", QMessageBox.Ok, QMessageBox.Ok)
    if longest_line.text().strip() == "":
        return QMessageBox.warning(window, "Error!", "Enter K parameter!", QMessageBox.Ok, QMessageBox.Ok)
    k = int(longest_line.text())
    ans, positions = find_repeats(suffix_tree, k)
    result_label.setText(str(ans) + "\n" + str(positions))


longest_button.clicked.connect(on_longest_button_click)

#LCS button
def on_lcs_button_click():
    global suffix_tree, ans, positions
    if suffix_tree == None:
        return QMessageBox.warning(window, "Error!", "Tree did not be generated!", QMessageBox.Ok, QMessageBox.Ok)
    if lcs_line.text().strip() == "":
        return QMessageBox.warning(window, "Error!", "Enter K parameter!", QMessageBox.Ok, QMessageBox.Ok)
    k = int(lcs_line.text())
    ans, positions = find_lcs(suffix_tree, k)
    result_label.setText(str(ans) + "\n" + str(positions))



lcs_button.clicked.connect(on_lcs_button_click)

#Palindrom button
def on_palindrom_button_click():
    global ans, positions, file_name
    if file_name:
        text = open(file_name).read().strip().replace(">\n", "").split("\n")[0]
    else:
        text = strings_text.toPlainText().strip().replace(">\n", "").split("\n")[0]
    ans, positions = find_palindrom(text)
    result_label.setText(str(ans) + "\n" + str(positions))

palindrom_button.clicked.connect(on_palindrom_button_click)

#Save button
def on_save_button_click():
    global ans, positions
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fileName, _ = QFileDialog.getSaveFileName(window,"QFileDialog.getSaveFileName()","","Text Files (*.txt)", options=options)
    if fileName and positions:
        if not fileName[-4:] == '.txt':
            fileName = fileName + ".txt"
        handler = open(fileName, "w+")
        handler.write(ans + "\n")
        handler.write(str(positions))

save_button.clicked.connect(on_save_button_click)

app.exec_()
