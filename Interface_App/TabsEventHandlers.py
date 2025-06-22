import pygame
import os
from typing import Dict
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from TabsComponents.RadioButtonsList import RadioButtonsList
from TabsComponents.Button import Button
from TabsComponents.InputBox import InputBox
from Helpers.processExperimentalDataFiles import modeling_list_for_pumping, get_data_folder, create_vocabulary_pumping_data
from Constants.lists import NTUPLE_VARS
from Helpers.processUserDataFiles import save_vocabulary_on_host, read_vocabulary_on_host, prepare_file_for_Init, parse_tmva_params
from Helpers.execute_local_commands import create_directory
from Helpers.enterHelpers import decrypt_credentials
from SSHManager import SSHManager
data_and_mc_selected_params = {}
selections_selected_params = {}
existing_data_input_params = {}
backgrounds_input_params = {}
tmva_params = {}
i = 0 #counter for backgrounds


def handle_events_Data_and_MC(event, pumping_list, modeling_signal_list, modeling_background_list, ntuples_vars_list,
                              link, launch_button):
    global data_and_mc_selected_params

    pumping_list.handle_event(event)
    modeling_signal_list.handle_event(event)
    modeling_background_list.handle_event(event)
    ntuples_vars_list.handle_event(event)
    link.handle_event(event)

    if event.type == pygame.MOUSEBUTTONDOWN:
        # Выбор элемента из списка
        if pumping_list.handle_click(event.pos):
            # After each change in chose of pumping reset button and lists
            launch_button.set_pressed(False)
            modeling_signal_list.set_projects([])
            modeling_background_list.set_projects([])
            ntuples_vars_list.set_projects([])
            if pumping_list.selected_project is not None:
                selected_pumping_release = pumping_list.projects[pumping_list.selected_project]
                selected_pumping = selected_pumping_release.split("-")[0]
                data_and_mc_selected_params["pumping"] = [selected_pumping]
                # После каждого изменения в выборе перекачки надо обнулять выбор моделирования
                data_and_mc_selected_params["signal"] = []
                data_and_mc_selected_params["backgrounds"] = []
                # Сразу добавляем все переменные как выбранные,
                # т.к. их много, и юзер может решить не кликать и взять все
                data_and_mc_selected_params["ntuples_vars"] = NTUPLE_VARS

                # beam points are necessary for Tab Selection, it is better to save them there
                results = create_vocabulary_pumping_data()
                energy_points = results[selected_pumping]["energy_points"]
                data_and_mc_selected_params["energy_points"] = energy_points

                abs_path = os.path.abspath(os.getcwd()) + "/WebPages/" + get_data_folder(selected_pumping) + r"/index.html"
                link.set_url(abs_path)

                modelings = modeling_list_for_pumping(selected_pumping)
                if modelings:
                    modeling_signal_list.set_projects(modelings)

        if modeling_signal_list.handle_click(event.pos):
            if modeling_signal_list.selected_project:
                selected_index = modeling_signal_list.selected_project
                backgrounds = modeling_signal_list.projects[:selected_index] + modeling_signal_list.projects[selected_index + 1:]
                modeling_background_list.set_projects(backgrounds)
                data_and_mc_selected_params["signal"] = [modeling_signal_list.projects[selected_index]]
        if modeling_background_list.handle_click(event.pos):
            if any(modeling_background_list.selected_projects):
                selected_modelings = [modeling for modeling, flag in
                                      zip(modeling_background_list.projects, modeling_background_list.selected_projects) if flag]
                data_and_mc_selected_params["backgrounds"] = selected_modelings
                ntuples_vars = NTUPLE_VARS
                if ntuples_vars:
                    ntuples_vars_list.set_projects(ntuples_vars)

        if ntuples_vars_list.handle_click(event.pos):
            if any(ntuples_vars_list.selected_projects):
                selected_ntuple_vars = [var for var, flag in
                                        zip(ntuples_vars_list.projects, ntuples_vars_list.selected_projects) if flag]
                data_and_mc_selected_params["ntuples_vars"] = selected_ntuple_vars

        if launch_button.is_clicked(event.pos):
            launch_button.set_pressed(True)
            save_vocabulary_on_host(data_and_mc_selected_params, "data and mc selected params.txt")
            # launch runreco.sh on server

    # Получаем позицию мыши
    mouse_pos = pygame.mouse.get_pos()
    # Обновление состояния ссылки
    link.update(mouse_pos)


