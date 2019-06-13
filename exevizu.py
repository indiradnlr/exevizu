import turtle as tu
import sys
import lief
import Tkinter as tk
import argparse
import sys
import re
import os

directions = [90, 67.5, 45, 22.5, 0, 337.5, 315, 292.5,
              270, 247.5, 225, 202.5, 180, 157.5, 135, 112.5]


def check_arguments(args):
    if check_hex(args.start_color):
        start_color = hex_to_rgb(args.start_color)
    elif check_rgb(args.start_color):
        start_color = eval(args.start_color)
    else:
        sys.exit("\033[1;91mInvalid start color : %s \033[00m" %
                 args.start_color)

    if check_hex(args.end_color):
        end_color = hex_to_rgb(args.end_color)
    elif check_rgb(args.end_color):
        end_color = eval(args.end_color)
    else:
        sys.exit("\033[1;91mInvalid end color : %s \033[00m" % args.end_color)

    if not check_omit(args.omit):
        sys.exit(
            "\033[1;91mInvalid list of values to ommit : %s \033[00m" % str(args.omit))

    try:
        binary = lief.parse(args.file)
        list_long = binary.get_section(".text").content
    except:
        sys.exit("\033[1;91mInvalid ELF/PE file : %s \033[00m" %
                 str(args.file))

    return binary, list_long, start_color, end_color


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def check_hex(value):
    return re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', value)


def check_rgb(value):
    try:
        tuple = eval(value)
        if len(tuple) != 3:
            return False
        if not (0 <= tuple[0] <= 255) or not (0 <= tuple[1] <= 255) or not (0 <= tuple[2] <= 255):
            return False
        return True
    except:
        return False


def check_omit(value):
    try:
        integers = [int(i, 0) for i in value]
        for i in integers:
            if not (0 <= i <= 16):
                return False
        return True
    except:
        return False


def color_range(color1, color2, steps):
    output = []
    r1, g1, b1 = tuple(float(ti)/255 for ti in color1)
    r2, g2, b2 = tuple(float(ti)/255 for ti in color2)
    rdelta, gdelta, bdelta = float(
        r2-r1)/steps, float(g2-g1)/steps, float(b2-b1)/steps
    for step in range(steps):
        r1 += rdelta
        g1 += gdelta
        b1 += bdelta
        output.append((r1, g1, b1))
    return output


def draw(args, list_long, start_color, end_color):

    def zoom(event):
        amount = 0.9 if event.delta < 0 else 1.1
        canvas.scale(tk.ALL, 0, 0, amount, amount)

    def scroll_start(event):
        canvas.scan_mark(event.x, event.y)

    def scroll_move(event):
        canvas.scan_dragto(event.x, event.y, gain=1)

    to_ommit = []

    for val in args.omit:
        val = bin(int(val, 16))
        to_ommit.append(val[2:].zfill(4))

    list_bin = []

    for long in list_long:
        binary = bin(long)[2:].zfill(8)
        bin_left = binary[:4]
        bin_right = binary[4:]
        if bin_left not in to_ommit:
            list_bin.append(bin_left)
        if bin_right not in to_ommit:
            list_bin.append(bin_right)

    n = len(list_bin)

    colors = color_range(start_color, end_color, n)

    root = tk.Tk()
    root.title(args.file)

    canvas = tu.ScrolledCanvas(master=root, width=2000, height=2000)
    canvas.pack(fill=tk.BOTH, expand=tk.YES)

    screen = tu.TurtleScreen(canvas)
    screen.screensize(20000, 15000)

    canvas.bind("<ButtonPress-1>", scroll_start)
    canvas.bind("<B1-Motion>", scroll_move)
    canvas.bind('<MouseWheel>', zoom)

    turtle = tu.RawTurtle(screen)
    turtle.hideturtle()
    turtle.speed(10)
    turtle.pensize(0.0008)
    turtle.tracer(0, 0)

    j = 0
    for digit in list_bin:
        u = int(digit, 2)
        dir = directions[u]

        turtle.setheading(0)
        turtle.setheading(dir)
        turtle.color(colors[j][0], colors[j][1], colors[j][2])
        turtle.forward(0.05)

        j = j+1

        if not args.silent:
            sys.stdout.write('\033[1;32;1m \rProgress : ' +
                             str(round(float(j)/n*100, 2)) + "%\033[00m")
            sys.stdout.flush()
    if not args.silent:
        print("\n\n \033[1;91m ---- Computation done ---- \033[00m \n")


