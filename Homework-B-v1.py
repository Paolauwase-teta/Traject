import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from matplotlib.animation import FuncAnimation

# --- Styling Constants ---
DARK_BG = "#212121"
DARK_FG = "#EEEEEE"
ACCENT_COLOR = "#00ADB5"  # Cyan-ish
BUTTON_BG = "#393E46"
BUTTON_ACTIVE = "#00ADB5"
ENTRY_BG = "#424242"
ENTRY_FG = "#FFFFFF"
PLOT_STYLE = 'dark_background'
LINE_COLOR = '#00FFFF' # Cyan
MARKER_COLOR = '#FF00FF' # Magenta

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
    ax.set_xlim(0, max(x)*1.1 if len(x) > 0 else 10)
    ax.set_ylim(0, max(y)*1.2 if len(y) > 0 else 10)
    ax.set_xlabel("Distance (m)", color=DARK_FG)
    ax.set_ylabel("Height (m)", color=DARK_FG)
    ax.set_title("Rocket Projectile Motion", color=ACCENT_COLOR, fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.3)
    
    # Customizing axes colors
    ax.spines['bottom'].set_color(DARK_FG)
    ax.spines['top'].set_color(DARK_FG) 
    ax.spines['right'].set_color(DARK_FG)
    ax.spines['left'].set_color(DARK_FG)
    ax.tick_params(axis='x', colors=DARK_FG)
    ax.tick_params(axis='y', colors=DARK_FG)

    # Line for trajectory and ball for rocket
    line, = ax.plot([], [], color=LINE_COLOR, linewidth=2, label='Trajectory')
    ball, = ax.plot([], [], marker='o', color=MARKER_COLOR, markersize=12, linestyle='None', label='Rocket', markeredgecolor='white')
    
    # Legend styling
    legend = ax.legend(facecolor=DARK_BG, edgecolor=DARK_FG, labelcolor=DARK_FG)

    # Animation function
    def animate(i):
        line.set_data(x[:i], y[:i])
        ball.set_data([x[i-1]], [y[i-1]])
        return line, ball

    # Create animation and stop when finished
    ani = FuncAnimation(fig, animate, frames=len(t), interval=20, blit=True, repeat=False)

    # Force canvas to update
    canvas.draw()

    label_result.config(text=f"Max Height: {Hmax:.2f} m    Range: {R:.2f} m")


# GUI Setup
root = tk.Tk()
root.title("Projectile Motion Simulator")
root.configure(bg=DARK_BG)
root.geometry("700x650")

# Header
header_frame = tk.Frame(root, bg=DARK_BG, pady=10)
header_frame.pack(fill='x')
title_label = tk.Label(header_frame, text="Projectile Motion Simulator", font=("Helvetica", 18, "bold"), bg=DARK_BG, fg=ACCENT_COLOR)
title_label.pack()

# Inputs Frame
input_frame = tk.Frame(root, bg=DARK_BG, pady=10)
input_frame.pack()

# Speed Input
tk.Label(input_frame, text="Initial Speed (m/s):", bg=DARK_BG, fg=DARK_FG, font=("Arial", 11)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_speed = tk.Entry(input_frame, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground='white', font=("Arial", 11), relief="flat", bd=5)
entry_speed.grid(row=0, column=1, padx=10, pady=5)

# Angle Input
tk.Label(input_frame, text="Launch Angle (deg):", bg=DARK_BG, fg=DARK_FG, font=("Arial", 11)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_angle = tk.Entry(input_frame, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground='white', font=("Arial", 11), relief="flat", bd=5)
entry_angle.grid(row=1, column=1, padx=10, pady=5)

# Simulate Button
btn_simulate = tk.Button(input_frame, text="LAUNCH ROCKET", command=simulate_projectile, 
                         bg=ACCENT_COLOR, fg='white', font=("Arial", 11, "bold"), 
                         activebackground=BUTTON_ACTIVE, activeforeground='white', 
                         relief="flat", width=20, pady=5)
btn_simulate.grid(row=2, column=0, columnspan=2, pady=15)

# Results Label
label_result = tk.Label(root, text="Max Height: -- m    Range: -- m", bg=DARK_BG, fg=ACCENT_COLOR, font=("Arial", 12, "bold"))
label_result.pack(pady=5)

# Plot Area
plt.style.use(PLOT_STYLE)
fig, ax = plt.subplots(figsize=(6, 4))
fig.patch.set_facecolor(DARK_BG)
ax.set_facecolor(DARK_BG)
# Initial empty grid
ax.grid(True, linestyle='--', alpha=0.3)
ax.set_title("Ready to Launch", color=DARK_FG)
ax.tick_params(colors=DARK_FG)
for spine in ax.spines.values():
    spine.set_color(DARK_FG)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(fill='both', expand=True, padx=20, pady=20)
canvas.get_tk_widget().configure(bg=DARK_BG, highlightthickness=0)

root.mainloop()