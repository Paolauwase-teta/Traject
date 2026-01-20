import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from matplotlib.animation import FuncAnimation

ani = None  # global animation

def simulate_projectile():
    global ani

    # Destroy previous animation if exists
    if ani is not None:
        ani.event_source.stop()
        ani = None

    try:
        Vo = float(entry_speed.get())
        angle_deg = float(entry_angle.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for speed and angle.")
        return

    angle_rad = np.radians(angle_deg)
    g = 9.81

    # Physics calculations
    Hmax = (Vo**2) * (np.sin(angle_rad)**2) / (2 * g)
    R = (Vo**2) * np.sin(2 * angle_rad) / g
    T = 2 * Vo * np.sin(angle_rad) / g

    t = np.linspace(0, T, 500)
    x = Vo * np.cos(angle_rad) * t
    y = Vo * np.sin(angle_rad) * t - 0.5 * g * t**2

    # Clear previous plot
    ax.clear()
    ax.set_xlim(0, max(x)*1.1)
    ax.set_ylim(0, max(y)*1.2)
    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("Height (m)")
    ax.set_title("Rocket Projectile Motion")
    ax.grid(True)

    # Line for trajectory and ball for rocket
    line, = ax.plot([], [], 'b-', label='Trajectory')
    ball, = ax.plot([], [], 'ro', markersize=10, label='Rocket')
    ax.legend()

    # Animation function
    def animate(i):
        line.set_data(x[:i], y[:i])
        ball.set_data([x[i-1]], [y[i-1]])
        return line, ball

    # Create animation and stop when finished
    ani = FuncAnimation(fig, animate, frames=len(t), interval=20, blit=True, repeat=False)

    # Force canvas to update
    canvas.draw()

    label_result.config(text=f"Max Height: {Hmax:.2f} m\nRange: {R:.2f} m")


# GUI Setup
root = tk.Tk()
root.title("Projectile Motion for Kids")

tk.Label(root, text="Initial Speed (m/s):").grid(row=0, column=0, padx=5, pady=5)
entry_speed = tk.Entry(root)
entry_speed.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Launch Angle (deg):").grid(row=1, column=0, padx=5, pady=5)
entry_angle = tk.Entry(root)
entry_angle.grid(row=1, column=1, padx=5, pady=5)

btn_simulate = tk.Button(root, text="Launch Rocket!", command=simulate_projectile)
btn_simulate.grid(row=2, column=0, columnspan=2, pady=10)

label_result = tk.Label(root, text="Max Height: \nRange: ")
label_result.grid(row=3, column=0, columnspan=2, pady=5)

fig, ax = plt.subplots(figsize=(6,4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=4, column=0, columnspan=2)

root.mainloop()