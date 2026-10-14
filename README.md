# Señales y Sistemas

Repositorio de scripts y recursos interactivos para acompañar las guías de ejercicios de la materia **16.68 - Señales y Sistemas** del **ITBA**.

El objetivo es facilitar la interpretación gráfica de los conceptos teóricos y complementar la resolución analítica de los ejercicios.

Consultas: pbenedetti@itba.edu.ar

## Recursos complementarios

### Producto de una senoide por un pulso unitario

Archivo: [`subplots_seno_pulso_producto.py`](./subplots_seno_pulso_producto.py)

El script representa gráficamente las señales:

```math
x(t)=\sin(2\pi t)
```

y un pulso rectangular unitario, de ancho 1 y centrado en $t=\frac{1}{2}$:

```math
p(t)=
\begin{cases}
1, & 0\leq t\leq 1,\\
0, & \text{en otro caso}.
\end{cases}
```

También muestra el producto entre ambas señales:

```math
y(t)=x(t)\,p(t)
```

Por lo tanto:

```math
y(t)=
\begin{cases}
\sin(2\pi t), & 0\leq t\leq 1,\\
0, & \text{en otro caso}.
\end{cases}
```

La visualización permite:

* observar la señal senoidal original en color rojo;
* identificar el intervalo de duración del pulso unitario en color azul;
* visualizar el producto entre ambas señales en color violeta;
* comprobar que el pulso actúa como una ventana temporal;
* comparar las tres señales en un mismo eje temporal.

El producto conserva la senoide únicamente en el intervalo $0\leq t\leq 1$ y la anula fuera de él.

## Guía 2

### Ejercicio 8 — Frecuencias fundamentales

Archivo: [`frecuencias_fundamentales.py`](./frecuencias_fundamentales.py)

El script representa las señales de los apartados **b**, **d** y **f** para facilitar el análisis de su periodicidad y la determinación de sus frecuencias fundamentales.

#### Inciso b)

```math
x(t)=3\sin\left(19\pi t-\frac{\pi}{3}\right)
+2\cos\left(10\pi t+\frac{\pi}{6}\right)
```

Las frecuencias de las componentes son:

```math
f_1=\frac{19}{2}\text{ Hz},
\qquad
f_2=5\text{ Hz}.
```

Como ambas son múltiplos enteros de $0{,}5\text{ Hz}$, la señal resultante tiene:

```math
f_0=0{,}5\text{ Hz},
\qquad
T_0=2\text{ s}.
```

La visualización muestra por separado el seno y el coseno. En el último gráfico se representa su suma, junto con las dos componentes mediante líneas punteadas.

#### Inciso d)

```math
x(t)=\frac{1}{2}
\left[
\cos\left(2t-\frac{\pi}{4}\right)
\right]^2
```

Usando la identidad del coseno al cuadrado:

```math
x(t)=
\frac{1}{4}
+
\frac{1}{4}\cos\left(4t-\frac{\pi}{2}\right).
```

Por lo tanto, su período y su frecuencia angular fundamental son:

```math
T_0=\frac{\pi}{2}\text{ s},
\qquad
\omega_0=4\text{ rad/s}.
```

El programa compara el coseno original con la señal obtenida al elevarlo al cuadrado y multiplicarlo por $\frac{1}{2}$.

#### Inciso f)

```math
x(t)=
\frac{\sin(5\pi t)}
{\sin(\pi t)}.
```

Para los puntos en los que el denominador no se anula, el cociente puede escribirse como:

```math
x(t)=
1+2\cos(2\pi t)+2\cos(4\pi t).
```

De esta expresión se obtiene:

```math
f_0=1\text{ Hz},
\qquad
T_0=1\text{ s}.
```

La visualización muestra el numerador, el denominador y el cociente. En el último gráfico también se superponen las dos señales originales mediante líneas punteadas.

Los círculos abiertos indican los valores enteros de $t$, donde la expresión original produce la indeterminación $0/0$. En esos puntos la función no está definida, aunque su límite es igual a 5.

El script permite:

* comparar las componentes que forman cada señal;
* visualizar sus repeticiones temporales;
* relacionar los períodos individuales con el período fundamental;
* observar cómo las operaciones de suma, potenciación y cociente modifican la periodicidad;
* distinguir los puntos donde una expresión no está definida.

### Ejercicio 15 — Transformada de Fourier de un tren de deltas

Archivo: [`tren_deltas_fourier_ideal.py`](./tren_deltas_fourier_ideal.py)

