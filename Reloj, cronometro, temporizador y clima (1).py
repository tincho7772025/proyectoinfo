import tkinter as tk
from tkinter import ttk
import time
import requests
from tkinter import messagebox

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
hora = 0
minutos = 0
segundos = 0
temporizador_stop = None
cronometro_stop = None


# ---------------------- Pestañas ---------------------------------
pestania = ttk.Notebook(ventana)
pestania.pack(expand=True, fill=tk.BOTH)

menu_opciones  = tk.Menu(ventana,title='Opciones',tearoff=0)
ventana.config(menu=menu_opciones)
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
frame_timer = tk.Frame(pestania,bg='DeepSkyBlue3')

#----------------------------Funciones------------------------------------
def confirmar():
    if combobox.get() == 'Seleccione la hora' or combobox_minutos.get() == 'Seleccione los minutos' or combobox_segundos.get() == 'Seleccione los segundos' : 
        messagebox.showwarning('Advertencia','Seleccione todos los valores del cronometro')
    else: 
        combobox.config(state='disabled')
        combobox_minutos.config(state='disabled')
        combobox_segundos.config(state='disabled')
        boton_timer_cancelar.config(state='active')
        boton_timer_iniciar.grid(row=4,pady=10)
        boton_timer_pausar.grid(column=1,row=4 ,pady=10)
        boton_timer_reiniciar.grid(column=2,row=4,pady=10)
        boton_timer_cancelar.grid(column=2,row=3)
        boton_timer_iniciar.config(state='active')
        
        temporizador_label.config(text=f'{hora}:{minutos}:{segundos}')

def cancelar():
    combobox.config(state='readonly')
    combobox_minutos.config(state='readonly')
    combobox_segundos.config(state='readonly')
    combobox.set('Seleccione la hora')
    combobox_minutos.set('Seleccione los minutos')
    combobox_segundos.set('Seleccione los segundos')



def seleccion_hora(event):
    global hora
    elemento_seleccionado = combobox.get()
    hora = int(elemento_seleccionado)
    
def seleccion_minutos(event):
    global minutos
    elemento_seleccionado = combobox_minutos.get()
    minutos = int(elemento_seleccionado)

    
def seleccion_segundos(event):
    global segundos
    elemento_seleccionado = combobox_segundos.get()
    segundos=int(elemento_seleccionado)

              

def iniciar_temporizador():
    global hora,minutos,segundos,temporizador_stop
    if segundos > 0:
        segundos = int(segundos)
        segundos -= 1
        temporizador_label.config(text=f'{hora}:{minutos}:{segundos}')
        boton_timer_iniciar.config(state='disabled')
        boton_timer_pausar.config(state='normal')
        boton_timer_reiniciar.config(state='normal')
        temporizador_stop = ventana.after(1000, iniciar_temporizador)
        if segundos == 0 and int(minutos)>0 :
            minutos = int(minutos)
            minutos -= 1
            segundos = 59
            temporizador_label.config(text=f'{hora}:{minutos}:{segundos}')
        if minutos == 0 and int(hora)>0:
            hora = int(hora)
            hora -= 1
            minutos = 59
            temporizador_label.config(text=f'{hora}:{minutos}:{segundos}')
    elif minutos > 0 and segundos == 0 and hora==0:
        minutos -= 1
        segundos = 59
        temporizador_label.config(text=f'{hora}:{minutos}:{segundos}')
        temporizador_stop = ventana.after(1000, iniciar_temporizador)
    elif hora > 0 and minutos==0 and segundos==0:
        hora = int(hora)
        hora -= 1
        minutos = 59
        segundos = 59
        temporizador_label.config(text=f'{hora}:{minutos}:{segundos}')
        temporizador_stop = ventana.after(1000, iniciar_temporizador)

    else:
        messagebox.showinfo('Notificacion','¡Tiempo!')
        combobox.set('Seleccione la hora')
        combobox_minutos.set('Seleccione los minutos')
        combobox_segundos.set('Seleccione los segundos')
        boton_timer_pausar.config(state='disabled')
        boton_timer_reiniciar.config(state='disabled')
        boton_timer_cancelar.config(state='disabled')
        combobox.config(state='readonly')
        combobox_minutos.config(state='readonly')
        combobox_segundos.config(state='readonly')
       

