import math
import re
from itertools import product
from typing import Union

from wfcrl.environments.data_cases import (
    DefaultControl,
    FarmRowFastfarm,
    FarmRowFloris,
    named_cases_dictionary,
)
from wfcrl.interface import FastFarmInterface, FlorisInterface
from wfcrl.multiagent_env import MAWindFarmEnv
from wfcrl.simple_env import WindFarmEnv
from wfcrl.wrappers import AECLogWrapper, LogWrapper

env_pattern = r"(Dec_)*(\w+\d*_)(\w+)"
layout_pattern = r"Turb(\d+)_Row(\d+)"

# Register named layouts
registered_simulators = ["Fastfarm", "Floris"]
registered_layouts = list(named_cases_dictionary.keys())
registered_layouts.extend([f"Turb{n}_Row1_" for n in range(1, 13)])
control_types = ["", "Dec_"]
registered_envs = [
    "".join(env_descs)
    for env_descs in product(control_types, registered_layouts, registered_simulators)
]


def get_default_control(controls):
    default_controls = DefaultControl()
    control_dict = {}
    if "yaw" in controls:
        control_dict["yaw"] = default_controls.yaw
    if "pitch" in controls:
        control_dict["pitch"] = default_controls.pitch
    if "torque" in controls:
        control_dict["torque"] = default_controls.torque
    return control_dict


def get_case(name: str, simulator: str):
    simulator_index = registered_simulators.index(simulator)
    # Check for named case
    if name in named_cases_dictionary:
        case = named_cases_dictionary[name][simulator_index]
        return case
    # Else Retrieve environment descriptor in env name
    match = re.match(layout_pattern, name)
    num_turbines = int(match.group(1))
    num_rows = int(match.group(2))
    # At this point, only single rowed envs should remain
    # to be procedurally generated
    assert num_rows == 1
    # Procedurally generate a single row wind farm
    cls = FarmRowFastfarm if simulator_index == 0 else FarmRowFloris
    case = cls(
        num_turbines=num_turbines,
        xcoords=cls.get_xcoords(num_turbines),
        ycoords=cls.get_ycoords(num_turbines),
        timestep_s=cls.timestep_s,
        warmup_time_s=cls.warmup_time_s,
        buffer_window=cls.buffer_window,
        set_wind_direction=cls.set_wind_direction,
        set_wind_speed=cls.set_wind_speed,
    )
    return case


def validate_case(env_id, case):
    try:
        assert len(case.xcoords) == len(
            case.ycoords
        ), "xcoords and ycoords layout coordinates must have the same length"
        # TODO: add other checks
    except Exception as e:
        raise ValueError(f"Invalid configuration for case {env_id}: {e}")


def make(env_id: str, controls: Union[dict, list] = ["yaw"], log=True, **env_kwargs):
    """Return a wind farm benchmark environment.

    Args:
        env_id: Environment identifier (e.g., "Dec_Ablaincourt_Floris")
        controls: Control specification dict or list of control names
        log: Whether to wrap environment with logging wrapper
        **env_kwargs: Additional arguments passed to environment constructor
            - episode_length: Number of steps per episode (replaces max_num_steps)
            - max_num_steps: DEPRECATED - use episode_length instead
            - load_coef: Load penalty coefficient
            - wind_speed: Wind speed in m/s
            - wind_direction: Wind direction in degrees

    Returns:
        WindFarmEnv or MAWindFarmEnv wrapped with logging if log=True
    """
    if env_id not in registered_envs:
        raise ValueError(f"{env_id} is not a registered WFCRL benchmark environment.")
    match = re.match(env_pattern, env_id)
    decentralized = match.group(1)
    name = match.group(2)
    simulator = match.group(3)
    case = get_case(name, simulator)
    validate_case(env_id, case)
    env_class = MAWindFarmEnv if decentralized == "Dec_" else WindFarmEnv
    simulator_class = FastFarmInterface if simulator == "Fastfarm" else FlorisInterface
    if not isinstance(controls, dict):
        controls = get_default_control(controls)
    if "wind_time_series" in env_kwargs:
        case.wind_time_series = env_kwargs["wind_time_series"]
        del env_kwargs["wind_time_series"]
    if "path_to_simulator" in env_kwargs:
        case.path_to_simulator = env_kwargs["path_to_simulator"]
        del env_kwargs["path_to_simulator"]
    if "vtk_wind" in env_kwargs:
        case.vtk_wind = env_kwargs["vtk_wind"]
        del env_kwargs["vtk_wind"]
    if "wind_speed" in env_kwargs:
        # Set wind speed as instance attribute (used in simul_params property)
        case.wind_speed = env_kwargs["wind_speed"]
        del env_kwargs["wind_speed"]
    if "wind_direction" in env_kwargs:
        # Set wind direction as instance attribute (rotates layout for FastFarm)
        case.wind_direction = env_kwargs["wind_direction"]
        del env_kwargs["wind_direction"]
    if "output_dir" in env_kwargs:
        # Set output directory for simulation files (FastFarm only)
        case.output_dir = env_kwargs["output_dir"]
        del env_kwargs["output_dir"]
    # Handle episode_length / max_num_steps naming
    # Prefer episode_length, but support max_num_steps for backward compatibility
    if "episode_length" in env_kwargs:
        pass  # Use as-is
    elif "max_num_steps" in env_kwargs:
        # Backward compatibility: rename to episode_length
        env_kwargs["episode_length"] = env_kwargs.pop("max_num_steps")

    # Calculate warmup_iters from warmup_time_s
    warmup_iters = math.ceil(case.warmup_time_s / case.timestep_s)

    env = env_class(
        interface=simulator_class,
        farm_case=case,
        controls=controls,
        warmup_iters=warmup_iters,
        **env_kwargs,
    )

    if log:
        wrapper_class = AECLogWrapper if decentralized == "Dec_" else LogWrapper
        env = wrapper_class(env)

    return env


def list_envs():
    return registered_envs
