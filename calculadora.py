import tkinter as tk
from tkinter import font, messagebox
import json
import os

class CalculadoraModern:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Avanzada")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        self.root.configure(bg='#000000')
        
        # Variables de estado
        self.operacion = ""
        self.ultima_operacion = ""
        self.nuevo_numero = True
        self.operacion_pendiente = False
        self.texto_display = "0"
        
        # Memoria
        self.memoria = 0
        self.memoria_activa = False
        
        # Historial
        self.historial = []
        self.max_historial = 10
        
        # Configurar fuentes
        self.fuente_numeros = font.Font(family="Helvetica", size=20)
        self.fuente_display = font.Font(family="Helvetica", size=28)
        self.fuente_pequena = font.Font(family="Helvetica", size=12)
        
        # Colores (tema oscuro tipo iOS)
        self.colores = {
            'fondo': '#000000',
            'display': '#000000',
            'texto_display': '#FFFFFF',
            'numero': '#333333',
            'operador': '#FF9500',
            'funcion': '#A5A5A5',
            'memoria': '#4A90E2',
            'historial': '#34C759',
            'texto_funcion': '#000000',
            'texto_operador': '#FFFFFF',
            'texto_numero': '#FFFFFF',
            'texto_memoria': '#FFFFFF',
            'borde_display': '#333333'
        }
        
        self.cargar_historial()
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Display principal
        self.crear_display()
        
        # Display de memoria
        self.crear_display_memoria()
        
        # Botones
        self.crear_botones()
    
    def crear_display(self):
        # Frame del display
        display_frame = tk.Frame(self.root, bg=self.colores['fondo'])
        display_frame.pack(expand=True, fill='both', padx=10, pady=(20, 5))
        
        # Display principal con borde sutil
        self.pantalla = tk.Label(
            display_frame,
            text=self.texto_display,
            font=self.fuente_display,
            bg=self.colores['display'],
            fg=self.colores['texto_display'],
            anchor='e',
            padx=20,
            relief='solid',
            bd=1,
            highlightbackground=self.colores['borde_display'],
            highlightthickness=1
        )
        self.pantalla.pack(expand=True, fill='both')
    
    def crear_display_memoria(self):
        # Frame para información de memoria
        memoria_frame = tk.Frame(self.root, bg=self.colores['fondo'])
        memoria_frame.pack(fill='x', padx=10, pady=5)
        
        # Indicador de memoria
        self.memoria_label = tk.Label(
            memoria_frame,
            text="M: 0",
            font=self.fuente_pequena,
            bg=self.colores['fondo'],
            fg=self.colores['memoria'],
            anchor='w'
        )
        self.memoria_label.pack(side='left')
        
        # Contador de historial
        self.historial_label = tk.Label(
            memoria_frame,
            text=f"Historial: {len(self.historial)}",
            font=self.fuente_pequena,
            bg=self.colores['fondo'],
            fg=self.colores['historial'],
            anchor='e'
        )
        self.historial_label.pack(side='right')
    
    def crear_botones(self):
        # Frame principal de botones
        botones_frame = tk.Frame(self.root, bg=self.colores['fondo'])
        botones_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Configurar grid para que sea flexible
        for i in range(7):  # 7 filas
            botones_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):  # 4 columnas
            botones_frame.grid_columnconfigure(j, weight=1)
        
        # DEFINICIÓN CORREGIDA DE BOTONES - EL BOTÓN "=" DEBE ESTAR VISIBLE
        botones = [
            # Fila 0: Memoria
            ['MC', 'MR', 'M+', 'M-'],
            # Fila 1: Funciones especiales
            ['MS', 'C', '±', '%'],
            # Fila 2: Números y operadores
            ['7', '8', '9', '÷'],
            # Fila 3: Números y operadores
            ['4', '5', '6', '×'],
            # Fila 4: Números y operadores
            ['1', '2', '3', '-'],
            # Fila 5: Números y operadores - CORREGIDA
            ['0', '', '.', '+'],  # Cambiamos el orden
            # Fila 6: Botones finales - AQUÍ ESTÁ EL "="
            ['', '', 'HIST', '=']   # El "=" en la última fila, columna 3
        ]
        
        # Crear botones
        for i, fila in enumerate(botones):
            for j, texto in enumerate(fila):
                if texto == '':  # Skip empty cells
                    continue
                    
                # Determinar tipo de botón y colores
                if texto in ['MC', 'MR', 'M+', 'M-', 'MS']:
                    bg_color = self.colores['memoria']
                    fg_color = self.colores['texto_memoria']
                elif texto == 'HIST':
                    bg_color = self.colores['historial']
                    fg_color = self.colores['texto_memoria']
                elif texto in ['C', '±', '%']:
                    bg_color = self.colores['funcion']
                    fg_color = self.colores['texto_funcion']
                elif texto in ['÷', '×', '-', '+', '=']:
                    bg_color = self.colores['operador']
                    fg_color = self.colores['texto_operador']
                else:
                    bg_color = self.colores['numero']
                    fg_color = self.colores['texto_numero']
                
                # Manejo especial para botones específicos
                if i == 5 and texto == '0':
                    # El 0 ocupa 2 columnas en la fila 5
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
                
                elif i == 5 and texto == '.':
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
                
                elif i == 5 and texto == '+':
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
                
                # Para el botón "=" en la fila 6
                elif i == 6 and texto == '=':
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
                    btn.grid(row=i, column=2, columnspan=2, sticky='nsew', padx=2, pady=2)
                
                # Para el botón HIST en la fila 6
                elif i == 6 and texto == 'HIST':
                    btn = tk.Button(
                        botones_frame,
                        text="📋 HISTORIAL",
                        font=('Helvetica', 14),
                        bg=bg_color,
                        fg=fg_color,
                        bd=0,
                        relief='flat',
                        command=self.mostrar_historial
                    )
                    btn.grid(row=i, column=0, columnspan=2, sticky='nsew', padx=2, pady=2)
                
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
        """Actualizar el display"""
        self.texto_display = texto
        self.pantalla.config(text=texto)
    
    def actualizar_memoria_display(self):
        """Actualizar el display de memoria"""
        if self.memoria_activa:
            self.memoria_label.config(text=f"M: {self.memoria}", fg='#FFD700')
        else:
            self.memoria_label.config(text=f"M: {self.memoria}", fg=self.colores['memoria'])
        
        self.historial_label.config(text=f"Historial: {len(self.historial)}")
    
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
        elif caracter in ['MC', 'MR', 'M+', 'M-', 'MS']:
            self.manejar_memoria(caracter)
        else:
            self.agregar_numero(caracter)
    
    def manejar_memoria(self, operacion):
        """Manejar operaciones de memoria"""
        try:
            valor_actual = float(self.texto_display) if self.texto_display not in ['Error', ''] else 0
            
            if operacion == 'MC':  # Memory Clear
                self.memoria = 0
                self.memoria_activa = False
            
            elif operacion == 'MR':  # Memory Recall
                if self.memoria_activa:
                    self.actualizar_display(str(self.memoria))
                    self.nuevo_numero = True
            
            elif operacion == 'M+':  # Memory Add
                self.memoria += valor_actual
                self.memoria_activa = True
                self.agregar_al_historial(f"M+ ({valor_actual})")
            
            elif operacion == 'M-':  # Memory Subtract
                self.memoria -= valor_actual
                self.memoria_activa = True
                self.agregar_al_historial(f"M- ({valor_actual})")
            
            elif operacion == 'MS':  # Memory Store
                self.memoria = valor_actual
                self.memoria_activa = True
                self.agregar_al_historial(f"MS ({valor_actual})")
            
            self.actualizar_memoria_display()
            
        except ValueError:
            self.mostrar_error()
    
    def agregar_al_historial(self, operacion):
        """Añadir operación al historial"""
        self.historial.insert(0, operacion)
        
        # Limitar el tamaño del historial
        if len(self.historial) > self.max_historial:
            self.historial.pop()
        
        self.guardar_historial()
        self.actualizar_memoria_display()
    
    def mostrar_historial(self):
        """Mostrar ventana de historial"""
        historial_window = tk.Toplevel(self.root)
        historial_window.title("Historial de Operaciones")
        historial_window.geometry("300x400")
        historial_window.configure(bg='#2C2C2E')
        historial_window.resizable(False, False)
        
        # Frame principal
        main_frame = tk.Frame(historial_window, bg='#2C2C2E')
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Título
        titulo = tk.Label(
            main_frame,
            text="📋 Historial de Operaciones",
            font=('Helvetica', 16, 'bold'),
            bg='#2C2C2E',
            fg='#FFFFFF'
        )
        titulo.pack(pady=(0, 10))
        
        # Lista de historial
        historial_frame = tk.Frame(main_frame, bg='#2C2C2E')
        historial_frame.pack(expand=True, fill='both')
        
        if not self.historial:
            vacio_label = tk.Label(
                historial_frame,
                text="El historial está vacío",
                font=('Helvetica', 12),
                bg='#2C2C2E',
                fg='#888888'
            )
            vacio_label.pack(expand=True)
        else:
            # Scrollbar
            scrollbar = tk.Scrollbar(historial_frame)
            scrollbar.pack(side='right', fill='y')
            
            # Listbox para historial
            listbox = tk.Listbox(
                historial_frame,
                bg='#3A3A3C',
                fg='#FFFFFF',
                font=('Helvetica', 11),
                selectbackground='#4A90E2',
                yscrollcommand=scrollbar.set
            )
            listbox.pack(expand=True, fill='both')
            
            scrollbar.config(command=listbox.yview)
            
            # Añadir items al listbox
            for i, item in enumerate(self.historial):
                listbox.insert('end', f"{i+1}. {item}")
        
        # Botones de acción
        botones_frame = tk.Frame(main_frame, bg='#2C2C2E')
        botones_frame.pack(fill='x', pady=(10, 0))
        
        tk.Button(
            botones_frame,
            text="Limpiar Historial",
            font=('Helvetica', 12),
            bg='#FF3B30',
            fg='#FFFFFF',
            bd=0,
            relief='flat',
            command=lambda: self.limpiar_historial(historial_window)
        ).pack(side='left', padx=(0, 5))
        
        tk.Button(
            botones_frame,
            text="Cerrar",
            font=('Helvetica', 12),
            bg='#4A90E2',
            fg='#FFFFFF',
            bd=0,
            relief='flat',
            command=historial_window.destroy
        ).pack(side='right')
    
    def limpiar_historial(self, ventana):
        """Limpiar todo el historial"""
        self.historial.clear()
        self.guardar_historial()
        self.actualizar_memoria_display()
        ventana.destroy()
        messagebox.showinfo("Historial", "Historial limpiado correctamente")
    
    def guardar_historial(self):
        """Guardar historial en archivo"""
        try:
            with open('calculadora_historial.json', 'w') as f:
                json.dump({
                    'memoria': self.memoria,
                    'historial': self.historial
                }, f)
        except:
            pass
    
    def cargar_historial(self):
        """Cargar historial desde archivo"""
        try:
            if os.path.exists('calculadora_historial.json'):
                with open('calculadora_historial.json', 'r') as f:
                    datos = json.load(f)
                    self.memoria = datos.get('memoria', 0)
                    self.historial = datos.get('historial', [])
                    self.memoria_activa = (self.memoria != 0)
        except:
            self.memoria = 0
            self.historial = []
    
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
            
            # Guardar en historial
            operacion_str = f"{num1} {self.ultima_operacion} {num2} = {resultado}"
            self.agregar_al_historial(operacion_str)
            
            # Formatear resultado
            if resultado.is_integer():
                texto_resultado = str(int(resultado))
            else:
                texto_resultado = str(round(resultado, 8))
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