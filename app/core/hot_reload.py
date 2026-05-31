import sys
import importlib
from pathlib import Path
from PyQt6.QtCore import QFileSystemWatcher, pyqtSignal, QObject


class HotReloader(QObject):
    module_reloaded = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.watcher = QFileSystemWatcher()
        self.watched_files = set()
        self.watcher.fileChanged.connect(self.on_file_changed)

    def add_watch(self, file_path):
        path = Path(file_path)
        if path.exists() and str(path) not in self.watched_files:
            self.watched_files.add(str(path))
            self.watcher.addPath(str(path))

    def on_file_changed(self, file_path):
        if file_path.endswith('.py'):
            self.reload_module(file_path)
            self.module_reloaded.emit(file_path)

    def reload_module(self, file_path):
        module_name = self._get_module_name(file_path)
        if module_name and module_name in sys.modules:
            importlib.reload(sys.modules[module_name])

    def _get_module_name(self, file_path):
        file_path = Path(file_path)
        parts = []
        while file_path.parent != file_path:
            init_file = file_path.parent / '__init__.py'
            if init_file.exists():
                parts.insert(0, file_path.stem)
                file_path = file_path.parent
            else:
                break
        return '.'.join(parts) if parts else None
