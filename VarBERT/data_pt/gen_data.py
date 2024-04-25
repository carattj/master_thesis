import javalang


### Extract method from file
def get_method_start_end(method_node, tree):
    startpos  = None
    endpos    = None
    startline = None
    endline   = None
    for path, node in tree:
        if startpos is not None and method_node not in path:
            endpos = node.position
            endline = node.position.line if node.position is not None else None
            break
        if startpos is None and node == method_node:
            startpos = node.position
            startline = node.position.line if node.position is not None else None
    return startpos, endpos, startline, endline

def get_method_text(startpos, endpos, startline, endline, last_endline_index, codelines):
    if startpos is None:
        return "", None, None, None
    else:
        startline_index = startline - 1 
        endline_index = endline - 1 if endpos is not None else None 

        # 1. check for and fetch annotations
        if last_endline_index is not None:
            for line in codelines[(last_endline_index + 1):(startline_index)]:
                if "@" in line: 
                    startline_index = startline_index - 1
        meth_text = "<ST>".join(codelines[startline_index:endline_index])
        meth_text = meth_text[:meth_text.rfind("}") + 1] 

        # 2. remove trailing rbrace for last methods & any external content/comments
        # if endpos is None and 
        if not abs(meth_text.count("}") - meth_text.count("{")) == 0:
            # imbalanced braces
            brace_diff = abs(meth_text.count("}") - meth_text.count("{"))

            for _ in range(brace_diff):
                meth_text  = meth_text[:meth_text.rfind("}")]    
                meth_text  = meth_text[:meth_text.rfind("}") + 1]     

        meth_lines = meth_text.split("<ST>")  
        meth_text  = "".join(meth_lines)                   
        last_endline_index = startline_index + (len(meth_lines) - 1) 

        return meth_text, (startline_index + 1), (last_endline_index + 1), last_endline_index, codelines

def read_code_file(filename):
    with open(filename, 'r') as r:
        codelines = r.readlines()
        code_text = ''.join(codelines)
    tree = javalang.parse.parse(code_text)    
    return codelines, tree

def get_methods_from_file(filename):
    try:
        codelines, tree = read_code_file(filename)
        methods = {}
        lex = None
        for _, method_node in tree.filter(javalang.tree.MethodDeclaration):
            startpos, endpos, startline, endline = get_method_start_end(method_node, tree)
            method_text, startline, endline, lex, codelines = get_method_text(startpos, endpos, startline, endline, lex, codelines)
            methods[method_node.name] = {'code': method_text, 'start_line': startpos, 'end_line': endpos}
        return methods
    except javalang.parser.JavaSyntaxError as e:
        # print(f"JavaSyntaxError in file: {filename}. Error message: {e}")
        return {}
    except RecursionError:
        # Handle RecursionError gracefully
        # Perform any necessary cleanup or other actions
        return {}
    



### Lexer
from enum import Enum, auto
from pygments import lex
from pygments.token import Token
from pygments.token import is_token_subtype
from pygments.lexer import inherit
from pygments.lexers.jvm import JavaLexer

Token.Placeholder = Token.Token.Placeholder


class Names(Enum):
    RAW = auto()
    SOURCE = auto()
    TARGET = auto()


class TokenError(Exception):
    def __init__(self, message):
        self.message = message


class Lexer:
    def __init__(self, raw_code):
        self.raw_code = raw_code
        self.tokens = list(lex(self.raw_code, HexRaysLexerComplete()))

    def get_tokens(self, var_names=Names.RAW):
        """Generate tokens from a raw_code string, skipping comments.

        Keyword arguments:
        var_names -- Which variable names to output (default RAW).
        """
        previous_string = None
        # print(self.tokens)
        for (token_type, token) in self.tokens:
            # Pygments breaks up strings into individual tokens representing
            # things like opening quotes and escaped characters. We want to
            # collapse all of these into a single string literal token.
            if previous_string and not is_token_subtype(token_type, Token.String):
                yield (Token.String, previous_string)
                previous_string = None
            if is_token_subtype(token_type, Token.String):
                if previous_string:
                    previous_string += token
                else:
                    previous_string = token
            elif is_token_subtype(token_type, Token.Number):
                yield (token_type, token)
            # Skip comments
            elif is_token_subtype(token_type, Token.Comment):
                continue
            # Skip the :: token added by HexRays
            elif is_token_subtype(token_type, Token.Operator) and token == '::':
                continue
            # Replace the text of placeholder tokens
            elif is_token_subtype(token_type, Token.Placeholder):
                yield {
                    Names.RAW : (token_type, token),
                    Names.SOURCE : (token_type, token.split('@@')[2]),
                    Names.TARGET : (token_type, token.split('@@')[3]),
                }[var_names]
            elif not is_token_subtype(token_type, Token.Text):
                yield (token_type, token.strip())
            # Skip whitespace
            elif is_token_subtype(token_type, Token.Text):
                continue
            else:
                raise TokenError(f"No token ({token_type}, {token})")

