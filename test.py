import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGroupBox, QLabel, QLineEdit


class Formularz(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Formularz')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        # Grupa dla maila
        group_mail = QGroupBox("Mail")
        layout_mail = QVBoxLayout()
        self.mail_login = QLineEdit()
        self.mail_password = QLineEdit()
        self.mail_login.setPlaceholderText("Login")
        self.mail_password.setPlaceholderText("Hasło")
        self.mail_password.setEchoMode(QLineEdit.Password)  # Ukryj wpisywane znaki
        layout_mail.addWidget(self.mail_login)
        layout_mail.addWidget(self.mail_password)
        group_mail.setLayout(layout_mail)
        layout.addWidget(group_mail)

        # Grupa dla kalendarza
        group_calendar = QGroupBox("Kalendarz")
        layout_calendar = QVBoxLayout()
        self.calendar_login = QLineEdit()
        self.calendar_password = QLineEdit()
        self.calendar_login.setPlaceholderText("Login")
        self.calendar_password.setPlaceholderText("Hasło")
        self.calendar_password.setEchoMode(QLineEdit.Password)  # Ukryj wpisywane znaki
        layout_calendar.addWidget(self.calendar_login)
        layout_calendar.addWidget(self.calendar_password)
        group_calendar.setLayout(layout_calendar)
        layout.addWidget(group_calendar)

        # Grupa dla spotykania
        group_meeting = QGroupBox("Spotkanie")
        layout_meeting = QVBoxLayout()
        self.meeting_login = QLineEdit()
        self.meeting_password = QLineEdit()
        self.meeting_login.setPlaceholderText("Login")
        self.meeting_password.setPlaceholderText("Hasło")
        self.meeting_password.setEchoMode(QLineEdit.Password)  # Ukryj wpisywane znaki
        layout_meeting.addWidget(self.meeting_login)
        layout_meeting.addWidget(self.meeting_password)
        group_meeting.setLayout(layout_meeting)
        layout.addWidget(group_meeting)

        self.setLayout(layout)


def run_app():
    app = QApplication(sys.argv)
    window = Formularz()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run_app()
