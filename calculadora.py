import tkinter as tk

class CalculadoraBasica:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Básica")
        self.root.geometry("350x400")
        
        # Variable para almacenar la operación
        self.operacion = ""
        self.resultado = 0
        self.ultima_operacion = ""
        
        # Crear interfaz
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Pantalla
        self.pantalla = tk.Entry(self.root, font=('Arial', 20), justify='right')
        self.pantalla.grid(row=0, column=0, columnspan=3, padx=10, pady=10, ipadx=10, ipady=10)
        
        # Botones básicos
        botones = [
            '7', '8', '9', 
            '4', '5', '6', 
            '1', '2', '3', 
            '0', '+', '-', 
            'C', '='
        ]
        
        # Posiciones de los botones
        row = 1
        col = 0
        
        for boton in botones:
            comando = lambda x=boton: self.click(x)
            tk.Button(
                self.root, 
                text=boton, 
                font=('Arial', 14),
                width=5, 
                height=2, 
                command=comando
            ).grid(row=row, column=col, padx=2, pady=2)
            
            col += 1
            if col > 2:
                col = 0
                row += 1
    
    def click(self, caracter):
        if caracter == '=':
            self.calcular_resultado()
        elif caracter == 'C':
            self.limpiar()
        elif caracter in ['+', '-']:
            self.agregar_operacion(caracter)
        else:
            self.agregar_numero(caracter)
    
    def agregar_numero(self, numero):
        actual = self.pantalla.get()
        self.pantalla.delete(0, tk.END)
        self.pantalla.insert(0, actual + numero)
    
    def agregar_operacion(self, operador):
        actual = self.pantalla.get()
        if actual:
            self.operacion = actual + operador
            self.ultima_operacion = operador
            self.pantalla.delete(0, tk.END)
    
    def calcular_resultado(self):
        try:
            segundo_numero = self.pantalla.get()
            if self.ultima_operacion == '+':
                resultado = float(self.operacion[:-1]) + float(segundo_numero)
            elif self.ultima_operacion == '-':
                resultado = float(self.operacion[:-1]) - float(segundo_numero)
            else:
                resultado = float(segundo_numero)
            
            self.pantalla.delete(0, tk.END)
            self.pantalla.insert(0, str(resultado))
            self.operacion = ""
            
        except Exception as e:
            self.pantalla.delete(0, tk.END)
            self.pantalla.insert(0, "Error")
    
    def limpiar(self):
        self.pantalla.delete(0, tk.END)
        self.operacion = ""
        self.ultima_operacion = ""

if __name__ == "__main__":
    root = tk.Tk()
    calc = CalculadoraBasica(root)
    root.mainloop()