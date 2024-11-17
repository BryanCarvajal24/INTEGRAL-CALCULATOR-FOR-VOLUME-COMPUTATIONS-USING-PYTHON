import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from sympy import symbols, integrate, lambdify, sympify, pi, sin, cos, tan
import tkinter as tk
from tkinter import ttk
from mpl_toolkits.mplot3d import Axes3D
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.integrate import dblquad


#pip install numpy matplotlib sympy tkinter scipy



root = tk.Tk()
root.title("Calculadora de Volumen con Integral Doble")

# Definir símbolos para x y y
x, y = symbols('x y')


#VENTANA INICIAL



def elegir_opcion():
    opcion_ventana = tk.Toplevel(root)
    opcion_ventana.title("Elegir Tipo de Cálculo")
    
    label_opcion = tk.Label(opcion_ventana, text="Selecciona el tipo de cálculo:")
    label_opcion.pack(pady=10)

    # Botones para seleccionar la opción
    boton_real = tk.Radiobutton(opcion_ventana, text="1. Volumen solo con limites de números reales",  command=abrir_ventana_opción1)
    boton_funcion = tk.Radiobutton(opcion_ventana, text="2. Volumen con limites de números reales y funciones", command=abrir_ventana_opción2)
    boton_volumen = tk.Radiobutton(opcion_ventana, text="3. Volumen de una región acotada por 2 superficies", command=abrir_ventana_opcion3)
    # Ensure buttons are packed in the window to make them visible
    boton_real.pack(pady=5)
    boton_funcion.pack(pady=5)
    boton_volumen.pack(pady=5)




#VENTANA PRIMERA OPCIÓN

def abrir_ventana_opción1():
    # Nueva ventana para el caso de solo números reales
    real_ventana = tk.Toplevel(root)
    real_ventana.title("Integrales con Números Reales")
    
    # Instrucciones para el usuario sobre pi, sqrt() para raíces, y funciones trigonométricas
    label_instrucciones = tk.Label(real_ventana, text="Puedes usar 'pi' para π y funciones trigonométricas como sin(x), cos(x), tan(x).")
    label_instrucciones.pack(pady=10)

    # Pedir los límites de integración y el tipo de integral
    global entry_funcion, entry_x_min, entry_x_max, entry_y_min, entry_y_max, tipo_var

    label_funcion = tk.Label(real_ventana, text="Ingrese la función f(x, y):")
    label_funcion.pack(pady=5)
    
    entry_funcion = tk.Entry(real_ventana)
    entry_funcion.pack(pady=5)

    # Pedir límites para x e y
    label_x_min = tk.Label(real_ventana, text="Límite inferior para x:")
    label_x_min.pack(pady=5)
    entry_x_min = tk.Entry(real_ventana)
    entry_x_min.pack(pady=5)
    
    label_x_max = tk.Label(real_ventana, text="Límite superior para x:")
    label_x_max.pack(pady=5)
    entry_x_max = tk.Entry(real_ventana)
    entry_x_max.pack(pady=5)

    label_y_min = tk.Label(real_ventana, text="Límite inferior para y:")
    label_y_min.pack(pady=5)
    entry_y_min = tk.Entry(real_ventana)
    entry_y_min.pack(pady=5)
    
    label_y_max = tk.Label(real_ventana, text="Límite superior para y:")
    label_y_max.pack(pady=5)
    entry_y_max = tk.Entry(real_ventana)
    entry_y_max.pack(pady=5)

    # Tipo de integral
    label_tipo = tk.Label(real_ventana, text="Selecciona el tipo de integral:")
    label_tipo.pack(pady=10)
    
    tipo_var = tk.StringVar(value='Tipo 1')
    
    boton_tipo1 = tk.Radiobutton(real_ventana, text="Tipo 1: dy dx", variable=tipo_var, value='Tipo 1')
    boton_tipo2 = tk.Radiobutton(real_ventana, text="Tipo 2: dx dy", variable=tipo_var, value='Tipo 2')
    
    boton_tipo1.pack(pady=5)
    boton_tipo2.pack(pady=5)
    
    # Botón para calcular el volumen
    boton_calcular = tk.Button(real_ventana, text="Calcular Volumen", command=calcular_volumen)
    boton_calcular.pack(pady=10)

