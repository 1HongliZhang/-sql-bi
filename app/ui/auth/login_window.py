from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox)
from PyQt6.QtCore import pyqtSignal


class LoginWindow(QWidget):
    login_success = pyqtSignal(dict)
    switch_to_register = pyqtSignal()

    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager
        self.current_user = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('智慧大棚管理系统 - 登录')
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        
        title = QLabel('智慧大棚农业管理系统')
        title.setStyleSheet('font-size: 24px; font-weight: bold; margin: 20px 0;')
        layout.addWidget(title)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('请输入用户名')
        layout.addWidget(self.username_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('请输入密码')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)
        
        btn_layout = QHBoxLayout()
        login_btn = QPushButton('登录')
        login_btn.clicked.connect(self.handle_login)
        btn_layout.addWidget(login_btn)
        
        register_btn = QPushButton('注册')
        register_btn.clicked.connect(self.switch_to_register.emit)
        btn_layout.addWidget(register_btn)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, '提示', '用户名和密码不能为空')
            return
        
        # 登录验证逻辑位置留空
        # 后续补充
        
        user = self._find_user(username, password)
        if user:
            self.current_user = user
            self.login_success.emit(user)
        else:
            QMessageBox.warning(self, '提示', '用户名或密码错误')

    def _find_user(self, username, password):
        for user in self.data_manager.users:
            if user['username'] == username and user['password'] == password:
                return user
        return None
