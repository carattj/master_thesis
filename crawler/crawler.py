import csv
import os
import subprocess
import shutil
import argparse
import hashlib
import subprocess
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup


def replace_string_in_file(file_path, old_string, new_string):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()

        modified_content = file_content.replace(old_string, new_string)

        with open(file_path, 'w') as file:
            file.write(modified_content)

    except FileNotFoundError:
        pass
    except Exception as e:
        pass

def check_string_in_file(file_path, target_string):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if target_string in line:
                    return True
        return False
    except FileNotFoundError:
        return False

def find_apk_files(directory):
    apk_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.apk'):
                apk_files.append(os.path.join(root, file))
    return apk_files

def create_file(file_path):
    try:
        with open(file_path, 'w') as file:
            print(f"File '{file_path}' created successfully.")
    except Exception as e:
        print(f"An error occurred while creating the file: {e}")

def find_row_by_repository(dataframe, start_repository):
    for i, row in dataframe.iterrows():
        if row['Repository'] == start_repository:
            return i
    return None

def check_repository_structure(url):
    print(f"####### 1. Checking project structure")
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print("### Request failed")
            return False

        soup = BeautifulSoup(response.text, 'html.parser')
        gradlew_links = soup.find_all('a', title='gradlew')

        if gradlew_links:
            print("### Match")
            return True
        else:
            print("### No match")
            return False

    except Exception as e:
        print("### Page not responding")
        return False

