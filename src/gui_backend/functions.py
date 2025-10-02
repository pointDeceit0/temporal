"""The file consist of functions kit for using in gui"""
import pandas as pd
import numpy as np
import os
import sys
from typing import Tuple


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from src.gui_backend.launch_exe_file import launch_cpp_from_python  # noqa


def amt(data: pd.DataFrame, batch_size: int = 1,
        path: str = "src/launch/compiled_exes/launch_amt.exe",
        *args, **kwargs) -> Tuple[bool, str | Tuple[dict, pd.DataFrame]]:
    """AMT - Analysis of Monotone Trend test

    Args:
        data (pd.DataFrame): numeric data, result of test will be returned for each column
        batch_size (int, optional): size for the batch mean procedure. Defaults to 1.
        path (str, optional): path to compiled file .exe. Defaults to "src/launch/compiled_exes/launch_amt.exe".

    Returns:
        Tuple[bool, str | Tuple[dict, pd.DataFrame]]: True if no errors & (dict of results of amt for different columns
                                                                           & paved data by columns)
                                                      False if errors & description of error

    !!! NOTE: due to next error:
        Error: Error in function boost::math::normal_distribution<long double>::normal_distribution:
                Scale parameter is nan, but must be > 0 !
        'NoneType' object has no attribute 'strip'
    which could be related with approximation error (too small numbers for large arrays) the programm breaks down
    when the input array size bigger than ~131000 (was obtained experimental way).
    """
    if kwargs.get('to_float32_type', True):
        data = data.astype(np.float32)

    ret = {}
    for c in data:
        if not (res := launch_cpp_from_python(data[c].values, path, str(batch_size)))[0]:
            return res  # tuple recieved

        pvalue, pav = res[1].split('\n')

        # collect return
        ret[c] = (np.float32(pvalue), list(map(np.float32, pav.split())))

    return True, ret


if __name__ == "__main__":
    d = {
        'x': np.random.random(10).astype(np.float32),
        'y': np.random.random(10),
        'z': np.random.random(10)
    }
    amt(pd.DataFrame(d), batch_size='2')
