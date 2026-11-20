from manim import (
    Text, Scene,
    Rectangle, VGroup, LEFT,
    DOWN, RIGHT, UP,
    Write, FadeIn,
    CurvedArrow, BOLD, Transform,
    Indicate, Flash,
    FadeOut, Create,
    RED, RED_A, RED_B, GREEN, GREEN_A, GREEN_B, GREEN_D,
    ORANGE, YELLOW, YELLOW_B, GREY_B, GREY_C, LIGHT_GRAY, BLUE_D, WHITE,
    Code
)
from manim import config


class BufferOverflowScene(Scene):

    def construct(self):
        # Настройка темного фона
        self.camera.background_color = "#1e1e2e"  # type: ignore

        # Шрифты
        UI_FONT = "Segoe UI"
        CODE_FONT = "Cascadia Mono"

        # ============================================================
        # ЧАСТЬ 1: ШТАТНАЯ РАБОТА С БУФЕРОМ
        # ============================================================

        # 1. Заголовок части 1
        title_part1 = Text(
            "Штатная работа с буфером",
            font=UI_FONT,
            font_size=28,
            color=GREEN_B,
        )
        title_part1.to_edge(UP, buff=0.25)
        self.play(Write(title_part1))

        # 2. Блок с исходным кодом на C (ТОЛЬКО vulnerable, без malware_shell)
        c_code_text_normal = (
            "void vulnerable(char *input) {\n"
            "    char buf[8];\n"
            "    strcpy(buf, input);\n"
            "    return;\n"
            "}"
        )

        code_bg = Rectangle(
            width=4.8, height=2.2, color=GREY_B, fill_color="#11111b", fill_opacity=1
        )
        code_mob = Code(
            code_string=c_code_text_normal,
            language="c",
            formatter_style="one-dark",
            background="rectangle",
            background_config={"fill_opacity": 0, "stroke_opacity": 0},
            paragraph_config={"font": CODE_FONT, "font_size": 14, "line_spacing": 1.2, "disable_ligatures": True},
        )
        code_mob.move_to(code_bg.get_center())

        code_group = VGroup(code_bg, code_mob)
        code_group.to_edge(LEFT, buff=1.8).shift(DOWN * 0.3)

        # Метка секции .text над блоком кода
        text_section = Text(
            ".text",
            font=CODE_FONT,
            font_size=14,
            color=GREY_B,
            weight=BOLD,
        )
        text_section.next_to(code_bg, UP, buff=0.2).align_to(code_bg, LEFT)

        # Легитимный адрес возврата ПОД блоком кода (зеленый)
        legit_ret_addr = Text(
            "0x401152  ← возврат в main()",
            font=CODE_FONT,
            font_size=12,
            color=GREEN_B,
        )
        legit_ret_addr.next_to(code_bg, DOWN, buff=0.2).align_to(code_bg, LEFT)

        # Адрес функции vulnerable слева от блока кода
        code_addr_vuln = Text("0x401150", font=CODE_FONT, font_size=12, color=BLUE_D)

        code_lines = code_mob.code_lines
        vuln_line = code_lines[0]  # void vulnerable...

        left_x = (code_bg.get_left() + LEFT * 0.6)[0]
        vuln_y = vuln_line.get_center()[1]
        code_addr_vuln.move_to((left_x, vuln_y, 0))

        self.play(
            FadeIn(code_group),
            FadeIn(code_addr_vuln),
            Write(text_section),
            Write(legit_ret_addr),
        )
        self.wait(1)

        # 3. Визуализация стека
        stack_title = Text(
            "Стек (растет вниз ↓)", font=UI_FONT, font_size=18, color=YELLOW_B
        )
        stack_title.move_to(RIGHT * 3.2 + UP * 2.2)

        cells_data = [
            {
                "label": "buf[0..3] (4б)",
                "val": "00 00 00 00",
                "color": GREEN_D,
                "addr": "0x7ff...e010",
            },
            {
                "label": "buf[4..7] (4б)",
                "val": "00 00 00 00",
                "color": GREEN_D,
                "addr": "0x7ff...e014",
            },
            {
                "label": "Saved RBP (8б)",
                "val": "0x7ff...e040",
                "color": GREY_C,
                "addr": "0x7ff...e018",
            },
            {
                "label": "Return Address",
                "val": "0x401152 (main)",
                "color": BLUE_D,
                "addr": "0x7ff...e020",
            },
        ]

        stack_group = VGroup()
        cell_boxes = []
        cell_texts = []

        for item in cells_data:
            rect = Rectangle(
                width=3.6,
                height=0.75,
                color=item["color"],
                fill_opacity=0.2,
                stroke_width=2,
            )
            val = Text(item["val"], font=CODE_FONT, font_size=14, color=WHITE)

            cell_vgroup = VGroup(rect, val)
            cell_boxes.append(rect)
            cell_texts.append(val)
            stack_group.add(cell_vgroup)

        stack_group.arrange(UP, buff=0.08)
        stack_group.move_to(RIGHT * 3.2 + DOWN * 0.4)

        # Подписи адресов (слева) и названий ячеек (справа)
        annotations = VGroup()
        for i, item in enumerate(cells_data):
            rect = cell_boxes[i]
            addr = Text(item["addr"], font=CODE_FONT, font_size=11, color=GREY_B)
            addr.next_to(rect, LEFT, buff=0.2)

            lbl = Text(item["label"], font=UI_FONT, font_size=12, color=item["color"])
            lbl.next_to(rect, RIGHT, buff=0.2)
            annotations.add(addr, lbl)

        self.play(
            Write(stack_title),
            Create(stack_group),
            FadeIn(annotations),
        )
        self.wait(1)

        # 4. Сценарий: Нормальный ввод "AAAA" (4 байта)
        status_text = Text(
            'Нормальный ввод input = "AAAA" (4 байта)',
            font=UI_FONT,
            font_size=16,
            color=GREEN_B,
        )
        status_text.to_edge(DOWN, buff=0.3)
        self.play(Write(status_text))

        new_val_0 = Text(
            "41 41 41 41 ('AAAA')", font=CODE_FONT, font_size=13, color=GREEN_A
        )
        new_val_0.move_to(cell_texts[0].get_center())

        self.play(
            Transform(cell_texts[0], new_val_0),
            cell_boxes[0].animate.set_fill(GREEN, opacity=0.4),
        )
        self.wait(1.5)

        # 5. Возврат: зеленая стрелка от return к Return Address в стеке
        return_line = code_mob.code_lines[3]  # return;

        # Немного смещаем точки начала/конца для красивого отступа
        start_pt = return_line.get_right() + RIGHT * 0.15
        end_pt = cell_boxes[3].get_left() + LEFT * 0.15

        arrow_return = CurvedArrow(
            start_point=start_pt,
            end_point=end_pt,
            color=GREEN,
            angle=-0.6,
            stroke_width=3,
            tip_length=0.2,
        )
        arrow_return_label = Text(
            "return → 0x401152 (main)", font=UI_FONT, font_size=12, color=GREEN_B
        )
        arrow_return_label.next_to(arrow_return, UP, buff=0.15)

        self.play(Create(arrow_return), Write(arrow_return_label))
        self.wait(2)

        # Подсветка правильного Return Address в стеке
        self.play(
            Indicate(cell_boxes[3], scale_factor=1.3, color=GREEN),
            Indicate(legit_ret_addr, scale_factor=1.3, color=GREEN),
        )
        self.wait(2)

        # Очистка части 1: убираем стрелку, лейбл, статус, сбрасываем стек
        reset_val_0 = Text(
            "00 00 00 00", font=CODE_FONT, font_size=14, color=WHITE
        ).move_to(cell_texts[0])

        self.play(
            FadeOut(arrow_return),
            FadeOut(arrow_return_label),
            FadeOut(status_text),
            Transform(cell_texts[0], reset_val_0),
            cell_boxes[0].animate.set_fill(GREEN_D, opacity=0.2),
        )
        self.wait(1)

        # ============================================================
        # ПОДГОТОВКА ЧАСТИ 2 (создаем объекты заранее)
        # ============================================================

        # Меняем заголовок
        title_part2 = Text(
            "Переполнение буфера в стеке",
            font=UI_FONT,
            font_size=28,
            color=RED_B,
        )
        title_part2.to_edge(UP, buff=0.25)

        # Расширяем фон кода для malware_shell
        new_code_bg = Rectangle(
            width=4.8, height=3, color=GREY_B, fill_color="#11111b", fill_opacity=1
        )
        new_code_bg.move_to(code_bg.get_center())

        # Новый код с malware_shell
        c_code_text_exploit = (
            "void vulnerable(char *input) {\n"
            "    char buf[8];\n"
            "    strcpy(buf, input);\n"
            "    return;\n"
            "}\n\n"
            "void malware_shell() {\n"
            "    // Вредоносный код\n"
            "}"
        )

        new_code_mob = Code(
            code_string=c_code_text_exploit,
            language="c",
            formatter_style="one-dark",
            background="rectangle",
            background_config={"fill_opacity": 0, "stroke_opacity": 0},
            paragraph_config={"font": CODE_FONT, "font_size": 14, "line_spacing": 1.2, "disable_ligatures": True},
        )
        new_code_mob.move_to(new_code_bg.get_center())

        # Адрес malware_shell слева
        code_addr_malware = Text("0x401196", font=CODE_FONT, font_size=12, color=RED_B)
        new_code_lines = new_code_mob.code_lines
        malware_line = new_code_lines[6]  # void malware_shell()...
        malware_y = malware_line.get_center()[1]
        code_addr_malware.move_to((left_x, malware_y, 0))

        # Легитимный адрес возврата под НОВЫМ блоком кода
        new_legit_ret_addr = Text(
            "0x401152  ← возврат в main()",
            font=CODE_FONT,
            font_size=12,
            color=GREEN_B,
        )
        new_legit_ret_addr.next_to(new_code_bg, DOWN, buff=0.2).align_to(new_code_bg, LEFT)

        # .text над НОВЫМ блоком кода
        new_text_section = Text(
            ".text",
            font=CODE_FONT,
            font_size=14,
            color=GREY_B,
            weight=BOLD,
        )
        new_text_section.next_to(new_code_bg, UP, buff=0.2).align_to(new_code_bg, LEFT)

        # ============================================================
        # ПЕРЕХОД: затемнение + мгновенная смена контента + осветление
        # ============================================================
        dim_rect = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            fill_color="#000000",
            fill_opacity=0.85,
            stroke_width=0,
        )
        self.play(FadeIn(dim_rect), run_time=0.6)

        # В темноте мгновенно меняем всё
        self.play(
            Transform(title_part1, title_part2),
            Transform(code_bg, new_code_bg),
            Transform(code_mob, new_code_mob),
            Transform(legit_ret_addr, new_legit_ret_addr),
            Transform(text_section, new_text_section),
            FadeIn(code_addr_malware),
            run_time=0.01,
        )

        self.play(FadeOut(dim_rect), run_time=0.6)
        self.wait(0.5)

        # 6. Сценарий 2: Переполнение буфера (Эксплойт)
        attack_text = Text(
            'Ввод 24 байт: "AAAAAAAAAAAAAAAA" + адрес malware_shell',
            font=UI_FONT,
            font_size=16,
            color=RED_B,
        )
        attack_text.to_edge(DOWN, buff=0.3)
        self.play(Write(attack_text))
        self.wait(0.5)

        # Заполнение buf[0..3]
        v0 = Text(
            "41 41 41 41 ('AAAA')", font=CODE_FONT, font_size=13, color=YELLOW
        ).move_to(cell_texts[0])
        self.play(
            Transform(cell_texts[0], v0),
            cell_boxes[0].animate.set_fill(YELLOW, opacity=0.35),
            run_time=0.5,
        )

        # Заполнение buf[4..7]
        v1 = Text(
            "41 41 41 41 ('AAAA')", font=CODE_FONT, font_size=13, color=YELLOW
        ).move_to(cell_texts[1])
        self.play(
            Transform(cell_texts[1], v1),
            cell_boxes[1].animate.set_fill(YELLOW, opacity=0.35),
            run_time=0.5,
        )

        # Перезапись Saved RBP
        v2 = Text(
            "41 41 41 41 41 41 41 41",
            font=CODE_FONT,
            font_size=11,
            color=ORANGE,
        ).move_to(cell_texts[2])
        self.play(
            Transform(cell_texts[2], v2),
            cell_boxes[2].animate.set_color(ORANGE).set_fill(ORANGE, opacity=0.45),
            Indicate(cell_boxes[2], color=ORANGE),
            run_time=0.7,
        )

        # Перезапись Return Address
        v3 = Text(
            "0x401196 (malware_shell)",
            font=CODE_FONT,
            font_size=11,
            color=RED_A,
        ).move_to(cell_texts[3])
        self.play(
            Transform(cell_texts[3], v3),
            cell_boxes[3].animate.set_color(RED).set_fill(RED, opacity=0.6),
            Flash(cell_boxes[3], color=RED, line_length=0.25),
            run_time=0.8,
        )
        self.wait(0.5)

        # 7. Стрелка 1: return в коде -> Return Address в стеке (оранжевая)
        return_line = new_code_mob.code_lines[3]  # return;

        # Смещаем точки для отступа
        start_pt1 = return_line.get_right() + RIGHT * 0.15
        end_pt1 = cell_boxes[3].get_left() + LEFT * 0.15

        arrow1 = CurvedArrow(
            start_point=start_pt1,
            end_point=end_pt1,
            color=ORANGE,
            angle=-0.6,
            stroke_width=3,
            tip_length=0.2,
        )
        arrow1_label = Text(
            "retn", font=UI_FONT, font_size=14, color=ORANGE, weight=BOLD
        )
        arrow1_label.next_to(arrow1, UP, buff=0.15)

        self.play(Create(arrow1), Write(arrow1_label))
        self.wait(0.5)

        # 8. Стрелка 2: Return Address в стеке -> malware_shell в коде (красная)
        malware_line = new_code_mob.code_lines[6]  # void malware_shell() {
        # Цель — название функции malware_shell, чуть правее центра строки
        target_point = malware_line.get_center() + RIGHT * 0.3

        # Начало чуть выше Return Address ячейки, конец чуть левее цели
        start_pt2 = cell_boxes[3].get_top() + UP * 0.1
        end_pt2 = target_point + LEFT * 0.15

        arrow2 = CurvedArrow(
            start_point=start_pt2,
            end_point=end_pt2,
            color=RED,
            angle=1.3,
            stroke_width=3,
            tip_length=0.2,
        )
        arrow2_label = Text(
            "ret → Прыжок в malware_shell()!",
            font=UI_FONT,
            font_size=14,
            color=RED_B,
            weight=BOLD,
        )
        arrow2_label.next_to(arrow2, UP, buff=0.15)

        self.play(
            Create(arrow2),
            Write(arrow2_label),
            Indicate(malware_line, scale_factor=1.2, color=RED),
            Indicate(code_addr_malware, scale_factor=1.3, color=RED),
        )
        self.wait(3)