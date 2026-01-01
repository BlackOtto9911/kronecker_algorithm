# main.py
import json
import os
import sys

import flet as ft

from kronecker_algorithm_ver_1_0 import kronecker_factorization_ver_1_0, print_polynomial_ver_1_0
from kronecker_algorithm_ver_1_1 import kronecker_factorization_ver_1_1, print_polynomial_ver_1_1
from kronecker_algorithm_ver_1_2 import kronecker_factorization_ver_1_2, print_polynomial_ver_1_2
from kronecker_algorithm_ver_1_3 import kronecker_factorization_ver_1_3, print_polynomial_ver_1_3
from kronecker_algorithm_ver_2 import kronecker_factorization_ver_2, print_polynomial_ver_2
from kronecker_algorithm_ver_3 import kronecker_factorization_ver_3, print_polynomial_ver_3
from kronecker_algorithm_ver_4 import kronecker_factorization_ver_4, print_polynomial_ver_4
from kronecker_algorithm_ver_6 import kronecker_factorization_ver_6, print_polynomial_ver_6
from kronecker_algorithm_ver_5 import kronecker_factorization_ver_5, print_polynomial_ver_5

# функция для загрузки примеров из файла examples.json
examples_data = []
load_data_error = False
def load_examples(data_file_json):
    global examples_data, load_data_error
    try:
        json_path = resource_path(data_file_json)
        if os.path.exists(json_path):  # ← теперь путь корректный
            with open(json_path, "r", encoding="utf-8") as f:
                examples_data = json.load(f)
    except Exception as e:
        load_data_error = True

def resource_path(relative_path):
    try:
        # PyInstaller временная папка при --onefile
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


