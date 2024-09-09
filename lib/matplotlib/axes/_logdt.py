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


def log_data_to_dir(axes, 
                    x, y, kargs,
                    file_id: str,
                    dir="/tmp/matplotlib/eval"):
    
    assert "user_command" in kargs, "user_command is required in kargs"
    axes_dir = os.path.join(dir, f"{id(axes)}")
    os.makedirs(axes_dir, exist_ok=True)

    data_file_path = os.path.join(axes_dir, f'{kargs["user_command"]}-{file_id}.json')
    with open(data_file_path, "w", encoding="utf-8") as f:
        json.dump({
            "axes_id": id(axes),
            "x": x,
            "y": y,
            "kargs": kargs
        }, f, indent=4, ensure_ascii=False, cls=NumpyEncoder)
    # save plotting data
    print(f'id(axes): {id(axes)}, {kargs["user_command"]}()', kargs)
    print(f"x({type(x)}):", x)
    print(f"y({type(x)}):", y)
    print()
    return data_file_path

def log_artist_to_dir(axes, user_command, 
                      artist,
                      file_id: str,
                      dir="/tmp/matplotlib/eval"):

    axes_dir = os.path.join(dir, f"{id(axes)}")
    os.makedirs(axes_dir, exist_ok=True)
    
    data_file_path = os.path.join(axes_dir, f'{user_command}-{file_id}.pickle')
    with open(data_file_path, "wb") as f:
        pickle.dump(artist, f)
    
