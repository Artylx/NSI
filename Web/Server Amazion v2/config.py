import sys
from pathlib import Path

def get_resource_path(relative_path: str) -> Path:
    """Retourne le chemin absolu de la ressource embarquée ou locale."""

    if hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS) / relative_path
    return Path(__file__).parent / relative_path

class Config:
    def __init__(self, filepath="./config.txt"):
        self.values = {}
        self.filepath = filepath

        self.load()

    def load(self) -> None:
        with open(get_resource_path(self.filepath), 'r', encoding='utf-8') as f:
            for line in f:
                key, value = line.strip().split('=')
                self.values[key] = value

    def set_value(self, key: str, value: str) -> None:
        self.values[key] = value
        self.save()

    def get_value(self, key: str, default=None) -> (str | None):
        return self.values.get(key, default)

    def save(self) -> None:
        with open(get_resource_path(self.filepath), 'w', encoding='utf-8') as f:
            for key, value in self.values.items():
                f.write(f"{key}={value}\n")

    def debug(self) -> None:
        for key, value in self.values.items():
            print(f"{key} => {value}")
    