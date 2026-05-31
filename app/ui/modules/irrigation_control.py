from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QMessageBox, 
                             QMenu, QComboBox, QLabel)
from PyQt6.QtCore import Qt, QTimer
from datetime import datetime


class IrrigationControl(QWidget):
    def __init__(self, data_manager, scheduler):
        super().__init__()
        self.data_manager = data_manager
        self.scheduler = scheduler
        self.init_ui()
        self.start_monitor()

    def init_ui(self):
        layout = QVBoxLayout()
        
        control_layout = QHBoxLayout()
        control_layout.addWidget(QLabel('选择大棚:'))
        
        self.greenhouse_combo = QComboBox()
        self.greenhouse_combo.currentTextChanged.connect(self.on_greenhouse_changed)
        control_layout.addWidget(self.greenhouse_combo)
        
        manual_btn = QPushButton('手动灌溉')
        manual_btn.clicked.connect(self.manual_irrigation)
        control_layout.addWidget(manual_btn)
        
        auto_btn = QPushButton('自动灌溉')
        auto_btn.clicked.connect(self.auto_irrigation)
        control_layout.addWidget(auto_btn)
        
        stop_btn = QPushButton('停止灌溉')
        stop_btn.clicked.connect(self.stop_irrigation)
        control_layout.addWidget(stop_btn)
        
        layout.addLayout(control_layout)
        
        btn_layout = QHBoxLayout()
        add_btn = QPushButton('新增记录')
        add_btn.clicked.connect(self.add_record)
        btn_layout.addWidget(add_btn)
        
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
        self.load_greenhouses()

    def start_monitor(self):
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self.monitor_conditions)
        self.monitor_timer.start(10000)

    def load_greenhouses(self):
        self.greenhouse_combo.clear()
        for gh in self.data_manager.greenhouses:
            self.greenhouse_combo.addItem(gh.get('name', ''), gh)

    def on_greenhouse_changed(self):
        pass

    def monitor_conditions(self):
        # 灌溉条件监控逻辑位置留空
        # 后续补充
        pass

    def manual_irrigation(self):
        # 手动灌溉资源调度逻辑位置留空
        # 后续补充
        QMessageBox.information(self, '提示', '手动灌溉功能待实现')

    def auto_irrigation(self):
        # 基于温湿度阈值的智能灌溉调度算法调用位置留空
        # 后续补充
        QMessageBox.information(self, '提示', '自动灌溉功能待实现')

    def stop_irrigation(self):
        # 停止灌溉状态流转逻辑位置留空
        # 后续补充
        QMessageBox.information(self, '提示', '停止灌溉功能待实现')

    def refresh_data(self):
        self.table.clear()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['ID', '大棚', '类型', '开始时间', '结束时间', '水量'])
        self.table.setRowCount(len(self.data_manager.irrigation_records))
        
        for row, record in enumerate(self.data_manager.irrigation_records):
            self.table.setItem(row, 0, QTableWidgetItem(str(record.get('id', ''))))
            self.table.setItem(row, 1, QTableWidgetItem(record.get('greenhouse', '')))
            self.table.setItem(row, 2, QTableWidgetItem(record.get('type', '')))
            self.table.setItem(row, 3, QTableWidgetItem(record.get('start_time', '')))
            self.table.setItem(row, 4, QTableWidgetItem(record.get('end_time', '')))
            self.table.setItem(row, 5, QTableWidgetItem(str(record.get('water_amount', ''))))

    def add_record(self):
        QMessageBox.information(self, '提示', '新增记录功能待实现')

    def show_context_menu(self, pos):
        menu = QMenu()
        menu.addAction('新增记录', self.add_record)
        menu.addSeparator()
        menu.addAction('查看详情', self.view_detail)
        menu.addSeparator()
        menu.addAction('刷新', self.refresh_data)
        menu.exec(self.table.mapToGlobal(pos))

    def view_detail(self):
        QMessageBox.information(self, '提示', '查看详情功能待实现')
