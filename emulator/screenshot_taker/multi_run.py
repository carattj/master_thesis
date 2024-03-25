import subprocess

# List of argument sets
prefix = '/home/ubuntu/'
argument_sets = [
    {"apk_directory": f"{prefix}apks/FieldRename/", "output_directory": f"{prefix}screenshots/FieldRename/", "avd_name": "a"},
    {"apk_directory": f"{prefix}apks/MethodRename/", "output_directory": f"{prefix}screenshots/MethodRename/", "avd_name": "a"},
    {"apk_directory": f"{prefix}apks/ClassRename/", "output_directory": f"{prefix}screenshots/ClassRename/", "avd_name": "a"},

    {"apk_directory": f"{prefix}apks/FieldRename_MethodRename/", "output_directory": f"{prefix}screenshots/FieldRename_MethodRename/", "avd_name": "a"},
    {"apk_directory": f"{prefix}apks/FieldRename_ClassRename/", "output_directory": f"{prefix}screenshots/FieldRename_ClassRename/", "avd_name": "a"},
    {"apk_directory": f"{prefix}apks/MethodRename_ClassRename/", "output_directory": f"{prefix}screenshots/MethodRename_ClassRename/", "avd_name": "a"}
]

# Function to run the main script with given arguments
def run_main_script(arguments):
    subprocess.run(["python3", "screen.py"] + [f"--{key}={value}" for key, value in arguments.items()])

# Run the main script with each set of arguments
for args in argument_sets:
    run_main_script(args)
