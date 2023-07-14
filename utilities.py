import discord
import matplotlib.pyplot as plt

def create_eq_image(equation):
    plt.figure()
    plt.axis('off') 
    eq = r''.join(equation) #Raw string to read Latex \ commands
    plt.text(0.4, 0.4, '$%s$' %eq, size=50, color='blue')
    filepath = "Images/equation.png"
    plt.savefig(filepath)
    plt.close()
    return filepath