def print_debug(binary, args, list_long):

    print('''\033[1;91m
  ________   __________      _______ _______    _
 |  ____\ \ / /  ____\ \    / /_   _|___  / |  | |
 | |__   \ V /| |__   \ \  / /  | |    / /| |  | |
 |  __|   > < |  __|   \ \/ /   | |   / / | |  | |
 | |____ / . \| |____   \  /   _| |_ / /__| |__| |
 |______/_/ \_\______|   \/   |_____/_____|\____/
\033[00m''')

    print(
        "\033[1;96m **** Loaded file :\033[00m \033[93m{}\033[00m" .format(args.file))
    print(
        "\033[1;96m **** File type :\033[00m \033[93m{}\033[00m" .format(binary.format))
    print("\033[1;96m **** Total file size (bytes) :\033[00m \033[93m{}\033[00m" .format(
        os.path.getsize(args.file)))
    print("\033[1;96m **** Number of 4-bits sequences in .text section :\033[00m \033[93m{}\033[00m" .format(str(2*len(list_long))))
    print(
        "\033[1;96m **** Start color :\033[00m \033[93m{}\033[00m" .format(args.start_color))
    print(
        "\033[1;96m **** End color :\033[00m \033[93m{}\033[00m" .format(args.end_color))
    print("\033[1;96m **** Legend display :\033[00m \033[93m{}\033[00m" .format(
        str(args.no_legend == False)))
    print("\033[1;96m **** Values to omit :\033[00m \033[93m{}\033[00m" .format(
        (str(args.omit) if isinstance(args.omit, list) else "None")))
    print "\n"
    print("\033[1;91m ---- Starting computation ---- \033[00m \n")


def draw_legend(colors):
    tu.setup(650, 275)
    tu.title('Legend')

    i = 0
    for dir in directions:
        lines = tu.Turtle()
        lines.penup()
        lines.setposition(-210, 0)
        lines.pendown()
        lines.tracer(0, 0)
        lines.speed(10)
        lines.shape("classic")
        lines.shapesize(0.5)
        lines.setheading(0)
        lines.setheading(dir)
        lines.forward(70)

        digit = tu.Turtle()
        digit.tracer(0, 0)
        digit.speed(10)
        digit.penup()
        digit.setposition(-210, -5)
        digit.setheading(0)
        digit.setheading(dir)
        digit.hideturtle()
        digit.forward(80)
        digit.write(str(hex(i)), align="center")

        i = i+1

    gradient = tu.Turtle()
    gradient.tracer(0, 0)
    gradient.hideturtle()
    gradient.penup()
    gradient.setposition(-30, -30)
    gradient.pendown()
    gradient.write("First digit", align="center")
    gradient.penup()
    gradient.setposition(-30, 0)
    gradient.pensize(30)
    gradient.pendown()
    for c in colors:
        gradient.color(c)
        gradient.forward(float(300)/len(colors))
    gradient.color(0, 0, 0)
    gradient.setheading(270)
    gradient.penup()
    gradient.forward(30)
    gradient.write("Last digit", align="center")


def main():

    argparser = argparse.ArgumentParser(description='''This python program displays a graphical representation of
    the binary code in the code section of a PE or an ELF file. Each sequence of four consecutive bits is
    represented by a line which direction depends on the value of the digit in hexadecimal basis.
    The colors of the lines give the order of the digits in the code section.
    You can use the mouse wheel to zoom and drag&drop to move inside the visualizer.''')

    argparser.add_argument("file", metavar='file',
                           help='Path of the executable')
    argparser.add_argument("-sc", "--start-color", default='#42b0f4',
                           help="Start color of gradient in HEX or RGB 255-tuple. e.g : '#42b0f4' or '(18,255,156)'")
    argparser.add_argument("-ec", "--end-color", default='#f441e2',
                           help="End color of gradient in HEX or RGB 255-tuple. e.g : '#42b0f4' or '(18,255,156)'")
    argparser.add_argument("-om", "--omit", nargs="+",  default='',
                           help="List of hex values to omit during the computation of the graphical visualization. One value between 0x0 and 0xf at a time. e.g : 0x1 0xa 0xe")
    argparser.add_argument("-nl", "--no-legend",  action="store_true",
                           help="Disable legend display.")
    argparser.add_argument("-s", "--silent",  action="store_true",
                           help="Disable all output messages.")

    args = argparser.parse_args()

    binary, list_long, start_color, end_color = check_arguments(args)

    if not args.silent:
        print_debug(binary, args, list_long)

    draw(args, list_long, start_color, end_color)

    colors_light = color_range(start_color, end_color, 100)
    if not args.no_legend:
        draw_legend(colors_light)
        tu.update()

    tu.mainloop()
    print('\n')


if __name__ == "__main__":
    main()
