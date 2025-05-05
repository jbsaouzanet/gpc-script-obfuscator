# -*- coding: utf-8 -*-

import re
import random
import string
import os
import sys


error_count = 0
warning_count = 0

# Load GPC script from file with error handling
def load_script(filename=None):
    if filename is None:
        while True:
            filename = input("Enter the pathname or name of your GPC script file: (ex: c:\\myscript.gpc or myscript.gpc): ")

            if not os.path.isfile(filename):
                print(f"❌ Error: File '{filename}' not found. Please enter a valid path.")
                continue  # Ask again
            break

    if not os.path.isfile(filename):
        print(f"❌ Error: File '{filename}' not found. Please provide a valid path.")
        sys.exit(1)

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
            sys.exit(1)


def toggle_dev_mod(script):
    """
    If `define devMod = TRUE;` exists, change it to `define devMod = FALSE;`
    """
    # Define the pattern to match `define devMod = TRUE;`
    pattern = r'\bdefine\s+devMod\s*=\s*TRUE\s*;'

    # Check if the pattern exists in the script
    if re.search(pattern, script):
        # Replace TRUE with FALSE
        script = re.sub(pattern, 'define devMod = FALSE;', script)

    return script


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
    define_map = {define[0]: generate_random_name("RocketMod_") for define in defines}

    for old_name, new_name in sorted(define_map.items(), key=lambda x: len(x[0]), reverse=True):
        print(f"🔄 Replacing define '{old_name}' with '{new_name}'")
        script = re.sub(rf'\bdefine\s+{re.escape(old_name)}\s*=\s*([^;]+);', f'define {new_name} = \\1;', script)

    script = replace_words_securely(script, define_map)
    return script

# Rename uint8 arrays
def rename_uint8_arrays(script):
    uint8_array_pattern = re.compile(r'\bconst\s+uint8\s+([a-zA-Z_][\w]*)\[\]')
    uint8_arrays = set(re.findall(uint8_array_pattern, script))
    uint8_array_map = {arr: generate_random_name("RocketMod_") for arr in uint8_arrays}

    for old_name, new_name in uint8_array_map.items():
        script = re.sub(rf'\b{re.escape(old_name)}\b', new_name, script)

    return script

# Rename functions
def rename_functions(script):
    function_pattern = re.compile(r'\bfunction\s+(\w+)\s*\(')
    functions = set(re.findall(function_pattern, script))
    function_map = {fn: generate_random_name("RocketMod_") for fn in functions}

    for old_name, new_name in function_map.items():
        print(f"🔄 Replacing function '{old_name}' with '{new_name}'")
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

    variable_map = {var: generate_random_name("RocketMod_") for var in variables}

    for old_name, new_name in variable_map.items():
        print(f"🔄 Replacing variable '{old_name}' with '{new_name}'")
        script = re.sub(rf'\b{re.escape(old_name)}\b', new_name, script)

    return script

# Rename integer arrays
def rename_int_arrays(script):
    array_pattern = re.compile(r'\bint\s+([a-zA-Z_][\w]*)\s*\[\d*\];')
    arrays = set(re.findall(array_pattern, script))
    array_map = {arr: generate_random_name("RocketMod_") for arr in arrays}

    for old_name, new_name in array_map.items():
        script = re.sub(rf'\b{re.escape(old_name)}\b', new_name, script)

    return script

# Rename 2D integer arrays
def rename_int_2d_arrays(script):
    int2d_pattern = re.compile(r'\bconst\s+int\s+([a-zA-Z_][\w]*)\[\]\[\]')
    int2d_arrays = set(re.findall(int2d_pattern, script))
    int2d_array_map = {arr: generate_random_name("RocketMod_") for arr in int2d_arrays}

    for old_name, new_name in int2d_array_map.items():
        script = re.sub(rf'\b{re.escape(old_name)}\b', new_name, script)

    return script

# Rename string constants
def rename_string_constants(script):
    global error_count
    global warning_count

    # Match constant string variables
    string_constant_pattern = re.compile(r'\bconst\s+string\s+(\w+)\s*=\s*"([^"]*)";')
    matches = string_constant_pattern.findall(script)

    string_map = {}

    for var_name, value in matches:
        obfuscated_name = generate_random_name("RocketMod_")
        string_map[var_name] = obfuscated_name

    for old_name, new_name in string_map.items():
        # Replace only the variable name in the declaration
        script = re.sub(rf'\b{re.escape(old_name)}\b(?=\s*=\s*")', new_name, script)

        # Replace occurrences of the variable throughout the script
        script = re.sub(rf'\b{re.escape(old_name)}\b', new_name, script)
        print(f"🔄 Replacing string constant '{old_name}' with '{new_name}'")
        # Check if the obfuscated variable name matches the string value (incorrect replacement)
        pattern = re.compile(rf'const string {re.escape(new_name)}\s*=\s*"{re.escape(new_name)}";')
        if pattern.search(script):
            print(f"⚠️ Warning: String constant '{old_name}' was replaced incorrectly with its own name '{new_name}'.")
            warning_count += 1
    return script




