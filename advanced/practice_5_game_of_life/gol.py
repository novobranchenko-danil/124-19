import os
import filecmp
import math
from PIL import Image, ImageDraw

INPUT_FILE = "init.csv"
OUTPUT_FILE_CSV = "generation.csv"
OUTPUT_TEST_FILE_CSV = os.path.join(f"{os.getcwd()}", "unit test file", "test_output_generation.csv")
OUTPUT_FILE_PNG = "generation.png"
OUTPUT_FILE_GIF = "generation.gif"
GENERATIONS = 10
BORDER = 2
CELL_SIZE = 100
FONT_SIZE = max(10, CELL_SIZE // 4)
DEBUG = False


def live_neighbors(grid, row, col):
    '''
    @requires:  grid which is a list of lists
        each list contains either 0 or 1 meaning the cell
        is alive (1) or dear (0). The size of all inner lists
        must be the same.
        [ [0, 1, 0],
          [0, 0, 0],
          [1, 1, 0] ]
        row and col are integers such that 0 <= row <= number of rows in grid
        and 0 <= col <= number of columns in grid

    @modifies:  None
    @effects:   None
    @raises:    None
    @returns:   the number of cells whose value is 1
    '''
    count = 0
    rows = len(grid)
    cols = len(grid[0])
    min_r = row - 1 if row >= 1 else 0
    max_r = row + 1 if row < rows - 1 else row
    min_c = col - 1 if col >= 1 else 0
    max_c = col + 1 if col < cols - 1 else col
    for idx_y in range(min_r, max_r + 1):
        for idx_x in range(min_c, max_c + 1):
            if idx_y == row and idx_x == col:
                continue
            if grid[idx_y][idx_x] != 0:
                count += 1
    return count


def model(grid):
    '''
    @requires:  grid which is a list of lists
        each list contains either 0 or 1 meaning the cell
        is alive (1) or dear (0). The size of all inner lists
        must be the same.
        [ [0, 1, 0],
          [0, 0, 0],
          [1, 1, 0] ]
    @modifies:  None
    @effects:   None
    @raises:    None
    @returns:   a new grid which follows the format of the
        input grid but with cell values that correspond to the new
        generation. The new generation is determined by applying
        the following rules:
            1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
            2. Any live cell with two or three live neighbours lives on to the next generation.
            3. Any live cell with more than three live neighbours dies, as if by overpopulation.
            4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
    '''
    try:
        rows, cols = len(grid), len(grid[0])
        new_grid = [[0 for _ in range(cols)] for _ in range(rows)]
        for row in range(rows):
            for col in range(cols):
                live_nb = live_neighbors(grid, row, col)
                # Rule 1
                if live_nb < 2 and grid[row][col] != 0:
                    new_grid[row][col] = 0
                # Rule 2
                elif 2 <= live_nb <= 3 and grid[row][col] != 0:
                    new_grid[row][col] = grid[row][col] + 1
                # Rule 3
                elif live_nb > 3 and grid[row][col] != 0:
                    new_grid[row][col] = 0
                # Rule 4
                elif grid[row][col] == 0 and live_nb == 3:
                    new_grid[row][col] = 1
                else:
                    new_grid[row][col] = 0
        return new_grid
    except IndexError:
        raise IndexError("Файл должен содержать как минимум две строки с числами rows и cols\n"
                         f"Подробности в {os.getcwd()}\README.md")


def read_input_init_v2(filename):
    '''
    Образец функции для init файлов по типу init_v2.csv
    '''
    grid = []
    with open(filename, "r") as input_file:
        lines = input_file.readlines()
        for line in lines:
            line = line.strip()
            line = line.split(";")
            line = [int(elem) for elem in line]
            grid.append(line)
    return grid


def read_input(filename=INPUT_FILE):
    '''
    :param filename:
    :return:
    '''
    with open(filename, "r") as input_file:
        lines = input_file.readlines()
        grid = []
        try:
            rows = int(lines[0].strip())
            cols = int(lines[1].strip())
            grid = [[0 for _ in range(cols)] for _ in range(rows)]
            # print(f"rows = {rows} cols = {cols}")
        except IndexError:
            raise IndexError("Файл должен содержать как минимум две строки с числами rows и cols\n"
                             f"Подробности в {os.getcwd()}\README.md")

        for line in lines[2:]:
            line = line.strip()
            line = line.split(",")
            line = [int(elem) for elem in line]
            line_y = line[0] - 1
            line_x = line[1] - 1
            grid[line_y][line_x] = 1
        print("init grid")
        print(*grid, sep="\n")
    return grid


def write_output(grid, gen, filename=OUTPUT_FILE_CSV):
    '''
    :param grid:
    :param gen:
    :param filename:
    :return:
    '''
    with open(filename, "a+") as output_file:
        output_file.write(f"Generation {gen}\n")
        rows, cols = len(grid), len(grid[0])
        output_file.write(f"{rows}\n")
        output_file.write(f"{cols}\n")
        for y, row in enumerate(grid, start=1):
            for x, col in enumerate(row, start=1):
                if col != 0:
                    output_file.write(f"{y},{x}\n")
    print(f"\noutput grid {gen} generation")
    print(*grid, sep="\n")


def write_png(grid, gen_count=0, filename=OUTPUT_FILE_PNG):
    '''
    :param grid:
    :param gen_count:
    :param filename:
    :param cell_age:
    :return:
    '''
    rows, cols = len(grid), len(grid[0])
    # print(f"rows = {rows} cols = {cols}")
    image_width = cols * (CELL_SIZE + BORDER) + BORDER
    image_height = rows * (CELL_SIZE + BORDER) + BORDER

    image = Image.new('RGB', (image_width, image_height), "white")
    draw = ImageDraw.Draw(image)

    for i in range(cols + 1):
        x = i * (CELL_SIZE + BORDER)
        draw.line([(x, 0), (x, image_height)],
                  fill="black", width=BORDER)

    for j in range(rows + 1):
        y = j * (CELL_SIZE + BORDER)
        draw.line([(0, y), (image_width, y)],
                  fill="black", width=BORDER)

    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if col != 0:
                top = BORDER + y * (CELL_SIZE + BORDER)
                left = BORDER + x * (CELL_SIZE + BORDER)
                right = left + CELL_SIZE - 1
                bottom = top + CELL_SIZE - 1

                r, g, b = gradient_color(col)
                draw.rectangle([left, top, right, bottom], fill=(r, g, b))

    draw.text((FONT_SIZE // 2, FONT_SIZE // 2), f"Gen {gen_count}", fill="black",
              font_size=FONT_SIZE, stroke_width=1, stroke_fill="gray")

    image.save(f"{gen_count:03d}_{filename}")
    return image


def gradient_color(age, max_age=GENERATIONS):
    start_color = (208, 240, 192)
    end_color = (0, 69, 36)

    t = min(1.0, (age - 1) / (max_age - 1)) if max_age > 1 else 0
    t = 1 - math.exp(-3 * t)

    r = int(start_color[0] * (1 - t) + end_color[0] * t)
    g = int(start_color[1] * (1 - t) + end_color[1] * t)
    b = int(start_color[2] * (1 - t) + end_color[2] * t)
    return r, g, b


def write_gif(frames, filename=OUTPUT_FILE_GIF, duration=500, loop=0):
    if not frames:
        return

    frames[0].save(
        filename,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=loop,
        optimize=True)


def remove_output_file_csv(filename):
    if os.path.exists(filename):
        os.remove(filename)
        print(f"Удалили старый csv файл генерации: {filename}")


def remove_output_file_png(filename):
    for generation in range(GENERATIONS):
        if os.path.exists(f"{generation:03d}_init_grid.png"):
            os.remove(f"{generation:03d}_init_grid.png")
        if os.path.exists(f"{generation+1:03d}_{OUTPUT_FILE_PNG}"):
            os.remove(f"{generation+1:03d}_{OUTPUT_FILE_PNG}")
        if os.path.exists(OUTPUT_FILE_GIF):
            os.remove(OUTPUT_FILE_GIF)
    print(f"Удалили старые png и gif файлы генераций: {filename}")
# TODO чистить все файлы с расширением png и gif посмотреть как


if DEBUG:
    grid = [[0, 1, 0],
            [0, 0, 0],
            [1, 1, 0]]
    expected = [[0, 0, 0],
                [1, 1, 0],
                [0, 0, 0]]
    actual = model(grid)
    if actual != expected:
        print("Test model failed!")

    expected = 3
    actual = live_neighbors(grid, 1, 0)
    if actual != expected:
        print("Test 1 live_neighbors failed!")

    expected = 1
    actual = live_neighbors(grid, 2, 2)
    if actual != expected:
        print("Test 2 live_neighbors failed!")

    expected = 0
    actual = live_neighbors(grid, 0, 1)
    if actual != expected:
        print("Test 3 live_neighbors failed!")

    expected = [[0, 1, 0],
                [1, 1, 1],
                [0, 1, 0]]
    actual = read_input(os.path.join(f"{os.getcwd()}", "unit test file", "test_input.csv"))
    if actual != expected:
        print("Test read_input failed!")

    grid = [[0, 1, 0],
            [0, 0, 0],
            [1, 1, 0]]
    gen = 1
    remove_output_file_csv(OUTPUT_TEST_FILE_CSV)
    write_output(grid, gen, OUTPUT_TEST_FILE_CSV)
    expected = os.path.join(f"{os.getcwd()}", "unit test file", "test_output_expected.csv")
    actual = OUTPUT_TEST_FILE_CSV
    if not filecmp.cmp(expected, actual, shallow=False):
        print("Test write_output failed!")

    # придумать тесты для функций write png и write gif
else:
    remove_output_file_csv(OUTPUT_FILE_CSV)
    remove_output_file_png(OUTPUT_FILE_PNG)
    try:
        frames = []
        grid = read_input()
        frame = write_png(grid, filename="init_grid.png")
        frames.append(frame)
        for generation in range(GENERATIONS):
            grid = model(grid)
            write_output(grid, generation + 1)
            frame = write_png(grid, generation + 1)
            frames.append(frame)
        write_gif(frames)
    except IndexError as ex:
        print(ex)
