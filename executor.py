import json
from data_connector import CONNECTORS
from tools import compute_slope, threshold_raster, raster_to_vector, spatial_join

# Map LLM 'tool' keys to functions
TOOL_MAP = {
    **CONNECTORS,
    'compute_slope': compute_slope,
    'threshold_raster': threshold_raster,
    'raster_to_vector': raster_to_vector,
    'spatial_join': spatial_join,
}


def run_workflow(wf: dict) -> dict:
    """
    Executes tasks in wf['workflow']['tasks'], returns dict of results keyed by step name.
    """
    results = {}

    for step in wf['workflow']['tasks']:
        name = step['name']
        tool = step['tool']
        args = step.get('args', {})

        # Resolve references to previous step outputs
        for k, v in args.items():
            if isinstance(v, str) and v in results:
                args[k] = results[v]

        func = TOOL_MAP.get(tool)
        if not func:
            raise KeyError(f"No tool registered for '{tool}'")

        out = func(**args)
        results[name] = out

    return results


def run_from_json(path: str):
    with open(path) as f:
        wf = json.load(f)
    return run_workflow({'workflow': wf})