# Rename string arrays
def rename_string_arrays(script):
    string_array_pattern = re.compile(r'\bconst\s+string\s+([a-zA-Z_][\w]*)\[\]')
    string_arrays = set(re.findall(string_array_pattern, script))
    string_array_map = {arr: generate_random_name("RocketMod_") for arr in string_arrays}

    for old_name, new_name in string_array_map.items():
        print(f"🔄 Replacing string constant '{old_name}' with '{new_name}'")
        script = re.sub(rf'\b{re.escape(old_name)}\b', new_name, script)

    return script

# Rename combos
def rename_combos(script):
    combo_pattern = re.compile(r'\bcombo\s+([a-zA-Z_][\w]*)\s+\{')
    combos = set(re.findall(combo_pattern, script))

    combo_map = {combo: generate_random_name("RocketMod_") for combo in combos}

    for old_name, new_name in combo_map.items():
        script = re.sub(rf'\bcombo\s+{re.escape(old_name)}\s+\{{', f'combo {new_name} {{', script)
        script = re.sub(rf'\b{re.escape(old_name)}\b', new_name, script)

    return script

import re

def rename_enums(script):
    """
    Finds all enums, renames them while ensuring we don't modify enums inside string literals.
    """
    global error_count
    global warning_count
    enum_pattern = re.compile(r'\benum\s*{([\s\S]*?)}', re.MULTILINE)  # Capture multi-line enums
    matches = enum_pattern.findall(script)

    enum_map = {}

    for match in matches:
        enum_lines = match.split(",")  # Split by comma to process individual entries

        # Extract enum names, handling both cases (with and without '=')
        enum_names = []
        for e in enum_lines:
            parts = e.strip().split("=")
            name = parts[0].strip()
            if name:  # Only consider valid names
                enum_names.append(name)

        # Generate obfuscated names
        for name in enum_names:
            enum_map[name] = generate_random_name("RocketMod_")

    # Function to check if an enum is inside double quotes and get the line number
    def is_inside_quotes(script, name):
        in_string = False
        escape = False
        line_number = 1  # Track line number

        for i, char in enumerate(script):
            if char == "\n":
                line_number += 1  # Increment line number at new lines

            if char == "\\" and not escape:  # Handle escaped quotes
                escape = True
                continue

            if char == '"' and not escape:
                in_string = not in_string  # Toggle string state

            escape = False  # Reset escape state

            # Check if the name is inside a string
            if in_string and script[i:i + len(name)] == name:
                return True, line_number

        return False, None

    # Replace each enum name with its obfuscated version
    for old_name, new_name in enum_map.items():
        inside_quotes, line_number = is_inside_quotes(script, old_name)
        if inside_quotes:
            print(f"⚠️ Warning: Enum '{old_name}' appears inside double quotes on line {line_number} and may be a string literal!")
            warning_count += 1
        else:
            print(f"🔄 Replacing enum '{old_name}' with '{new_name}'")
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

# Helper function to replace parameter names inside the function body
def replace_parameters_in_body(function_body, param_map):
    """ Replaces all occurrences of parameters inside the function body using the given mapping. """
    for old_param, new_param in param_map:
        function_body = re.sub(rf'\b{re.escape(old_param)}\b', new_param, function_body)
    return function_body

# Rename function parameters and ensure they are replaced inside the function body
def rename_function_parameters(script):
    # Correctly capture entire function blocks using regex
    function_pattern = re.compile(r'(function\s+\w+)\s*\((.*?)\)\s*\{([\s\S]*?)\n\}', re.DOTALL)

    def obfuscate_parameters(match):
        function_declaration = match.group(1)  # Capture "function fn_name"
        parameters = match.group(2)            # Capture parameters inside parentheses
        function_body = match.group(3)         # Capture the entire function body

        # Process parameter names and store mappings
        param_list = [p.strip() for p in parameters.split(',') if p.strip()]
        param_map = [(param, generate_random_name("RocketMod_")) for param in param_list]

        # Replace parameters in function signature
        obfuscated_signature = f"{function_declaration}(" + ", ".join(new for _, new in param_map) + ") {"

        # Replace parameters inside function body
        function_body = replace_parameters_in_body(function_body, param_map)

        return obfuscated_signature + function_body + "\n}"

    return function_pattern.sub(obfuscate_parameters, script)

