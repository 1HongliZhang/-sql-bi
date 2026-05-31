from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QMessageBox, 
                             QTimer, QMenu)
from PyQt6.QtCore import Qt
from datetime import datetime


class SensorMonitor(QWidget):
    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager
        self.init_ui()
        self.start_refresh_timer()

    def init_ui(self):
        layout = QVBoxLayout()
        
        btn_layout = QHBoxLayout()
        add_btn = QPushButton('新增传感器')
        add_btn.clicked.connect(self.add_sensor)
        btn_layout.addWidget(add_btn)
        
        edit_btn = QPushButton('编辑传感器')
        edit_btn.clicked.connect(self.edit_sensor)
        btn_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton('删除传感器')
        delete_btn.clicked.connect(self.delete_sensor)
        btn_layout.addWidget(delete_btn)
        
        refresh_btn = QPushButton('立即刷新')
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

    def start_refresh_timer(self):
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.auto_refresh)
        self.refresh_timer.start(5000)

    def auto_refresh(self):
        # 传感器数据实时更新逻辑位置留空
        # 后续补充
        pass

    def refresh_data(self):
        self.table.clear()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['ID', '名称', '类型', '大棚', '当前值', '状态', '更新时间'])
        self.table.setRowCount(len(self.data_manager.sensors))
        
        for row, sensor in enumerate(self.data_manager.sensors):
            self.table.setItem(row, 0, QTableWidgetItem(str(sensor.get('id', ''))))
            self.table.setItem(row, 1, QTableWidgetItem(sensor.get('name', '')))
            self.table.setItem(row, 2, QTableWidgetItem(sensor.get('type', '')))
            self.table.setItem(row, 3, QTableWidgetItem(sensor.get('greenhouse', '')))
            self.table.setItem(row, 4, QTableWidgetItem(str(sensor.get('current_value', ''))))
            self.table.setItem(row, 5, QTableWidgetItem(sensor.get('status', '')))
            self.table.setItem(row, 6, QTableWidgetItem(sensor.get('update_time', '')))

    def add_sensor(self):
        # 新增传感器业务逻辑位置留空
        # 后续补充
        QMessageBox.information(self, '提示', '新增功能待实现')

    def edit_sensor(self):
        # 编辑传感器逻辑位置留空
        # 后续补充
        QMessageBox.information(self, '提示', '编辑功能待实现')

    def delete_sensor(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, '提示', '请选择要删除的传感器')
            return
        
        reply = QMessageBox.question(self, '确认', '确定要删除吗？', 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.data_manager.sensors.pop(selected)
            self.data_manager.save_all()
            self.refresh_data()
            QMessageBox.information(self, '提示', '删除成功')

    def show_context_menu(self, pos):
        menu = QMenu()
        menu.addAction('新增', self.add_sensor)
        menu.addAction('编辑', self.edit_sensor)
        menu.addAction('删除', self.delete_sensor)
        menu.addSeparator()
        menu.addAction('查看历史数据', self.view_history)
        menu.addSeparator()
        menu.addAction('刷新', self.refresh_data)
        menu.exec(self.table.mapToGlobal(pos))

    def view_history(self):
        # 查看历史数据逻辑位置留空
        # 后续补充
        QMessageBox.information(self, '提示', '查看历史数据功能待实现')