def calcular_volumen():
    # Obtener la función ingresada
    funcion_str = entry_funcion.get()
    funcion = sympify(funcion_str)  # Convertir string a expresión simbólica
    
    # Obtener el tipo de integral seleccionado
    tipo_integral = tipo_var.get()

    # Obtener los límites para x e y
    if tipo_integral == 'Tipo 1':
        # Integral de tipo 1: dx dy (x con números y y con curvas)
        x_lim_inf = sympify(entry_x_min.get())
        x_lim_sup = sympify(entry_x_max.get())
        y_lim_inf = sympify(entry_y_min.get())
        y_lim_sup = sympify(entry_y_max.get())
        integral = integrate(integrate(funcion, (x, x_lim_inf, x_lim_sup)), (y, y_lim_inf, y_lim_sup))
    elif tipo_integral == 'Tipo 2':
        # Integral de tipo 2: dy dx (y con números y x con curvas)
        y_lim_inf = sympify(entry_y_min.get())
        y_lim_sup = sympify(entry_y_max.get())
        x_lim_inf = sympify(entry_x_min.get())
        x_lim_sup = sympify(entry_x_max.get())
        integral = integrate(integrate(funcion, (y, y_lim_inf, y_lim_sup)), (x, x_lim_inf, x_lim_sup))

    # Graficar el volumen con colores y paredes
    graficar_volumen(funcion, x_lim_inf, x_lim_sup, y_lim_inf, y_lim_sup, integral)

def graficar_volumen(funcion, x_lim_inf, x_lim_sup, y_lim_inf, y_lim_sup, integral):
    funcion_lamb = lambdify([x, y], funcion)  # Convertir la función simbólica en una función numérica

    # Crear la cuadrícula para la región de integración
    x_vals = np.linspace(float(x_lim_inf), float(x_lim_sup), 100)
    y_vals = np.linspace(float(y_lim_inf), float(y_lim_sup), 100)
    X_vals, Y_vals = np.meshgrid(x_vals, y_vals)
    Z_vals = funcion_lamb(X_vals, Y_vals)

    # Crear la figura para el gráfico 3D
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Mostrar el valor de la integral como título del gráfico
    fig.suptitle(f"Volumen calculado: {integral}", fontsize=16)

    # Crear el gráfico de la superficie
    ax.plot_surface(X_vals, Y_vals, Z_vals, cmap=cm.viridis, alpha=0.8)

    # Pared en x = x_lim_inf
    Y0 = np.linspace(float(y_lim_inf), float(y_lim_sup), 100)
    X0 = np.full_like(Y0, float(x_lim_inf))
    Z0 = np.array([float(funcion.subs({x: x_lim_inf, y: yi})) for yi in Y0])
    ax.plot_surface(X0[np.newaxis, :], Y0[np.newaxis, :], np.array([Z0, np.zeros_like(Z0)]), color='cyan', alpha=0.5)

    # Pared en x = x_lim_sup
    X1 = np.full_like(Y0, float(x_lim_sup))
    Z1 = np.array([float(funcion.subs({x: x_lim_sup, y: yi})) for yi in Y0])
    ax.plot_surface(X1[np.newaxis, :], Y0[np.newaxis, :], np.array([Z1, np.zeros_like(Z1)]), color='cyan', alpha=0.5)

    # Pared en y = y_lim_inf
    Z_min = np.array([float(funcion.subs({x: xi, y: y_lim_inf})) for xi in x_vals])
    ax.plot_surface(x_vals[np.newaxis, :], np.full_like(x_vals, float(y_lim_inf))[np.newaxis, :], np.array([Z_min, np.zeros_like(Z_min)]), color='cyan', alpha=0.5)

    # Pared en y = y_lim_sup
    Z_max = np.array([float(funcion.subs({x: xi, y: y_lim_sup})) for xi in x_vals])
    ax.plot_surface(x_vals[np.newaxis, :], np.full_like(x_vals, float(y_lim_sup))[np.newaxis, :], np.array([Z_max, np.zeros_like(Z_max)]), color='cyan', alpha=0.5)

    # Etiquetas para los ejes
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('f(x, y)')
    
    plt.show()







