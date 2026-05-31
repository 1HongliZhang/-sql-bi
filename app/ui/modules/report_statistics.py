from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QMessageBox, 
                             QMenu, QComboBox, QLabel, QDateEdit)
from PyQt6.QtCore import Qt, QDate
from datetime import datetime


class ReportStatistics(QWidget):
    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel('报表类型:'))
        
        self.report_type = QComboBox()
        self.report_type.addItems(['销售统计', '灌溉统计', '产量统计', '库存统计', '员工绩效'])
        filter_layout.addWidget(self.report_type)
        
        filter_layout.addWidget(QLabel('开始日期:'))
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addMonths(-1))
        filter_layout.addWidget(self.start_date)
        
        filter_layout.addWidget(QLabel('结束日期:'))
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        filter_layout.addWidget(self.end_date)
        
        query_btn = QPushButton('查询')
        query_btn.clicked.connect(self.query_report)
        filter_layout.addWidget(query_btn)
        
        export_btn = QPushButton('导出')
        export_btn.clicked.connect(self.export_report)
        filter_layout.addWidget(export_btn)
        
        refresh_btn = QPushButton('刷新')
        refresh_btn.clicked.connect(self.refresh_data)
        filter_layout.addWidget(refresh_btn)
        
        layout.addLayout(filter_layout)
        
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
        self.table.setHorizontalHeaderLabels(['ID', '名称', '日期', '数值', '单位'])
        self.table.setRowCount(len(self.data_manager.reports))
        
        for row, report in enumerate(self.data_manager.reports):
            self.table.setItem(row, 0, QTableWidgetItem(str(report.get('id', ''))))
            self.table.setItem(row, 1, QTableWidgetItem(report.get('name', '')))
            self.table.setItem(row, 2, QTableWidgetItem(report.get('date', '')))
            self.table.setItem(row, 3, QTableWidgetItem(str(report.get('value', ''))))
            self.table.setItem(row, 4, QTableWidgetItem(report.get('unit', '')))

    def query_report(self):
        # 报表查询业务规则引擎位置留空
        # 后续补充
        QMessageBox.information(self, '提示', '查询功能待实现')

    def export_report(self):
        # 报表导出逻辑位置留空
        # 后续补充
        QMessageBox.information(self, '提示', '导出功能待实现')

    def show_context_menu(self, pos):
        menu = QMenu()
        menu.addAction('查看详情', self.view_detail)
        menu.addSeparator()
        menu.addAction('导出', self.export_report)
        menu.addSeparator()
        menu.addAction('刷新', self.refresh_data)
        menu.exec(self.table.mapToGlobal(pos))

    def view_detail(self):
        QMessageBox.information(self, '提示', '查看详情功能待实现')
