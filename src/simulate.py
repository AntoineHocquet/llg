# src/simulate.py
import subprocess
import os
import platform
from config import load_config

# function to inject params into the FreeFEM .edp script
def generate_edp_with_params(template_path, output_path, params):
    with open(template_path, 'r') as f:
        template = f.read()

    # Use FreeFEM macros: replace %%T%%, %%dt%% etc.
    for key, value in params.items():
        template = template.replace(f"%%{key}%%", str(value))

    with open(output_path, 'w') as f:
        f.write(template)

# function to run FreeFEM via Docker
def run_simulation():
    current_os = platform.system()
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    edp_path = os.path.join(project_root, "edp")

    # Load parameters from JSON
    params = load_config()

    # Template and final EDP paths
    template_edp = os.path.join(edp_path, "llg_disk_template.edp")
    final_edp = os.path.join(edp_path, "llg_disk.edp")

    print("Generating .edp file with parameters from params.json...")
    generate_edp_with_params(template_edp, final_edp, params)

    # Docker command to run the simulation
    docker_cmd = [
        "docker", "run", "--rm",
        "-v", f"{edp_path}:/data",
        "antoinehocquet/freefem", "FreeFem++", "/data/llg_disk.edp"
    ]

    print("Running FreeFEM via Docker...")
    try:
        subprocess.run(docker_cmd, check=True)
        # print success with fancy emoji
        print("\u2705 Simulation completed successfully!") 
        print("\u2705 Results saved in data/solution_data.csv")
    except subprocess.CalledProcessError as e:
        print("Simulation failed:", e)