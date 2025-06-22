import pygame
from Helpers.processExperimentalDataFiles import formatted_info_about_pumping
from Helpers.processUserDataFiles import read_vocabulary_on_host, get_picture_path, parse_tmva_params, prepare_dict_for_Selector
from Helpers.draw_additions import *

from Constants.figures import *
from Constants.colors import *
from Constants.sizes import *
from Constants.text import *



def draw_Data_and_MC_tab(screen, pumping_list, modeling_signal_list, modeling_background_list, ntuples_vars_list, link, launch_task_button):

    draw_long_text_in_words(screen, "Выберите перекачку", SELECT_PUMPING_RECT, FONT, BLACK)  # Сама надпись
    pumping_list.draw(screen)  # Отрисовка списка перекачек

    draw_long_text_in_words(screen, "Выберите сигнал", SELECT_SIGNAL_RECT, FONT, BLACK)
    modeling_signal_list.draw(screen)

    draw_long_text_in_words(screen, "Выберите фоны", SELECT_BACKGROUND_RECT, FONT, BLACK)
    modeling_background_list.draw(screen)

    draw_long_text_in_words(screen, "Выберите переменные в NTuple ", SELECT_NTUPLE_VARS_RECT, FONT, BLACK)
    ntuples_vars_list.draw(screen)

    launch_task_button.draw(screen)

    if pumping_list.selected_project is not None:
        draw_rounded_rect(screen, TAB_ACTIVE_COLOR, PUMPING_INFO_RECT, 15, width=2)
        selected_pumping_release = pumping_list.projects[pumping_list.selected_project]
        selected_pumping = selected_pumping_release.split("-")[0]
        text_about_pumping = formatted_info_about_pumping(selected_pumping)
        draw_long_text_in_lines(screen, text_about_pumping, PUMPING_INFO_RECT, FONT, GRAY, center=False)
        link.draw(screen)

    else:
        draw_rounded_rect(screen, TAB_ACTIVE_COLOR, PUMPING_INFO_RECT, 15, width=2)
        text_about_pumping = f"Краткая информация о выбранной перекачке"
        draw_long_text_in_words(screen, text_about_pumping, PUMPING_INFO_RECT, FONT, GRAY)


def draw_Project_tab(screen, project_button, proj_name_input, end_state_boxes, back_button):
    project_button.draw(screen)
    back_button.draw(screen)

    proj_name_rect = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 100, 400, 40)
    draw_text(screen, "Введите название проекта", proj_name_rect, FONT, BLACK)

    proj_name_input.draw(screen)
    end_state_rect = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 + 20, 400, 40)

    draw_text(screen, "Укажите количество частиц каждого вида в конечном состоянии", end_state_rect, FONT,
              BLACK)
    for box in end_state_boxes:
        box.draw(screen)


def draw_Selections_tab(screen, ntuples_vars_selected_list, beam_points_list, left_border, right_border, selections_input,
                        optimize_selections_button,renew_hist_button):
    draw_long_text_in_words(screen, "Выберите для рисования", SELECT_PUMPING_RECT, FONT, BLACK)  # Сама надпись
    ntuples_vars_selected_list.draw(screen)

    beam_points_list.draw(screen)
    draw_long_text_in_words(screen, "Выберите энергию", BEAM_POINTS_RECT, FONT, BLACK)

    end_state_rect = pygame.Rect(MODELING_LIST_POSITION, 80, 2*LISTS_WIDTH, TEXT_HIGH)
    # TODO
    # read end state from a file with settings of project tab
    end_state = ""
    draw_long_text_in_words(screen, "Конечное состояние:" + end_state, end_state_rect, FONT, BLACK)


    # FIRST DRAW
    if ntuples_vars_selected_list.selected_project and not renew_hist_button.is_pressed:
        selected_param = ntuples_vars_selected_list.projects[ntuples_vars_selected_list.selected_project]
        image_paths = get_picture_path(selected_param)
        if image_paths:
            image_png = image_paths['.png'][0]
            image = pygame.image.load(image_png)
            image_resized = pygame.transform.scale(image, (HIST_RECT.width, HIST_RECT.height))
            screen.blit(image_resized, HIST_RECT.topleft)

    if renew_hist_button.is_pressed and left_border.text and right_border.text and ntuples_vars_selected_list.selected_project:
        param = ntuples_vars_selected_list.projects[ntuples_vars_selected_list.selected_project]
        left = left_border.text
        right = right_border.text
        # ReDraw with new limits
        if param and left and right:
            handle_redrawing_of_param(screen, param, left, right)


    draw_rounded_rect(screen, ACTIVE_BUTTON, HIST_RECT, 15, 2)

    draw_long_text_in_words(screen, "Введите границы рисования", INPUT_LIMITS_RECT, FONT, BLACK, horizontal_center=False, vertical_center=False)
    left_border.draw(screen)
    right_border.draw(screen)

    draw_long_text_in_words(screen, "Введите условия отбора", INPUT_SELECTION_CONDITIONS_RECT, FONT, BLACK, horizontal_center=False)
    selections_input.draw(screen)
    optimize_selections_button.draw2(screen)
    renew_hist_button.draw2(screen)