#VENTANA SEGUNDA OPCIÓN

def abrir_ventana_opción2():
    blank_window = tk.Toplevel(root)
    blank_window.title("Números y Funciones")
    blank_window.geometry("100x100")  # Set the size of the blank window

    global varTipo
    varTipo = tk.StringVar(value='Tipo 1')
    
    boton_tipo1 = tk.Radiobutton(blank_window, text="Tipo 1: dy dx", variable=varTipo, value='Tipo1', command=pestaña_tipo1)
    boton_tipo2 = tk.Radiobutton(blank_window, text="Tipo 2: dx dy", variable=varTipo, value='Tipo2', command=pestaña_tipo2)

    boton_tipo1.pack(pady=5)
    boton_tipo2.pack(pady=5)

def calcular_volumen_tipo2(funcion, x_lim, y_lim):
    try:
        # Resolver la integral doble simbólicamente
        if varTipo.get() == 'Tipo1':
            integral_doble = integrate(integrate(funcion, (y, y_lim[0], y_lim[1])), (x, x_lim[0], x_lim[1]))
        else:
            integral_doble = integrate(integrate(funcion, (x, x_lim[0], x_lim[1])), (y, y_lim[0], y_lim[1]))
        return integral_doble
    except Exception as e:
        messagebox.showerror("Error", f"Error al calcular el volumen: {e}")
        return None

# Función para graficar la figura en 3D con paredes y límites funcionales y mostrar el volumen calculado
def graficar_figura_con_paredes(funcion, x_lim, y_lim, volumen):
    try:
        # Crear la gráfica 3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        if varTipo.get() == 'Tipo1':
            # Crear una malla de valores para X
            x_vals = np.linspace(float(x_lim[0]), float(x_lim[1]), 100)
            y_min_vals = np.array([float(y_lim[0].subs(x, xi)) for xi in x_vals])
            y_max_vals = np.array([float(y_lim[1].subs(x, xi)) for xi in x_vals])
            X = np.array([[xi for _ in range(100)] for xi in x_vals])
            Y = np.array([np.linspace(y_min_vals[i], y_max_vals[i], 100) for i in range(100)])
            Z = np.array([[float(funcion.subs({x: X[i][j], y: Y[i][j]})) for j in range(100)] for i in range(100)])
            ax.plot_surface(X, Y, Z, cmap=cm.viridis, alpha=0.8)

            # Dibujar las paredes
            X0 = np.full_like(Y[0], float(x_lim[0]))
            Y0 = np.linspace(float(y_lim[0].subs(x, x_lim[0])), float(y_lim[1].subs(x, x_lim[0])), 100)
            Z0 = np.array([float(funcion.subs({x: x_lim[0], y: yi})) for yi in Y0])
            ax.plot_surface(X0[np.newaxis, :], Y0[np.newaxis, :], np.array([Z0, np.zeros_like(Z0)]), color='cyan', alpha=0.5)
            X1 = np.full_like(Y[0], float(x_lim[1]))
            Y1 = np.linspace(float(y_lim[0].subs(x, x_lim[1])), float(y_lim[1].subs(x, x_lim[1])), 100)
            Z1 = np.array([float(funcion.subs({x: x_lim[1], y: yi})) for yi in Y1])
            ax.plot_surface(X1[np.newaxis, :], Y1[np.newaxis, :], np.array([Z1, np.zeros_like(Z1)]), color='cyan', alpha=0.5)
            Y_min = np.array([float(y_lim[0].subs(x, xi)) for xi in x_vals])
            Z_min = np.array([float(funcion.subs({x: xi, y: y_lim[0].subs(x, xi)})) for xi in x_vals])
            ax.plot_surface(x_vals[np.newaxis, :], Y_min[np.newaxis, :], np.array([Z_min, np.zeros_like(Z_min)]), color='cyan', alpha=0.5)
            Y_max = np.array([float(y_lim[1].subs(x, xi)) for xi in x_vals])
            Z_max = np.array([float(funcion.subs({x: xi, y: y_lim[1].subs(x, xi)})) for xi in x_vals])
            ax.plot_surface(x_vals[np.newaxis, :], Y_max[np.newaxis, :], np.array([Z_max, np.zeros_like(Z_max)]), color='cyan', alpha=0.5)
        else:
            y_vals = np.linspace(float(y_lim[0]), float(y_lim[1]), 100)
            x_min_vals = np.array([float(x_lim[0].subs(y, yi)) for yi in y_vals])
            x_max_vals = np.array([float(x_lim[1].subs(y, yi)) for yi in y_vals])
            Y = np.array([[yi for _ in range(100)] for yi in y_vals])
            X = np.array([np.linspace(x_min_vals[i], x_max_vals[i], 100) for i in range(100)])
            Z = np.array([[float(funcion.subs({x: X[i][j], y: Y[i][j]})) for j in range(100)] for i in range(100)])
            ax.plot_surface(X, Y, Z, cmap=cm.viridis, alpha=0.8)
        
        # Etiquetas de los ejes
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(f"Volumen calculado: {volumen}")

        # Mostrar el gráfico
        plt.show()

    except Exception as e:
        messagebox.showerror("Error", f"Error al graficar la figura: {e}")

