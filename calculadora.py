import tkinter as tk

class Calculadora:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Avanzada")
        self.root.geometry("350x450")
        
        # Variables de estado
        self.operacion = ""
        self.resultado = 0
        self.ultima_operacion = ""
        self.nuevo_numero = True
        self.operacion_pendiente = False
        
        # Crear interfaz
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Pantalla
        self.pantalla = tk.Entry(
            self.root, 
            font=('Arial', 20), 
            justify='right',
            bd=10,
            relief=tk.RIDGE
        )
        self.pantalla.grid(row=0, column=0, columnspan=4, padx=10, pady=10, ipadx=8, ipady=8)
        self.pantalla.insert(0, "0")
        
        # Botones - diseño mejorado
        botones = [
            ('C', 1, 0), ('±', 1, 1), ('%', 1, 2), ('÷', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('×', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('0', 5, 0, 2), ('.', 5, 2), ('=', 5, 3)
        ]
        
        # Crear botones
        for boton in botones:
            texto = boton[0]
            fila = boton[1]
            columna = boton[2]
            
            if texto == '0' and len(boton) > 3:
                colspan = boton[3]
                tk.Button(
                    self.root, 
                    text=texto, 
                    font=('Arial', 14),
                    width=11,
                    height=2,
                    command=lambda x=texto: self.click(x)
                ).grid(row=fila, column=columna, columnspan=colspan, padx=2, pady=2)
            else:
                tk.Button(
                    self.root, 
                    text=texto, 
                    font=('Arial', 14),
                    width=5,
                    height=2,
                    command=lambda x=texto: self.click(x)
                ).grid(row=fila, column=columna, padx=2, pady=2)
    
    def click(self, caracter):
        if caracter == '=':
            self.calcular_resultado()
        elif caracter == 'C':
            self.limpiar()
        elif caracter in ['+', '-', '×', '÷']:
            self.agregar_operacion(caracter)
        elif caracter == '±':
            self.cambiar_signo()
        elif caracter == '%':
            self.porcentaje()
        else:
            self.agregar_numero(caracter)
    
    def agregar_numero(self, numero):
        actual = self.pantalla.get()
        
        if self.nuevo_numero or actual == "0":
            self.pantalla.delete(0, tk.END)
            self.nuevo_numero = False
        
        if numero == '.' and '.' in self.pantalla.get():
            return
            
        self.pantalla.insert(tk.END, numero)
        self.operacion_pendiente = False
    
    def agregar_operacion(self, operador):
        try:
            if self.operacion_pendiente and not self.nuevo_numero:
                self.calcular_resultado()
            
            self.operacion = self.pantalla.get()
            self.ultima_operacion = operador
            self.nuevo_numero = True
            self.operacion_pendiente = True
            
        except Exception as e:
            self.mostrar_error()
    
    def calcular_resultado(self):
        try:
            if not self.ultima_operacion or self.nuevo_numero:
                return
            
            segundo_numero = self.pantalla.get()
            num1 = float(self.operacion)
            num2 = float(segundo_numero)
            resultado = 0
            
            if self.ultima_operacion == '+':
                resultado = num1 + num2
            elif self.ultima_operacion == '-':
                resultado = num1 - num2
            elif self.ultima_operacion == '×':
                resultado = num1 * num2
            elif self.ultima_operacion == '÷':
                if num2 == 0:
                    self.pantalla.delete(0, tk.END)
                    self.pantalla.insert(0, "Error: Div/0")
                    return
                resultado = num1 / num2
            
            # Mostrar resultado
            self.pantalla.delete(0, tk.END)
            if resultado.is_integer():
                self.pantalla.insert(0, str(int(resultado)))
            else:
                self.pantalla.insert(0, str(round(resultado, 8)))
            
            # Resetear estado
            self.operacion = ""
            self.ultima_operacion = ""
            self.nuevo_numero = True
            self.operacion_pendiente = False
            
        except Exception as e:
            self.mostrar_error()
    
    def cambiar_signo(self):
        try:
            actual = self.pantalla.get()
            if actual and actual != "0":
                valor = float(actual)
                self.pantalla.delete(0, tk.END)
                self.pantalla.insert(0, str(-valor))
        except:
            self.mostrar_error()
    
    def porcentaje(self):
        try:
            actual = float(self.pantalla.get())
            self.pantalla.delete(0, tk.END)
            self.pantalla.insert(0, str(actual / 100))
        except:
            self.mostrar_error()
    
    def limpiar(self):
        self.pantalla.delete(0, tk.END)
        self.pantalla.insert(0, "0")
        self.operacion = ""
        self.ultima_operacion = ""
        self.nuevo_numero = True
        self.operacion_pendiente = False
    
    def mostrar_error(self):
        self.pantalla.delete(0, tk.END)
        self.pantalla.insert(0, "Error")
        self.nuevo_numero = True

if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculadora(root)
    root.mainloop()