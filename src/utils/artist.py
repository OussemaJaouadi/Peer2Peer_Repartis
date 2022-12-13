from utils import UI_colors
import pyfiglet as figlet
TAB = '\t'*3
projet = figlet.figlet_format(text="Projet Repartis",font="big")
authors = f"{TAB}Presented By :\n{TAB}{TAB}\nGhassen Abida{TAB}{TAB}  Oussema Jaouadi\n{TAB}{TAB} Taha Mediouni"
def print_art():
    UI_colors.print_violet(projet,end=' ')
    UI_colors.print_violet(authors)