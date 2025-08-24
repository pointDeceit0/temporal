import subprocess
import tempfile
from typing import Any, Tuple
from numpy.typing import ArrayLike
import os


def launch_cpp_from_python(data: ArrayLike, path: str, *args) -> Tuple[bool, Any]:
    """Function takes data and forwards it to specified C++ compiled script

    The attempt to create generic function for launching compiled c++ scripts to launch it from python

    Args:
        data (ArrayLike[float]): data
        path (str): path to compiled c++ designed specific way

        * args[0] (int): batch mean size

    Returns:
        Tuple[bool, Any]: True/False is No error/error. Being processed then depends on task.
                          If False then description of an error, otherwise necessary result
    """
    try:
        # create input temporary file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin') as tmp_file:
            tmp_file.write(data.tobytes())
            in_temp_filename = tmp_file.name

        # create c++ output temporary file
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.out') as tmp_file:
            out_temp_filename = tmp_file.name

        # open pipe for c++ .exe transfering of path of
        # (1) .exe, (2) input temp file name, (3) .exe output file name, (4) array of args
        proc = subprocess.Popen(
            ['./' + path, in_temp_filename, out_temp_filename] + list(args),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            bufsize=0
        )

        stdout_data, stderr_data = proc.communicate()  # start pipe

        # read from output file
        with open(out_temp_filename, 'r') as result_file:
            result = result_file.read().strip()

        if proc.returncode != 0:  # if something went wrong on the .exe side
            return False, f"C++ error (code {proc.returncode}): {stderr_data.strip() or stdout_data.strip()}"

        return True, result

    except Exception as e:
        return False, str(e)

    finally:
        for temp_file in [in_temp_filename, out_temp_filename]:
            if temp_file and os.path.exists(temp_file):
                try:
                    os.unlink(temp_file)
                except Exception as e:  # if any removing error
                    print(e)
                    pass


if __name__ == "__main__":
    import numpy as np
    print(
        launch_cpp_from_python(
            np.random.random(20).astype(np.float32),
            "src/launch/compiled_exes/launch_amt.exe",
            '2'  # batch mean group
        )
    )
