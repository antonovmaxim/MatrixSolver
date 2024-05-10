from manim import *
from fractions import Fraction

class GaussianEliminationScene(Scene):
    def construct(self):
        # Исходная система уравнений в matrix
        global matrix, solution
        # Преобразуем все элементы в обыкновенные дроби
        matrix = [[Fraction(i) for i in row] for row in matrix]

        # Функция для создания матричного объекта
        def create_matrix_mob(matrix):
            return Matrix(
                [[(x) for x in row] for row in matrix],
                left_bracket="[",
                right_bracket="]"
            ).scale(0.8).to_edge(UP)

        # Создаем начальное отображение матрицы
        matrix_mob = create_matrix_mob(matrix)
        self.add(matrix_mob)

        # Функция для вывода текста о текущей операции
        def show_operation(text):
            operation_text = Text(text, font_size=24).center()
            self.play(Write(operation_text))
            self.wait(1)
            # self.play(Uncreate(operation_text))
            return operation_text

        # Прямой ход
        for i in range(len(matrix)):
            max_row = i + np.argmax([abs(matrix[k][i]) for k in range(i, len(matrix))])
            if i != max_row:
                op = show_operation(f"Меняем местами {i+1} и {max_row+1} строки")
                matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
                matrix_mob_new = create_matrix_mob(matrix)
                self.play(Transform(matrix_mob, matrix_mob_new))
                self.wait(1)
                self.play(Uncreate(op), run_time=.4)

            if matrix[i][i] != 0:
                op = show_operation(f"Домножаем {i+1} строку на {(1 / matrix[i][i])}")
                factor = matrix[i][i]
                matrix[i] = [x / factor for x in matrix[i]]
                matrix_mob_new = create_matrix_mob(matrix)
                self.play(Transform(matrix_mob, matrix_mob_new))
                self.wait(1)
                self.play(Uncreate(op), run_time=.4)

            for j in range(i + 1, len(matrix)):
                if matrix[j][i] != 0:
                    op = show_operation(f"Вычитаем из {j+1} строки {i+1} строку, умноженную на {(matrix[j][i] / matrix[i][i])}")
                    factor = matrix[j][i] / matrix[i][i]
                    matrix[j] = [xj - factor * xi for xi, xj in zip(matrix[i], matrix[j])]
                    matrix_mob_new = create_matrix_mob(matrix)
                    self.play(Transform(matrix_mob, matrix_mob_new))
                    self.wait(1)
                    self.play(Uncreate(op), run_time=.4)

        # Обратный ход
        num_vars = len(matrix[0]) - 1
        solution = [None] * num_vars
        free_vars = []

        for i in range(len(matrix) - 1, -1, -1):
            if all(matrix[i][j] == 0 for j in range(num_vars)) and matrix[i][-1] != 0:
                show_operation("Система несовместна")
                self.play(Write(Text("Нет решений", color=RED).scale(0.8).next_to(matrix_mob, DOWN)))
                self.wait(3)
                solution = [["Система несовместна; Нет решений"]]
                return
            if all(matrix[i][j] == 0 for j in range(num_vars)) and matrix[i][-1] == 0:
                continue

            for j in range(i - 1, -1, -1):
                if matrix[j][i] != 0:
                    op = show_operation(f"Вычитаем из {j+1} строки {i+1} строку, умноженную на {(matrix[j][i] / matrix[i][i])}")
                    factor = matrix[j][i] / matrix[i][i]
                    matrix[j] = [xj - factor * xi for xi, xj in zip(matrix[i], matrix[j])]
                    matrix_mob_new = create_matrix_mob(matrix)
                    self.play(Transform(matrix_mob, matrix_mob_new), run_time=1)
                    self.wait(1)
                    self.play(Uncreate(op), run_time = 0.4)

            main_var = None
            for j in range(num_vars):
                if matrix[i][j] != 0:
                    main_var = j
                    break

            if main_var is None:
                continue

            expr = Fraction(matrix[i][-1])
            expr_parts = []

            for j in range(main_var + 1, num_vars):
                if matrix[i][j] != 0:
                    if solution[j] is None:
                        solution[j] = f"x_{j + 1}"
                        free_vars.append(j)
                    if isinstance(solution[j], str):
                        expr_parts.append(f" - ({(matrix[i][j])})*{solution[j]}")
                    else:
                        expr -= matrix[i][j] * solution[j]

            if expr_parts:
                solution[main_var] = f"{(expr)}" + "".join(expr_parts)
            else:
                solution[main_var] = expr / matrix[i][main_var]

        # Выражаем неопределенные переменные
        for i in range(num_vars):
            if solution[i] is None:
                solution[i] = f"x_{i + 1}"

        # Отображаем окончательный результат
        result_text = Text("Решение системы:").to_edge(DOWN)
        self.play(Write(result_text))

        solution = [[(f"x_{i + 1} = {(sol)}" if (sol)!=f"x_{i + 1}" else f"x_{i + 1} \in \mathbb{{R}}").replace("*", " \cdot ") for i, sol in enumerate(solution)]]

        # Выводим решение
        solution_mob = MathTable(
            solution,
            element_to_mobject=lambda m: MathTex(m).set_color(WHITE)
        ).scale(0.8).next_to(result_text, UP)
        self.play(Write(solution_mob))
        self.wait(3)

print("Сколько переменных в данной системе?\n>>> ", end='')
k = int(input())
print("Введите матрицу (разделитель столбцов - пробел, строк - \\n):")
matrix = [[int(i) for i in input(">>> ").split()] for j in range(k)]
print(matrix)
scene = GaussianEliminationScene()
scene.render(True)

print(f"Answer: ${' | '.join((solution)[0])}$")