# -*- coding: utf-8 -*-

import re
import random
import string
import os

# Load GPC script from file with error handling
def load_script():
    while True:
        filename = input("Enter the pathname or name of your GPC script file: (ex: c:\\myscript.gpc or myscript.gpc): ")
        
        if not os.path.isfile(filename):
            print(f"❌ Error: File '{filename}' not found. Please enter a valid path.")
            continue  # Ask again
        
        try:
            with open(filename, "r", encoding="utf-8") as file:
                content = file.read()
            return filename, remove_comments(content)
        except UnicodeDecodeError:
            print(f"⚠️ Error: Could not decode '{filename}' properly. Trying an alternative encoding...")
            try:
                with open(filename, "r", encoding="windows-1252", errors="replace") as file:
                    content = file.read()
                return filename, remove_comments(content)
            except Exception as e:
                print(f"❌ Critical Error: Could not open '{filename}'. Error: {str(e)}")
                continue  # Ask again

# Remove single-line (//) and multi-line (/* */) comments
def remove_comments(script):
    script = re.sub(r'//.*', '', script)
    script = re.sub(r'/\*.*?\*/', '', script, flags=re.DOTALL)
    return script

# Save updated script to a new file
def save_script(original_filename, content):
    base_name, ext = os.path.splitext(original_filename)
    new_filename = f"{base_name}_obfuscated.gpc"
    with open(new_filename, "w", encoding="utf-8") as file:
        file.write(content)
    return new_filename

# Generate a random name with a prefix
def generate_random_name(prefix):
    return prefix + ''.join(random.choices(string.ascii_letters + string.digits, k=8))

# Rename defines while preserving values (semicolon optional)
def rename_defines(script):
    define_pattern = re.compile(r'\bdefine\s+([a-zA-Z_][\w]*)\s*=\s*([^;]+);')
    defines = set(re.findall(define_pattern, script))
    define_map = {define[0]: generate_random_name("def_") for define in defines}

    for old_name, new_name in sorted(define_map.items(), key=lambda x: len(x[0]), reverse=True):
        script = re.sub(rf'\bdefine\s+{re.escape(old_name)}\s*=\s*([^;]+);', f'define {new_name} = \\1;', script)
        
    script = replace_words_securely(script, define_map)
    return script

# Rename uint8 arrays
def rename_uint8_arrays(script):
    uint8_array_pattern = re.compile(r'\bconst\s+uint8\s+([a-zA-Z_][\w]*)\[\]')
    uint8_arrays = set(re.findall(uint8_array_pattern, script))
    uint8_array_map = {arr: generate_random_name("uint8Arr_") for arr in uint8_arrays}

    for old_name, new_name in uint8_array_map.items():
        script = re.sub(rf'\b{re.escape(old_name)}\b', new_name, script)

    return script

# Rename functions
def rename_functions(script):
    function_pattern = re.compile(r'\bfunction\s+(\w+)\s*\(')
    functions = set(re.findall(function_pattern, script))
    function_map = {fn: generate_random_name("fn_") for fn in functions}

    for old_name, new_name in function_map.items():
        script = re.sub(rf'\bfunction\s+{re.escape(old_name)}\s*\(', f'function {new_name}(', script)
        script = re.sub(rf'\b{re.escape(old_name)}\b', new_name, script)

    return script

# Rename integer variables
def rename_variables(script):
    variable_pattern = re.compile(r'\bint\s+([a-zA-Z_][\w,\s]*)\s*(?:=[^;]*)?;')
    matches = variable_pattern.findall(script)
    variables = set()

    for match in matches:
        var_names = [v.strip() for v in match.split(",")]
        variables.update(var_names)

    variable_map = {var: generate_random_name("var_") for var in variables}

    for old_name, new_name in variable_map.items():
        script = re.sub(rf'\b{re.escape(old_name)}\b', new_name, script)

    return script

# Rename integer arrays
def rename_int_arrays(script):
    array_pattern = re.compile(r'\bint\s+([a-zA-Z_][\w]*)\s*\[\d*\];')
    arrays = set(re.findall(array_pattern, script))
    array_map = {arr: generate_random_name("varArr_") for arr in arrays}

    for old_name, new_name in array_map.items():
        script = re.sub(rf'\b{re.escape(old_name)}\b', new_name, script)

    return script

