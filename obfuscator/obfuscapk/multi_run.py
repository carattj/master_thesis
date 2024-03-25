import subprocess

# List of argument sets
prefix = './'
input_dir = '/U0_apks'
output_dir = '/U4_apks'
argument_sets = [
    {"input_directory": f"{prefix}{input_dir}", "output_directory": f"{prefix}{output_dir}"},
]

# Function to run the main script with given arguments
def run_main_script(arguments):
    subprocess.run(["python3", "./obf/1obf.py"] + [f"{value}" for key, value in arguments.items()])
    subprocess.run(["python3", "./obf/3obf.py"] + [f"{value}" for key, value in arguments.items()])
    subprocess.run(["python3", "./obf/3obf.py"] + [f"{value}" for key, value in arguments.items()])

# Run the main script with each set of arguments
for args in argument_sets:
    run_main_script(args)
