import subprocess


def run_subprocess(command:str, args:dict={}) -> None:
    command = command.format(**args)
    try:
        subprocess.run(command.split(" "), text=True, check=True)

    except subprocess.CalledProcessError:
        return