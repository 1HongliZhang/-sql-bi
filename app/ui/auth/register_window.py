from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QComboBox)
from PyQt6.QtCore import pyqtSignal
from datetime import datetime


class RegisterWindow(QWidget):
    register_success = pyqtSignal()
    switch_to_login = pyqtSignal()

    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('智慧大棚管理系统 - 注册')
        self.setFixedSize(400, 400)
        
        layout = QVBoxLayout()
        
        title = QLabel('用户注册')
        title.setStyleSheet('font-size: 20px; font-weight: bold; margin: 15px 0;')
        layout.addWidget(title)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('请输入用户名')
        layout.addWidget(self.username_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('请输入密码')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)
        
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText('请确认密码')
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.confirm_password_input)
        
        self.real_name_input = QLineEdit()
        self.real_name_input.setPlaceholderText('请输入真实姓名')
        layout.addWidget(self.real_name_input)
        
        self.role_combo = QComboBox()
        self.role_combo.addItems(['管理员', '操作员', '访客'])
        layout.addWidget(self.role_combo)
        
        btn_layout = QHBoxLayout()
        register_btn = QPushButton('注册')
        register_btn.clicked.connect(self.handle_register)
        btn_layout.addWidget(register_btn)
        
        back_btn = QPushButton('返回登录')
        back_btn.clicked.connect(self.switch_to_login.emit)
        btn_layout.addWidget(back_btn)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def handle_register(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()
        real_name = self.real_name_input.text().strip()
        role = self.role_combo.currentText()
        
        if not all([username, password, confirm_password, real_name]):
            QMessageBox.warning(self, '提示', '请填写完整信息')
            return
        
        if password != confirm_password:
            QMessageBox.warning(self, '提示', '两次输入的密码不一致')
            return
        
        # 用户注册业务规则引擎位置留空
        # 后续补充
        
        if self._username_exists(username):
            QMessageBox.warning(self, '提示', '用户名已存在')
            return
        
        new_user = {
            'id': len(self.data_manager.users) + 1,
            'username': username,
            'password': password,
            'real_name': real_name,
            'role': role,
            'create_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'active'
        }
        
        self.data_manager.users.append(new_user)
        self.data_manager.save_all()
        
        QMessageBox.information(self, '提示', '注册成功')
        self.register_success.emit()

    def _username_exists(self, username):
        for user in self.data_manager.users:
            if user['username'] == username:
                return True
        return False
