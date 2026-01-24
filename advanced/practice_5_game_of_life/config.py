import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input', default="init.csv", help='Input CSV file')
parser.add_argument('--generations', type=int, default=10, help='Number of generations')
parser.add_argument('--debug', action='store_true', help='Enable debug mode')
parser.add_argument('--cell-size', type=int, default=100, help='Cell size for visualization')

args = parser.parse_args()

if not os.path.isfile(args.input):
    print(f"Внимание: файл '{args.input}' не найден. Использую 'init.csv'")
    INPUT_FILE = "init.csv"
else:
    INPUT_FILE = args.input

GENERATIONS = args.generations
DEBUG = args.debug
CELL_SIZE = args.cell_size
FONT_SIZE = max(10, CELL_SIZE // 4)

TEMP_OUTPUT_FILE_CSV = os.path.join(f"{os.getcwd()}", "unit test file", "temp_output_generation.csv")
OUTPUT_FILE_CSV = "generation.csv"
OUTPUT_FILE_PNG = "generation.png"
OUTPUT_FILE_GIF = "evolution.gif"
BORDER = 2