def draw_TMVA_tab(screen, ntuples_vars_selected_list, discriminators_list, backgrounds_list, backgrounds_selection_input, signal_selection_input,
                        launch_train_button):
    data_and_mc_params = read_vocabulary_on_host("data and mc selected params.txt")
    # Check if there are selected var in file
    signal = ""
    if data_and_mc_params:
        signal = data_and_mc_params["signal"][0]

        if not ntuples_vars_selected_list.projects and not backgrounds_list.projects:
            ntuples_vars = data_and_mc_params["ntuples_vars"]
            backgrounds = data_and_mc_params["backgrounds"]
            if ntuples_vars:
                ntuples_vars_selected_list.set_projects(ntuples_vars)
            if backgrounds:
                backgrounds_list.set_projects(backgrounds)


    draw_long_text_in_words(screen, "Выберите для обучения", SELCTED_PARAMS_RECT, FONT, BLACK)
    ntuples_vars_selected_list.draw(screen)

    draw_long_text_in_words(screen, "Выберите фоны", BACKGROUNDS_LIST_RECT, FONT, BLACK)
    backgrounds_list.draw(screen)

    draw_long_text_in_words(screen, "Выбранный сигнал: " + signal, SELECT_BACKGROUND_RECT, FONT, BLACK)

    draw_long_text_in_words(screen, "Выберите Дискриминаторы", DISCRIMINATORS_RECT, FONT, BLACK)
    discriminators_list.draw(screen)

    draw_long_text_in_words(screen, "Условия отбора сигнала", SELECTIONS_SIGNAL_INPUT, FONT, BLACK,
                            horizontal_center=False, vertical_center=True)
    signal_selection_input.draw(screen)

    draw_long_text_in_words(screen, "Условия отбора фонa", SELECTIONS_BACKGR_INPUT, FONT, BLACK,
                            horizontal_center=False)
    backgrounds_selection_input.draw(screen)

    launch_train_button.draw2(screen)


