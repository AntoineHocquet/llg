# main.py
import argparse
from simulate import run_simulation
from visualize import generate_visualizations, generate_gif
from config import load_config, save_config
import os

def parse_overrides(overrides):
    updated = {}
    for kv in overrides:
        if '=' not in kv:
            raise ValueError(f"Invalid format: '{kv}'. Use key=value.")
        key, val = kv.split("=", 1)
        try:
            parsed_val = int(val)
        except ValueError:
            try:
                parsed_val = float(val)
            except ValueError:
                parsed_val = val
        updated[key] = parsed_val
    return updated

def main():
    parser = argparse.ArgumentParser(description="LLG Simulation Pipeline")
    parser.add_argument('--sim', action='store_true', help="Run simulation")
    parser.add_argument('--viz', action='store_true', help="Generate PNG visualization")
    parser.add_argument('--gif', action='store_true', help="Generate animated GIF")
    parser.add_argument('--set', nargs='*', help="Override simulation parameters (key=value)")

    args = parser.parse_args()

    # 🧠 Step 1: load current params
    params = load_config()

    # 🧠 Step 2: apply --set overrides
    if args.set:
        overrides = parse_overrides(args.set)
        print("Overriding params:", overrides)
        params.update(overrides)
        save_config(params)

    # 🧠 Step 3: Execute selected actions with fresh reloads
    if args.sim:
        print("Running simulation...")
        run_simulation()  # will internally reload params

    if args.viz:
        print("Generating visualization...")
        fresh_params = load_config()
        generate_visualizations(fresh_params)

    if args.gif:
        print("Generating GIF...")
        fresh_params = load_config()
        generate_gif(fresh_params)

    if not any([args.sim, args.viz, args.gif]):
        print("No action specified. Use --sim, --viz, or --gif.")

if __name__ == "__main__":
    main()
