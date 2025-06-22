import os
import ast
import re

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def save_vocabulary_on_host(data, filename, dirname="ML_APP"):
    """
    Saves a list or a vocabulary (dictionary) to a file in the specified directory.

    Args:
        data (list or dict): The vocabulary (dictionary) or list to save.
        dirname (str): The path to the directory where the file will be saved.
        filename (str): The name of the file to save the list.

    Returns:
        str: A message indicating success or any failure.
    """
    try:
        directory = os.path.join(BASE_PATH, dirname)
        # Check if the directory exists, if not, create it
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Construct the complete file path
        file_path = os.path.join(directory, filename)

        # Save data to the file depending on its type
        with open(file_path, 'w') as file:
            if isinstance(data, dict):
                # If data is a dictionary, save its keys and values
                for key, value in data.items():
                    file.write(f"{key}: {value}\n")
            elif isinstance(data, list):
                # If data is a list, save its items
                for item in data:
                    file.write(f"{item}\n")
            else:
                return "Invalid data type. Only lists and dictionaries are supported."

        return f"Data successfully saved to {file_path}"

    except Exception as e:
        return f"An error occurred: {e}"


def read_vocabulary_on_host(filename, dirname="ML_APP"):
    """
    Reads data from a file in the specified directory and returns it as a list or dictionary.

    Args:
        filename (str): The name of the file to read data from.
        dirname (str): The path to the directory where the file is located.

    Returns:
        list or dict: The data read from the file, either as a list or dictionary.
        str: A message indicating any failure.
    """
    try:
        directory = os.path.join(BASE_PATH, dirname)
        # Construct the complete file path
        file_path = os.path.join(directory, filename)

        # Check if the file exists
        if not os.path.exists(file_path):
            return f"File not found: {file_path}"

        # Read data from the file
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Determine if the data is a dictionary or a list
        if all(": " in line for line in lines):
            # If all lines contain ": ", interpret it as a dictionary
            data = {}
            for line in lines:
                key, value = line.strip().split(": ", 1)
                string_data = value.strip("[").strip("]").replace("'", "").split(", ")
                value = [item for item in string_data]
                data[key] = value
            return data
        else:
            # Otherwise, interpret it as a list
            data = [line.strip() for line in lines]
            return data

    except Exception as e:
        return f"An error occurred: {e}"