# Rename 2D integer arrays
def rename_int_2d_arrays(script):
    int2d_pattern = re.compile(r'\bconst\s+int\s+([a-zA-Z_][\w]*)\[\]\[\]')
    int2d_arrays = set(re.findall(int2d_pattern, script))
    int2d_array_map = {arr: generate_random_name("intArr2D_") for arr in int2d_arrays}

    for old_name, new_name in int2d_array_map.items():
        script = re.sub(rf'\b{re.escape(old_name)}\b', new_name, script)

    return script

# Rename string constants
def rename_string_constants(script):
    string_constant_pattern = re.compile(r'\bconst\s+string\s+([a-zA-Z_][\w]*)\s*=')
    string_constants = set(re.findall(string_constant_pattern, script))
    string_constant_map = {const: generate_random_name("str_") for const in string_constants}

    for old_name, new_name in string_constant_map.items():
        script = re.sub(rf'\b{re.escape(old_name)}\b', new_name, script)

    return script

# Rename string arrays
def rename_string_arrays(script):
    string_array_pattern = re.compile(r'\bconst\s+string\s+([a-zA-Z_][\w]*)\[\]')
    string_arrays = set(re.findall(string_array_pattern, script))
    string_array_map = {arr: generate_random_name("strArr_") for arr in string_arrays}

    for old_name, new_name in string_array_map.items():
        script = re.sub(rf'\b{re.escape(old_name)}\b', new_name, script)

    return script

# Rename combos
def rename_combos(script):
    combo_pattern = re.compile(r'\bcombo\s+([a-zA-Z_][\w]*)\s+\{')
    combos = set(re.findall(combo_pattern, script))

    combo_map = {combo: generate_random_name("combo_") for combo in combos}

    for old_name, new_name in combo_map.items():
        script = re.sub(rf'\bcombo\s+{re.escape(old_name)}\s+\{{', f'combo {new_name} {{', script)
        script = re.sub(rf'\b{re.escape(old_name)}\b', new_name, script)

    return script

# Rename enums
def rename_enums(script):
    enum_pattern = re.compile(r'\benum\s*{([^}]*)}', re.MULTILINE)
    matches = enum_pattern.findall(script)

    enum_map = {}

    for match in matches:
        enum_lines = match.split(",")
        enum_names = [e.strip().split("=")[0] for e in enum_lines if e.strip()]

        for name in enum_names:
            enum_map[name] = generate_random_name("enum_")

    for old_name, new_name in enum_map.items():
        script = re.sub(rf'\b{re.escape(old_name)}\b', new_name, script)

    return script

# Prepend obfuscation message at the top of the script
def prepend_obfuscation_comment(script):
    obfuscation_message = "// Obfuscation done with gpc-script-obfuscator script\n"
    obfuscation_message += "// (join Discord: https://discord.gg/7ZGANnFEUS to get more info and last update)\n"
    obfuscation_message += "// you liked ? pay me a coffee : https://buymeacoffee.com/jorel1337\n\n"
    return obfuscation_message + script.strip()


# General function to replace words securely
def replace_words_securely(script, mapping):
    for old_name in sorted(mapping.keys(), key=len, reverse=True):
        new_name = mapping[old_name]
        script = re.sub(rf'\b{re.escape(old_name)}\b', new_name, script)
    return script
    
# Process the script
def process_script():
    filename, script = load_script()
    script = prepend_obfuscation_comment(script)  # Add message at the top
    script = rename_uint8_arrays(script)
    script = rename_defines(script)
    script = rename_functions(script)
    script = rename_variables(script)
    script = rename_int_arrays(script)
    script = rename_int_2d_arrays(script)
    script = rename_string_constants(script)
    script = rename_string_arrays(script)
    script = rename_combos(script)
    script = rename_enums(script)
    new_filename = save_script(filename, script)
    print(f"✅ Script processed! Saved as: {new_filename}")

if __name__ == "__main__":
    process_script()
