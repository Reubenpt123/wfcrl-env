"""
Example demonstrating how to enable VTK wind visualization dynamically using reset options.

This shows how to control VTK output on a per-episode basis without changing the
farm case configuration. Useful for enabling VTK only for specific episodes during training.
"""
import numpy as np
from wfcrl import environments as envs

# Create environment (VTK is OFF by default in the farm case)
env = envs.make(
    "Turb3_Row1_Fastfarm",
    max_num_steps=50,
    controls=["yaw", "pitch"],
)

print("=" * 70)
print("Episode 1: Running WITHOUT VTK output")
print("=" * 70)

# Reset without VTK - normal operation
observation = env.reset(
    options={
        "wind_speed": 8.0,
        "wind_direction": 270
    }
)

# Run simulation
for step in range(10):
    action = {
        "yaw": np.zeros(env.num_turbines),
        "pitch": np.zeros(env.num_turbines)
    }
    observation, reward, terminated, truncated, info = env.step(action)
    
    if step % 5 == 0:
        print(f"Step {step}: Reward = {reward:.4f}")
    
    if terminated or truncated:
        break

print("\n" + "=" * 70)
print("Episode 2: Running WITH VTK output enabled")
print("=" * 70)

# Reset WITH VTK enabled - will generate visualization files
observation = env.reset(
    options={
        "wind_speed": 10.0,
        "wind_direction": 280,
        "vtk_wind": True  # Enable VTK wind field output for this episode
    }
)

# Run simulation with VTK output
for step in range(10):
    # Apply some yaw control to see effects in VTK
    action = {
        "yaw": np.array([5.0, 0.0, -5.0]),
        "pitch": np.zeros(env.num_turbines)
    }
    observation, reward, terminated, truncated, info = env.step(action)
    
    if step % 5 == 0:
        print(f"Step {step}: Reward = {reward:.4f}")
    
    if terminated or truncated:
        break

print("\n" + "=" * 70)
print("Episode 3: Back to normal (no VTK)")
print("=" * 70)

# Reset again without VTK
observation = env.reset(
    options={
        "wind_speed": 9.0,
        "vtk_wind": False  # Explicitly disable (or just omit the parameter)
    }
)

for step in range(10):
    action = {
        "yaw": np.zeros(env.num_turbines),
        "pitch": np.zeros(env.num_turbines)
    }
    observation, reward, terminated, truncated, info = env.step(action)
    
    if step % 5 == 0:
        print(f"Step {step}: Reward = {reward:.4f}")
    
    if terminated or truncated:
        break

print("\n" + "=" * 70)
print("Summary:")
print("=" * 70)
print("✓ Episode 1: No VTK files generated")
print("✓ Episode 2: VTK files generated in simulation output directory")
print("✓ Episode 3: No VTK files generated")
print("\nVTK output can be controlled per-episode using the 'vtk_wind' option in reset()!")
print("This is useful for:")
print("  - Generating visualizations only for evaluation episodes")
print("  - Saving disk space during training")
print("  - Debugging specific scenarios")