project_selected_params = {}


def handle_events_Project(event, proj_name_input, project_button, tab_manager, end_state_boxes, back_buttton):
    global project_selected_params
    proj_name_input.handle_event(event)

    # Обрабатываем события для каждого InputBox
    for box in end_state_boxes:
        box.handle_event(event)
        project_selected_params[box.placeholder] = box.text

    if event.type == pygame.MOUSEBUTTONDOWN:
        if project_button.is_clicked(event.pos):
            project_button.set_pressed(True)
            folder_name = "ML_APP"
            if proj_name_input.text:
                folder_name = proj_name_input.text
            project_selected_params["project_name"] = folder_name
            create_directory(folder_name)
            save_vocabulary_on_host(project_selected_params, "project_selected_params.txt", folder_name)

            username, password = decrypt_credentials()

            '''
            Если сервер не доступен, эта часть долго виснет 
            Пока не придумано, как сделать так, чтоюы не зависало
            
            ssh_manager = SSHManager("sndhw3.inp.nsk.su", 22, username, password)
            try:

                if ssh_manager.connect():
                    comand0 = f"mkdir /online/users2/{username}/{folder_name}"
                    stdout, stderr = ssh_manager.run_command(comand0)

            finally:
                ssh_manager.close()
            '''
            tab_manager.active_tab = 1  # После подтверждения перекидываем на следующую вкладку "Данные и МС"



def handle_events_Selections(
        event: pygame.event.Event,
        ntuples_vars_selected_list: RadioButtonsList,
        beam_points_list: RadioButtonsList,
        left_border_input: InputBox,
        right_border_input: InputBox,
        selections_input: InputBox,
        optimize_selections_button: Button,
        renew_hist_button: Button ):

    ntuples_vars_selected_list.handle_event(event)
    beam_points_list.handle_event(event)
    left_border_input.handle_event(event)
    right_border_input.handle_event(event)
    selections_input.handle_event(event)

    data_and_mc_params = read_vocabulary_on_host("data and mc selected params.txt")
    # Check if there are selected var in file
    if data_and_mc_params:
        try:
            ntuples_vars = data_and_mc_params["ntuples_vars"]
            energy_points = data_and_mc_params["energy_points"]

            if ntuples_vars:
                ntuples_vars_selected_list.set_projects(ntuples_vars)
            if energy_points and not beam_points_list.projects:
                beam_points_list.set_projects(energy_points)
        except KeyError as e:
            # TODO
            # create function for drawing warning message
            pass


    if event.type == pygame.MOUSEBUTTONDOWN:
        if ntuples_vars_selected_list.handle_click(event.pos):
            # at each press clear the input box for selection conditions
            selections_input.text = ""
            left_border_input.text = ""
            right_border_input.text = ""
            renew_hist_button.is_pressed = False

        if beam_points_list.handle_click(event.pos):
            print("beam points list clicked")
            if any(beam_points_list.selected_projects):
                # ask about beams
                selected_beams = [beam for beam, flag in
                                  zip(beam_points_list.projects, beam_points_list.selected_projects) if flag]

        if optimize_selections_button.is_clicked(event.pos):
            pass

        if renew_hist_button.is_clicked(event.pos):
            renew_hist_button.is_pressed = not renew_hist_button.is_pressed