# Función para manejar el botón de "Calcular Volumen"
def calcular_y_graficar():
    try:
        # Obtener la función ingresada
        funcion_str = entry_funcion.get()
        funcion = sympify(funcion_str)

        # Obtener los límites de x e y
        if varTipo.get() == 'Tipo1':
            x_lim = [sympify(entry_xmin.get()), sympify(entry_xmax.get())]
            y_lim = [sympify(entry_ymin.get()), sympify(entry_ymax.get())]
        else:
            x_lim = [sympify(entry_xmin.get()), sympify(entry_xmax.get())]
            y_lim = [sympify(entry_ymin.get()), sympify(entry_ymax.get())]

        # Calcular el volumen
        volumen = calcular_volumen_tipo2(funcion, x_lim, y_lim)
        if volumen is not None:
            # Graficar el sólido y mostrar el volumen
            graficar_figura_con_paredes(funcion, x_lim, y_lim, volumen)

    except Exception as e:
        messagebox.showerror("Error", f"Error en el cálculo o entrada de datos: {e}")

# Definición de las pestañas para los tipos de integrales
def pestaña_tipo1():
    root = tk.Tk()
    root.title("Calculadora de Volumen con Doble Integral")
    global entry_funcion, entry_ymin, entry_ymax, entry_xmin, entry_xmax

    # Etiquetas y entradas para la función y límites
    tk.Label(root, text="Función f(x, y):").grid(row=0, column=0)
    entry_funcion = tk.Entry(root)
    entry_funcion.grid(row=0, column=1)

    tk.Label(root, text="Límite inferior de x:").grid(row=1, column=0)
    entry_xmin = tk.Entry(root)
    entry_xmin.grid(row=1, column=1)

    tk.Label(root, text="Límite superior de x:").grid(row=2, column=0)
    entry_xmax = tk.Entry(root)
    entry_xmax.grid(row=2, column=1)

    tk.Label(root, text="Límite inferior de y (en función de x):").grid(row=3, column=0)
    entry_ymin = tk.Entry(root)
    entry_ymin.grid(row=3, column=1)

    tk.Label(root, text="Límite superior de y (en función de x):").grid(row=4, column=0)
    entry_ymax = tk.Entry(root)
    entry_ymax.grid(row=4, column=1)

    # Botón para calcular el volumen y graficar
    boton_calcular = tk.Button(root, text="Calcular Volumen y Graficar", command=calcular_y_graficar)
    boton_calcular.grid(row=5, column=0, columnspan=2)

    # Ejecutar la aplicación
    root.mainloop()

