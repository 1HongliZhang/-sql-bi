from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                             QTableWidgetItem, QPushButton, QMessageBox, 
                             QMenu)
from PyQt6.QtCore import Qt
from datetime import datetime


class InventoryManager(QWidget):
    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        btn_layout = QHBoxLayout()
        add_btn = QPushButton('新增物品')
        add_btn.clicked.connect(self.add_item)
        btn_layout.addWidget(add_btn)
        
        edit_btn = QPushButton('编辑物品')
        edit_btn.clicked.connect(self.edit_item)
        btn_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton('删除物品')
        delete_btn.clicked.connect(self.delete_item)
        btn_layout.addWidget(delete_btn)
        
        in_btn = QPushButton('入库')
        in_btn.clicked.connect(self.stock_in)
        btn_layout.addWidget(in_btn)
        
        out_btn = QPushButton('出库')
        out_btn.clicked.connect(self.stock_out)
        btn_layout.addWidget(out_btn)
        
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
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['ID', '名称', '类型', '数量', '单价', '位置'])
        self.table.setRowCount(len(self.data_manager.inventory))
        
        for row, item in enumerate(self.data_manager.inventory):
            self.table.setItem(row, 0, QTableWidgetItem(str(item.get('id', ''))))
            self.table.setItem(row, 1, QTableWidgetItem(item.get('name', '')))
            self.table.setItem(row, 2, QTableWidgetItem(item.get('type', '')))
            self.table.setItem(row, 3, QTableWidgetItem(str(item.get('quantity', ''))))
            self.table.setItem(row, 4, QTableWidgetItem(str(item.get('price', ''))))
            self.table.setItem(row, 5, QTableWidgetItem(item.get('location', '')))

    def add_item(self):
        # 新增物品业务规则引擎位置留空
        # 后续补充
        QMessageBox.information(self, '提示', '新增功能待实现')

    def edit_item(self):
        QMessageBox.information(self, '提示', '编辑功能待实现')

    def delete_item(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, '提示', '请选择要删除的物品')
            return
        
        reply = QMessageBox.question(self, '确认', '确定要删除吗？', 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            # 删除数据一致性处理位置留空
            # 后续补充
            
            self.data_manager.inventory.pop(selected)
            self.data_manager.save_all()
            self.refresh_data()
            QMessageBox.information(self, '提示', '删除成功')

    def stock_in(self):
        # 入库业务规则引擎位置留空
        # 后续补充
        QMessageBox.information(self, '提示', '入库功能待实现')

    def stock_out(self):
        # 出库业务规则引擎位置留空
        # 后续补充
        QMessageBox.information(self, '提示', '出库功能待实现')

    def show_context_menu(self, pos):
        menu = QMenu()
        menu.addAction('新增', self.add_item)
        menu.addAction('编辑', self.edit_item)
        menu.addAction('删除', self.delete_item)
        menu.addSeparator()
        menu.addAction('入库', self.stock_in)
        menu.addAction('出库', self.stock_out)
        menu.addSeparator()
        menu.addAction('刷新', self.refresh_data)
        menu.exec(self.table.mapToGlobal(pos))
