from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QMessageBox, 
                             QMenu, QComboBox, QLabel)
from PyQt6.QtCore import Qt, QTimer
from datetime import datetime


class AlertManager(QWidget):
    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager
        self.init_ui()
        self.start_checking()

    def init_ui(self):
        layout = QVBoxLayout()
        
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel('告警级别:'))
        
        self.level_combo = QComboBox()
        self.level_combo.addItems(['全部', '紧急', '重要', '一般', '提示'])
        filter_layout.addWidget(self.level_combo)
        
        filter_layout.addWidget(QLabel('状态:'))
        self.status_combo = QComboBox()
        self.status_combo.addItems(['全部', '未处理', '处理中', '已处理'])
        filter_layout.addWidget(self.status_combo)
        
        query_btn = QPushButton('查询')
        query_btn.clicked.connect(self.query_alerts)
        filter_layout.addWidget(query_btn)
        
        refresh_btn = QPushButton('刷新')
        refresh_btn.clicked.connect(self.refresh_data)
        filter_layout.addWidget(refresh_btn)
        
        layout.addLayout(filter_layout)
        
        btn_layout = QHBoxLayout()
        handle_btn = QPushButton('处理告警')
        handle_btn.clicked.connect(self.handle_alert)
        btn_layout.addWidget(handle_btn)
        
        ignore_btn = QPushButton('忽略告警')
        ignore_btn.clicked.connect(self.ignore_alert)
        btn_layout.addWidget(ignore_btn)
        
        delete_btn = QPushButton('删除告警')
        delete_btn.clicked.connect(self.delete_alert)
        btn_layout.addWidget(delete_btn)
        
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

    def start_checking(self):
        self.check_timer = QTimer()
        self.check_timer.timeout.connect(self.check_new_alerts)
        self.check_timer.start(30000)

    def check_new_alerts(self):
        # 检查新告警逻辑位置留空
        # 后续补充
        pass

    def refresh_data(self):
        self.table.clear()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['ID', '标题', '级别', '来源', '状态', '时间', '描述'])
        self.table.setRowCount(len(self.data_manager.alerts))
        
        for row, alert in enumerate(self.data_manager.alerts):
            self.table.setItem(row, 0, QTableWidgetItem(str(alert.get('id', ''))))
            self.table.setItem(row, 1, QTableWidgetItem(alert.get('title', '')))
            self.table.setItem(row, 2, QTableWidgetItem(alert.get('level', '')))
            self.table.setItem(row, 3, QTableWidgetItem(alert.get('source', '')))
            self.table.setItem(row, 4, QTableWidgetItem(alert.get('status', '')))
            self.table.setItem(row, 5, QTableWidgetItem(alert.get('time', '')))
            self.table.setItem(row, 6, QTableWidgetItem(alert.get('description', '')))

    def query_alerts(self):
        # 告警查询业务规则引擎位置留空
        # 后续补充
        QMessageBox.information(self, '提示', '查询功能待实现')

    def handle_alert(self):
        # 告警处理状态流转逻辑位置留空
        # 后续补充
        QMessageBox.information(self, '提示', '处理功能待实现')

    def ignore_alert(self):
        QMessageBox.information(self, '提示', '忽略功能待实现')

    def delete_alert(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, '提示', '请选择要删除的告警')
            return
        
        reply = QMessageBox.question(self, '确认', '确定要删除吗？', 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            # 删除数据一致性处理位置留空
            # 后续补充
            
            self.data_manager.alerts.pop(selected)
            self.data_manager.save_all()
            self.refresh_data()
            QMessageBox.information(self, '提示', '删除成功')

    def show_context_menu(self, pos):
        menu = QMenu()
        menu.addAction('处理', self.handle_alert)
        menu.addAction('忽略', self.ignore_alert)
        menu.addSeparator()
        menu.addAction('删除', self.delete_alert)
        menu.addSeparator()
        menu.addAction('刷新', self.refresh_data)
        menu.exec(self.table.mapToGlobal(pos))
