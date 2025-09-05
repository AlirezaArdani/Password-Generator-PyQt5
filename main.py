from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QSlider, QCheckBox, QProgressBar
from PyQt5 import uic
import sys
import string
from secrets import choice, SystemRandom
import resources
from PyQt5.QtCore import QTimer


class PasswordGenerator(QMainWindow):
    def __init__(self):
        super(PasswordGenerator, self).__init__()
        '''
        --- Password Characters Option ---
        uppercase : ABCDEFGHIJKLMNOPQRSTUVWXYZ
        lowercase : abcdefghijklmnopqrstuvwxyz
        digits : 0123456789
        symbols : !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
        '''
        self.UPPERCASE = string.ascii_uppercase
        self.LOWERCASE = string.ascii_lowercase
        self.SYMBOLS = string.punctuation
        self.NUMBERS = string.digits

        self.initUi()

    def initUi(self):
        # Load Ui
        uic.loadUi('password_generator.ui', self)

        # Define and Modify Widgets
        self.passwordOutput = self.findChild(QLineEdit, 'generatedPasswordLineEdit')
        self.copyToClipboardButton = self.findChild(QPushButton, 'copyPushButton')
        self.passwordLengthLabel = self.findChild(QLabel, 'passwordLengthLabel')
        self.sliderValueLabel = self.findChild(QLabel, 'sliderValueLabel')
        self.passwordLengthSlider = self.findChild(QSlider, 'passwordLengthSlider')
        # Check Boxes
        self.uppercaseCheckBox = self.findChild(QCheckBox, 'uppercaseCheckBox')
        self.lowercaseCheckBox = self.findChild(QCheckBox, 'lowercaseCheckBox')
        self.numbersCheckBox = self.findChild(QCheckBox, 'numbersCheckBox')
        self.symbolCheckBox = self.findChild(QCheckBox, 'symbolCheckBox')

        # Strength
        self.strengthLabel = self.findChild(QLabel, 'passwordStrengthLabel')
        self.strengthProgressBar = self.findChild(QProgressBar, 'passwordStrengthProgressBar')
        self.strengthProgressBar.setRange(0, 100)
        self.strengthProgressBar.setValue(0)
        # Generate Password Button
        self.generateButton = self.findChild(QPushButton, 'generatePushButton')


        # connect signals to buttons
        self.copyToClipboardButton.clicked.connect(self.copy_to_clipboard)
        self.passwordLengthSlider.valueChanged.connect(self.update_slider)
        self.generateButton.clicked.connect(self.generate_password)

        self.generate_password()

    def copy_to_clipboard(self):
        # Copy Password
        clipboard = QApplication.clipboard()
        clipboard.setText(self.passwordOutput.text())
        # Show When Copied
        # QMessageBox.about(self, '    Copy To Clipboard    ', 'Password Copied!')
        # print('Password Copied! ---- {} ----'.format(clipboard.text()))
        org_text = self.passwordOutput.text()
        self.passwordOutput.setStyleSheet("background-color:#3B4252;color:green;border-color:#3B4252;")
        self.passwordOutput.setText("Copied!")

        QTimer.singleShot(1500, lambda: (
            self.passwordOutput.setText(org_text),
            self.passwordOutput.setStyleSheet("background-color:#3B4252;color:#E6E6E6;border-color:#3B4252;")
        ))

    def generate_password(self):

        # Store options that we use in password
        selected_characters = []
        password = []
        # Length of password
        length = self.passwordLengthSlider.value()
        # length = int(self.sliderValueLabel.text())
        print(length)
        try:
            # Check which options will be included in password, make sure to have at least one of these options characters
            if self.uppercaseCheckBox.isChecked():
                selected_characters.extend(list(self.UPPERCASE))
                password.append(choice(list(self.UPPERCASE)))

            if self.lowercaseCheckBox.isChecked():
                selected_characters.extend(list(self.LOWERCASE))
                password.append(choice(list(self.LOWERCASE)))

            if self.numbersCheckBox.isChecked():
                selected_characters.extend(list(self.NUMBERS))
                password.append(choice(list(self.NUMBERS)))

            if self.symbolCheckBox.isChecked():
                selected_characters.extend(list(self.SYMBOLS))
                password.append(choice(list(self.SYMBOLS)))
            print(password)
            # print(selected_characters)

            # handle if no checkbox checked
            if not selected_characters:
                self.passwordOutput.setText("Please select at least one character set.")
                self.strengthProgressBar.setValue(0)
                return

            if length > len(selected_characters):
                self.passwordOutput.setText("Password is longer than characters set length.")

            else:
                remaining_length = length - len(password)
                # use secrets.choice() instead in loop
                # temp = sample(selected_characters,remaining_length)
                for _ in range(remaining_length):
                    password.append(choice(selected_characters))

                print(password)
                # use random.sample()
                # temp = sample(selected_characters, remaining_length)
                # password.extend(temp)

                # Shuffle list using secrets shuffle
                SystemRandom().shuffle(password)
                print(password)
                # Create password
                final_password = ''.join(password)
                print(final_password)
                self.passwordOutput.setText(final_password)
                self.update_password_strength()

        except Exception as e:
            self.passwordOutput.setText(f"{str(e)}")

    def update_slider(self, slider_value):
        self.sliderValueLabel.setText(str(slider_value))

    def update_password_strength(self):
        used_char = 0
        score = 0
        length = len(self.passwordOutput.text())
        # score base on length
        if length >= 8:
            score += 20
        if length >= 16:
            score += 20
        if length >= 30:
            score += 20
        # score if  any of characters used
        if self.uppercaseCheckBox.isChecked():
            used_char += 1
        if self.lowercaseCheckBox.isChecked():
            used_char += 1
        if self.numbersCheckBox.isChecked():
            used_char += 1
        if self.symbolCheckBox.isChecked():
            used_char += 1
        # score base on used characters
        if used_char == 2:
            score += 20
        if used_char == 3:
            score += 30
        if used_char == 4:
            score += 40
        print(score)
        self.strengthProgressBar.setValue(score)

        if score <= 40:
            color = "#E3CF10"
        elif score <= 60:
            color = "#E36110"
        elif 75 <= score < 90:
            color = "#10E337"
        elif score >= 90:
            color = "#1E5E1A"

        self.strengthProgressBar.setStyleSheet(f"QProgressBar::chunk{{ background-color:{color}; }}")


# Initialize App
app = QApplication(sys.argv)
password_generator = PasswordGenerator()
# Show App
password_generator.show()
sys.exit(app.exec_())
