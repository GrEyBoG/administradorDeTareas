import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from threading import Thread
import time
import psutil

root = ThemedTk(theme="black")  
root.title('Administrador de Tareas')

tab_parent = ttk.Notebook(root)

tab1 = ttk.Frame(tab_parent)
tab2 = ttk.Frame(tab_parent)

tab_parent.add(tab1, text='Procesos')
tab_parent.add(tab2, text='Gráficos')

tab_parent.pack(expand=1, fill='both')

frame1 = ttk.Frame(tab1)
frame1.pack(fill='both', expand=True)

tree = ttk.Treeview(frame1)
tree['columns'] = ('PID', 'Nombre', 'RAM')

tree.column('#0', width=0, stretch='NO')
tree.column('PID', anchor='center', width=80)
tree.column('Nombre', anchor='w', width=200)
tree.column('RAM', anchor='center', width=100)

tree.heading('#0', text='', anchor='center')
tree.heading('PID', text='PID', anchor='center')
tree.heading('Nombre', text='Nombre', anchor='center')
tree.heading('RAM', text='RAM (MB)', anchor='center')

tree.pack(fill='both', expand=True)

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 6), dpi=100)
fig.patch.set_facecolor('black')
for ax in [ax1, ax2, ax3, ax4]:
    ax.set_facecolor('black')
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

canvas = FigureCanvasTkAgg(fig, master=tab2)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

cpu_percents = []
ram_percents = []
net_stats = []
disk_stats = []


def update_process_list():
    for i in tree.get_children():
        tree.delete(i)
    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
        tree.insert('', 'end', values=(
            proc.info['pid'], proc.info['name'], proc.info['memory_info'].rss / 1024 / 1024))
    root.after(1000, update_process_list)


def update_graph():
    while True:
        cpu_percents.append(psutil.cpu_percent())
        ram_percents.append(psutil.virtual_memory().percent)
        net_stats.append(psutil.net_io_counters().bytes_sent +
                         psutil.net_io_counters().bytes_recv)
        disk_stats.append(psutil.disk_io_counters().read_bytes +
                          psutil.disk_io_counters().write_bytes)
        ax1.cla()
        ax2.cla()
        ax3.cla()
        ax4.cla()
        ax1.plot(cpu_percents, label="CPU", color='purple')
        ax2.plot(ram_percents, label="RAM", color='blue')
        ax3.plot(net_stats, label="Wifi", color='green')
        ax4.plot(disk_stats, label="Disk", color='pink')
        ax1.legend()
        ax2.legend()
        ax3.legend()
        ax4.legend()
        canvas.draw()
        time.sleep(1)


root.after(1000, update_process_list)

graph_thread = Thread(target=update_graph)
graph_thread.start()

root.mainloop()