def draw_Existing_Data_tab(screen,data_var_input, data_filename_input, data_path_input, signal_var_input,
                           signal_filename_input, signal_path_input, background_var_input, background_filename_input,
                           background_path_input, pumping_list, go_to_draw_button, add_background_button):

    draw_rounded_rect(screen, TAB_ACTIVE_COLOR, EXISTING_DATA_INPUT_TEXT_RECT, 15, 2)

    draw_long_text_in_words(screen, EXISTING_DATA_TAB_TEXT, EXISTING_DATA_INPUT_TEXT_RECT, FONT, BLACK)  # Сама надпись

    var_name_rect = pygame.Rect(data_var_input.rect.x, 80 + 200 + 8, data_var_input.rect.w, TEXT_RECT_HEIGHT)
    draw_long_text_in_words(screen, "имя переменной", var_name_rect, FONT, BLACK)

    filename_rect = pygame.Rect(data_filename_input.rect.x, 80 + 200 + 8, data_filename_input.rect.w, TEXT_RECT_HEIGHT)
    draw_long_text_in_words(screen, "название текстового файла", filename_rect, FONT, BLACK)

    path_rect = pygame.Rect(data_path_input.rect.x, 80 + 200 + 8, data_path_input.rect.w, TEXT_RECT_HEIGHT)
    draw_long_text_in_words(screen, "путь к папке с результатами (output)", path_rect, FONT, BLACK,
                            vertical_center=False)

    data_rect = pygame.Rect(data_var_input.rect.x - 150, data_var_input.rect.y - 15, 100, data_var_input.rect.h)
    draw_long_text_in_words(screen, "Данные", data_rect, FONT, BLACK)

    data_var_input.draw(screen)
    data_filename_input.draw(screen)
    data_path_input.draw(screen)

    signal_rect = pygame.Rect(signal_var_input.rect.x - 150, signal_var_input.rect.y - 15, 100, signal_var_input.rect.h)
    draw_long_text_in_words(screen, "Cигнал", signal_rect, FONT, BLACK)

    signal_var_input.draw(screen)
    signal_filename_input.draw(screen)
    signal_path_input.draw(screen)

    background_rect = pygame.Rect(background_var_input.rect.x - 150, background_var_input.rect.y - 15, 100,
                                  background_var_input.rect.h)
    draw_long_text_in_words(screen, "Фон", background_rect, FONT, BLACK)

    background_var_input.draw(screen)
    background_filename_input.draw(screen)
    background_path_input.draw(screen)

    background_counter_rect = pygame.Rect(WIDTH // 2 - 2 * LISTS_WIDTH,
                               BACKGROUND_INPUT_START_Y + INPUT_HEIGHT + DISTANCE_BETWEEN_Y, 4 * LISTS_WIDTH,
                               TEXT_RECT_HEIGHT)
    draw_rounded_rect(screen, TAB_ACTIVE_COLOR, background_counter_rect, 15, 2)
    from TabsEventHandlers import i
    draw_long_text_in_words(screen, "Количество добавленных фонов: " + str(i), background_counter_rect, FONT, BLACK)





    pumping_rect = pygame.Rect(WIDTH // 2 - 2 * LISTS_WIDTH,
                               BACKGROUND_INPUT_START_Y + INPUT_HEIGHT + 2*DISTANCE_BETWEEN_Y + TEXT_RECT_HEIGHT, 4 * LISTS_WIDTH,
                               TEXT_RECT_HEIGHT)
    draw_rounded_rect(screen, TAB_ACTIVE_COLOR, pumping_rect, 15, 2)
    draw_long_text_in_words(screen, "Выберите перекачку (опционально)", pumping_rect, FONT, BLACK)
    pumping_list.draw(screen)

    go_to_draw_button.draw(screen)
    add_background_button.draw(screen)

def draw_Enter_screen(screen,username_input, pswd_input, next_button):

    draw_text(screen, "Введите имя пользователя", USERNAME_RECT, FONT, BLACK)
    username_input.draw(screen)

    draw_text(screen, "Введите пароль", PSWD_RECT, FONT, BLACK)
    pswd_input.draw(screen)

    next_button.draw(screen)


def draw_Choose_screen(screen, new_project_button, existing_project_button, own_data_button, back_button):
    new_project_button.draw(screen)
    existing_project_button.draw(screen)
    own_data_button.draw(screen)
    back_button.draw(screen)


def draw_TMVA_results_tab(screen, backgrounds_selected_list, picture_buttons,  ):
    backgrounds_selected_list.draw(screen)
    draw_rounded_rect(screen, TAB_ACTIVE_COLOR, PICTURE_RECT, 15, width=2)

    draw_long_text_in_words(screen, "Выберите фон, для которого будем рисовать", SELECT_BKG_RECT, FONT, BLACK)  # Сама надпись
    tmva_params_selected = parse_tmva_params("tmva_params.txt")
    if tmva_params_selected:
        backgrounds = tmva_params_selected["backgrounds"]
        if backgrounds and not backgrounds_selected_list.projects:
            backgrounds_selected_list.set_projects(backgrounds)

    # Рисуем все кнопки
    for btn in picture_buttons:
        btn.draw2(screen)  # Используем draw2 для многострочного текста

    # Рисуем изображение активной кнопки
    for btn in picture_buttons:
        if btn.is_pressed:
            btn.draw_image(screen)


def draw_TMVA_usage(screen, discriminators_selected_list, generate_selector_button):
    # рисуем как вкладку Отбор
    draw_long_text_in_words(screen, "Выберите дискр+фон для применения", SELECT_TO_DRAW_RECT, FONT, BLACK)
    discriminators_selected_list.draw(screen)
    draw_rounded_rect(screen, ACTIVE_BUTTON, HIST_RECT, 15, 2)
    generate_selector_button.draw(screen)

    tmva_params_selected = prepare_dict_for_Selector("tmva_params.txt")
    if tmva_params_selected:
        discrs = tmva_params_selected["tmva_vars_for_clone"]
        if discrs and not discriminators_selected_list.projects:
            discriminators_selected_list.set_projects(discrs)
    image = pygame.image.load("ML_APP/TMVAusage/BDTKsKl2pi0.png")
    image_resized = pygame.transform.scale(image, (HIST_RECT.width, HIST_RECT.height))
    screen.blit(image_resized, HIST_RECT.topleft)
