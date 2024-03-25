import subprocess

# List of argument sets
prefix = '/Volumes/My Passport/'
# argument_sets = [
#     {"dir_a": f"{prefix}U0/screenshots/success", "dir_b": f"{prefix}U1/screenshots/FieldRename", "out_dir": 'out', "fail_img": "fail.png"},
#     {"dir_a": f"{prefix}U0/screenshots/success", "dir_b": f"{prefix}U1/screenshots/MethodRename", "out_dir": 'out', "fail_img": "fail.png"},
#     {"dir_a": f"{prefix}U0/screenshots/success", "dir_b": f"{prefix}U1/screenshots/ClassRename", "out_dir": 'out', "fail_img": "fail.png"},

#     {"dir_a": f"{prefix}U0/screenshots/success", "dir_b": f"{prefix}U1/screenshots/FieldRename_MethodRename", "out_dir": 'out', "fail_img": "fail.png"},
#     {"dir_a": f"{prefix}U0/screenshots/success", "dir_b": f"{prefix}U1/screenshots/FieldRename_ClassRename", "out_dir": 'out', "fail_img": "fail.png"},
#     {"dir_a": f"{prefix}U0/screenshots/success", "dir_b": f"{prefix}U1/screenshots/MethodRename_ClassRename", "out_dir": 'out', "fail_img": "fail.png"},
# ]

argument_sets = [
    {"dir_a": f"{prefix}U1/screenshots/FieldRename", "dir_b": f"{prefix}U2/screenshots/FieldRename", "out_dir": 'outt', "fail_img": "fail.png"},
    {"dir_a": f"{prefix}U1/screenshots/MethodRename", "dir_b": f"{prefix}U2/screenshots/MethodRename", "out_dir": 'outt', "fail_img": "fail.png"},
    {"dir_a": f"{prefix}U1/screenshots/ClassRename", "dir_b": f"{prefix}U2/screenshots/ClassRename", "out_dir": 'outt', "fail_img": "fail.png"},

    {"dir_a": f"{prefix}U1/screenshots/FieldRename_MethodRename", "dir_b": f"{prefix}U2/screenshots/FieldRename_MethodRename", "out_dir": 'outt', "fail_img": "fail.png"},
    {"dir_a": f"{prefix}U1/screenshots/FieldRename_ClassRename", "dir_b": f"{prefix}U2/screenshots/FieldRename_ClassRename", "out_dir": 'outt', "fail_img": "fail.png"},
    {"dir_a": f"{prefix}U1/screenshotsMethodRename_ClassRename", "dir_b": f"{prefix}U2/screenshots/MethodRename_ClassRename", "out_dir": 'outt', "fail_img": "fail.png"},
]

# Function to run the main script with given arguments
def run_main_script(arguments):
    subprocess.run(["python3", "screenshot_similarity.py"] + [f"--{key}={value}" for key, value in arguments.items()])

# Run the main script with each set of arguments
for args in argument_sets:
    run_main_script(args)