def prepare_file_for_Init(input_file_path="ML_APP/existing data input params.txt",
                          output_file_path="ML_APP/file for Init.txt") -> None:
    """
    If signal, data or background IS NOT  in input_file, file for Init.C WILL NOT BE PREPARED!!!

    Reads the dictionary like file with info abot data that user type in input fields.

    Example of input_file:
    background_var1: mumumu
    background_filename1: sa;ldjldf
    background_path1: fdjlsajlskla;
    data_var: opopo
    data_filename: gfgddskj
    data_path: online

    Write to ouput file:
    data opopo gfgddskj online
    background1 mumumu sa;ldjldf fdjlsajlskla;

    Output file is used for generating Init.C
    """
    # Read and normalize the input from file
    absolute_input_path = os.path.join(BASE_PATH, input_file_path)
    absolute_output_path = os.path.join(BASE_PATH, output_file_path)
    with open(absolute_input_path, 'r', encoding='utf-8') as input_file:
        input_content = input_file.read().strip()
    # Extract key-value pairs
    parts = input_content.split('\n')
    data = {}
    backgrounds = []
    for part in parts:
        if ': ' in part:
            key, value = part.split(': ', 1)
            data[key] = value

    # Find the maximum number in the keys for preparing all backgrounds
    max_number = max(
        int(key.split('_')[-1].strip('abcdefghijklmnopqrstuvwxyz'))
        for key in data if key.split('_')[-1][-1].isdigit()
    )

    # Check for each number if all parts are available
    for i in range(1, max_number + 1):
        var_key = f'background_var{i}'
        filename_key = f'background_filename{i}'
        path_key = f'background_path{i}'

        if var_key in data and filename_key in data and path_key in data:
            backgrounds.append(f"{data[var_key]} {data[filename_key]} {data[path_key]}")

    if not backgrounds:
        print("Can not prepare file for generating Init.C: backgrounds are empty!")
    # Write to output file
    try:
        with open(absolute_output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(f"data {data['data_var']} {data['data_filename']} {data['data_path']}\n")
            output_file.write(f"signal {data['signal_var']} {data['signal_filename']} {data['signal_path']}\n")
            for i, background in enumerate(backgrounds):
                output_file.write(f"background{i+1} {background}\n")

    except KeyError as e:
        print(f"Can not prepare file for generating Init.C: {e}!")


def get_picture_path(param_name: str, dir_name="ML_APP/Pics"):
    """
    Function to search for images in .png and .C formats within a specified directory
    and return a dictionary categorizing them by file extension.

    Args:
        param_name (str): The name or part of the name of the file to search for.
        dir_name (str): The directory to search in. Default is "ML_APP/Pics".

    Returns:
        dict: A dictionary with extensions as keys and lists of matching file paths as values.
              If no images are found, returns an empty dictionary.
    """
    # Dictionary to store paths categorized by extension
    picture_paths = {".png": [], ".C": []}

    # Supported extensions
    supported_extensions = [".png", ".C"]

    # Walk through directory to identify matching files
    for root, dirs, files in os.walk(dir_name):
        for file in files:
            file_name, file_extension = os.path.splitext(file)
            # Check if the filename matches param_name exactly and extension is supported
            if file_name == param_name and file_extension in supported_extensions:
                picture_paths[file_extension].append(os.path.join(root, file))

            # Check if any images found; if not, return an empty dict
        if not any(picture_paths.values()):
            return {}

        return picture_paths



def check_file(filename:str, directory:str)-> bool:
    """
    Checks if a file exists and is not empty in the specified directory.

    Parameters:
    - filename (str): The file name.
    - directory (str): The directory name.

    Returns:
    - bool: `True` if the file exists and has content; `False` otherwise.
    """
    directory_path = os.path.join(BASE_PATH, directory)
    file_path = os.path.join(directory_path, filename)

    # Check if the file exists
    if os.path.isfile(file_path):
        # Check if the file has any content
        if os.path.getsize(file_path) > 0:
            return True
        else:
            return False
    else:
        return False


def parse_tmva_params(filename="tmva_params.txt", directory="ML_APP"):
    """
    Parses a TMVA parameters file.
    Reads each line, splits by colon, and tries to convert the value
    to a Python type (int, float, list, etc.) using ast.literal_eval.
    Returns a dictionary with parameter names and their values.
    """
    directory_path = os.path.join(BASE_PATH, directory)
    file_path = os.path.join(directory_path, filename)

    params = {}
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comment lines
            if not line or line.startswith('#'):
                continue
            # Only process lines containing a colon
            if ':' not in line:
                continue
            key, value = line.split(':', 1)
            try:
                # Try to parse the value to a Python data type
                value = ast.literal_eval(value.strip())
            except Exception:
                # If parsing fails, keep as a string
                value = value.strip()
            params[key.strip()] = value
    return params

def parse_var_to_draw(filename="variables_to_draw.txt", directory="ML_APP"):
    """
    Reads a file with variables and prepares a dictionary of variables.
    For array variables (detected as [N]), changes them to [12] format,
    keeping the rest of the description unchanged.
    Returns a dictionary where the key is a variable name,
    and the value is its formatted description.
    """
    directory_path = os.path.join(BASE_PATH, directory)
    file_path = os.path.join(directory_path, filename)

    result = {}
    with open(file_path, 'r') as f:
        for line in f:
            var = line.strip()
            # Skip empty lines
            if not var:
                continue
            # Attempt to match variables written as name(N)
            arr_match = re.match(r'^(\w+)\[(\d+)\](.*)', var)
            if arr_match:
                # For arrays, use name[12] in the description
                name = arr_match.group(1)
                desc = f"{name}[12]{arr_match.group(3)}"
            else:
                # For others, extract the name part before '[' or '/'
                name = var.split('[')[0].split('/')[0]
                desc = var
            result[name] = desc
    return result


def prepare_dict_for_Selector(tmva_params_fn="tmva_params.txt", vars_to_draw_fn="variables_to_draw.txt", directory="ML_APP"):
    """
    Main function to collect and prepare all required data.
    Parses both the parameters file and the variables file,
    creates:
      - a list of variables to read for backgrounds and discriminators,
      - a list of reader names,
      - a list of variables for the ntuple.
    Returns a dictionary containing all lists and the raw parsed info.
    """

    directory_path = os.path.join(BASE_PATH, directory)
    tmva_path = os.path.join(directory_path, tmva_params_fn)
    vars_path = os.path.join(directory_path, vars_to_draw_fn)

    # Parse TMVA parameters
    tmva_params = parse_tmva_params(tmva_path)
    # Parse variables to draw
    var_dict = parse_var_to_draw(vars_path)

    # Get discriminators and backgrounds list from TMVA parameters
    disc_list = tmva_params.get('discriminators', [])
    bkg_list = tmva_params.get('backgrounds', [])

    # Form a list of variable names to read by combining discriminators and backgrounds
    tmva_vars_for_clone = [
        f"{d}{b}"
        for d in disc_list
        for b in bkg_list
    ]

    # Build list of reader names for each background
    reader_names = [f"reader{b}" for b in bkg_list]

    tmva_var_names = tmva_params['ntuples_vars']
    ntuples_vars = [var_dict[v] for v in tmva_var_names if v in var_dict]

    return {
        "tmva_vars_for_clone": tmva_vars_for_clone,
        "reader_names": reader_names,
        "ntuples_vars": ntuples_vars,
        "discriminators": disc_list,
        "backgrounds": bkg_list
    }
