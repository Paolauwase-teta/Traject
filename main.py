import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button

# -----------------------------
# 1. Experimental Data
# -----------------------------
angles = np.array([30, 45, 60, 75, 30, 45, 60, 75, 30, 80, 60, 75, 80])
ranges = np.array([23.1, 27.8, 20.4, 14.2, 15.6, 18.1, 22.7, 16.5, 11.9, 8.1, 11.5, 8.5, 3.9])

# -----------------------------
# 2. Fit Polynomial Model
# -----------------------------
coefficients = np.polyfit(angles, ranges, 2)
model = np.poly1d(coefficients)

# -----------------------------
# 3. Model Accuracy (R²)
# -----------------------------
predicted_values = model(angles)
ss_res = np.sum((ranges - predicted_values) ** 2)
ss_tot = np.sum((ranges - np.mean(ranges)) ** 2)
r2 = 1 - (ss_res / ss_tot)

# -----------------------------
# 4. Create Graph
# -----------------------------
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.35)  # more space for input & button

# Experimental data points (blue)
ax.scatter(angles, ranges, color='blue', label="Experimental Data")

# Polynomial curve
x_smooth = np.linspace(min(angles), max(angles), 100)
y_smooth = model(x_smooth)
ax.plot(x_smooth, y_smooth, color='blue', label="Polynomial Prediction Model")

ax.set_xlabel("Inclination Angle (degrees)")
ax.set_ylabel("Range")
ax.set_title("Projectile Range vs Inclination Angle")
ax.legend()
ax.grid(True)

# -----------------------------
# 5. Display accuracy at bottom
# -----------------------------
accuracy_text = ax.text(
    0.02, 0.02,
    f"Model Accuracy (R²) = {r2:.3f}",
    transform=ax.transAxes,
    fontsize=12,
    verticalalignment='bottom'
)

# -----------------------------
# 6. Output text on graph
# -----------------------------
result_text = ax.text(
    0.02, 0.08,
    "",
    transform=ax.transAxes,
    fontsize=12,
    color="darkorange"
)

# -----------------------------
# 7. TextBox for angle input
# -----------------------------
axbox = plt.axes([0.25, 0.15, 0.4, 0.05])
text_box = TextBox(axbox, "Enter Angle (°): ")

# -----------------------------
# 8. Submit button
# -----------------------------
axbutton = plt.axes([0.7, 0.15, 0.1, 0.05])
button = Button(axbutton, 'Submit', color='lightblue', hovercolor='cyan')

# -----------------------------
# 9. Orange dot for predicted range
# -----------------------------
predicted_dot, = ax.plot([], [], marker='X', markersize=10, color='orange', label="Predicted Range")

# -----------------------------
# 10. Function to calculate range & update graph
# -----------------------------
def calculate_range(text):
    try:
        angle_input = float(text)
        if not (0 <= angle_input <= 90):
            result_text.set_text("Angle must be 0–90°")
            predicted_dot.set_data([], [])
        else:
            range_predicted = model(angle_input)
            # Update text and orange dot
            result_text.set_text(f"Angle: {angle_input}°, Predicted Range: {range_predicted:.2f}")
            predicted_dot.set_data([angle_input], [range_predicted])
    except:
        result_text.set_text("Invalid input")
        predicted_dot.set_data([], [])
    fig.canvas.draw_idle()

# Connect TextBox and Button
text_box.on_submit(calculate_range)
button.on_clicked(lambda event: calculate_range(text_box.text))

plt.show()