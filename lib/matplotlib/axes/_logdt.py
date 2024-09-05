import os
import json
import pickle
import pandas as pd

import numpy as np


class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """
    def default(self, obj):
        try:
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, pd.Series):
                return obj.tolist()
            elif isinstance(obj, pd.Index):
                return obj.tolist()
            return json.JSONEncoder.default(self, obj)
        except:
            return str(obj)



def log_data_to_dir(mpl_command, axes, x, y, kargs, dir="/tmp/matplotlib/eval"):
    command_dir = os.path.join(dir, mpl_command)
    os.makedirs(command_dir, exist_ok=True)

    if "user_command" not in kargs:
        kargs["user_command"] = mpl_command

    counter = 0
    while True:
        filename = os.path.join(command_dir, f"{counter}.json")
        if not os.path.exists(filename):
            # save plotting data
            # print(f"id(axes): {id(axes)}, {mpl_command}()", kargs)
            # print(f"x({type(x)}):", x)
            # print(f"y({type(x)}):", y)
            # print()
            with open(filename, "w", encoding="utf-8") as f:
                json.dump({
                    "axes_id": id(axes),
                    "x": x,
                    "y": y,
                    "kargs": kargs
                }, f, indent=4, ensure_ascii=False, cls=NumpyEncoder)
            break
        counter += 1
