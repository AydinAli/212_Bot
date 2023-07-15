import discord
import matplotlib.pyplot as plt

def create_eq_image(equation):
    f = plt.figure()
    r = f.canvas.get_renderer()
    plt.axis('off') 
    eq = r''.join(equation) #Raw string to read Latex \ commands
    t = plt.text(-0.05, 0.2, '$%s$' %eq, size=50, color='black')
    bb = t.get_window_extent(renderer=r).transformed(plt.gca().transData.inverted())
    width = bb.width
    height = bb.height
    f.set_size_inches(width * 6.4, height * 6.4) #6.4 4.8 are default dimensions for x:[0,1] y:[0,1] plot
    filepath = "Images/equation.png"
    plt.savefig(filepath)
    plt.close()
    return filepath

def find_line(filepath, name):
    with open(filepath, 'r') as file:
        for line_num, line in enumerate(file):
            if (line.split(":")[0] == name): return line_num #Returns index of line if found
    return -1 #Value for line not found

def delete_eq_by_line_num(filepath, line_num):
    with open(filepath, 'r') as file: lines = file.readlines()
    with open(filepath, 'w') as file:
        for ln, line in enumerate(lines):
            if (ln != line_num): file.writelines(line) #Rewrites every line except one to be deleted

def write_eq_def(filepath, line_num, eq_name, eq_def):
    delete_eq_by_line_num(filepath, line_num)
    with open(filepath, 'a') as file:
        file.write(eq_name + ": " + eq_def + "\n")