def clone_repository(tmp_dir, repository_url):
    print(f"####### 2. Cloning")
    old_dir = os.listdir(tmp_dir)
    process = subprocess.Popen(['git', 'clone', repository_url], cwd=tmp_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    if process.returncode == 0:
        print("### Success")
        new_dir = os.listdir(tmp_dir)
        temp = [x for x in new_dir if x not in old_dir]
        return(temp[0])
    else:
        print("### Fail")
        return False

def disable_obfuscation(tmp_dir, cloned_repo):
    print(f"####### 3. Minification")
    project_app_dir_path = os.path.join(tmp_dir, cloned_repo, 'app')

    if os.path.exists(project_app_dir_path):

        groovy_path = os.path.join(project_app_dir_path, 'build.gradle')
        kotlin_path = os.path.join(project_app_dir_path, 'build.gradle.kts')

        if os.path.exists(groovy_path):
            print('### Groovy detected')
            
            is_minified = False
            if check_string_in_file(groovy_path, 'minifyEnabled true'):
                replace_string_in_file(groovy_path, 'minifyEnabled true', 'minifyEnabled false')
                is_minified = True
                print("### Disabled")
            else:
                print("### Already disabled")
            return 'groovy', is_minified

        elif os.path.exists(kotlin_path):
            print('### Kotlin detected')

            is_minified = False
            if check_string_in_file(kotlin_path, 'isMinifyEnabled = true'):
                replace_string_in_file(kotlin_path, 'isMinifyEnabled = true', 'isMinifyEnabled = false')
                is_minified = True
                print("### Disabled")
            else:
                print("### Already disabled")
            return 'kotlin', is_minified

    else:
        print("### Groovy/Kotlin not detected")
        return None,None

def compile(tmp_dir, cloned_repo):
    print(f"####### 4. Compilation")
    gradle_path = os.path.join(tmp_dir, cloned_repo)
    gradlew_path = os.path.join(gradle_path, 'gradlew')

    try:
        os.chmod(gradlew_path, 0o755)
        process = subprocess.run(['./gradlew', 'assembleRelease'], cwd=gradle_path, capture_output=True, text=True)
        output = process.stdout
        if 'BUILD SUCCESSFUL' in output:
            print("### Successful")
            return True
        else:
            print("### Fail")
    except PermissionError:
        print("### Permission denied - Skip compilation")
    except FileNotFoundError:
        print("### gradlew script not found - Skip compilation")
    return False


def save_apk(tmp_dir, cloned_repo, output_dir, apk_name):
    print(f"####### 5. Saving APK")
    release_dir = os.path.join(tmp_dir, cloned_repo, 'app', 'build', 'outputs', 'apk')
    if os.path.exists(release_dir) and find_apk_files(release_dir)[0]:
        shutil.copy(find_apk_files(release_dir)[0], os.path.join(output_dir, apk_name, '.apk'))        
        shutil.rmtree(os.path.join(tmp_dir, cloned_repo))
        print("### Success")
        return True
    else:
        print("### Fail")
        return False

def data_cleaning(df):
    print(f'Input csv:')
    print(f'- {len(df)} repositories')

    corrupted = df[df.Repository.isnull()].Name.tolist()
    n_corrupted = len(corrupted)
    print(f'- {n_corrupted} corrupted repositories')

    duplicated = df.Repository[df.Repository.duplicated()]
    n_duplicated = len(duplicated)
    print(f'- {n_duplicated} duplicated repositories')

    df = df.drop_duplicates(subset=['Repository'], keep='last')  # remove duplicates
    df = df.dropna(subset=['Repository'])  # remove corrupted data

    return df, n_corrupted, n_duplicated

def write_to_file(file_path, content):
    with open(file_path, 'a') as file:
        file.write(f'{content}\n')

def process_projects(df, output_csv, output_dir, tmp_dir, start_repository):

    repositories_list = df.Repository.tolist()

    start_index = 0
    if start_repository:
        start_index = repositories_list.index(start_repository)

    for i, current_repository in enumerate(repositories_list):

        if i < start_index:
            continue

        name = df[df.Repository == current_repository].Name.to_list()[0]

        print(f"\n################## {i} - {name} - {current_repository}")
        apk_hash = hashlib.sha256(current_repository.encode()).hexdigest()
        
        if check_repository_structure(current_repository):
            cloned_repository_name = clone_repository(tmp_dir, current_repository)
            if not cloned_repository_name:
                write_to_file(output_csv, f'{apk_hash},{current_repository},,,{False},')
                continue
 
            language, is_minified = disable_obfuscation(tmp_dir, cloned_repository_name)
            
            start_time = time.time()  # Record start time
            if not compile(tmp_dir, cloned_repository_name):
                end_time = time.time()
                compilation_time = end_time - start_time
                write_to_file(output_csv, f'{apk_hash},{current_repository},{language},{is_minified},{False},{compilation_time}')
                shutil.rmtree(os.path.join(os.path.join(tmp_dir, cloned_repository_name)))
                continue 

            end_time = time.time()
            compilation_time = end_time - start_time
            is_saved = save_apk(tmp_dir, cloned_repository_name, output_dir, apk_hash)
            write_to_file(output_csv, f'{apk_hash},{current_repository},{language},{is_minified},{is_saved},{compilation_time}')
        else:
            write_to_file(output_csv, f'{apk_hash},{current_repository},,,{False},')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Process APK files and generate CSV output")
    parser.add_argument("-i", "--input", dest="input_csv", help="Input csv")
    parser.add_argument("-s", "--starting", dest="starting_apk", help="APK from which to start")
    args = parser.parse_args()

    input_csv = args.input_csv
    start_repository = args.starting_apk
    output_csv = 'apks.csv'
    output_statistics = 'statistics.csv'
    output_dir = 'apks'
    tmp_dir = 'tmp'

    df = pd.read_csv(input_csv)
    df, corrupted, duplicated = data_cleaning(df)

    if not start_repository:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        if os.path.exists(tmp_dir):
            shutil.rmtree(os.path.join(tmp_dir))
        os.makedirs(tmp_dir)

        create_file(output_csv)
        write_to_file(output_csv, 'hash,repository,language,is_minified,compiled,compilation_time')
        
        create_file(output_statistics)
        write_to_file(output_statistics, f'dataset,corrupted_samples,duplicated_samples\n{input_csv},{corrupted},{duplicated}')
    # else:
        # start_index = find_row_by_repository(df, start)

    process_projects(df, output_csv, output_dir, tmp_dir, start_repository)