def handle_events_TMVA(
    event: pygame.event.Event,
    ntuples_vars_selected_list: RadioButtonsList,
    discriminators_list: RadioButtonsList,
    backgrounds_list: RadioButtonsList,
    backgrounds_selection_input: InputBox,
    signal_selection_input: InputBox,
    launch_train_button: Button):
    '''
    this function is for new data
    for existing one need to create a new function
    '''

    ntuples_vars_selected_list.handle_event(event)
    discriminators_list.handle_event(event)
    backgrounds_list.handle_event(event)
    backgrounds_selection_input.handle_event(event)
    signal_selection_input.handle_event(event)

    data_and_mc_params = read_vocabulary_on_host("data and mc selected params.txt")
    if data_and_mc_params and not ntuples_vars_selected_list.projects and not backgrounds_list.projects:
        signal = data_and_mc_params["signal"][0]
        tmva_params['signal'] = signal

    if event.type == pygame.MOUSEBUTTONDOWN:
        if ntuples_vars_selected_list.handle_click(event.pos):
            pass

        if discriminators_list.handle_click(event.pos):
            pass

        if backgrounds_list.handle_click(event.pos):
            pass


        if launch_train_button.is_clicked(event.pos):
            launch_train_button.is_pressed = not launch_train_button.is_pressed
            if any(discriminators_list.selected_projects):
                selected_discriminators = [discr for discr, flag in
                                  zip(discriminators_list.projects, discriminators_list.selected_projects) if flag]
                tmva_params['discriminators'] = selected_discriminators

            if any(ntuples_vars_selected_list.selected_projects):
                selected_vars = [var for var, flag in
                                  zip(ntuples_vars_selected_list.projects, ntuples_vars_selected_list.selected_projects) if flag]
                tmva_params['ntuples_vars'] = selected_vars

            if any(backgrounds_list.selected_projects):
                selected_backs = [back for back, flag in
                                  zip(backgrounds_list.projects, backgrounds_list.selected_projects) if flag]
                tmva_params['backgrounds'] = selected_backs

            if signal_selection_input.text:
                tmva_params['selections_signal'] = [signal_selection_input.text]

            if backgrounds_selection_input.text:
                tmva_params['selections_back'] = [backgrounds_selection_input.text]

            save_vocabulary_on_host(tmva_params, 'tmva_params2.txt')
            #generate_tmva_script(input_filename="ML_APP/tmva_params2.txt", output_filename="ML_APP/TMVAnalysis.C")



def handle_events_Existing_Data(
    event: pygame.event.Event,
    input_boxes: Dict,
    pumping_list: RadioButtonsList,
    go_to_draw_button: Button,
    add_background_button: Button):

    global i
    for name, box in input_boxes.items():
        box.handle_event(event)
    pumping_list.handle_event(event)
    if event.type == pygame.MOUSEBUTTONDOWN:
        if pumping_list.handle_click(event.pos):
            if pumping_list.selected_project:
                selected_pumping = pumping_list.projects[pumping_list.selected_project]

                # beam points are necessary for Tab Selection, it is better to save them there
                results = create_vocabulary_pumping_data()
                energy_points = results[selected_pumping]["energy_points"]
                existing_data_input_params["energy_points"] = energy_points

                existing_data_input_params["pumping"] = selected_pumping
                #print(pumping_list.projects[pumping_list.selected_project])
        if add_background_button.is_clicked(event.pos):
            i+=1
            for name, box in input_boxes.items():
                if box.text and "background" in name:
                    existing_data_input_params[name[:-6] + str(i)] = box.text
                    box.text = ""

        if go_to_draw_button.is_clicked(event.pos):
            go_to_draw_button.set_pressed(True)
            for name, box in input_boxes.items():
                if box.text and "background" not in name:
                    existing_data_input_params[name[:-6]] = box.text
                if box.text and "background" in name:
                    i+=1
                    existing_data_input_params[name[:-6] + str(i)] = box.text

            save_vocabulary_on_host(existing_data_input_params, "existing data input params.txt")
            # check if data is enough !
            prepare_file_for_Init("ML_APP/existing data input params.txt", "ML_APP/file for Init.txt")
            # generate scripts
            # send to sndhw3, launch Init, launch FirstDrawCommand.sh and get list of vars to draw and pictures


def handle_events_TMVA_results(event, picture_buttons, backgrounds_selected_list):
    for btn in picture_buttons:
        btn.handle_event(event, picture_buttons)

    if event.type == pygame.MOUSEBUTTONDOWN:
        if backgrounds_selected_list.handle_click(event.pos):
            if backgrounds_selected_list.selected_project is not None:
                selected_bkg = backgrounds_selected_list.projects[backgrounds_selected_list.selected_project]
                for btn in picture_buttons:
                    selected_bkg = "KsKlpi022" # пока так, чтобы рисовать
                    btn.update_image_path_with_background(selected_bkg)

def handle_events_TMVA_usage(event, discriminators_selected_list, generate_selector_button):
    pass