def pestaña_tipo2():
    root = tk.Tk()
    root.title("Calculadora de Volumen con Doble Integral")
    global entry_funcion, entry_ymin, entry_ymax, entry_xmin, entry_xmax

    # Etiquetas y entradas para la función y límites
    tk.Label(root, text="Función f(x, y):").grid(row=0, column=0)
    entry_funcion = tk.Entry(root)
    entry_funcion.grid(row=0, column=1)

    tk.Label(root, text="Límite inferior de x (en función de y):").grid(row=1, column=0)
    entry_xmin = tk.Entry(root)
    entry_xmin.grid(row=1, column=1)

    tk.Label(root, text="Límite superior de x (en función de y):").grid(row=2, column=0)
    entry_xmax = tk.Entry(root)
    entry_xmax.grid(row=2, column=1)

    tk.Label(root, text="Límite inferior de y:").grid(row=3, column=0)
    entry_ymin = tk.Entry(root)
    entry_ymin.grid(row=3, column=1)

    tk.Label(root, text="Límite superior de y:").grid(row=4, column=0)
    entry_ymax = tk.Entry(root)
    entry_ymax.grid(row=4, column=1)

    # Botón para calcular el volumen y graficar
    boton_calcular = tk.Button(root, text="Calcular Volumen y Graficar", command=calcular_y_graficar)
    boton_calcular.grid(row=5, column=0, columnspan=2)

    # Ejecutar la aplicación
    root.mainloop()







#VENTANA OPCIÓN 3


def abrir_ventana_opcion3():
    ventana_volumen = tk.Toplevel(root)
    ventana_volumen.title("Volumen de una Región Acotada por 2 Superficies")

    # Selección del orden de integración (dy dx o dx dy)
    tk.Label(ventana_volumen, text="Selecciona el tipo de integración:").pack(pady=5)
    global seleccion_orden_opcion3
    seleccion_orden_opcion3 = tk.StringVar()
    seleccion_orden_opcion3.set("dy dx")
    tk.Radiobutton(ventana_volumen, text="dy dx", variable=seleccion_orden_opcion3, value="dy dx", command=lambda: actualizar_campos_limites_opcion3(limites_frame, seleccion_orden_opcion3.get())).pack()
    tk.Radiobutton(ventana_volumen, text="dx dy", variable=seleccion_orden_opcion3, value="dx dy", command=lambda: actualizar_campos_limites_opcion3(limites_frame, seleccion_orden_opcion3.get())).pack()

    # Preguntar si el plano está por encima o por debajo de la función
    tk.Label(ventana_volumen, text="¿El plano está por encima o por debajo de la función?").pack(pady=5)
    global seleccion_plano_opcion3
    seleccion_plano_opcion3 = tk.StringVar()
    seleccion_plano_opcion3.set("encima")
    tk.Radiobutton(ventana_volumen, text="Encima", variable=seleccion_plano_opcion3, value="encima").pack()
    tk.Radiobutton(ventana_volumen, text="Debajo", variable=seleccion_plano_opcion3, value="debajo").pack()

    # Entrada de la función y el plano
    tk.Label(ventana_volumen, text="Función:").pack()
    entrada_funcion = tk.Entry(ventana_volumen)
    entrada_funcion.pack()
    
    tk.Label(ventana_volumen, text="Plano:").pack()
    entrada_plano = tk.Entry(ventana_volumen)
    entrada_plano.pack()

    # Frame para los límites
    limites_frame = tk.Frame(ventana_volumen)
    limites_frame.pack(pady=10)

    global entrada_limite_x_inferior, entrada_limite_x_superior, entrada_limite_y_inferior, entrada_limite_y_superior
    entrada_limite_x_inferior = tk.Entry(limites_frame)
    entrada_limite_x_superior = tk.Entry(limites_frame)
    entrada_limite_y_inferior = tk.Entry(limites_frame)
    entrada_limite_y_superior = tk.Entry(limites_frame)

    actualizar_campos_limites_opcion3(limites_frame, seleccion_orden_opcion3.get())

    # Botón para calcular el volumen y mostrar gráfica
    tk.Button(ventana_volumen, text="Calcular Volumen", command=lambda: validar_entradas_y_calcular_volumen_opcion3(
        entrada_funcion.get(),
        entrada_plano.get(),
        entrada_limite_x_inferior.get(),
        entrada_limite_x_superior.get(),
        entrada_limite_y_inferior.get(),
        entrada_limite_y_superior.get(),
        seleccion_orden_opcion3.get(),
        seleccion_plano_opcion3.get(),
        ventana_volumen)).pack(pady=10)

    # Label para mostrar el resultado
    resultado_volumen = tk.StringVar()
    tk.Label(ventana_volumen, textvariable=resultado_volumen).pack(pady=10)