import re

def warn_unnecessary_int(script):
    """
    Identifies function signatures where 'int' appears inconsistently before parameters
    and logs a warning with the line number.
    """
    global error_count
    global warning_count
    lines = script.split("\n")  # Split script into lines
    function_pattern = re.compile(r'function\s+\w+\s*\((.*?)\)\s*\{')  # Function signature regex

    for line_num, line in enumerate(lines, start=1):
        match = function_pattern.search(line)
        if match:
            params = match.group(1).split(',')
            has_untyped = any("int" not in p.strip() for p in params)  # Check if there's a mix
            has_int = any("int" in p.strip() for p in params)  # Check if "int" exists

            if has_untyped and has_int:
                # Find the misplaced "int" and log a warning
                for param in params:
                    param = param.strip()
                    if param.startswith("int "):  # Find where int is wrongly placed
                        print(f"❌ Error: Remove 'int' in function parameter list on line {line_num}:")
                        print(f"   -> {line.strip()}")
                        error_count += 1
                        break  # No need to check further


def rename_int16_2d_arrays(script):
    """
    Finds and renames all 2D int16 arrays while replacing occurrences across the script.
    """
    int16_2d_pattern = re.compile(r'\bconst\s+int16\s+([a-zA-Z_][\w]*)\s*\[\]\[\]\s*=\s*\{', re.MULTILINE)
    matches = int16_2d_pattern.findall(script)

    array_map = {array_name: generate_random_name("RocketMod_") for array_name in matches}

    for old_name, new_name in array_map.items():
        print(f"🔄 Replacing int16 2D array '{old_name}' with '{new_name}'")
        script = re.sub(rf'\b{re.escape(old_name)}\b', new_name, script)

    return script

import re

def rename_int16_arrays(script):
    """
    Finds and renames all int16 arrays while replacing occurrences across the script.
    """
    int16_array_pattern = re.compile(r'\bconst\s+int16\s+([a-zA-Z_][\w]*)\s*\[\]\s*=\s*\{', re.MULTILINE)
    matches = int16_array_pattern.findall(script)

    array_map = {array_name: generate_random_name("RocketMod_") for array_name in matches}

    for old_name, new_name in array_map.items():
        print(f"🔄 Replacing int16 array '{old_name}' with '{new_name}'")
        script = re.sub(rf'\b{re.escape(old_name)}\b', new_name, script)

    return script

def warn_colon_at_end_of_line(script):
    """
    Identifies lines where a colon (:) appears at the end and logs an error with the line number.
    """
    global error_count
    global warning_count
    lines = script.split("\n")  # Split script into lines
    pattern = re.compile(r':\s*(//|$)')  # Matches ':' at the end of a line or before a comment

    for line_num, line in enumerate(lines, start=1):
        if pattern.search(line.strip()):  # Check for ':' at the end of the line
            print(f"❌ Error: Unexpected ':' found at the end of line {line_num}:")
            error_count += 1
            print(f"   -> {line.strip()}")


# Process the script
 
def process_script(filename=None):
    global error_count
    global warning_count
    filename, script = load_script(filename)
    warn_unnecessary_int(script)
    warn_colon_at_end_of_line(script)
    script = toggle_dev_mod(script)
    script = rename_uint8_arrays(script)
    script = rename_defines(script)
    script = rename_functions(script)
    script = rename_function_parameters(script)  # <-- Added this step
    script = rename_variables(script)
    script = rename_int_arrays(script)
    script = rename_int_2d_arrays(script)
    script = rename_int16_arrays(script)
    script = rename_int16_2d_arrays(script)
    script = rename_string_constants(script)
    script = rename_string_arrays(script)
    script = rename_combos(script)
    script = rename_enums(script)
    # Replace every newline by a space
    script = script.replace('\n', ' ')
    script = prepend_obfuscation_comment(script)  # Add message at the top
    new_filename = save_script(filename, script)
    print("\n✅ Script processed with :")
    print(f"❌ Total Errors: {error_count}")
    print(f"⚠️ Total Warnings: {warning_count}")
    print(f"📄 Saved as: {new_filename}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        process_script(sys.argv[1])
    else:
        process_script()
