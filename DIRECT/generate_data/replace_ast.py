import tarfile
from io import BytesIO

def process_jsonl_content(content, string_a, string_b):
    """
    Process the content of a single jsonl file.
    Replaces '"ast": {}'.
    """
    modified_lines = []
    for line in content.splitlines():
        modified_line = line.replace(string_a, string_b)
        modified_lines.append(modified_line)
    return "\n".join(modified_lines)

def process_tar_gz(input_path, output_path, string_a, string_b):
    """
    Process each jsonl file in the input tar.gz archive.
    Outputs a new tar.gz archive with modified jsonl files.
    """
    # Create a new tar.gz archive for output
    with tarfile.open(output_path, "w:gz") as tar_out:
        with tarfile.open(input_path, "r:gz") as tar_in:
            for member in tar_in.getmembers():
                # Ensure we only process .jsonl files
                if member.isfile() and member.name.endswith('.jsonl'):
                    # Extract the file content
                    f = tar_in.extractfile(member)
                    content = f.read().decode("utf-8")
                    
                    # Process the .jsonl content
                    modified_content = process_jsonl_content(content, string_a, string_b)
                    
                    # Convert modified content back to bytes
                    bytes_content = modified_content.encode("utf-8")
                    
                    # Create a new TarInfo object to add to the output tar file
                    info = tarfile.TarInfo(name=member.name)
                    info.size = len(bytes_content)
                    
                    # Add the modified file to the output archive
                    tar_out.addfile(tarinfo=info, fileobj=BytesIO(bytes_content))

# Example usage:
string_a = '"ast": {}'
string_b = '"ast":{"node_id":0,"node_type":"block","address":"0040142E","name":"net_written","children":[{"node_id":1,"node_type":"if","address":"0040142E","children":[{"node_id":2,"node_type":"block","address":"0040143A","children":[{"node_id":3,"node_type":"expr","address":"0040143A","children":[{"node_id":4,"node_type":"asg","address":"0040143A","x":{"node_id":5,"node_type":"var","address":"FFFFFFFFFFFFFFFF","parent_address":"0040143A","var_id":"VAR_93","type_tokens":["int64"],"ref_width":8,"type":"__int64","old_name":"result","is_arg":false,"new_name":"result"},"y":{"node_id":6,"node_type":"call","address":"0040143A","x":{"node_id":7,"node_type":"obj","address":"FFFFFFFFFFFFFFFF","parent_address":"0040143A","name":"sel_rfd_unfreeze","type_tokens":["int64","fastcall","*","int64"],"ref_width":-1,"type":"__int64 (__fastcall *)(__int64)"},"type_tokens":["int64"],"type":"__int64","children":[{"node_id":8,"node_type":"obj","address":"00401437","ref_width":8,"type_tokens":["int64"],"name":"ptyr","type":"__int64"}]},"type_tokens":["int64"],"type":"__int64"}]}]},{"node_id":9,"node_type":"ule","address":"0040142E","x":{"node_id":10,"node_type":"var","address":"FFFFFFFFFFFFFFFF","parent_address":"0040142E","var_id":"VAR_94","type_tokens":["unsigned","int64"],"ref_width":8,"type":"unsigned __int64","old_name":"a2","is_arg":true,"new_name":"bufsize"},"y":{"node_id":11,"node_type":"num","address":"00401426","name":"NUMBER","type_tokens":["signed","int"],"type":"signed int"},"type_tokens":["bool"],"type":"bool"}]},{"node_id":12,"node_type":"return","address":"0040143F","children":[{"node_id":13,"node_type":"var","address":"FFFFFFFFFFFFFFFF","parent_address":"0040143F","var_id":"VAR_93","type_tokens":["int64"],"ref_width":8,"type":"__int64","old_name":"result","is_arg":false,"new_name":"result"}]}]}'
input_tar_gz_path = '/Volumes/My Passport/data_gen/archive.tar.gz'
output_tar_gz_path = '/Volumes/My Passport/data_gen/reduced_new.tar.gz'
process_tar_gz(input_tar_gz_path, output_tar_gz_path, string_a, string_b)