El script representa el par de transformadas de Fourier del tren periódico de deltas.

En el dominio temporal:

```math
\widetilde{\delta}_{T_0}(t)
=
\sum_{k=-\infty}^{\infty}\delta(t-kT_0)
```

Su transformada de Fourier es:

```math
\mathcal{F}\left\{
\widetilde{\delta}_{T_0}(t)
\right\}
=
\frac{1}{T_0}
\sum_{n=-\infty}^{\infty}
\delta\left(f-\frac{n}{T_0}\right)
```

La visualización permite:

* modificar el período temporal $T_0$ mediante un control deslizante;
* observar el tren de deltas en el dominio temporal;
* visualizar el tren de deltas resultante en el dominio frecuencial;
* comprobar que la separación entre las deltas frecuenciales es $F_0=1/T_0$;
* observar que el peso de cada delta en frecuencia también es $1/T_0$;
* comparar gráficamente la relación inversa entre las separaciones temporal y frecuencial.

Las deltas se representan simbólicamente mediante flechas verticales. Su altura indica su peso y no el valor ordinario de una función.

#### Controles

* **Período temporal $T_0$:** modifica la separación entre las deltas temporales.
* **Reiniciar:** vuelve a la configuración inicial, con $T_0=1$.

La relación fundamental mostrada por el programa es:

```math
\widetilde{\delta}_{T_0}(t)
\longleftrightarrow
\frac{1}{T_0}\widetilde{\delta}_{1/T_0}(f)
```

Por lo tanto, al aumentar la separación entre las deltas en el tiempo, disminuye su separación en frecuencia, y viceversa.

## Guía 3

### Ejercicio 2 — Convolución continua

Archivo: [`convolucion_interactiva.py`](./convolucion_interactiva.py)

El script representa la convolución entre las señales:

$$
x(t)=
\begin{cases}
1, & -1\leq t\leq 1,\\
0, & \text{en otro caso},
\end{cases}
$$

y

$$
g(t)=
\begin{cases}
\dfrac{t}{3}, & 0\leq t\leq 3,\\
0, & \text{en otro caso}.
\end{cases}
$$

La herramienta permite:

- desplazar una de las señales mediante un control deslizante;
- elegir cuál de las dos señales se mantiene fija (la que se evalúa en $\tau$);
- observar la inversión y el desplazamiento respecto de la variable $\tau$;
- visualizar la zona de superposición;
- identificar los límites efectivos de integración;
- relacionar cada posición con el valor de la convolución $y(t)$.

#### Controles

- **Valor de $t$:** desplaza la señal seleccionada.
- **Mover $g$ / Mover $x$:** permite elegir cuál de las dos señales se invierte y desplaza.
- **Reiniciar:** vuelve a la configuración inicial.

La conmutatividad de la convolución garantiza que ambas formas de representación producen el mismo resultado:

$$
x(t)*g(t)=g(t)*x(t).
$$

## Guía 6

### Ejercicios 11, 12 y 13 — DTFT, DFT y agregado de ceros

Archivo: [`DFT_interactiva_ceros.py`](./DFT_interactiva_ceros.py)

La GUI representa la señal $x[n]=3\delta[n]+2\delta[n-1]+3\delta[n-2]$ y permite agregar ceros al final para comparar su DTFT con la DFT de $N$ puntos.

```math
X(f)=e^{-j2\pi f}\left[2+6\cos(2\pi f)\right],
\qquad X_N[k]=X\left(\frac{k}{N}\right),
\qquad N=3+\text{cantidad de ceros},\quad \Delta f=\frac{1}{N}.
```

La frecuencia se expresa en ciclos por muestra. Agregar ceros mantiene la DTFT y aumenta la densidad de muestras de la DFT, sin agregar información ni mejorar la resolución determinada por la duración del registro original.

- **Panel izquierdo:** módulo y fase de la DTFT superpuestos con las muestras de la DFT.
- **Panel derecho:** señal temporal, con valores originales y ceros agregados diferenciados por color.
- **Información:** valores de $N$ y $\Delta f$. Los ejes de frecuencia y módulo permanecen fijos.

#### Controles

- **Ceros agregados:** cuadro editable con flechas para aumentar o disminuir la cantidad; comienza en 0.
- **Clic en el espectro:** selecciona la muestra DFT más cercana, marca su frecuencia en ambos paneles y muestra $k$, $f_k$, módulo y fase.

El script utiliza **NumPy**, **Matplotlib** y **Tkinter**.

