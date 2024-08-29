import os
import json
import pickle

import numpy as np


def is_external_call(call_stack):
    last_call = call_stack[0]
    slast_call = call_stack[1]
    if last_call.filename != slast_call.filename:
        return True
    else:
        return False


class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)



def log_data_to_dir(mpl_command, axes, x, y, kargs, artist, dir="/tmp/matplotlib/eval"):
    command_dir = os.path.join(dir, mpl_command)
    os.makedirs(command_dir, exist_ok=True)

    counter = 0
    while True:
        filename = os.path.join(command_dir, f"{counter}.json")
        if not os.path.exists(filename):
            # save original data
            print(f"id(axes): {id(axes)}, {mpl_command}()", kargs)
            print(f"x({type(x)}):", x)
            print(f"y({type(x)}):", y)
            print()
            with open(filename, "w", encoding="utf-8") as f:
                json.dump({
                    "axes_id": id(axes),
                    "x": x,
                    "y": y,
                    "kargs": kargs
                }, f, indent=4, ensure_ascii=False, cls=NumpyEncoder)

            # save artist
            artist_filename = os.path.join(command_dir, f"{counter}_artist.pickle")
            with open(artist_filename, "wb") as f:
                pickle.dump(artist, f)
            
            break
        counter += 1