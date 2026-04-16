import tkinter as tk
import random
from bubble_sort import bubble_sort
from insertion_sort import insertion_sort
from merge_sort import merge_sort
from quick_sort import quick_sort

WIDTH = 800
HEIGHT = 400
BAR_WIDTH = 10
MARGIN = 5

# Fenêtre
root = tk.Tk()
root.title("Visualisation des tris")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

# UI
speed_slider = tk.Scale(root, from_=1, to=200, orient="horizontal", label="Vitesse")
speed_slider.set(50)
speed_slider.pack()

algo_var = tk.StringVar(value="Bubble")

menu = tk.OptionMenu(root, algo_var, "Bubble", "Insertion", "Merge", "Quick")
menu.pack()

# Variables globales
data = []
rects = []
steps = None

def generate_data():
    return [random.randint(10, 100) for _ in range(WIDTH // BAR_WIDTH)]

def get_algorithm(data):
    if algo_var.get() == "Bubble":
        return bubble_sort(data)
    elif algo_var.get() == "Merge":
        return merge_sort(data)
    elif algo_var.get() == "Quick":
        return quick_sort(data)
    else:
        return insertion_sort(data)

def draw_bars(arr, active):
    for index, (rect, val) in enumerate(zip(rects, arr)):
        x0 = index * BAR_WIDTH
        y0 = HEIGHT - val * 3
        x1 = x0 + BAR_WIDTH - MARGIN
        y1 = HEIGHT

        if index == active[0] or index == active[1]:
            color = "red"        # comparaison
        elif index >= active[0] and index <= active[1]:
            color = "yellow"     # zone de merge
        else:
            color = "white"

        canvas.coords(rect, x0, y0, x1, y1)
        canvas.itemconfig(rect, fill=color)

def update():
    global steps

    try:
        arr, active = next(steps)
        draw_bars(arr, active)
        root.after(speed_slider.get(), update)

    except StopIteration:
        for rect in rects:
            canvas.itemconfig(rect, fill="green")

def restart():
    global data, rects, steps

    canvas.delete("all")

    data = generate_data()
    rects = []

    for i, val in enumerate(data):
        x0 = i * BAR_WIDTH
        y0 = HEIGHT - val * 3
        x1 = x0 + BAR_WIDTH - 2
        y1 = HEIGHT

        rect = canvas.create_rectangle(x0, y0, x1, y1, fill="white")
        rects.append(rect)

    steps = get_algorithm(data)
    update()

# Bouton restart
btn_restart = tk.Button(root, text="Restart", command=restart)
btn_restart.pack()

# Initialisation
restart()

root.mainloop()