### Ejercicio 28 — Ecuación en diferencias, retardos y sumadores

Archivo: [`ecuacion_diferencias_interactiva.py`](./ecuacion_diferencias_interactiva.py)

La GUI representa el sistema:

```math
y[n+2]-5y[n+1]+6y[n]=3x[n+1]+5x[n].
```

Para calcular la salida en cada instante se utiliza:

```math
y[n]=3x[n-1]+5x[n-2]+5y[n-1]-6y[n-2].
```

Los retardos $z^{-1}$ se ordenan de arriba hacia abajo. Las ramas directas tienen $b_0=0$, $b_1=3$ y $b_2=5$; la realimentación usa $-a_1=5$ y $-a_2=-6$, con $1/a_0=1$.

La visualización permite:

- identificar las señales retrasadas y los valores guardados en cada memoria;
- distinguir los valores de $x$ en azul y los de $y$ en naranja, con los coeficientes del mismo color;
- seguir los valores sin ponderar en marcadores circulares amarillos centrados en el último tramo que entra a cada sumador;
- observar en negro el resultado de cada sumador, con los coeficientes aplicados;
- consultar el historial de entradas, memorias y salidas en una tabla.

#### Controles

- **Entrada manual:** permite ingresar $x[n]$. Al presionar **Enter** o **Ingresar y avanzar**, calcula la salida y avanza el reloj. El cuadro comienza en 1 y vuelve a 1 después de cada avance manual; la entrada pendiente del diagrama se indica con «?».
- **Entrada automática:** usa $x[n]=(0.5)^n u[n]$ en cada paso confirmado.
- **Volver atrás:** restaura las memorias y la entrada del paso anterior para modificarlo y repetirlo.
- **Condiciones iniciales:** permite elegir condiciones nulas o las del inciso b: $y[-1]=11/6$ y $y[-2]=37/36$. Se toma $x[n]=0$ para $n<0$.
- **Reiniciar con estas condiciones:** borra el historial y vuelve a $n=0$ usando la opción seleccionada.

El diagrama muestra las memorias del próximo instante y mantiene debajo el último cálculo. Como $b_0=0$, es posible conocer $y[n]$ antes de ingresar $x[n]$: la entrada actual comienza a afectar la salida en el instante siguiente.

Los sumadores y marcadores conservan su forma circular al redimensionar la ventana. El script utiliza **Tkinter**.

## Primer parcial — 2.º cuatrimestre de 2026

### Ejercicio 1a — Diagrama de Bode interactivo

Archivo: [`bode_ejercicio_1a.py`](./bode_ejercicio_1a.py)

El script representa el módulo y la fase del filtro pasabanda utilizado en el acondicionamiento de un electromiógrafo:

```math
H(s)=\frac{s}{s+\omega_1}\,
\frac{\omega_2^2}{s^2+2\xi\omega_2s+\omega_2^2},
\qquad
\omega_1=2\pi\cdot10\text{ rad/s},\quad
\omega_2=2\pi\cdot500\text{ rad/s},\quad
\xi=0{,}4.
```

La visualización tiene dos paneles con un eje común de frecuencia en Hz y escala logarítmica:

- **Módulo:** superpone la respuesta exacta en dB y su aproximación asintótica, indicando las pendientes de cada tramo.
- **Fase:** muestra el argumento de la respuesta en frecuencia, expresado en grados.

El módulo asintótico se construye sumando las contribuciones en decibeles del pasaaltos de primer orden y del pasabajos de segundo orden:

```math
20\log_{10}|H(i2\pi f)|\approx
\begin{cases}
20\log_{10}(f/10), & 0<f<10,\\
0, & 10\leq f\leq500,\\
-40\log_{10}(f/500), & f>500.
\end{cases}
```

Las pendientes son **+20 dB/década**, **0 dB/década** y **−40 dB/década**, respectivamente.

#### Controles

- **Frecuencia [Hz]:** permite ingresar una frecuencia entre 0,1 y 10 000 Hz. Al presionar **Enter**, se actualizan las líneas verticales y los puntos de ambos paneles.
- **Etiqueta de módulo:** informa el valor exacto en dB, la ganancia lineal y el valor asintótico.
- **Etiqueta de fase:** informa el ángulo en grados y radianes.

El cuadro admite punto o coma decimal y comienza en 120 Hz. Los valores se calculan directamente a partir de la transferencia, sin aproximarlos al punto más cercano de la grilla. Permite explorar también las componentes de 120 y 2000 Hz del inciso 1b.

