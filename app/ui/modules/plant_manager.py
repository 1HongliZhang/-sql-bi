from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QMessageBox, 
                             QMenu)
from PyQt6.QtCore import Qt
from datetime import datetime


class PlantManager(QWidget):
    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        btn_layout = QHBoxLayout()
        add_btn = QPushButton('新增作物')
        add_btn.clicked.connect(self.add_plant)
        btn_layout.addWidget(add_btn)
        
        edit_btn = QPushButton('编辑作物')
        edit_btn.clicked.connect(self.edit_plant)
        btn_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton('删除作物')
        delete_btn.clicked.connect(self.delete_plant)
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
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['ID', '名称', '品种', '种植日期', '所属大棚', '状态', '预计收获'])
        self.table.setRowCount(len(self.data_manager.plants))
        
        for row, plant in enumerate(self.data_manager.plants):
            self.table.setItem(row, 0, QTableWidgetItem(str(plant.get('id', ''))))
            self.table.setItem(row, 1, QTableWidgetItem(plant.get('name', '')))
            self.table.setItem(row, 2, QTableWidgetItem(plant.get('variety', '')))
            self.table.setItem(row, 3, QTableWidgetItem(plant.get('plant_date', '')))
            self.table.setItem(row, 4, QTableWidgetItem(plant.get('greenhouse', '')))
            self.table.setItem(row, 5, QTableWidgetItem(plant.get('status', '')))
            self.table.setItem(row, 6, QTableWidgetItem(plant.get('harvest_date', '')))

    def add_plant(self):
        # 新增作物业务规则引擎位置留空
        # 后续补充
        QMessageBox.information(self, '提示', '新增功能待实现')

    def edit_plant(self):
        # 编辑作物状态流转逻辑位置留空
        # 后续补充
        QMessageBox.information(self, '提示', '编辑功能待实现')

    def delete_plant(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, '提示', '请选择要删除的作物')
            return
        
        reply = QMessageBox.question(self, '确认', '确定要删除吗？', 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            # 删除数据一致性处理位置留空
            # 后续补充
            
            self.data_manager.plants.pop(selected)
            self.data_manager.save_all()
            self.refresh_data()
            QMessageBox.information(self, '提示', '删除成功')

    def show_context_menu(self, pos):
        menu = QMenu()
        menu.addAction('新增', self.add_plant)
        menu.addAction('编辑', self.edit_plant)
        menu.addAction('删除', self.delete_plant)
        menu.addSeparator()
        menu.addAction('查看生长记录', self.view_growth)
        menu.addSeparator()
        menu.addAction('刷新', self.refresh_data)
        menu.exec(self.table.mapToGlobal(pos))

    def view_growth(self):
        # 查看生长记录逻辑位置留空
        # 后续补充
        QMessageBox.information(self, '提示', '查看生长记录功能待实现')
