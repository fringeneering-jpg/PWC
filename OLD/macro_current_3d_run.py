import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT_PATH = r"C:\Users\jaden\AppData\Local\Temp\claude\C--Users-jaden\fdd1dbff-e23b-4754-8b76-37298eda019c\scratchpad\macro_current_3d.png"

print("Intake: Loading PSZ2 Shockwave Telemetry...")
try:
    df = pd.read_csv(r"C:\Users\jaden\analysis_verified_rerun\data_raw\tsz_pressure\psz2.csv")
except FileNotFoundError:
    print("Error: Save the raw text block you pasted as 'psz2.csv' in your 'data_raw/tsz_pressure' folder.")
    df = pd.read_csv("psz2.csv")

df_clean = df[df['z'] > 0].copy()
print(f"Tracking {len(df_clean)} massive fluid-friction events (Galaxy Clusters) with confirmed 3D depth.")

lon_rad = np.radians(df_clean['GLON'])
lat_rad = np.radians(df_clean['GLAT'])
dist = df_clean['z'] * 4280

df_clean['X'] = dist * np.cos(lat_rad) * np.cos(lon_rad)
df_clean['Y'] = dist * np.cos(lat_rad) * np.sin(lon_rad)
df_clean['Z'] = dist * np.sin(lat_rad)

fig = plt.figure(figsize=(12, 10), facecolor='black')
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')

scatter = ax.scatter(
    df_clean['X'], df_clean['Y'], df_clean['Z'],
    s=df_clean['MSZ'] * 12,
    c=df_clean['Y5R500'],
    cmap='inferno',
    alpha=0.8,
    edgecolor='black',
    linewidth=0.5
)

ax.set_title("Test 5: 3D Fluid Map (Filaments & Cavitation Voids)", color='white', fontsize=14, pad=20)
ax.set_xlabel("Distance X (Mpc)", color='white')
ax.set_ylabel("Distance Y (Mpc)", color='white')
ax.set_zlabel("Distance Z (Mpc)", color='white')

ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.tick_params(colors='white')
ax.xaxis.pane.set_edgecolor('white')
ax.yaxis.pane.set_edgecolor('white')
ax.zaxis.pane.set_edgecolor('white')
ax.grid(True, linestyle=':', color='gray', alpha=0.5)

cbar = plt.colorbar(scatter, shrink=0.6, pad=0.1)
cbar.set_label("Thermal Friction Signature (Y5R500)", color='white')
cbar.ax.yaxis.set_tick_params(color='white')
plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

plt.savefig(OUT_PATH, dpi=150, bbox_inches="tight", facecolor='black')
plt.close()
print("Saved:", OUT_PATH)
