# src/visualize.py

import pandas as pd
import matplotlib.pyplot as plt
import os
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import animation


def draw_llg_frame(ax, x, y, u0, u1, u2, t, elev, azim, arrow_length, arrow_width):
    """
    Draw a 3D frame for the LLG vector field at time t.
    """
    ax.clear()

    # Plot vectors
    ax.quiver(
        x, y, [0] * len(x),
        u0, u1, u2,
        length=arrow_length,
        linewidth=arrow_width,
        normalize=True,
        color='b',
        arrow_length_ratio=0.6
    )

    # Plot unit disk
    ax.plot_trisurf(x, y, [0] * len(x), color='lightgreen', alpha=0.3)

    # Labels and view
    ax.set_title(f"LLG equation at time = {t:.2f}s")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.view_init(elev=elev, azim=azim)


def generate_visualizations(params):
    """
    Generate static visualizations of the LLG equation.
    The visualizations are saved in the 'data' directory.
    """
    elev = params["elev"]
    azim = params["azim"]
    arrow_length = params["arrow_length"]
    arrow_width = params["arrow_width"]

    # Data paths
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(project_root, "edp", "solution_data.csv")
    output_path = os.path.join(project_root, "data", "llg_final.png")

    if not os.path.exists(data_path):
        print(f"❌ CSV data file not found: {data_path}")
        return

    df = pd.read_csv(data_path)

    # Get the last time-slice
    T = df["time"].max()
    sub_df = df[df["time"] == T]

    # Extract coordinates and magnetization
    x = sub_df["x"]
    y = sub_df["y"]
    u0 = sub_df["u0"]
    u1 = sub_df["u1"]
    u2 = sub_df["u2"]

    # 3D plot
    fig = plt.figure()
    ax: Axes3D = fig.add_subplot(111, projection='3d')

    draw_llg_frame(ax, x, y, u0, u1, u2, T, elev, azim, arrow_length, arrow_width)

    # Save the figure
    plt.savefig(output_path)
    print(f"✅ Saved final frame to: {output_path}")


def generate_gif(params):
    """
    Generate a GIF animation of the LLG equation.
    The animation is saved in the 'data' directory.
    """
    elev = params["elev"]
    azim = params["azim"]
    arrow_length = params["arrow_length"]
    arrow_width = params["arrow_width"]
    fps = params["fps"]

    # Paths
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(project_root, "edp", "solution_data.csv")
    gif_path = os.path.join(project_root, "data", "llg_equation_simulation.gif")

    if not os.path.exists(csv_path):
        print(f"❌ CSV data file not found: {csv_path}")
        return

    data = pd.read_csv(csv_path)
    time_steps = data['time'].unique()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    def update_quiver(frame):
        current_data = data[data['time'] == time_steps[frame]]
        draw_llg_frame(
            ax,
            current_data['x'],
            current_data['y'],
            current_data['u0'],
            current_data['u1'],
            current_data['u2'],
            time_steps[frame],
            elev, azim, arrow_length, arrow_width
        )

    anim = animation.FuncAnimation(
        fig,
        update_quiver,
        frames=len(time_steps),
        interval=1000 / fps,
        repeat=False
    )

    anim.save(gif_path, writer='imagemagick')
    plt.close()
    print(f"✅ Animation saved to: {gif_path}")