def actualizar_campos_limites_opcion3(frame, orden_integracion):
    global entrada_limite_x_inferior, entrada_limite_x_superior, entrada_limite_y_inferior, entrada_limite_y_superior
    for widget in frame.winfo_children():
        widget.destroy()
    if orden_integracion == "dy dx":
        tk.Label(frame, text="Límite inferior de x:").pack()
        entrada_limite_x_inferior = tk.Entry(frame)
        entrada_limite_x_inferior.pack()
        
        tk.Label(frame, text="Límite superior de x:").pack()
        entrada_limite_x_superior = tk.Entry(frame)
        entrada_limite_x_superior.pack()

        tk.Label(frame, text="Límite inferior de y (función de x):").pack()
        entrada_limite_y_inferior = tk.Entry(frame)
        entrada_limite_y_inferior.pack()

        tk.Label(frame, text="Límite superior de y (función de x):").pack()
        entrada_limite_y_superior = tk.Entry(frame)
        entrada_limite_y_superior.pack()
    else:
        tk.Label(frame, text="Límite inferior de y:").pack()
        entrada_limite_y_inferior = tk.Entry(frame)
        entrada_limite_y_inferior.pack()
        
        tk.Label(frame, text="Límite superior de y:").pack()
        entrada_limite_y_superior = tk.Entry(frame)
        entrada_limite_y_superior.pack()

        tk.Label(frame, text="Límite inferior de x (función de y):").pack()
        entrada_limite_x_inferior = tk.Entry(frame)
        entrada_limite_x_inferior.pack()

        tk.Label(frame, text="Límite superior de x (función de y):").pack()
        entrada_limite_x_superior = tk.Entry(frame)
        entrada_limite_x_superior.pack()


def validar_entradas_y_calcular_volumen_opcion3(funcion_str, plano_str, x_inf, x_sup, y_inf_str, y_sup_str, orden, seleccion_plano, ventana_volumen):
    """
    Intenta realizar el cálculo numérico para el Ejemplo 1 y si falla, cambia al cálculo simbólico para el Ejemplo 2.
    """
    x, y = symbols('x y')
    
    # Validar que las entradas no estén vacías
    if not funcion_str or not plano_str or not x_inf or not x_sup or not y_inf_str or not y_sup_str:
        return
    
    try:
        # Intentar hacer el cálculo numérico para Ejemplo 1
        calcular_volumen_numerico_opcion3(funcion_str, plano_str, x_inf, x_sup, y_inf_str, y_sup_str, orden, seleccion_plano, ventana_volumen)
    
    except Exception:
        try:
            # Si el cálculo numérico falla, pasar al cálculo simbólico para Ejemplo 2
            funcion = sympify(funcion_str)
            plano = sympify(plano_str)
            limite_x_inferior = sympify(x_inf)
            limite_x_superior = sympify(x_sup)
            limite_y_func_inferior = sympify(y_inf_str)
            limite_y_func_superior = sympify(y_sup_str)

            calcular_volumen_simbolico_opcion3(funcion, plano, limite_x_inferior, limite_x_superior, limite_y_func_inferior, limite_y_func_superior, orden, seleccion_plano, ventana_volumen)
        
        except Exception as e:
            tk.Label(ventana_volumen, text=f"Error: {e}").pack(pady=10)


