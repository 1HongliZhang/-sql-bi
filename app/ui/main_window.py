from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QStackedWidget, QListWidget, QListWidgetItem, 
                             QLabel, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from pathlib import Path

from app.ui.auth import LoginWindow, RegisterWindow
from app.ui.modules import (
    GreenhouseManager, SensorMonitor, PlantManager, 
    IrrigationControl, TaskManager, InventoryManager,
    EmployeeManager, ReportStatistics, AlertManager
)
from app.models import DataManager, IrrigationScheduler
from app.core import HotReloader


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data_manager = DataManager()
        self.irrigation_scheduler = IrrigationScheduler()
        self.current_user = None
        self.init_ui()
        self.setup_hot_reload()

    def init_ui(self):
        self.setWindowTitle('智慧大棚农业管理系统')
        self.setMinimumSize(1200, 800)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        main_layout = QVBoxLayout(self.central_widget)
        
        self.stacked_widget = QStackedWidget()
        
        self.login_window = LoginWindow(self.data_manager)
        self.login_window.login_success.connect(self.on_login_success)
        self.login_window.switch_to_register.connect(self.show_register)
        self.stacked_widget.addWidget(self.login_window)
        
        self.register_window = RegisterWindow(self.data_manager)
        self.register_window.register_success.connect(self.show_login)
        self.register_window.switch_to_login.connect(self.show_login)
        self.stacked_widget.addWidget(self.register_window)
        
        self.main_app_widget = None
        main_layout.addWidget(self.stacked_widget)
        
        self.show_login()

    def setup_hot_reload(self):
        self.hot_reloader = HotReloader(self)
        self.hot_reloader.module_reloaded.connect(self.on_module_reloaded)
        
        project_root = Path(__file__).parent.parent.parent
        for py_file in project_root.rglob('*.py'):
            self.hot_reloader.add_watch(str(py_file))

    def on_module_reloaded(self, file_path):
        pass

    def show_login(self):
        self.stacked_widget.setCurrentWidget(self.login_window)

    def show_register(self):
        self.stacked_widget.setCurrentWidget(self.register_window)

    def on_login_success(self, user):
        self.current_user = user
        self.init_main_app()
        self.stacked_widget.setCurrentWidget(self.main_app_widget)

    def init_main_app(self):
        if self.main_app_widget is None:
            self.main_app_widget = QWidget()
            main_layout = QHBoxLayout(self.main_app_widget)
            
            self.menu_list = QListWidget()
            self.menu_list.setFixedWidth(200)
            
            menus = [
                '大棚管理',
                '传感器监控',
                '作物管理',
                '灌溉控制',
                '任务管理',
                '库存管理',
                '员工管理',
                '报表统计',
                '告警管理'
            ]
            
            for menu in menus:
                item = QListWidgetItem(menu)
                self.menu_list.addItem(item)
            
            self.menu_list.currentRowChanged.connect(self.switch_module)
            main_layout.addWidget(self.menu_list)
            
            self.module_stack = QStackedWidget()
            
            self.greenhouse_manager = GreenhouseManager(self.data_manager)
            self.module_stack.addWidget(self.greenhouse_manager)
            
            self.sensor_monitor = SensorMonitor(self.data_manager)
            self.module_stack.addWidget(self.sensor_monitor)
            
            self.plant_manager = PlantManager(self.data_manager)
            self.module_stack.addWidget(self.plant_manager)
            
            self.irrigation_control = IrrigationControl(self.data_manager, self.irrigation_scheduler)
            self.module_stack.addWidget(self.irrigation_control)
            
            self.task_manager = TaskManager(self.data_manager)
            self.module_stack.addWidget(self.task_manager)
            
            self.inventory_manager = InventoryManager(self.data_manager)
            self.module_stack.addWidget(self.inventory_manager)
            
            self.employee_manager = EmployeeManager(self.data_manager)
            self.module_stack.addWidget(self.employee_manager)
            
            self.report_statistics = ReportStatistics(self.data_manager)
            self.module_stack.addWidget(self.report_statistics)
            
            self.alert_manager = AlertManager(self.data_manager)
            self.module_stack.addWidget(self.alert_manager)
            
            main_layout.addWidget(self.module_stack)
            
            self.stacked_widget.addWidget(self.main_app_widget)

    def switch_module(self, index):
        self.module_stack.setCurrentIndex(index)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '确认', '确定要退出系统吗？', 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.data_manager.save_all()
            event.accept()
        else:
            event.ignore()