def pausar_temporizador():
    global temporizador_stop
    if temporizador_stop:
        ventana.after_cancel(temporizador_stop)
        boton_timer_iniciar.config(state='normal')

def reiniciar_temporizador():
    global hora,minutos,segundos, temporizador_stop
    if temporizador_stop:
        ventana.after_cancel(temporizador_stop)
    hora = 0
    minutos = 0
    segundos = 0
    temporizador_label.config(text=f'{hora}:{minutos}:{segundos}')
    boton_timer_iniciar.config(state='disabled')
    boton_timer_pausar.config(state='disabled')
    boton_timer_reiniciar.config(state='disabled')
    combobox.config(state='readonly')
    combobox_minutos.config(state='readonly')
    combobox_segundos.config(state='readonly')
    combobox.set('Seleccione la hora')
    combobox_minutos.set('Seleccione los minutos')
    combobox_segundos.set('Seleccione los segundos')

#-------------------------  horas del cronometro ----------------------------------------
frame_horas = tk.Frame(frame_timer,bg='DeepSkyBlue3')


label_horas = tk.Label(frame_horas,text='Horas',bg='DeepSkyBlue3')

combobox = ttk.Combobox(frame_horas,font=('arial',8),foreground='gray',state='normal',width=20,height=10)
combobox.set('Seleccione la hora')
combobox.config(state='readonly')

elementos = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
combobox['values']=elementos

combobox.bind('<<ComboboxSelected>>', seleccion_hora)

label_horas.grid()
combobox.grid()
frame_horas.grid(column=0,row=0)
#------------------------------------ minutos del cronometro-------------------------------------------
frame_minutos = tk.Frame(frame_timer,bg='DeepSkyBlue3')

label_minutos = tk.Label(frame_minutos,text='Minutos',bg='DeepSkyBlue3')

combobox_minutos = ttk.Combobox(frame_minutos,font=('arial',8),foreground='gray',state='normal')
combobox_minutos.config(state='readonly')
combobox_minutos.set('Seleccione los minutos')

elementos_minutos = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59]
combobox_minutos['values']=elementos_minutos



combobox_minutos.bind('<<ComboboxSelected>>', seleccion_minutos)

label_minutos.grid()

combobox_minutos.grid()
frame_minutos.grid(column=1,row=0)
#------------------------------------------ segundos del cronometro---------------------------------------
frame_segundos = tk.Frame(frame_timer,bg='DeepSkyBlue3')

label_segundos = tk.Label(frame_segundos,text='Segundos',bg='DeepSkyBlue3')

combobox_segundos = ttk.Combobox(frame_segundos,font=('arial',8),foreground='gray',background='white',state='normal')
combobox_segundos.config(state='readonly')
combobox_segundos.set('Seleccione los segundos')
elementos_segundos = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59]
combobox_segundos['values']=elementos_segundos



combobox_segundos.bind('<<ComboboxSelected>>', seleccion_segundos)

label_segundos.grid()

combobox_segundos.grid()

frame_segundos.grid(column=2,row=0)

#------------------------------------------ label del timer---------------------------------------------------------

temporizador_label = tk.Label(frame_timer, text=f'{hora}:{minutos}:{segundos}', font=('Cambria Math',12), bg='DeepSkyBlue3', fg='red')



#----------------------Botones------------------------------------------------------------------

boton_timer_confirmar = tk.Button(frame_timer, text='Confirmar', command=confirmar,font=('arial',11),bg='SeaGreen2')
boton_timer_iniciar = tk.Button(frame_timer, text='Iniciar',command=iniciar_temporizador,bg='SeaGreen2',width=10)
boton_timer_pausar = tk.Button(frame_timer, text='Pausar',command=pausar_temporizador,bg='SeaGreen2',width=10)
boton_timer_reiniciar = tk.Button(frame_timer, text='Reiniciar',command=reiniciar_temporizador,bg='SeaGreen2',width=10)
boton_timer_cancelar  = tk.Button(frame_timer,text='cancelar',command=cancelar,bg='SeaGreen2',width=10)


#----------------------------------------------------Empaquetado
temporizador_label.grid(column=1,row=2)
boton_timer_confirmar.grid(column=1,row=3)
boton_timer_iniciar.grid_forget()
boton_timer_pausar.grid_forget()
boton_timer_reiniciar.grid_forget()
boton_timer_cancelar.grid_forget()
frame_timer.grid_anchor(tk.N)
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