def calcular_volumen_simbolico_opcion3(funcion, plano, limite_x_inferior, limite_x_superior, limite_y_func_inferior, limite_y_func_superior, orden, seleccion_plano, ventana_volumen):
    if seleccion_plano == "encima":
        integrando = plano - funcion
    else:
        integrando = funcion - plano

    try:
        if orden == "dy dx":
            volumen = integrate(integrando, (y, limite_y_func_inferior, limite_y_func_superior))
            volumen = integrate(volumen, (x, limite_x_inferior, limite_x_superior))
        else:
            volumen = integrate(integrando, (x, limite_y_func_inferior, limite_y_func_superior))
            volumen = integrate(volumen, (y, limite_x_inferior, limite_x_superior))
    except Exception as e:
        tk.Label(ventana_volumen, text=f"Error simbólico: {e}").pack(pady=10)
        return
    
    volumen_eval = volumen.evalf()
    if volumen_eval.is_real:
        volumen_redondeado = round(float(volumen_eval), 5)
    else:
        volumen_redondeado = volumen_eval
    
    tk.Label(ventana_volumen, text=f"El volumen es: {volumen_redondeado}").pack(pady=10)
    graficar_volumen_opcion3(funcion, plano, limite_x_inferior, limite_x_superior, limite_y_func_inferior, limite_y_func_superior, ventana_volumen)


def calcular_volumen_numerico_opcion3(funcion_str, plano_str, x_inf, x_sup, y_inf_str, y_sup_str, orden, seleccion_plano, ventana_volumen):
    # Convertir las entradas a expresiones simbólicas
    funcion = sympify(funcion_str)
    plano = sympify(plano_str)
    limite_x_inferior = sympify(x_inf)
    limite_x_superior = sympify(x_sup)
    limite_y_func_inferior = sympify(y_inf_str)
    limite_y_func_superior = sympify(y_sup_str)

    # Convertir las funciones a expresiones numéricas
    integrando_numeric = lambdify((x, y), plano - funcion if seleccion_plano == "encima" else funcion - plano, "numpy")
    limite_x_inf_numeric = lambdify(y, limite_x_inferior, "numpy")
    limite_x_sup_numeric = lambdify(y, limite_x_superior, "numpy")

    # Definir los límites de integración en y
    y_inferior = float(limite_y_func_inferior.evalf())
    y_superior = float(limite_y_func_superior.evalf())

    # Integrar usando dblquad
    volumen, error = dblquad(integrando_numeric, y_inferior, y_superior, limite_x_inf_numeric, limite_x_sup_numeric)

    # Mostrar el volumen
    tk.Label(ventana_volumen, text=f"El volumen es: {volumen:.5f}").pack(pady=10)

    # Generar gráfica 3D de las superficies
    graficar_volumen_opcion3(funcion, plano, limite_x_inferior, limite_x_superior, y_inferior, y_superior, ventana_volumen)


