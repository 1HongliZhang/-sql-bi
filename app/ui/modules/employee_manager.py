from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QMessageBox, 
                             QMenu)
from PyQt6.QtCore import Qt
from datetime import datetime


class EmployeeManager(QWidget):
    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        btn_layout = QHBoxLayout()
        add_btn = QPushButton('新增员工')
        add_btn.clicked.connect(self.add_employee)
        btn_layout.addWidget(add_btn)
        
        edit_btn = QPushButton('编辑员工')
        edit_btn.clicked.connect(self.edit_employee)
        btn_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton('删除员工')
        delete_btn.clicked.connect(self.delete_employee)
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
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(['ID', '姓名', '工号', '职位', '部门', '电话', '入职日期', '状态'])
        self.table.setRowCount(len(self.data_manager.employees))
        
        for row, emp in enumerate(self.data_manager.employees):
            self.table.setItem(row, 0, QTableWidgetItem(str(emp.get('id', ''))))
            self.table.setItem(row, 1, QTableWidgetItem(emp.get('name', '')))
            self.table.setItem(row, 2, QTableWidgetItem(emp.get('employee_id', '')))
            self.table.setItem(row, 3, QTableWidgetItem(emp.get('position', '')))
            self.table.setItem(row, 4, QTableWidgetItem(emp.get('department', '')))
            self.table.setItem(row, 5, QTableWidgetItem(emp.get('phone', '')))
            self.table.setItem(row, 6, QTableWidgetItem(emp.get('hire_date', '')))
            self.table.setItem(row, 7, QTableWidgetItem(emp.get('status', '')))

    def add_employee(self):
        # 新增员工审批流程位置留空
        # 后续补充
        QMessageBox.information(self, '提示', '新增功能待实现')

    def edit_employee(self):
        # 编辑员工状态流转逻辑位置留空
        # 后续补充
        QMessageBox.information(self, '提示', '编辑功能待实现')

    def delete_employee(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, '提示', '请选择要删除的员工')
            return
        
        reply = QMessageBox.question(self, '确认', '确定要删除吗？', 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            # 删除数据一致性处理位置留空
            # 后续补充
            
            self.data_manager.employees.pop(selected)
            self.data_manager.save_all()
            self.refresh_data()
            QMessageBox.information(self, '提示', '删除成功')

    def show_context_menu(self, pos):
        menu = QMenu()
        menu.addAction('新增', self.add_employee)
        menu.addAction('编辑', self.edit_employee)
        menu.addAction('删除', self.delete_employee)
        menu.addSeparator()
        menu.addAction('查看详情', self.view_detail)
        menu.addSeparator()
        menu.addAction('刷新', self.refresh_data)
        menu.exec(self.table.mapToGlobal(pos))

    def view_detail(self):
        QMessageBox.information(self, '提示', '查看详情功能待实现')
