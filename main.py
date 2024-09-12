import tkinter as tk
from ttkbootstrap import Window
from src.view.main_window import MainWindow
def main():
    # Configuração do banco de dados
    # Configuração da janela principal
    root = Window(themename="simplex")
    root.title("TAC Etiquetas")
    root.geometry("350x200")
    root.resizable(False, False)
    
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
