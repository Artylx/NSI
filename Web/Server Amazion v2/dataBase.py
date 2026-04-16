import sys
from pathlib import Path
import json
import os

def get_resource_path(relative_path: str) -> Path:
    """Retourne le chemin absolu de la ressource embarquée ou locale."""

    if hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS) / relative_path
    return Path(__file__).parent / relative_path


class Product_DataBase:
    def __init__(self, filepath="./products.json"):
        self.filepath = filepath
        self.data = self.load()

    def load(self) -> list:
        with open(get_resource_path(self.filepath), "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self) -> None:
        with open(get_resource_path(self.filepath), "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def get_products(self) -> list:
        return self.data

    def add_product(self, product: dict) -> None:
        self.data.append(product)
        self.save()

    def debug(self):
        print("Products in database:")
        i = 0
        for product in self.data:
            print(f"Product {i}: {product}")
            i += 1

class User_DataBase:
    def __init__(self, filepath="./users.json"):
        self.filepath = filepath
        self.data = self.load()

    def load(self) -> list:
        with open(get_resource_path(self.filepath), "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self) -> None:
        with open(get_resource_path(self.filepath), "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def get_users(self) -> list:
        return self.data
    
    def get_user_by_email(self, email: str) -> dict:
        for user in self.data:
            if user.get("email") == email:
                return user
        return None
    
    def try_login(self, email: str, password: str) -> bool:
        user = self.get_user_by_email(email)
        if user and user.get("password") == password:
            return True
        return False

    def add_user(self, user: dict) -> None:
        self.data.append(user)
        self.save()

    def debug(self):
        print("Users in database:")
        i = 0
        for user in self.data:
            print(f"User {i}: {user}")
            i += 1