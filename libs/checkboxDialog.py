from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QDialog, QVBoxLayout, QHBoxLayout, QRadioButton, QPushButton, QLabel, QGroupBox

class CheckboxDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rate Your Preferences")
        self.setMinimumSize(300, 400)

        # Layout for the dialog
        self.layout = QVBoxLayout()

        # Dictionary to store the radio buttons for each question
        self.question_ratings = {}

        # Questions and their options
        self.questions = [
            ("Q1", ['1', '2', '3', '4', '5']),
            ("Q2", ['1', '2', '3', '4', '5']),
            ("Q3", ['A', 'B', 'C']),
            ("Q4", ['A', 'B', 'C']),
        ]

        # Create a group of radio buttons for each question
        for question, options in self.questions:
            group_box = QGroupBox(question)
            radio_layout = QVBoxLayout()

            # Store radio buttons in a dictionary for each question
            radio_buttons = []
            for option in options:
                radio_button = QRadioButton(option)
                radio_layout.addWidget(radio_button)
                radio_buttons.append(radio_button)

            # Store the radio buttons for each question
            self.question_ratings[question] = radio_buttons

            group_box.setLayout(radio_layout)
            self.layout.addWidget(group_box)

        # Add OK Button
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)  # Close dialog on OK
        self.layout.addWidget(self.ok_button)

        self.setLayout(self.layout)

    def get_selected_ratings(self):
        """Return the selected ratings for each question."""
        ratings = []
        for question, radio_buttons in self.question_ratings.items():
            selected = None
            for radio_button in radio_buttons:
                if radio_button.isChecked():
                    selected = radio_button.text()
                    break
            ratings.append(selected)
        return ratings