def graficar_volumen_opcion3(funcion, plano, limite_x_inferior, limite_x_superior, limite_y_inferior, limite_y_superior, ventana_volumen):
    if seleccion_orden_opcion3.get() == "dy dx":
        # Convertir límites de x a numéricos
        x_inf_numeric = float(limite_x_inferior.evalf())
        x_sup_numeric = float(limite_x_superior.evalf())
        
        # Generar los valores de x dentro del rango de integración
        x_vals = np.linspace(x_inf_numeric, x_sup_numeric, 100)

        # Definir funciones numéricas para los límites de y
        f_lim_y_inf = lambdify(x, limite_y_inferior, "numpy")
        f_lim_y_sup = lambdify(x, limite_y_superior, "numpy")
        
        # Para cada valor de x, calcular los límites de y
        y_vals_inf = f_lim_y_inf(x_vals)
        y_vals_sup = f_lim_y_sup(x_vals)
        
        # Generar una malla para X y Y
        X, Y = np.meshgrid(x_vals, np.linspace(y_vals_inf.min(), y_vals_sup.max(), 100))

        # Evaluar las funciones de la superficie y el plano numéricamente
        f_funcion = lambdify([x, y], funcion, "numpy")
        f_plano = lambdify([x, y], plano, "numpy")

        Z_funcion = f_funcion(X, Y)
        Z_plano = f_plano(X, Y)

    else:
        y_inf_numeric = float(limite_y_inferior.evalf())
        y_sup_numeric = float(limite_y_superior.evalf())

        # Generar los valores de y dentro del rango de integración
        y_vals = np.linspace(y_inf_numeric, y_sup_numeric, 100)

        # Definir funciones numéricas para los límites de x
        f_lim_x_inf = lambdify(y, limite_x_inferior, "numpy")
        f_lim_x_sup = lambdify(y, limite_x_superior, "numpy")

        # Para cada valor de y, calcular los límites de x
        x_vals_inf = f_lim_x_inf(y_vals)
        x_vals_sup = f_lim_x_sup(y_vals)

        # Generar una malla para X y Y
        Y, X = np.meshgrid(y_vals, np.linspace(x_vals_inf.min(), x_vals_sup.max(), 100))

        # Evaluar las funciones de la superficie y el plano numéricamente
        f_funcion = lambdify([x, y], funcion, "numpy")
        f_plano = lambdify([x, y], plano, "numpy")

        # Evaluar las superficies
        Z_funcion = f_funcion(X, Y)
        Z_plano = f_plano(X, Y)

    # Graficar solo el sólido donde Z_funcion esté por debajo de Z_plano
    if seleccion_plano_opcion3.get() == "encima":
        # Solo mostrar el sólido donde Z_funcion está por debajo de Z_plano
        Z_solid = np.where(Z_funcion <= Z_plano, Z_funcion, np.nan)

        # Crear un enrejado para la base del sólido
        Z_base = np.where(Z_funcion <= Z_plano, Z_plano, np.nan)
    else:
        # Solo mostrar el sólido donde Z_funcion está por debajo de Z_plano
        Z_solid = np.where(Z_funcion >= Z_plano, Z_funcion, np.nan)

        # Crear un enrejado para la base del sólido
        Z_base = np.where(Z_funcion >= Z_plano, Z_plano, np.nan)
   
    # Crear la figura
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Superficie del sólido
    ax.plot_surface(X, Y, Z_solid, alpha=0.7, cmap='viridis', edgecolor='none')

    # Graficar la base del sólido (el plano)
    ax.plot_surface(X, Y, Z_base, alpha=0.4, cmap='plasma', edgecolor='none')

    # Configuración de etiquetas y título
    ax.set_title("Sólido entre la Función y el Plano")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()









# Crear un botón para iniciar el proceso de elección
boton_iniciar = tk.Button(root, text="Elegir Tipo de Cálculo", command=elegir_opcion)
boton_iniciar.pack(pady=20)

root.mainloop()
















"""
EJEMPLOS


OPCION 1------------------------------------------

EJ1

función: x+y
orden de indegración: dy dx
limite inferior dx: 0
limite superior dx: 1
limite inferior dy: 0
limite superior dy: 2


volumen calculado: 3


EJ2

función: y*cos(x)
orden de indegración: dy dx
limite inferior dx: 0
limite superior dx: pi/2
limite inferior dy: 0
limite superior dy: 1


volumen calculado: 1/2



EJ3

función: 2-x**2-y**2
orden de indegración: dx dy
limite inferior dx: -1
limite superior dx: 1
limite inferior dy: 0
limite superior dy: 1


volumen calculado: 8/3=  2.66666






OPCION 2------------------------------------------


EJ1

función: x**2+y**2
orden de indegración: dy dx
limite inferior dx: 0
limite superior dx: 2
limite inferior dy: x**2
limite superior dy: 2*x


volumen calculado: 216/35 = 6.1714 


EJ2

función: x*y
orden de indegración: dx dy
limite inferior dx: (y**2-6)/2
limite superior dx: y+1
limite inferior dy: -2
limite superior dy: 4


volumen calculado: 36 





OPCION 3------------------------------------------


Ej1

función: 1-x**2-y**2
plano: 1-y
plano por debajo
orden de indegración: dx dy
limite inferior dx: -(y-y**2)**(1/2)
limite superior dx: (y-y**2)**(1/2)
limite inferior dy: 0
limite superior dy: 1


volumen calculado: pi/32 = 0.09817.....



Ej2

función: x**2+y**2
plano: 2*x
orden de indegración: dy dx
limite inferior dx: 0
limite superior dx: 2
limite inferior dy: -(2*x-x**2)**(1/2)
limite superior dy: (2*x-x**2)**(1/2)


volumen calculado: pi/2 = 1.57079







"""