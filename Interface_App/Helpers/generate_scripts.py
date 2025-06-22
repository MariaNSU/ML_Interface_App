import os
from processUserDataFiles import prepare_dict_for_Selector
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def generate_init_c(input_filename, output_filename="ML_APP/Init.C", pattern_filename="ML_APP/Init_pattern.C "):
    # Read pattern file and prepare for data substitution
    with open(pattern_filename, "r") as pattern_file:
        pattern_content = pattern_file.read()

    # Placeholder for TChain definitions
    tchain_definitions = ""

    # Process each line in the input file
    with open(input_filename, "r") as infile:
        for line in infile:
            if line.strip():  # Check if line is not empty
                parts = line.split()
                if len(parts) >= 4:  # Check if there are enough parts in the line
                    comment_type = parts[0]
                    var_name = parts[1]
                    file_name = parts[2]
                    path = parts[3]

                    # Prepare TChain definition string
                    tchain_definitions += f'    // {comment_type}\n'
                    tchain_definitions += f'    TChain* {var_name} = makeCh("{file_name}", "{path}", "t1");\n\n'

    # Substitute placeholders in pattern with generated data
    output_content = pattern_content.replace("{TCHAIN_DEFINITIONS}", tchain_definitions)

    # Write the final content to the output file
    with open(output_filename, "w") as outfile:
        outfile.write(output_content)


# input_filename = "ML_APP/data and mc input params.txt"
# generate_init_c(input_filename)


def generate_runreco():
    pass


def parse_input_file(filename):
    data = {}

    with open(filename, 'r') as file:
        for line in file:
            if ":" in line:
                key, values = line.split(":", 1)
                key = key.strip()
                values = values.strip().strip("[]").replace('"', '').split(',')
                data[key] = [value.strip() for value in values if value.strip()]

    return data

def generate_tmva_script(input_filename="ML_APP/tmva_params.txt", output_filename="ML_APP/TMVAnalysisMy.C",
                         pattern_filename="ML_APP/TMVA_pattern.C"):
    # Разбор входного файла
    input_filename_path = os.path.join(BASE_PATH, input_filename)
    data = parse_input_file(input_filename_path)
    pattern_filename_path = os.path.join(BASE_PATH, pattern_filename)
    output_filename_path = os.path.join(BASE_PATH, output_filename)

    # Чтение шаблона скрипта
    with open(pattern_filename_path, 'r') as file:
        template_lines = file.readlines()

    # Список дискриминаторов из словаря
    discriminators = data['discriminators']

    # Процессинг дискриминаторов (строки 36-78)
    for i, line in enumerate(template_lines):
        if line.strip().startswith("Bool_t Use_"):
            # Получаем имя дискриминатора после "Bool_t Use_"
            discriminator_name = line.split()[1].split("_")[1].strip('=').strip()
            # Проставляем 1, если дискриминатор в словаре, иначе 0
            if discriminator_name in discriminators:
                template_lines[i] = line.replace("= 0;", "= 1;")
            else:
                template_lines[i] = line.replace("= 1;", "= 0;")

    # Обработка сигналов и фонов
    signal = data['signal'][0].strip()
    backgrounds = [bg.strip() for bg in data['backgrounds']]

    for background in backgrounds:
        script_lines = template_lines.copy()

        # Function Name
        output_filename = output_filename.split("/")[-1]
        function_name = output_filename.replace(".C", f"_{background}")
        function_string = f"void {function_name}( TString myMethodList = \"\" )"

        script_lines = script_lines[:83] + [function_string] + script_lines[84:]

        # Замена названия переменной для сигнала и фона на строках 233 и 234
        signal_section = f'      TTree *signal     = {signal};\n'
        back_section = f'      TTree *background     = {background};\n'
        script_lines = script_lines[:232] +  [signal_section] + [back_section] + script_lines[235:]


        # Обработка переменных ntuples_vars
        ntuples_vars = data['ntuples_vars']
        variables_section = [f'factory->AddVariable("{var}", \'F\');\n' for var in ntuples_vars]

        start, end = 249, 320  # предполагаемые линии переменных в шаблоне
        script_lines = script_lines[:start] + variables_section + script_lines[end:]

        # Обработка условий отбора для сигнала и фона
        selection_signal = data['selections_signal'][0].strip()
        selection_back = data['selections_back'][0].strip()

        for i, line in enumerate(script_lines):
            if 'TCut mycuts =' in line:
                script_lines[i] = f'TCut mycuts = "{selection_signal}";\n'

            if 'TCut mycutb =' in line:
                script_lines[i] = f'TCut mycutb = "{selection_back}";\n'

        # Запись скрипта в выходной файл
        output_filename_current = output_filename_path.replace(".C", f"_{background}.C")
        with open(output_filename_current, 'w') as file:
            file.writelines(script_lines)

        print(f"Скрипт для фона '{background}' сохранён как '{output_filename_current}'.")

