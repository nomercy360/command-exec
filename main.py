import os
import subprocess
import importlib.util

executed_commands = set()


def execute_command(command):
    if command in executed_commands:
        print(f'команда "{command}" уже выполнялась')
    else:
        try:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            print(result.stdout.strip())
            executed_commands.add(command)
        except subprocess.CalledProcessError as e:
            print(e.stderr.strip())


def get_cmds_from_file(file_path):
    spec = importlib.util.spec_from_file_location("module.name", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, 'CMDS', [])


def main(directory):
    all_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                all_files.append(os.path.join(root, file))

    for file_path in sorted(all_files):
        cmds = get_cmds_from_file(file_path)
        for cmd in cmds:
            execute_command(cmd)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python main.py <directory>")
    else:
        main(sys.argv[1])