### Ejercicio 3b — Convolución con una exponencial y una delta retrasada

Archivo: [`convolucion_ejercicio_3b_gui.py`](./convolucion_ejercicio_3b_gui.py)

La GUI representa la salida de un sistema LTI cuya respuesta impulsiva es:

```math
h(t)=e^{-3t}u(t)+2\delta(t-1),
```

ante el pulso rectangular:

```math
x(t)=\Pi\left(\frac{t-2}{4}\right)=u(t)-u(t-4).
```

El pulso tiene altura 1, centro en 2 s y ancho de 4 s. Por linealidad, la convolución se separa en dos contribuciones:

```math
y(t)=(x*h)(t)=y_e(t)+y_\delta(t),
\qquad
y_\delta(t)=2x(t-1).
```

La parte exponencial es:

```math
y_e(t)=
\begin{cases}
0, & t<0,\\
\dfrac{1-e^{-3t}}{3}, & 0\leq t<4,\\
\dfrac{1-e^{-12}}{3}e^{-3(t-4)}, & t\geq4.
\end{cases}
```

La contribución de la delta es una copia de la entrada, retrasada 1 s y multiplicada por 2. La salida total presenta saltos de +2 en $t=1$ y de −2 en $t=5$; en $t=4$ es continua y comienza a decaer la parte exponencial.

La visualización tiene dos paneles:

- **Superposición:** muestra una señal fija y la otra invertida y desplazada, el área del producto de las partes regulares y la delta como una flecha simbólica de peso 2.
- **Resultado:** compara la contribución exponencial, la contribución de la delta y la suma total; un cursor indica el instante seleccionado.

El texto lateral muestra los soportes, los límites efectivos de integración y el valor de cada contribución. La delta se evalúa mediante su propiedad de selección, sin aproximarla por un pico numérico.

#### Controles

- **Tiempo $t$:** deslizador entre −1 y 7 s, con pasos de 0,01 s.
- **Cuadro $t$ [s]:** permite ingresar un instante y confirmar con **Enter**, usando punto o coma decimal.
- **Mover $h$ / Mover $x$:** permite elegir qué señal se invierte y desplaza. Ambas opciones producen la misma salida por conmutatividad.
- **Animar / Pausar:** recorre automáticamente el intervalo temporal o detiene el recorrido.
- **Reiniciar:** detiene la animación y vuelve a $t=-1$ s.

La GUI adopta $\Pi(\pm1/2)=1/2$, equivalente a $u(0)=1/2$. Por eso, exactamente en $t=1$ y $t=5$, la contribución de la delta vale 1. Se distinguen esos valores puntuales de los límites laterales mediante marcadores.

Ambos scripts utilizan **NumPy** y **Matplotlib**.

## Trabajo práctico 1

### Ejercicio 1
Archivo: [`ClaseTP1.ipynb`](./ClaseTP1.ipynb)

#### Creación de arreglos temporales
Vemos el uso de las funciones np.linspace() y np.arange().

#### Configuración de gráficos
Vemos cómo podemos configurar los distintos parámetros de un plot de matplotlib, tales como:
- Títulos
- Colores
- Grosor de líneas
- Estilo de líneas
- Etiquetas
- Anotaciones
- Superposición de gráficos

### Ejercicio 2

Vemos cómo cargar un archivo .mat (formato de tabla de Matlab) almacenado de forma local. En este caso usamos como ejemplo ECGPCG0001.mat, pero podría ser otro. En mi computadora el archivo se encuentra en la ruta "D:\SyS\TPs\ECGPCG0001.mat", pero deberían cambiarlo para poder ejecutarlo sin errores.



### Ejercicio 3

Simulamos el muestreo de una señal usando la función plt.stem().

### Ejercicio 4

- Generamos 6 señales senoidales con distintas frecuencias y mostramos cómo hacer un subplot con plt.subplots().
- Definimos un sistema pasaaltos de primer orden $H(s)=\frac{s}{s+2}$.
- Generamos su función de transferencia usando sg.TransferFunction().
- Generamos su diagrama de polos y ceros usando ct.pzmap(ct.tf(num,den)).
- Aplicamos este filtro a las señales previamente generadas usando sg.lsim().
- Graficamos su módulo y fase. Para ello generamos primero un eje horizontal con escala logarítmica para las frecuencias angulares. Calculamos su módulo en decibeles y su fase.

Para poder visualizarlo correctamente, en la misma carpeta del script deben tener los archivos colorpython.png y linestyles.png.