class HexRaysLexerComplete(JavaLexer):
    # Additional tokens
    tokens = {
        'root' : [
            (r'@@VAR_[0-9]+@@\w+@@\w+', Token.Placeholder.Var),
            inherit
        ]
    }

class CTLexer:
    def __init__(self, raw_code):
        self.raw_code = raw_code
        self.tokens = list(lex(self.raw_code, HexRaysLexerPartial()))

    def get_tokens(self, var_names=Names.RAW):
        """Generate tokens from a raw_code string, skipping comments.

        Keyword arguments:
        var_names -- Which variable names to output (default RAW).
        """
        previous_string = None
        # print(self.tokens)
        for (token_type, token) in self.tokens:
            # Pygments breaks up strings into individual tokens representing
            # things like opening quotes and escaped characters. We want to
            # collapse all of these into a single string literal token.
            if previous_string and not is_token_subtype(token_type, Token.String):
                yield (Token.String, previous_string)
                previous_string = None
            if is_token_subtype(token_type, Token.String):
                if previous_string:
                    previous_string += token
                else:
                    previous_string = token
            elif is_token_subtype(token_type, Token.Number):
                yield (token_type, token)
            # Skip comments
            elif is_token_subtype(token_type, Token.Comment):
                continue
            # Skip the :: token added by HexRays
            elif is_token_subtype(token_type, Token.Operator) and token == '::':
                continue
            # Replace the text of placeholder tokens
            elif is_token_subtype(token_type, Token.Placeholder):
                yield {
                    Names.RAW: (token_type, token),
                    Names.SOURCE : (token_type, token.split('@@')[1]),
                    Names.TARGET: (token_type, ''),
                }[var_names]
            elif not is_token_subtype(token_type, Token.Text):
                yield (token_type, token.strip())
            # Skip whitespace
            elif is_token_subtype(token_type, Token.Text):
                continue
            else:
                raise TokenError(f"No token ({token_type}, {token})")

class HexRaysLexerPartial(JavaLexer):
    # Additional tokens
    tokens = {
        'root' : [
            (r'@@\w+@@', Token.Placeholder.Var),
            inherit
        ]
    }




### raw_code and code_tokens
import re
import uuid
import hashlib

def compare_methods(generator_a, generator_b):
    a_list = list(generator_a)
    b_list = list(generator_b)

    if len(a_list) != len(list(b_list)):
        # print("Number of fields in the files are different.")
        return None
        
    a_diff, b_diff = [], []
    for a, b in zip(a_list, b_list):
        if a[0] == Token.Name.Attribute and a[1] not in a_diff and a[1] != b[1]:
            a_diff.append(a[1])
            b_diff.append(b[1])
    return tuple(zip(a_diff, b_diff))

def get_func(func, obfuscated_strings):
    norm_func = func
    for original_string, obfuscated_string in obfuscated_strings:
        pattern = r'\b{}\b'.format(re.escape(original_string))  # Construct regex pattern to match only whole words
        func = re.sub(pattern, f'@@{obfuscated_string}@@{original_string}@@', func)  # Replace only exact matches
        norm_func = re.sub(pattern, f'@@{normalize_var(obfuscated_string)}@@{normalize_var(original_string)}@@', norm_func)
    return func, norm_func

def normalize_var(var):
    var = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', var)
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', var).lower()

def parse_methods_in_file(filename_a, filename_b):
    methods_a = get_methods_from_file(filename_a)
    methods_b = get_methods_from_file(filename_b)

    if methods_a.keys() == methods_b.keys():
        methods = []
        for method in methods_a.keys():
            tokens_a = Lexer(methods_a[method]['code']).get_tokens()
            tokens_b = Lexer(methods_b[method]['code']).get_tokens()

            obfuscated_strings_tuples_list = compare_methods(tokens_a, tokens_b)
            if obfuscated_strings_tuples_list is None or len(obfuscated_strings_tuples_list) == 0: continue

            orig_func = methods_a[method]['code'].strip()
            orig_func = re.sub(r' {4}', '\t', orig_func)

            id = uuid.uuid1().int
            mongo_id = id
            md5 = hashlib.md5(orig_func.encode()).hexdigest()

            func_name = method
            func, norm_func = get_func(orig_func, obfuscated_strings_tuples_list)

            var = [vars[0] for vars in obfuscated_strings_tuples_list]

            vars_map = [[vars[0], normalize_var(vars[0])] for vars in obfuscated_strings_tuples_list]

            method_obj = {'id': id, 'mongo_id': mongo_id, 'md5': md5, 'func_name': func_name, 'func': func, 'norm_func': norm_func, 'var': var, 'vars_map': vars_map}

            methods.append(method_obj)

        return methods


