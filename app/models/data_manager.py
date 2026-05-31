import json
from pathlib import Path


class DataManager:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent.parent / "data"
        self.data_dir.mkdir(exist_ok=True)
        
        self.users = self._load_data("users.json")
        self.greenhouses = self._load_data("greenhouses.json")
        self.sensors = self._load_data("sensors.json")
        self.plants = self._load_data("plants.json")
        self.irrigation_records = self._load_data("irrigation_records.json")
        self.tasks = self._load_data("tasks.json")
        self.inventory = self._load_data("inventory.json")
        self.employees = self._load_data("employees.json")
        self.reports = self._load_data("reports.json")
        self.alerts = self._load_data("alerts.json")

    def _load_data(self, filename):
        file_path = self.data_dir / filename
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def _save_data(self, filename, data):
        file_path = self.data_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def save_all(self):
        self._save_data("users.json", self.users)
        self._save_data("greenhouses.json", self.greenhouses)
        self._save_data("sensors.json", self.sensors)
        self._save_data("plants.json", self.plants)
        self._save_data("irrigation_records.json", self.irrigation_records)
        self._save_data("tasks.json", self.tasks)
        self._save_data("inventory.json", self.inventory)
        self._save_data("employees.json", self.employees)
        self._save_data("reports.json", self.reports)
        self._save_data("alerts.json", self.alerts)
