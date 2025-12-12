# VARIABLES D4ENVIRONEMENT
import sys
from pathlib import Path

def get_resource_path(relative_path):
    """Retourne le chemin absolu de la ressource embarquée ou locale."""

    if hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS) / relative_path
    return Path(__file__).parent / relative_path