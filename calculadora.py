import tkinter as tk
from tkinter import font

class CalculadoraModern:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora")
        self.root.geometry("350x500")
        self.root.resizable(False, False)
        self.root.configure(bg='#000000')
        
        # Variables de estado
        self.operacion = ""
        self.ultima_operacion = ""
        self.nuevo_numero = True
        self.operacion_pendiente = False
        self.texto_display = "0"  # Variable para almacenar el texto del display
        
        # Configurar fuentes
        self.fuente_numeros = font.Font(family="Helvetica", size=24)
        self.fuente_display = font.Font(family="Helvetica", size=32)
        
        # Colores (tema oscuro tipo iOS)
        self.colores = {
            'fondo': '#000000',
            'display': '#000000',
            'texto_display': '#FFFFFF',
            'numero': '#333333',
            'operador': '#FF9500',
            'funcion': '#A5A5A5',
            'texto_funcion': '#000000',
            'texto_operador': '#FFFFFF',
            'texto_numero': '#FFFFFF'
        }
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Display
        self.crear_display()
        
        # Botones
        self.crear_botones()
    
    def crear_display(self):
        # Frame del display con borde redondeado visual
        display_frame = tk.Frame(self.root, bg=self.colores['fondo'])
        display_frame.pack(expand=True, fill='both', padx=10, pady=20)
        
        # Usar un Label en lugar de Entry para mejor control visual
        self.pantalla = tk.Label(
            display_frame,
            text=self.texto_display,
            font=self.fuente_display,
            bg=self.colores['display'],
            fg=self.colores['texto_display'],
            anchor='e',
            padx=20,
            relief='flat',
            bd=1,
            highlightbackground='#333333',  # Borde gris oscuro sutil
            highlightthickness=1
        )
        self.pantalla.pack(expand=True, fill='both')
    
    def crear_botones(self):
        # Frame principal de botones
        botones_frame = tk.Frame(self.root, bg=self.colores['fondo'])
        botones_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Configurar grid para que sea flexible
        for i in range(5):  # 5 filas
            botones_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):  # 4 columnas
            botones_frame.grid_columnconfigure(j, weight=1)
        
        # Definición de botones en grid
        botones = [
            ['C', '±', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]
        
        # Crear botones
        for i, fila in enumerate(botones):
            for j, texto in enumerate(fila):
                if texto == '':  # Skip empty cells
                    continue
                    
                # Determinar tipo de botón y colores
                if texto in ['C', '±', '%']:
                    bg_color = self.colores['funcion']
                    fg_color = self.colores['texto_funcion']
                elif texto in ['÷', '×', '-', '+', '=']:
                    bg_color = self.colores['operador']
                    fg_color = self.colores['texto_operador']
                else:
                    bg_color = self.colores['numero']
                    fg_color = self.colores['texto_numero']
                
                # Manejo especial para el botón 0 en la última fila
                if i == 4 and texto == '0':
                    # El 0 ocupa 2 columnas y está alineado con 1 y 2
                    btn = tk.Button(
                        botones_frame,
                        text=texto,
                        font=self.fuente_numeros,
                        bg=bg_color,
                        fg=fg_color,
                        bd=0,
                        relief='flat',
                        command=lambda x=texto: self.click(x)
                    )
                    btn.grid(row=i, column=0, columnspan=2, sticky='nsew', padx=2, pady=2)
                
                # Para . y = en la última fila
                elif i == 4 and texto == '.':
                    btn = tk.Button(
                        botones_frame,
                        text=texto,
                        font=self.fuente_numeros,
                        bg=bg_color,
                        fg=fg_color,
                        bd=0,
                        relief='flat',
                        command=lambda x=texto: self.click(x)
                    )
                    btn.grid(row=i, column=2, sticky='nsew', padx=2, pady=2)
                
                elif i == 4 and texto == '=':
                    btn = tk.Button(
                        botones_frame,
                        text=texto,
                        font=self.fuente_numeros,
                        bg=bg_color,
                        fg=fg_color,
                        bd=0,
                        relief='flat',
                        command=lambda x=texto: self.click(x)
                    )
                    btn.grid(row=i, column=3, sticky='nsew', padx=2, pady=2)
                
                # Para todas las demás filas
                else:
                    btn = tk.Button(
                        botones_frame,
                        text=texto,
                        font=self.fuente_numeros,
                        bg=bg_color,
                        fg=fg_color,
                        bd=0,
                        relief='flat',
                        command=lambda x=texto: self.click(x)
                    )
                    btn.grid(row=i, column=j, sticky='nsew', padx=2, pady=2)
    
    def actualizar_display(self, texto):
        """Actualizar el display usando Label en lugar de Entry"""
        self.texto_display = texto
        self.pantalla.config(text=texto)
    
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
        actual = self.texto_display
        
        if self.nuevo_numero or actual == "0":
            self.actualizar_display("")
            self.nuevo_numero = False
        
        # Evitar múltiples puntos decimales
        if numero == '.' and '.' in self.texto_display:
            return
            
        nuevo_texto = self.texto_display + numero
        self.actualizar_display(nuevo_texto)
        self.operacion_pendiente = False
    
    def agregar_operacion(self, operador):
        try:
            if self.operacion_pendiente and not self.nuevo_numero:
                self.calcular_resultado()
            
            self.operacion = self.texto_display
            self.ultima_operacion = operador
            self.nuevo_numero = True
            self.operacion_pendiente = True
            
        except Exception as e:
            self.mostrar_error()
    
    def calcular_resultado(self):
        try:
            if not self.ultima_operacion or self.nuevo_numero:
                return
            
            segundo_numero = self.texto_display
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
                    self.actualizar_display("Error")
                    return
                resultado = num1 / num2
            
            # Formatear resultado (eliminar .0 si es entero)
            if resultado.is_integer():
                texto_resultado = str(int(resultado))
            else:
                texto_resultado = str(round(resultado, 8))
                # Eliminar ceros decimales innecesarios
                if '.' in texto_resultado:
                    texto_resultado = texto_resultado.rstrip('0').rstrip('.')
            
            self.actualizar_display(texto_resultado)
            
            # Resetear estado
            self.operacion = ""
            self.ultima_operacion = ""
            self.nuevo_numero = True
            self.operacion_pendiente = False
            
        except Exception as e:
            self.mostrar_error()
    
    def cambiar_signo(self):
        try:
            actual = self.texto_display
            if actual and actual != "0" and actual != "Error":
                valor = float(actual)
                self.actualizar_display(str(-valor))
        except:
            self.mostrar_error()
    
    def porcentaje(self):
        try:
            actual = float(self.texto_display)
            self.actualizar_display(str(actual / 100))
        except:
            self.mostrar_error()
    
    def limpiar(self):
        self.actualizar_display("0")
        self.operacion = ""
        self.ultima_operacion = ""
        self.nuevo_numero = True
        self.operacion_pendiente = False
    
    def mostrar_error(self):
        self.actualizar_display("Error")
        self.nuevo_numero = True

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraModern(root)
    root.mainloop()