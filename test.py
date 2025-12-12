from pynput import keyboard
from pynput.keyboard import Controller

kb = Controller()
kb.press('a')
kb.release('a')