def main(page: ft.Page):
    page.title = "Алгоритм Кронекера"
    page.window_icon = resource_path("icon.png")
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(
        scrollbar_theme=ft.ScrollbarTheme(thickness=0)
    )

    page.window.width = 700
    page.window.min_width = 600
    page.window.max_width = 1300
    page.window.height = 800
    page.window.min_height = 50
    page.window.max_height = 1200

    page.padding = 10

    page.current_selected_version = 5

    ##########################################################

    # функция для смены вкладок
    def change_tab(e):
        # Скрываем все вкладки
        algorithm_tab_content.visible = False
        examples_tab_content.visible = False
        versions_tab_content.visible = False

        # Снимаем выделение со всех вкладок
        for i in range(len(tabs.controls)-1):
            tabs.controls[i].bgcolor = ft.Colors.GREY_50
            tabs.controls[i].color = ft.Colors.BLACK

        # Показываем выбранную вкладку
        if e.control == tabs.controls[0]:  # Алгоритм
            algorithm_tab_content.visible = True
            e.control.bgcolor = ft.Colors.GREY_300
        elif e.control == tabs.controls[1]:  # База примеров
            examples_tab_content.visible = True
            e.control.bgcolor = ft.Colors.GREY_300
        elif e.control == tabs.controls[2]:  # Версии
            versions_tab_content.visible = True
            e.control.bgcolor = ft.Colors.GREY_300

        page.update()

    ##########################################################

    def on_input_change(e):
        input_text = polynomial_input.value

        if not input_text:
            return

        success, coefficients = parse_polynomial_input(input_text)

        if not success:
            important_text.height = 20
            important_text.value = "Error: недопустимый формат ввода"
            important_text.color = ft.Colors.RED

        elif len(coefficients) > 10:
            important_text.height = 20
            important_text.value = "Warning: введено более 10 чисел, алгоритм может выполняться долго"
            important_text.color = ft.Colors.ORANGE

        else:
            important_text.height = 0
            important_text.value = ""


        page.update()

    def active_copy_button(button):
        button.disabled = False
        button.bgcolor = ft.Colors.TRANSPARENT
        button.icon_color = ft.Colors.GREY_500
        page.update()

    def show_snack_bar(snack_bar):
        page.open(snack_bar)
        page.update()

    def copy_my_input_array(e):
        text_to_copy = f"{my_input_array.value}"
        page.set_clipboard(text_to_copy)
        show_snack_bar(copy_snack_bar)

    def copy_my_input(e):
        text_to_copy = f"{my_input.value}"
        page.set_clipboard(text_to_copy)
        show_snack_bar(copy_snack_bar)

    def copy_result_array(e):
        text_to_copy = f"{result_array.value}"
        page.set_clipboard(text_to_copy)
        show_snack_bar(copy_snack_bar)

    def copy_result(e):
        text_to_copy = f"{result.value}"
        page.set_clipboard(text_to_copy)
        show_snack_bar(copy_snack_bar)

    def copy_lagrange(e):
        text_to_copy = f"{lagrange.value}"
        page.set_clipboard(text_to_copy)
        show_snack_bar(copy_snack_bar)

    ##########################################################

    def parse_polynomial_input(text):
        # убираем квадратные/круглые скобки и пробелы
        text = text.strip()

        # проверяем на наличие скобок
        if text.startswith('[') and text.endswith(']'):
            text = text[1:-1].strip()
        elif text.startswith('(') and text.endswith(')'):
            text = text[1:-1].strip()

        # заменяем пробелы на запятые если нет запятых
        if ',' not in text and ' ' in text:
            text = text.replace(' ', ',')

        # разделяем по запятым
        parts = [part for part in text.split(',')]

        try:
            coefficients = [int(part) for part in parts]
            return True, coefficients
        except ValueError:
            return False, []

    def run_algorithm(e):
        input_text = polynomial_input.value
        my_input_array.value = ""
        my_input.value = ""
        result_array.value = ""
        result.value = ""
        lagrange.value = ""

        if not input_text:
            important_text.height = 20
            important_text.value = "Error: введите полином"
            important_text.color = ft.Colors.RED
            page.update()
            return

        success, coefficients = parse_polynomial_input(input_text)

        if success:
            algorithm_started = False
            try:
                # индикатор загрузки
                show_snack_bar(execution_snack_bar)
                loading_indicator.visible = True
                page.update()

                # по версиям
                factorization = {}
                if page.current_selected_version == 10:
                    if len(coefficients) > 6:
                        important_text.height = 40
                        important_text.value = f"Error: алгоритм был остановлен из высокой степени полинома,\nвозможно превышение использования памяти"
                        important_text.color = ft.Colors.RED
                        loading_indicator.visible = False
                        page.update()
                    else:
                        algorithm_started = True
                        factorization = kronecker_factorization_ver_1_0(coefficients)
                elif page.current_selected_version == 11:
                    if len(coefficients) > 6:
                        important_text.height = 40
                        important_text.value = f"Error: алгоритм был остановлен из высокой степени полинома,\nвозможно превышение использования памяти"
                        important_text.color = ft.Colors.RED
                        loading_indicator.visible = False
                        page.update()
                    else:
                        algorithm_started = True
                        factorization = kronecker_factorization_ver_1_1(coefficients)
                elif page.current_selected_version == 12:
                    if len(coefficients) > 6:
                        important_text.height = 40
                        important_text.value = f"Error: алгоритм был остановлен из высокой степени полинома,\nвозможно превышение использования памяти"
                        important_text.color = ft.Colors.RED
                        loading_indicator.visible = False
                        page.update()
                    else:
                        algorithm_started = True
                        factorization = kronecker_factorization_ver_1_2(coefficients)
                elif page.current_selected_version == 13:
                    if len(coefficients) > 6:
                        important_text.height = 40
                        important_text.value = f"Error: алгоритм был остановлен из высокой степени полинома,\nвозможно превышение использования памяти"
                        important_text.color = ft.Colors.RED
                        loading_indicator.visible = False
                        page.update()
                    else:
                        algorithm_started = True
                        factorization = kronecker_factorization_ver_1_3(coefficients)
                elif page.current_selected_version == 2:
                    if len(coefficients) > 6:
                        important_text.height = 40
                        important_text.value = f"Error: алгоритм был остановлен из высокой степени полинома,\nвозможно превышение использования памяти"
                        important_text.color = ft.Colors.RED
                        loading_indicator.visible = False
                        page.update()
                    else:
                        algorithm_started = True
                        factorization = kronecker_factorization_ver_2(coefficients)
                elif page.current_selected_version == 3:
                    if len(coefficients) > 6:
                        important_text.height = 40
                        important_text.value = f"Error: алгоритм был остановлен из высокой степени полинома,\nвозможно превышение использования памяти"
                        important_text.color = ft.Colors.RED
                        loading_indicator.visible = False
                        page.update()
                    else:
                        algorithm_started = True
                        factorization = kronecker_factorization_ver_3(coefficients)
                elif page.current_selected_version == 4:
                        algorithm_started = True
                        factorization = kronecker_factorization_ver_4(coefficients)
                elif page.current_selected_version == 5:
                        algorithm_started = True
                        factorization = kronecker_factorization_ver_5(coefficients)
                elif page.current_selected_version == 6:
                        algorithm_started = True
                        factorization = kronecker_factorization_ver_6(coefficients)

                if factorization is None and algorithm_started:
                    important_text.height = 20
                    important_text.value = "Error: алгоритм не вернул результат"
                    important_text.color = ft.Colors.RED
                    loading_indicator.visible = False
                    page.update()
                    return

                # скрываем индикатор загрузки
                loading_indicator.visible = False

                # my_input_array
                my_input_array.value = f"{factorization['original']}"
                active_copy_button(copy_my_input_array_button)

                # my_input
                polynomial_str = ''
                if page.current_selected_version == 10: polynomial_str = print_polynomial_ver_1_0(factorization['original'])
                if page.current_selected_version == 11: polynomial_str = print_polynomial_ver_1_1(factorization['original'])
                if page.current_selected_version == 12: polynomial_str = print_polynomial_ver_1_2(factorization['original'])
                if page.current_selected_version == 13: polynomial_str = print_polynomial_ver_1_3(factorization['original'])
                if page.current_selected_version == 2: polynomial_str = print_polynomial_ver_2(factorization['original'])
                if page.current_selected_version == 3: polynomial_str = print_polynomial_ver_3(factorization['original'])
                if page.current_selected_version == 4: polynomial_str = print_polynomial_ver_4(factorization['original'])
                if page.current_selected_version == 5: polynomial_str = print_polynomial_ver_5(factorization['original'])
                if page.current_selected_version == 6: polynomial_str = print_polynomial_ver_6(factorization['original'])
                my_input.value = f"{polynomial_str}"
                active_copy_button(copy_my_input_button)

                # result_array
                result_array.value = f"{factorization['factorization']}"
                active_copy_button(copy_result_array_button)

                # result
                if factorization['factorization']:
                    for factor in factorization['factorization']:
                        factor_str = ''
                        if page.current_selected_version == 10: factor_str = print_polynomial_ver_1_0(factor)
                        if page.current_selected_version == 11: factor_str = print_polynomial_ver_1_1(factor)
                        if page.current_selected_version == 12: factor_str = print_polynomial_ver_1_2(factor)
                        if page.current_selected_version == 13: factor_str = print_polynomial_ver_1_3(factor)
                        if page.current_selected_version == 2: factor_str = print_polynomial_ver_2(factor)
                        if page.current_selected_version == 3: factor_str = print_polynomial_ver_3(factor)
                        if page.current_selected_version == 4: factor_str = print_polynomial_ver_4(factor)
                        if page.current_selected_version == 5: factor_str = print_polynomial_ver_5(factor)
                        if page.current_selected_version == 6: factor_str = print_polynomial_ver_6(factor)

                        result.value += f"({factor_str})"
                active_copy_button(copy_result_button)

                # lagrange
                expected = 2 ** ((len(coefficients) - 1) // 2)
                lagrange.value += f"Ожидалось: {expected}\n"
                lagrange.value += f"Выполнено: {factorization['lagrange_count']}"
                active_copy_button(copy_lagrange_button)


            except Exception as ex:
                if algorithm_started:
                    important_text.height = 20
                    important_text.value = f"Error: невозможно выполнить алгоритм: {str(ex)}"
                    important_text.color = ft.Colors.RED
                    loading_indicator.visible = False

            page.update()

    ##########################################################

    def create_examples_table(examples_data):
        global header_text
        if not examples_data:
            return ft.Text(
                "Нет данных для отображения!",
                color=ft.Colors.RED,
                size=14
            )

        # стили
        border_style = ft.border.all(0.5, ft.Colors.GREY_400)

        # названия столбцов
        header_row = ft.Row([
            # Полином
            ft.Container(
                content=ft.Text("Полином", size=12, weight=ft.FontWeight.BOLD),
                padding=5,
                height=40,
                alignment=ft.alignment.center,
                bgcolor=ft.Colors.GREY_300,
                border=border_style,
                expand=True,
                width=page.window.max_width // 4
            ),
            # Факторизация
            ft.Container(
                content= ft.Text("Факторизация", size=12, weight=ft.FontWeight.BOLD),
                padding=5,
                height=40,
                alignment=ft.alignment.center,
                bgcolor=ft.Colors.GREY_300,
                border=border_style,
                expand=True,
                width=page.window.max_width // 4
            ),
            # Приводим?
            ft.Container(
                content= ft.Text("Приводим?", size=12, weight=ft.FontWeight.BOLD),
                padding=5,
                height=40,
                alignment=ft.alignment.center,
                bgcolor=ft.Colors.GREY_300,
                border=border_style,
                expand=True,
                width=page.window.max_width // 4
            ),
            # Формула Лагранжа
            ft.Container(
                content=ft.Text("Ожидание", size=12, weight=ft.FontWeight.BOLD),
                padding=5,
                height=40,
                alignment=ft.alignment.center,
                bgcolor=ft.Colors.GREY_300,
                border=border_style,
                expand=True,
                width=page.window.max_width // 4
            ),
        ], spacing=0, expand=True)

        # строки
        table_rows = []
        for i, example in enumerate(examples_data):

            def copy_cell_text(e, text_to_copy):
                page.set_clipboard(text_to_copy)
                show_snack_bar(copy_snack_bar)

            cells = []
            for j in range(4):
                text_to_copy = str(example[j])
                cells.append(
                    ft.Container(
                        content=ft.Text(str(example[j]), size=12),
                        padding=10,
                        height=40,
                        alignment=ft.alignment.center,
                        bgcolor=ft.Colors.GREY_50,
                        border=border_style,
                        expand=True,
                        width=page.window.max_width // 4,
                        on_click=lambda e, text=text_to_copy: copy_cell_text(e, text)
                    )
                )

            row = ft.Row([ *cells ], spacing=0, expand=True)

            table_rows.append(row)

        table = ft.Row(
            controls=[ft.Column(
                controls=[
                    header_row,
                    *table_rows
                ],
                spacing=0,
                expand=True,
                scroll=ft.ScrollMode.AUTO
            )],
            spacing=0,
            expand=True,
            scroll=ft.ScrollMode.AUTO
        )

        return ft.Container(
                content=ft.Stack(
                    controls=[table],
                    clip_behavior=ft.ClipBehavior.NONE
                ),
                expand=True
        )

    ##########################################################

    def on_version_container_click(e, version_index):
        page.current_selected_version = version_index

        for i in version_containers.keys():
            if i == version_index:
                version_containers[i].bgcolor = ft.Colors.GREEN_50
                version_containers[i].border = ft.border.all(2, ft.Colors.GREEN_500)
                version_checkboxes[i].value = True
                if i < 10: version_display.content.value = f"version {page.current_selected_version}.0"
                else: version_display.content.value = f"version 1.{page.current_selected_version-10}.0"

            else:
                if i < 10: version_containers[i].bgcolor = ft.Colors.GREY_50
                else: version_containers[i].bgcolor = ft.Colors.GREY_300
                version_containers[i].border = ft.border.all(1, ft.Colors.GREY_400)
                version_checkboxes[i].value = False

        page.update()

    def on_checkbox_change(e, version_index):
        # если чекбокс отмечен, выбираем соответствующую версию
        if e.control.value:
            on_version_container_click(e, version_index)

    ##########################################################

    # создаем вкладки
    algorithm_tab = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.NUMBERS, size=16, color=ft.Colors.BLACK),
            ft.Text("Алгоритм", size=14),
        ], spacing=5),
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
        bgcolor=ft.Colors.GREY_300,  # Активная вкладка по умолчанию
        border_radius=ft.border_radius.only(top_left=8, top_right=8),
        border=ft.border.all(1, ft.Colors.GREY_400),
        on_click=change_tab
    )

    examples_tab = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.LIBRARY_BOOKS, size=16, color=ft.Colors.BLACK),
            ft.Text("База примеров", size=14),
        ], spacing=5),
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
        bgcolor=ft.Colors.GREY_50,
        border_radius=ft.border_radius.only(top_left=8, top_right=8),
        border=ft.border.all(1, ft.Colors.GREY_400),
        on_click=change_tab
    )

    versions_tab = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.HISTORY, size=16, color=ft.Colors.BLACK),
            ft.Text("Версии", size=14),
        ], spacing=5),
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
        bgcolor=ft.Colors.GREY_50,
        border_radius=ft.border_radius.only(top_left=8, top_right=8),
        border=ft.border.all(1, ft.Colors.GREY_400),
        on_click=change_tab
    )

    # контроль выбранной версии
    version_display = ft.Container(
        content=ft.Text(f"version {page.current_selected_version}.0", size=14, weight=ft.FontWeight.BOLD),
        alignment=ft.alignment.top_right,
        width=100
    )

    ##########################################################

    # контейнер для вкладок
    tabs = ft.Row(
        controls=[algorithm_tab, examples_tab, versions_tab, version_display],
        spacing=0
    )

    ##########################################################

    # создаем элементы интерфейса
    title = ft.Container(
        ft.Text(
            "Алгоритм Кронекера",
            size=22,
            weight=ft.FontWeight.BOLD
        ),
        padding=ft.Padding(0,15, 0,0)
    )

    examples_container = ft.Container(
        content=ft.Row(
            [ft.TextField(
                label=ft.Text("Пример ввода"),
                multiline=True,
                read_only=True,
                expand=True,
                border_width=1,
                border_color=ft.Colors.GREY_400,
                border_radius=8,
                bgcolor=ft.Colors.GREY_50,
                text_size=14,
                label_style=ft.TextStyle(
                    size=20,
                    color=ft.Colors.BLACK,
                    weight=ft.FontWeight.W_500
                ),
                min_lines=10,
                mouse_cursor=ft.MouseCursor.BASIC
            ),
            ft.TextField(
                label=ft.Text("Пример выполнения алгоритма"),
                multiline=True,
                read_only=True,
                expand=True,
                border_width=1,
                border_color=ft.Colors.GREY_400,
                border_radius=8,
                bgcolor=ft.Colors.GREY_50,
                text_size=14,
                label_style=ft.TextStyle(
                    size=20,
                    color=ft.Colors.BLACK,
                    weight=ft.FontWeight.W_500
                ),
                min_lines=10,
                mouse_cursor=ft.MouseCursor.BASIC
            ),
        ], expand=True, vertical_alignment=ft.CrossAxisAlignment.START),
        expand=True
    )

    examples_container.content.controls[0].value =  "[-3, -5, 0, 1, 1]   →\n" + \
                                                    "[-3 -5 0 1 1]       →\n" + \
                                                    "(-3, -5, 0, 1, 1)   →    x⁴ + x³ - 5x - 3\n" + \
                                                    "(-3 -5 0 1 1)       →\n" + \
                                                    "-3, -5, 0, 1, 1     →\n" + \
                                                    "-3 -5 0 1 1         →\n\n" + \
                                                    "Первое число - свободный член, \nпоследнее число - старший коэффициент!"
    examples_container.content.controls[1].value = "[-3, -5, 0, 1, 1]\n" + \
                                                   "      ↓\n" + \
                                                   "[-1, -1, 1] [3, 2, 1]\n" + \
                                                   "      ↓\n" + \
                                                   "(x² - 1 - 1)(x² + 2x + 3)"

    polynomial_input = ft.TextField(
        label=ft.Text("Введите исходный полином", size=14, color=ft.Colors.BLACK),
        text_size=14,
        on_change=on_input_change,
        border_color=ft.Colors.GREY_400,
        border_radius=8,
        border_width=1,
        bgcolor=ft.Colors.GREY_50
    )

    important_text = ft.Text(height=0, size=14)

    loading_indicator = ft.ProgressRing(width=40, height=40, stroke_width=3, color=ft.Colors.GREY_500, padding=10, visible=False)

    run_button = ft.Container(
        content=ft.Row([
            ft.ElevatedButton(
                "Запустить алгоритм",
                icon=ft.Icons.PLAY_ARROW,
                on_click=run_algorithm,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.GREY_500,
                    color=ft.Colors.WHITE,
                    shape=ft.RoundedRectangleBorder(radius=8),
                    padding=ft.Padding(10,20,15,20),
                    text_style=ft.TextStyle(size=14)
                )
            ),
            loading_indicator
        ])
    )

    copy_my_input_array_button = ft.IconButton(
        icon=ft.Icons.COPY,
        icon_color=ft.Colors.WHITE,
        icon_size=25,
        on_click=copy_my_input_array,
        tooltip="Копировать результаты",
        disabled=True,
        bgcolor=ft.Colors.GREY_500
    )

    copy_my_input_button = ft.IconButton(
        icon=ft.Icons.COPY,
        icon_color=ft.Colors.WHITE,
        icon_size=25,
        on_click=copy_my_input,
        tooltip="Копировать результаты",
        disabled=True,
        bgcolor=ft.Colors.GREY_500
    )

    copy_result_array_button = ft.IconButton(
        icon=ft.Icons.COPY,
        icon_color=ft.Colors.WHITE,
        icon_size=25,
        on_click=copy_result_array,
        tooltip="Копировать результаты",
        disabled=True,
        bgcolor=ft.Colors.GREY_500
    )

    copy_result_button = ft.IconButton(
        icon=ft.Icons.COPY,
        icon_color=ft.Colors.WHITE,
        icon_size=25,
        on_click=copy_result,
        tooltip="Копировать результаты",
        disabled=True,
        bgcolor=ft.Colors.GREY_500
    )

    copy_lagrange_button = ft.IconButton(
        icon=ft.Icons.COPY,
        icon_color=ft.Colors.WHITE,
        icon_size=25,
        on_click=copy_lagrange,
        tooltip="Копировать результаты",
        disabled=True,
        bgcolor=ft.Colors.GREY_500
    )

    output_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    [ft.TextField(
                        label=ft.Text("Введенный полином в виде массива"),
                        multiline=True,
                        read_only=True,
                        expand=True,
                        border_width=1,
                        border_color=ft.Colors.GREY_400,
                        border_radius=8,
                        bgcolor=ft.Colors.GREY_50,
                        text_size=14,
                        label_style=ft.TextStyle(
                            size=20,
                            color=ft.Colors.BLACK,
                            weight=ft.FontWeight.W_500
                        ),
                        min_lines=3,
                        mouse_cursor=ft.MouseCursor.BASIC
                    ),
                    copy_my_input_array_button],
                    expand=True, vertical_alignment=ft.CrossAxisAlignment.START),
                ft.Row(
                    [ft.TextField(
                        label=ft.Text("Введенный полином"),
                        multiline=True,
                        read_only=True,
                        expand=True,
                        border_width=1,
                        border_color=ft.Colors.GREY_400,
                        border_radius=8,
                        bgcolor=ft.Colors.GREY_50,
                        text_size=14,
                        label_style=ft.TextStyle(
                            size=20,
                            color=ft.Colors.BLACK,
                            weight=ft.FontWeight.W_500
                        ),
                        min_lines=3,
                        mouse_cursor=ft.MouseCursor.BASIC
                    ),
                    copy_my_input_button], expand=True, vertical_alignment=ft.CrossAxisAlignment.START),
                ft.Row(
                    [ft.TextField(
                        label=ft.Text("Разложение полинома в виде массива"),
                        multiline=True,
                        read_only=True,
                        expand=True,
                        border_width=1,
                        border_color=ft.Colors.GREY_400,
                        border_radius=8,
                        bgcolor=ft.Colors.GREY_50,
                        text_size=14,
                        label_style=ft.TextStyle(
                            size=20,
                            color=ft.Colors.BLACK,
                            weight=ft.FontWeight.W_500
                        ),
                        min_lines=3,
                        mouse_cursor=ft.MouseCursor.BASIC
                    ),
                    copy_result_array_button], expand=True, vertical_alignment=ft.CrossAxisAlignment.START),
                ft.Row(
                    [ft.TextField(
                        label=ft.Text("Разложение полинома"),
                        multiline=True,
                        read_only=True,
                        expand=True,
                        border_width=1,
                        border_color=ft.Colors.GREY_400,
                        border_radius=8,
                        bgcolor=ft.Colors.GREY_50,
                        text_size=14,
                        label_style=ft.TextStyle(
                            size=20,
                            color=ft.Colors.BLACK,
                            weight=ft.FontWeight.W_500
                        ),
                        min_lines=3,
                        mouse_cursor=ft.MouseCursor.BASIC
                    ),
                    copy_result_button], expand=True, vertical_alignment=ft.CrossAxisAlignment.START),
                ft.Row(
                    [ft.TextField(
                        label=ft.Text("Использование формулы Лагранжа"),
                        multiline=True,
                        read_only=True,
                        expand=True,
                        border_width=1,
                        border_color=ft.Colors.GREY_400,
                        border_radius=8,
                        bgcolor=ft.Colors.GREY_50,
                        text_size=14,
                        label_style=ft.TextStyle(
                            size=20,
                            color=ft.Colors.BLACK,
                            weight=ft.FontWeight.W_500
                        ),
                        min_lines=3,
                        mouse_cursor=ft.MouseCursor.BASIC
                    ),
                    copy_lagrange_button], expand=True, vertical_alignment=ft.CrossAxisAlignment.START),
            ]
        ),
        padding=ft.Padding(0,0,0,10)
    )

    # сохраняем ссылки на поля вывода для обновления
    my_input_array = output_container.content.controls[0].controls[0]
    my_input = output_container.content.controls[1].controls[0]
    result_array = output_container.content.controls[2].controls[0]
    result = output_container.content.controls[3].controls[0]
    lagrange = output_container.content.controls[4].controls[0]

    copy_snack_bar = ft.SnackBar(content=ft.Text("Скопировано!"), bgcolor=ft.Colors.GREY_800, duration=500)
    execution_snack_bar = ft.SnackBar(
        content=ft.Text("Алгоритм выполняется..."),
        bgcolor=ft.Colors.GREY_800,
        duration=1000
    )

    # контент для вкладки "Алгоритм"
    algorithm_tab_content = ft.Container(
        content=ft.Column(
        [ title,
            ft.Divider(height=20),
            examples_container,
            polynomial_input,
            important_text,
            run_button,
            ft.Divider(height=20),
            output_container
        ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=10
        ),
        visible=True,
        padding=ft.Padding(10, 0, 10, 0),
        expand=True
    )

    ##########################################################

    # контент для вкладки "База примеров"
    examples_tab_content = ft.Container(
        content=create_examples_table(examples_data),
        visible=False,
        expand=True
    )


    ##########################################################

    versions_data = [
        {
            "number": "1.0",
            "description": "- базовая реализация алгоритма Кронекера\n- без оптимизаций\n- для полиномов низкой степени"
        },
        {
            "number": "2.0",
            "description": "- проверка точек: точка пропускается алгоритмом, если значение полинома в ней имеет свыше 200 делителей\n- на этапе подбора подходящих точек отбрасываются найденные множители вида (x - a)\n- проверка комбинаций перед использованием формулы Лагранжа: текущая комбинация и она же со значениями полинома *(-1) в дальнейшем будут пропускаться"
        },
        {
            "number": "3.0",
            "description": "- 2 проверки перед использованием формулы Лагранжа\n- проверка №1 на старший коэффициент интерполяционного многочлена\n- проверка №2 на свободный член интерполяционного члена"
        },
        {
            "number": "4.0",
            "description": "- изменение порядка генерации комбинаций\n- вычисление множителя НОД перед началом алгоритма"
        },
        {
            "number": "5.0",
            "description": "- признак Эйзенштейна"
        },
        {
            "number": "6.0",
            "description": "- эксперимент: реализация без рекурсии"
        }
    ]

    mini_versions_data = [
        {
            "number": "1.0.0",
            "description": "- значения точек по порядку: 0,1,2,3 ...\n- без сортировки делителей"
        },
        {
            "number": "1.1.0",
            "description": "- значения точек по порядку: 0,1,2,3 ...\n- с сортировкой делителей"
        },
        {
            "number": "1.2.0",
            "description": "- значения точек по порядку: 0,1,-1,2,-2 ...\n- без сортировки делителей"
        },
        {
            "number": "1.3.0",
            "description": "- значения точек по порядку: 0,1,-1,2,-2 ...\n- с сортировкой делителей"
        },
    ]

    version_containers = {}
    version_checkboxes = {}

    versions_column = ft.Column(
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

    for i, version in enumerate(versions_data):
        # Для версии 1.0 (с мини-версиями):
        if i == 0:
            description_field = ft.TextField(
                # основное описание
                value=version["description"],
                multiline=True,
                read_only=True,
                expand=True,
                border_width=1,
                border_color=ft.Colors.GREY_400,
                border_radius=8,
                bgcolor=ft.Colors.GREY_50,
                text_size=14,
                label_style=ft.TextStyle(
                    size=20,
                    color=ft.Colors.BLACK,
                    weight=ft.FontWeight.W_500
                ),
                min_lines=2,
                max_lines=16,
                mouse_cursor=ft.MouseCursor.CLICK
            )

            mini_version_containers = []
            for j, mini_version in enumerate(mini_versions_data):
                mini_description_data = ft.TextField(
                    value=mini_version["description"],
                    multiline=True,
                    read_only=True,
                    expand=True,
                    border_width=1,
                    border_color=ft.Colors.GREY_400,
                    border_radius=8,
                    bgcolor=ft.Colors.GREY_50,
                    text_size=14,
                    label_style=ft.TextStyle(
                        size=20,
                        color=ft.Colors.BLACK,
                        weight=ft.FontWeight.W_500
                    ),
                    min_lines=2,
                    max_lines=16,
                    mouse_cursor=ft.MouseCursor.CLICK
                )
                mini_checkbox = ft.Checkbox(
                    value=(i*10+j == page.current_selected_version),
                    on_change=lambda e, idx=10+j: on_checkbox_change(e, idx),
                    shape=ft.RoundedRectangleBorder(radius=3),
                    active_color=ft.Colors.GREEN_500
                )
                version_checkboxes[10+j] = mini_checkbox

                # контейнер для мини-версии
                mini_version_container = ft.Container(
                    content=ft.Row([
                        ft.Column([
                            ft.Text(f"Версия {mini_version['number']}",
                                    size=14,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLACK),
                            mini_description_data
                        ], expand=True, spacing=5),
                        mini_checkbox
                    ], expand=True, vertical_alignment=ft.CrossAxisAlignment.START),
                    padding=15,
                    border_radius=10,
                    border=ft.border.all(1, ft.Colors.GREY_400),
                    bgcolor=ft.Colors.GREEN_50 if (10 * i + j) == page.current_selected_version else ft.Colors.GREY_300,
                    on_click=lambda e, idx=10+j: on_version_container_click(e, idx)
                )
                mini_version_containers.append(mini_version_container)
                version_containers[10+j] = mini_version_container

            # контейнер для версии
            version_container = ft.Container(
                content=ft.Row([
                    ft.Column([
                        ft.Text(f"Версия {version['number']}",
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLACK),
                        description_field,
                        *mini_version_containers
                    ], expand=True, spacing=5)
                ], expand=True, vertical_alignment=ft.CrossAxisAlignment.START),
                padding=15,
                border_radius=10,
                border=ft.border.all(1, ft.Colors.GREY_400),
                bgcolor=ft.Colors.GREY_50
            )
            versions_column.controls.append(version_container)

        else:
            description_field = ft.TextField(
                value=version["description"],
                multiline=True,
                read_only=True,
                expand=True,
                border_width=1,
                border_color=ft.Colors.GREY_400,
                border_radius=8,
                bgcolor=ft.Colors.GREY_50,
                text_size=14,
                label_style=ft.TextStyle(
                    size=20,
                    color=ft.Colors.BLACK,
                    weight=ft.FontWeight.W_500
                ),
                min_lines=2,
                max_lines=16,
                mouse_cursor=ft.MouseCursor.CLICK
            )

            # чекбокс
            checkbox = ft.Checkbox(
                value=(i+1 == page.current_selected_version),
                on_change=lambda e, idx=i+1: on_checkbox_change(e, idx),
                shape=ft.RoundedRectangleBorder(radius=3),
                active_color=ft.Colors.GREEN_500
            )
            version_checkboxes[i+1] = checkbox

            # контейнер для версии
            version_container = ft.Container(
                content=ft.Row([
                    ft.Column([
                        ft.Text(f"Версия {version['number']}",
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLACK),
                        description_field
                    ], expand=True, spacing=5),
                    checkbox
                ], expand=True, vertical_alignment=ft.CrossAxisAlignment.START),
                padding=15,
                border_radius=10,
                border=ft.border.all(2 if i+1 == page.current_selected_version else 1, ft.Colors.GREEN_500 if i+1 == page.current_selected_version else ft.Colors.GREY_400),
                bgcolor=ft.Colors.GREEN_50 if i+1 == page.current_selected_version else ft.Colors.GREY_50,
                on_click=lambda e, idx=i+1: on_version_container_click(e, idx)
            )

            version_containers[i+1] = version_container
            versions_column.controls.append(version_container)

    # заголовок
    versions_title = ft.Container(
        ft.Text("Выбор версии алгоритма",
                size=22,
                weight=ft.FontWeight.BOLD),
        padding=ft.Padding(0,15,0,0)
    )

    # контент для вкладки "Версии"
    versions_tab_content = ft.Container(
        content=ft.Column(
            [
                versions_title,
                ft.Divider(20),
                ft.Text("По умолчанию выбрана версия 5.0, она считается самой стабильной!", size=14),
                ft.Divider(20),
                versions_column
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO),
        visible=False,
        padding=ft.Padding(10,0,10,0),
        expand=True
    )

    ##########################################################

    # главный контейнер с вкладками и контентом
    main_container = ft.Column([
        ft.Column([tabs]),  # вкладки сверху и номер текущей версии
        ft.Container(
            content=ft.Stack([
                algorithm_tab_content,
                examples_tab_content,
                versions_tab_content,
            ]),
            expand=True,
            width=page.width,
            height=page.height,
            border_radius=ft.border_radius.only(bottom_left=8, bottom_right=8, top_right=8),
            border=ft.border.all(1, ft.Colors.GREY_400)
        ),
    ], expand=True, spacing=0)

    page.add(main_container)


if __name__ == "__main__":
    load_examples("examples.json")
    ft.app(
        target=main,
        assets_dir="."
    )