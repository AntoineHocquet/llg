# src/visualize.py

import pandas as pd
import matplotlib.pyplot as plt
import os
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import animation


# Constants
FPS = 10 # frames per second
INTERVAL = 1000 / FPS # interval between frames in milliseconds
ARROW_LENGTH_RATIO = 0.04 # relative length of the arrows
ARROW_WIDTH=0.3 # relative width of the arrows


# static visualization
def generate_visualizations():
    """
    Generate static visualizations of the LLG equation.
    The visualizations are saved in the 'data' directory.
    """
    print("Generating visualization...")

    # Data paths
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(project_root, "edp", "solution_data.csv")
    output_path = os.path.join(project_root, "data", "llg_final.png")

    # Load the CSV data
    df = pd.read_csv(data_path)
    last_t = df["time"].max()
    sub_df = df[df["time"] == last_t]

    # 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x=sub_df["x"]
    y=sub_df["y"]
    z=[0]*len(x)

    # plot of the LLG vectors
    ax.quiver(
        x,
        y,
        z,
        sub_df["u0"],
        sub_df["u1"],
        sub_df["u2"],
        length=ARROW_LENGTH_RATIO
    )
    ax.set_title(f"LLG at final time t = {last_t}")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

    # plot of the x,y unit disk in lightgreen
    ax.plot_trisurf(
        x,
        y,
        z,
        color='lightgreen',
        alpha=0.3)

    # Save the figure
    plt.savefig(output_path)
    print(f"\u2705 Saved final frame to: {output_path}")


# animation
def generate_gif():
    """
    Generate a GIF animation of the LLG equation.
    The animation is saved in the 'data' directory.
    """
    print("Generating animation...")

    # Data paths
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(project_root, "edp", "solution_data.csv")
    gif_path = os.path.join(project_root, "data", "llg_equation_simulation.gif")

    # Load the CSV data
    data = pd.read_csv(csv_path)

    # Extract unique time steps
    time_steps = data['time'].unique()

    # Prepare plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Extract mesh points from the first time step
    sub_data = data[data['time'] == time_steps[0]]
    x = sub_data['x']
    y = sub_data['y']
    z = [0] * len(x)

    # plot of the LLG vectors
    ax.quiver(
        x,
        y,
        z,
        sub_data['u0'],
        sub_data['u1'],
        sub_data['u2'],
        length=ARROW_LENGTH_RATIO,
        linewidth=ARROW_WIDTH,
        normalize=True,
        color='b'
    )

        # plot of the x,y unit disk in lightgreen
    ax.plot_trisurf(
        x,
        y,
        z,
        color='lightgreen',
        alpha=0.3)


    # Update function for the animation
    def update_quiver(frame):
        """
        Update the quiver plot for the given frame.
        It is passed as an argument to FuncAnimation.
        Input:
            frame (int): The current frame index.
        Output:
            None
        """
        current_data = data[data['time'] == time_steps[frame]]
        ax.clear()
        
        # update the vector field
        quiver = ax.quiver(
            current_data['x'],
            current_data['y'],
            [0] * len(current_data['x']),
            current_data['u0'],
            current_data['u1'],
            current_data['u2'],
            length=ARROW_LENGTH_RATIO,
            linewidth=ARROW_WIDTH,
            normalize=True,
            color='b'
        )

        # update the unit disk
        ax.plot_trisurf(
            current_data['x'],
            current_data['y'],
            [0] * len(current_data['x']),
            color='lightgreen',
            alpha=0.3
        )

        ax.set_title(f"LLG equation at time = {time_steps[frame]:.2f}s")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")


    # Create the animation
    anim = animation.FuncAnimation(
        fig,
        update_quiver,
        frames=len(time_steps),
        interval=INTERVAL,
        repeat=False
        )

    # Save the animation as a GIF
    anim.save(gif_path, writer='imagemagick')

    # Close the plot after saving
    plt.close()

    print(f"\u2705 Animation saved to: {gif_path}")
