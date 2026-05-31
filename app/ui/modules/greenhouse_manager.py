from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QMessageBox, 
                             QDialog, QFormLayout, QLineEdit, QComboBox, QMenu)
from PyQt6.QtCore import Qt
from datetime import datetime


class GreenhouseManager(QWidget):
    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        btn_layout = QHBoxLayout()
        add_btn = QPushButton('新增大棚')
        add_btn.clicked.connect(self.add_greenhouse)
        btn_layout.addWidget(add_btn)
        
        edit_btn = QPushButton('编辑大棚')
        edit_btn.clicked.connect(self.edit_greenhouse)
        btn_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton('删除大棚')
        delete_btn.clicked.connect(self.delete_greenhouse)
        btn_layout.addWidget(delete_btn)
        
        refresh_btn = QPushButton('刷新')
        refresh_btn.clicked.connect(self.refresh_data)
        btn_layout.addWidget(refresh_btn)
        
        layout.addLayout(btn_layout)
        
        self.table = QTableWidget()
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setDragDropMode(QTableWidget.DragDropMode.InternalMove)
        self.table.setDragEnabled(True)
        self.table.setAcceptDrops(True)
        self.table.setDropIndicatorShown(True)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        self.refresh_data()

    def refresh_data(self):
        self.table.clear()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['ID', '名称', '位置', '面积', '状态'])
        self.table.setRowCount(len(self.data_manager.greenhouses))
        
        for row, gh in enumerate(self.data_manager.greenhouses):
            self.table.setItem(row, 0, QTableWidgetItem(str(gh.get('id', ''))))
            self.table.setItem(row, 1, QTableWidgetItem(gh.get('name', '')))
            self.table.setItem(row, 2, QTableWidgetItem(gh.get('location', '')))
            self.table.setItem(row, 3, QTableWidgetItem(str(gh.get('area', ''))))
            self.table.setItem(row, 4, QTableWidgetItem(gh.get('status', '')))

    def add_greenhouse(self):
        dialog = GreenhouseDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            # 数据一致性处理位置留空
            # 后续补充
            
            new_gh = {
                'id': len(self.data_manager.greenhouses) + 1,
                'name': data['name'],
                'location': data['location'],
                'area': data['area'],
                'status': 'active',
                'create_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            self.data_manager.greenhouses.append(new_gh)
            self.data_manager.save_all()
            self.refresh_data()
            QMessageBox.information(self, '提示', '添加成功')

    def edit_greenhouse(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, '提示', '请选择要编辑的大棚')
            return
        
        gh = self.data_manager.greenhouses[selected]
        dialog = GreenhouseDialog(self, gh)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            # 状态流转逻辑位置留空
            # 后续补充
            
            self.data_manager.greenhouses[selected].update(data)
            self.data_manager.save_all()
            self.refresh_data()
            QMessageBox.information(self, '提示', '编辑成功')

    def delete_greenhouse(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, '提示', '请选择要删除的大棚')
            return
        
        reply = QMessageBox.question(self, '确认', '确定要删除吗？', 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            # 删除审批逻辑位置留空
            # 后续补充
            
            self.data_manager.greenhouses.pop(selected)
            self.data_manager.save_all()
            self.refresh_data()
            QMessageBox.information(self, '提示', '删除成功')

    def show_context_menu(self, pos):
        menu = QMenu()
        menu.addAction('新增', self.add_greenhouse)
        menu.addAction('编辑', self.edit_greenhouse)
        menu.addAction('删除', self.delete_greenhouse)
        menu.addSeparator()
        menu.addAction('刷新', self.refresh_data)
        menu.exec(self.table.mapToGlobal(pos))


class GreenhouseDialog(QDialog):
    def __init__(self, parent, data=None):
        super().__init__(parent)
        self.data = data
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('大棚信息')
        self.setFixedSize(300, 250)
        
        layout = QFormLayout()
        
        self.name_input = QLineEdit()
        if self.data:
            self.name_input.setText(self.data.get('name', ''))
        layout.addRow('名称:', self.name_input)
        
        self.location_input = QLineEdit()
        if self.data:
            self.location_input.setText(self.data.get('location', ''))
        layout.addRow('位置:', self.location_input)
        
        self.area_input = QLineEdit()
        if self.data:
            self.area_input.setText(str(self.data.get('area', '')))
        layout.addRow('面积:', self.area_input)
        
        self.status_combo = QComboBox()
        self.status_combo.addItems(['active', 'inactive', 'maintenance'])
        if self.data:
            self.status_combo.setCurrentText(self.data.get('status', 'active'))
        layout.addRow('状态:', self.status_combo)
        
        btn_layout = QHBoxLayout()
        ok_btn = QPushButton('确定')
        ok_btn.clicked.connect(self.accept)
        btn_layout.addWidget(ok_btn)
        
        cancel_btn = QPushButton('取消')
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        layout.addRow(btn_layout)
        self.setLayout(layout)

    def get_data(self):
        return {
            'name': self.name_input.text(),
            'location': self.location_input.text(),
            'area': float(self.area_input.text()) if self.area_input.text() else 0,
            'status': self.status_combo.currentText()
        }
