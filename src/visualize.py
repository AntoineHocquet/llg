# src/visualize.py

import pandas as pd
import matplotlib.pyplot as plt
import os
from mpl_toolkits.mplot3d import Axes3D


ARROW_LENGTH_RATIO = 0.04


# static visualization
def generate_visualizations():
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