# Пример вызова функции
#generate_tmva_script()

def fill_generated_selector(input_file, output_file, config_dict, red_list_path,
                            weights_base_dir="/online/users2/harlamov/TMVA/macros/"):
    """
    Fill the generated selector file with TMVA-related code based on the configuration.

    Args:
        input_file: Path to the generated selector file (sel.cpp)
        output_file: Path to save the filled selector file
        config_dict: Dictionary from prepare_dict_for_Selector()
        red_list_path: Path for the redList variable
        weights_base_dir: Base directory for TMVA weights files
    """
    # Read the original generated file
    input_file_path = os.path.join(BASE_PATH, input_file)
    with open(input_file_path, 'r') as f:
        content = f.read()

    # Prepare the additions
    begin_additions = []
    process_additions = []
    terminate_additions = []

    # 1. Add redList path and file processing at the beginning of Begin()
    begin_additions.append(f'    std::string redList = "{red_list_path}";\n')
    begin_additions.append('''
    std::ifstream f(redList.c_str());

    int N = 0;
    double tmp = 0;
    std::vector<double> x;
    std::vector<double> y;

    int Nco = 0;

    while(!f.eof()) {
        f >> N;
        if(f.fail()) break;
        f >> tmp;
        x.push_back(tmp);
        f >> tmp;
        y.push_back(tmp);
        Nco++;
    }
    f.close();

    if(Nco > 0) {
        const int NN = Nco;
        double *xx = new double[NN];
        double *yy = new double[NN];

        for(int i = 0; i < NN; i++) {
            xx[i] = x[i];
            yy[i] = y[i];
        }

        MCcr = new TSpline3("MCcr", xx, yy, NN);
    } else {
        MCcr = NULL;
    }
    ''')

    # 2. Add file creation and tree initialization
    begin_additions.append('''
    TString option = GetOption();
    fFor = new TFile(option.Data(), "recreate");
    fFor->cd();

    Clone = new TTree("Mas", "Mas");
    ''')

    # 3. Add TMVA branch declarations
    begin_additions.append("    //TMVA branches\n")
    for var in config_dict["tmva_vars_for_clone"]:
        begin_additions.append(f'    Clone->Branch("{var}", &{var}, "{var}/D");\n')

    # 4. Add standard branches that we want to keep
    begin_additions.append('''
    Clone->Branch("CutV", &CutV, "CutV/I");
    Clone->Branch("CutV2", &CutV2, "CutV2/I");
    Clone->Branch("CutV25", &CutV25, "CutV25/I");
    Clone->Branch("CutV30", &CutV30, "CutV30/I");
    Clone->Branch("CutV36", &CutV36, "CutV36/I");
    Clone->Branch("CutV40", &CutV40, "CutV40/I");
    Clone->Branch("CutV45", &CutV45, "CutV45/I");
    Clone->Branch("wMC", &wMC, "wMC/D");
    ''')

    # 5. Add TMVA readers initialization
    begin_additions.append("    //TMVA readers initialization\n")
    for reader_name in config_dict["reader_names"]:
        begin_additions.append(f'    {reader_name} = new TMVA::Reader("!Color");\n')

    # 6. Add variables to each reader
    begin_additions.append("    //Add variables to readers\n")
    for var_desc in config_dict["ntuples_vars"]:
        var_name = var_desc.split('[')[0].split('/')[0]
        begin_additions.append(f'    reader->AddVariable("{var_desc}", &{var_name});\n')

    # 7. Book MVA methods for each reader with customizable paths
    begin_additions.append('''
    TString prefix = "TMVAnalysis";
    ''')

    for reader_name in config_dict["reader_names"]:
        bg_name = reader_name.replace("reader", "")
        weights_dir = f'{weights_base_dir}weights{bg_name}/'
        begin_additions.append(
            f'    {reader_name}->BookMVA("BDT method", "{weights_dir}" + prefix + "_BDT.weights.txt");\n')
        begin_additions.append(
            f'    {reader_name}->BookMVA("Fisher method", "{weights_dir}" + prefix + "_Fisher.weights.txt");\n\n')

    # 8. Process() function content
    process_content = '''   GetEntry(entry);

    // Initialize variables
    wMC = 0;
    if (MCcr) {
        wMC = MCcr->Eval(2*beam)*GetLum(beam)/100000.0;
        if (wMC < 0.0) wMC = 0.0;
    }
'''
    # Initialize TMVA variables
    for var in config_dict["tmva_vars_for_clone"]:
        process_content += f'    {var} = 88888888;\n'

    process_content += '''
    // Initialize other variables
    CutV = 0;
    CutV2 = 0;
    CutV25 = 0;
    CutV30 = 0;
    CutV36 = 0;
    CutV40 = 0;
    CutV45 = 0;

    // Basic cut conditions
    if (cnp == 6 && nn4 == 1 && trin > 0 && ptrn < 0.12 && cosm == 0 && Meta < 800 && Meta > 300 && PTeta < 100 && 
        etot > 400 && etot < (beam * 150.0 / 470 + 480.85) && 
        cx2g[0] < 0 && cx2g[1] < 0 && cx2g[2] < 0 && 
        cx2g[3] < 0 && cx2g[4] < 0 && cx2g[5] < 0 && Ch3pi0 < 100) {
        CutV = 1;
    }

    if (cnp == 6 && nn4 == 1 && trin > 0 && ptrn < 0.12 && cosm == 0 && Meta < 800 && Meta > 300 && 
        etot > 400 && etot < (beam * 150.0 / 470 + 480.85) && 
        cx2g[0] < 0 && cx2g[1] < 0 && cx2g[2] < 0 && 
        cx2g[3] < 0 && cx2g[4] < 0 && cx2g[5] < 0 && Ch3pi0 < 100) {
        CutV2 = 1;
    }

    // Angular cuts
    int a25=0, a30=0, a36=0, a40=0, a45=0;
    for(int zbj = 0; zbj < 6; zbj++) {
        if((ctheta[zbj]*180.0/3.14) > 25 && (ctheta[zbj]*180.0/3.14) < (180-25)) a25++;
        if((ctheta[zbj]*180.0/3.14) > 30 && (ctheta[zbj]*180.0/3.14) < (180-30)) a30++;
        if((ctheta[zbj]*180.0/3.14) > 36 && (ctheta[zbj]*180.0/3.14) < (180-36)) a36++;
        if((ctheta[zbj]*180.0/3.14) > 40 && (ctheta[zbj]*180.0/3.14) < (180-40)) a40++;
        if((ctheta[zbj]*180.0/3.14) > 45 && (ctheta[zbj]*180.0/3.14) < (180-45)) a45++;
    }

    if(CutV2 == 1 && a25 == 6) CutV25 = 1;
    if(CutV2 == 1 && a30 == 6) CutV30 = 1;
    if(CutV2 == 1 && a36 == 6) CutV36 = 1;
    if(CutV2 == 1 && a40 == 6) CutV40 = 1;
    if(CutV2 == 1 && a45 == 6) CutV45 = 1;

    // Evaluate MVA methods
    if(cnp == 6 && nn4 == 1 && trin > 0) {
'''

    # Add MVA evaluations for each reader and discriminator
    for reader_name, bg_name in zip(config_dict["reader_names"], config_dict["backgrounds"]):
        for disc in config_dict["discriminators"]:
            process_content += f'        {disc}{bg_name} = {reader_name}->EvaluateMVA("{disc} method");\n'

    process_content += '''    }

    Clone->Fill();
    return kTRUE;
'''

    # 9. Terminate() function content
    terminate_content = '''    Clone->Write();
    fFor->Close();
    if (MCcr) delete MCcr;
'''

    # Insert the additions into the appropriate places
    # For Begin() - insert after the opening brace
    begin_pos = content.find("void sel::Begin(TTree * /*tree*/)\n{")
    if begin_pos != -1:
        begin_pos = content.find("{", begin_pos) + 1
        content = content[:begin_pos] + "".join(begin_additions) + content[begin_pos:]

    # For Process() - replace the entire function
    process_start = content.find("Bool_t sel::Process(Long64_t entry)")
    process_end = content.find("}", process_start) + 1
    content = content[:process_start] + "Bool_t sel::Process(Long64_t entry)\n{" + process_content + "\n}" + content[
                                                                                                             process_end:]

    # For Terminate() - replace the entire function
    terminate_start = content.find("void sel::Terminate()")
    terminate_end = content.find("}", terminate_start) + 1
    content = content[:terminate_start] + "void sel::Terminate()\n{" + terminate_content + "\n}" + content[
                                                                                                   terminate_end:]

    # Write the modified content
    output_file_path = os.path.join(BASE_PATH, output_file)
    with open(output_file_path, 'w') as f:
        f.write(content)


config = prepare_dict_for_Selector()

fill_generated_selector(
    input_file="ML_APP/mc22Selector.C",
    output_file="ML_APP/NEWmc22Selector.C",
    config_dict=config,
    red_list_path="/online/users2/harlamov/R008-002/yyEta2/eeEtaPAlaRad.txt",
    weights_base_dir="/online/users2/harlamov/TMVA/macros/"
)