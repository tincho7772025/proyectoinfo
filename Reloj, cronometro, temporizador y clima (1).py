
import tkinter as tk
from tkinter import ttk
import time
import requests

# --------------------- Configuración inicial ---------------------
ventana = tk.Tk()
ventana.title('Reloj con cronómetro, temporizador y clima')
ventana.geometry('800x600')
ventana.configure(bg="lightblue")

API_KEY = 'ff0cac37ef568da2b6f677578ee6a5ab'
CIUDAD = 'Resistencia,AR'

fuente_hora = ('Helvetica', 60)
fuente_fecha = ('Helvetica', 30)
fuente_mensaje = ('Helvetica', 20)

# -------------------- Variables globales -------------------------
cronometro_tiempo = 0.0
temporizador_tiempo = 0
cronometro_stop = None
temporizador_stop = None

# ---------------------- Pestañas ---------------------------------
pestania = ttk.Notebook(ventana)
pestania.pack(expand=True, fill=tk.BOTH)

# ------------------ Pestaña: Fecha y hora ------------------------
frame_hora = tk.Frame(pestania, bg='lightblue')
reloj = tk.Label(frame_hora, font=fuente_hora, fg='white', bg="lightblue")
fecha = tk.Label(frame_hora, font=fuente_fecha, fg='white', bg="lightblue")
reloj.pack(pady=20)
fecha.pack()

def actualizar_reloj():
    tiempo_actual = time.strftime('%H:%M:%S')
    fecha_actual = time.strftime('%d/%m/%Y')
    reloj.config(text=tiempo_actual)
    fecha.config(text=fecha_actual)
    ventana.after(1000, actualizar_reloj)

actualizar_reloj()
pestania.add(frame_hora, text='Reloj')

# ------------------- Pestaña: Cronómetro -------------------------
frame_crono = tk.Frame(pestania, bg='lightblue')
cronometro_label = tk.Label(frame_crono, text='0.0', font=fuente_hora, bg='lightblue', fg='white')
cronometro_label.pack(pady=20)

def iniciar_cronometro():
    global cronometro_tiempo, cronometro_stop
    boton_crono_inicio.config(state='disabled')
    cronometro_tiempo += 0.1
    cronometro_label.config(text=f'{cronometro_tiempo:.1f}')
    cronometro_stop = ventana.after(100, iniciar_cronometro)

def pausar_cronometro():
    global cronometro_stop
    if cronometro_stop:
        ventana.after_cancel(cronometro_stop)
        boton_crono_inicio.config(state='normal')

def reiniciar_cronometro():
    global cronometro_tiempo, cronometro_stop
    if cronometro_stop:
        ventana.after_cancel(cronometro_stop)
    cronometro_tiempo = 0.0
    cronometro_label.config(text='0.0')
    boton_crono_inicio.config(state='normal')

boton_crono_inicio = tk.Button(frame_crono, text='Iniciar', command=iniciar_cronometro, font=fuente_mensaje)
boton_crono_pausa = tk.Button(frame_crono, text='Pausar', command=pausar_cronometro, font=fuente_mensaje)
boton_crono_reiniciar = tk.Button(frame_crono, text='Reiniciar', command=reiniciar_cronometro, font=fuente_mensaje)

boton_crono_inicio.pack(side='left', padx=20)
boton_crono_pausa.pack(side='left', padx=20)
boton_crono_reiniciar.pack(side='left', padx=20)

pestania.add(frame_crono, text='Cronómetro')

# ------------------ Pestaña: Temporizador ------------------------
frame_timer = tk.Frame(pestania, bg='lightblue')

entrada_tiempo = tk.Entry(frame_timer, font=fuente_mensaje, justify='center')
entrada_tiempo.pack(pady=10)

temporizador_label = tk.Label(frame_timer, text='0', font=fuente_hora, bg='lightblue', fg='white')
temporizador_label.pack(pady=20)

def confirmar_temporizador():
    global temporizador_tiempo
    try:
        temporizador_tiempo = int(entrada_tiempo.get())
        temporizador_label.config(text=str(temporizador_tiempo))
        entrada_tiempo.config(state='disabled')
        boton_timer_iniciar.config(state='normal')
    except ValueError:
        temporizador_label.config(text='Inválido')

def iniciar_temporizador():
    global temporizador_tiempo, temporizador_stop
    if temporizador_tiempo > 0:
        temporizador_tiempo -= 1
        temporizador_label.config(text=str(temporizador_tiempo))
        boton_timer_iniciar.config(state='disabled')
        boton_timer_pausar.config(state='normal')
        boton_timer_reiniciar.config(state='normal')
        temporizador_stop = ventana.after(1000, iniciar_temporizador)
    else:
        temporizador_label.config(text="¡Tiempo!")

def pausar_temporizador():
    global temporizador_stop
    if temporizador_stop:
        ventana.after_cancel(temporizador_stop)
        boton_timer_iniciar.config(state='normal')

def reiniciar_temporizador():
    global temporizador_tiempo, temporizador_stop
    if temporizador_stop:
        ventana.after_cancel(temporizador_stop)
    temporizador_tiempo = 0
    temporizador_label.config(text='0')
    entrada_tiempo.config(state='normal')
    boton_timer_iniciar.config(state='disabled')
    boton_timer_pausar.config(state='disabled')
    boton_timer_reiniciar.config(state='disabled')

boton_timer_confirmar = tk.Button(frame_timer, text='Confirmar', command=confirmar_temporizador, font=fuente_mensaje)
boton_timer_iniciar = tk.Button(frame_timer, text='Iniciar', command=iniciar_temporizador, font=fuente_mensaje, state='disabled')
boton_timer_pausar = tk.Button(frame_timer, text='Pausar', command=pausar_temporizador, font=fuente_mensaje, state='disabled')
boton_timer_reiniciar = tk.Button(frame_timer, text='Reiniciar', command=reiniciar_temporizador, font=fuente_mensaje, state='disabled')

boton_timer_confirmar.pack()
boton_timer_iniciar.pack(side='left', padx=10)
boton_timer_pausar.pack(side='left', padx=10)
boton_timer_reiniciar.pack(side='left', padx=10)

pestania.add(frame_timer, text='Temporizador')

# --------------------- Pestaña: Clima ---------------------------
frame_clima = tk.Frame(pestania, bg='lightblue')
clima_label = tk.Label(frame_clima, font=fuente_mensaje, fg='white', bg="lightblue")
clima_label.pack(pady=50)

def obtener_clima():
    url = f'http://api.openweathermap.org/data/2.5/weather?q={CIUDAD}&appid={API_KEY}&units=metric&lang=es'
    try:
        respuesta = requests.get(url)
        datos = respuesta.json()
        if datos['cod'] == 200:
            temp = datos['main']['temp']
            feels_like = datos['main']['feels_like']
            descripcion = datos['weather'][0]['description']
            clima_label.config(text=f'{temp}°C (ST: {feels_like}°C) - {descripcion.capitalize()}')
        else:
            clima_label.config(text='Clima no disponible')
    except requests.exceptions.RequestException:
        clima_label.config(text='Error de conexión')

def actualizar_clima():
    obtener_clima()
    ventana.after(600000, actualizar_clima)  # Cada 10 minutos

actualizar_clima()
pestania.add(frame_clima, text='Clima')

# -------------------- Ejecutar interfaz -------------------------
ventana.mainloop()








