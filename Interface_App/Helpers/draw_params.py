import re
import ROOT
import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def update_limits(input_file_path, output_file_path, xmin, xmax, output_image=""):
    """
    Updates a ROOT script (.C file) to apply new x-axis limits for TH1 histograms
    and generates a new ROOT script that saves a plot with the updated limits.

    Arguments:
        input_file_path (str): Path to the original ROOT .C file.
        output_file_path (str): Path to save the updated ROOT .C file.
        xmin (float): New minimum value for the x-axis.
        xmax (float): New maximum value for the x-axis.
        output_image (str): Filename for the output image saved by ROOT script.
    """
    input_file_path = os.path.join(BASE_PATH, input_file_path)
    # Read the input ROOT .C file
    with open(input_file_path, 'r') as file:
        content = file.readlines()

    # Find all TH1 histogram objects in the script
    histograms = []
    for line in content:
        match = re.match(r'TH1\s*\*\s*(\w+)\s*=', line.strip())
        if match:
            histograms.append(match.group(1))  # Extract histogram object name

    # Insert commands just before the closing bracket
    insert_index = -1  # Default in case no closing bracket is found
    for i, line in enumerate(content):
        if line.strip() == "}":  # Find last closing bracket
            insert_index = i
            break

    # Commands to update x-axis limits for histograms
    new_lines = []
    new_lines.append("\n  // Update x-axis limits for histograms\n")
    for hist in histograms:
        new_lines.append(f'  {hist}->GetXaxis()->SetLimits({xmin}, {xmax});\n')

    # Command to save the canvas as an image
    new_lines.append(f'\n  // Save the canvas as an image\n')
    if output_image:
        new_lines.append(f'  c1->SaveAs("{output_image}");\n')
    else:
        param_name = input_file_path.split(".C")[0]
        new_lines.append(f'  c1->SaveAs("{param_name + str(xmin) + "_" + str(xmax) + ".png"}");\n')

    # Insert new lines before the closing bracket
    if insert_index != -1:
        content = content[:insert_index] + new_lines + content[insert_index:]

    # Write the updated script to a new file
    with open(output_file_path, 'w') as file:
        file.writelines(content)

    #print(f"Updated ROOT script saved to {output_file_path}")
    #print(f"The resulting image will be saved as '{output_image}' when the script is executed in ROOT.")


# Example usage:
# update_limits('ML_APP/Pics/beam.C', './new_beam.C', 880, 900)



def execute_root_script(script_path):
    """
    Executes the given ROOT script using PyROOT and saves the output image.

    Arguments:
        script_path (str): Path to the ROOT .C script to be executed.
    """
    # Initialize ROOT without graphical display
    ROOT.gROOT.SetBatch(True)

    # Load and run the ROOT script
    ROOT.gROOT.ProcessLine(f".x {script_path}")


# Specify the path to your updated ROOT script
# new_script_path = "./new_beam.C"

# Execute the script and save the image
# execute_root_script(new_script_path)



