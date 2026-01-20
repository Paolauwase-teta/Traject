import numpy as np
import matplotlib.pyplot as plt

def projectile_motion(Vo, angle_deg, g=9.81):
    """
    Simulate projectile motion.

    Parameters:
    Vo : float : Initial speed (m/s)
    angle_deg : float : Launch angle in degrees
    g : float : Acceleration due to gravity (default 9.81 m/s^2)

    Returns:
    Hmax : float : Maximum height
    R : float : Range of the projectile
    """
    # Convert angle to radians
    angle_rad = np.radians(angle_deg)

    # Maximum height
    Hmax = (Vo**2) * (np.sin(angle_rad)**2) / (2 * g)

    # Range
    R = (Vo**2) * np.sin(2 * angle_rad) / g

    # Time of flight
    T = 2 * Vo * np.sin(angle_rad) / g

    # Trajectory points
    t = np.linspace(0, T, num=500)
    x = Vo * np.cos(angle_rad) * t
    y = Vo * np.sin(angle_rad) * t - 0.5 * g * t**2

    # Plot trajectory
    plt.figure(figsize=(8,5))
    plt.plot(x, y, label='Projectile trajectory')
    plt.title('Projectile Motion Trajectory')
    plt.xlabel('Distance (m)')
    plt.ylabel('Height (m)')
    plt.grid(True)
    plt.legend()
    plt.show()

    return Hmax, R

# Example usage
Vo = 20  # m/s
angle = 45  # degrees
Hmax, R = projectile_motion(Vo, angle)
print(f"Maximum height: {Hmax:.2f} m")
print(f"Range: {R:.2f} m")