### process an APK
import os

def decompile_apk(apk_path, apk_name, tmp_dir):
    out_dir = os.path.join(tmp_dir, apk_name)
    os.system(f"jadx {apk_path} -d {out_dir} -r")
    return out_dir

def list_java_files(directory):
    java_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".java"):
                java_files.append(os.path.join(root, file))
    return java_files

def find_shared_files(directory1, directory2):
    java_files_dir1 = set([file[len(directory1)+1:] for file in list_java_files(directory1)])
    java_files_dir2 = set([file[len(directory2)+1:] for file in list_java_files(directory2)])
    shared_files = java_files_dir1.intersection(java_files_dir2)
    return list(shared_files)

def files_have_different_content(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        content1 = f1.read()
        content2 = f2.read()
        return content1 != content2
    
def get_shared_and_different_files(directory1, directory2, shared_files):
    shared_and_different_files = []
    for f in shared_files:
        file1 = os.path.join(directory1, f)
        file2 = os.path.join(directory2, f)
        if files_have_different_content(file1, file2):
            shared_and_different_files.append((file1, file2))
    return shared_and_different_files

# def filter_files(shared_files): #???
#     filtered_paths = [path for path in shared_files if '/android/' not in path and '/androidx/' not in path and '/kotlin/' not in path and '/kotlinx/' not in path]
#     return filtered_paths

def get_training_files_paths(apk1, apk2):
    tmp_dir = './tmp'
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.makedirs(tmp_dir)

    apk1_name = os.path.splitext(apk1)[0]
    apk2_name = os.path.splitext(apk2)[0]
    
    out_dir_1 = decompile_apk(apk1, apk1_name, tmp_dir)
    out_dir_2 = decompile_apk(apk2, apk2_name, tmp_dir)

    shared_files = find_shared_files(out_dir_1, out_dir_2)
    # filtered_files = filter_files(shared_files)
    shared_and_different_files = get_shared_and_different_files(out_dir_1, out_dir_2, shared_files)
    return shared_and_different_files



### raw_code and code_tokens on two APKs
import json
import hashlib
import shutil

# def create_out_file(apk, file, tmp_dir):
#     file_general_path = '/'.join(file.split('/')[3:])
#     # filename = hashlib.sha256(file_general_path.encode()).hexdigest()
#     # filename = file_general_path.replace('/','-')
#     filename = hashlib.md5((file_general_path).encode()).hexdigest()
#     # with open('files.txt', 'a') as f:
#     #     f.write(f'{filename}\n')
#     out_file_name = f'{filename}.jsonl'
#     out_file_path = os.path.join(tmp_dir, out_file_name)
#     print(out_file_path)
#     if os.path.isfile(out_file_path):
#         print(f"Error: {out_file_path} already exists")
#     with open(out_file_path, 'w') as f:
#         f.write('')
#     return out_file_path

def create_training_data_for_apk(apk1, apk2, md5_list_path, out_jsonl_path):

    with open(md5_list_path, 'r') as f:
        md5_list = f.read().splitlines()

    training_files = get_training_files_paths(apk1, apk2)

    for index, files in enumerate(training_files):
        print(f'# {index} - Processing {files[0]}')
        methods_from_file = parse_methods_in_file(files[0], files[1])
        if methods_from_file is None or len(methods_from_file) == 0: continue

        for method in methods_from_file:
            if method['md5'] not in md5_list:
                with open(md5_list_path, 'a') as f:
                    f.write(method['md5'] + '\n')

                with open(out_jsonl_path, 'a') as f:
                    json.dump(method, f)
                    f.write('\n')
            else:
                print('Skipping duplicate method {}'.format(method['md5']))

## main
import argparse

def main():
    parser = argparse.ArgumentParser(description='Process APK files.')
    parser.add_argument('-p1', '--path1', type=str, help='Path to directory containing APK files')
    parser.add_argument('-p2', '--path2', type=str, help='Path to directory containing APK files')

    args = parser.parse_args()

    path1 = args.path1
    path2 = args.path2

    with open('log.txt', 'w') as f:
        f.write('')

    with open('md5.txt', 'w') as f:
        f.write('')

    with open('out.jsonl', 'w') as f:
        f.write('')

    apks1 = set(os.listdir(path1))
    apks2 = set(os.listdir(path2))

    apks = sorted(list(apks1.intersection(apks2)))

    for index, apk in enumerate(apks):
        print(f'\n{index} - {apk}')
        with open('log.txt', 'a') as f:
            f.write(f'{apk}\n')
        apk1 = os.path.join(path1, apk)
        apk2 = os.path.join(path2, apk)
        create_training_data_for_apk(apk1, apk2, 'md5.txt', 'out.jsonl')

if __name__ == '__main__':
    main()