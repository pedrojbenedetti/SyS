# Señales y Sistemas

Repositorio de scripts, visualizaciones y recursos interactivos para acompañar las guías de ejercicios de la materia **16.68 - Señales y Sistemas** del **ITBA**.

El objetivo es facilitar la interpretación gráfica de los conceptos teóricos y complementar la resolución analítica de los ejercicios.

Consultas: pbenedetti@itba.edu.ar

## Contenido

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
* comparar las tres señales sobre un mismo eje temporal.


El producto conserva la senoide únicamente dentro del intervalo $0\leq t\leq 1$ y la anula fuera de él.

### Guía 2 — Ejercicio 8: frecuencias fundamentales

Archivo: [`frecuencias_fundamentales.py`](./frecuencias_fundamentales.py)

El script representa las señales de los apartados **b**, **d** y **f** para facilitar el análisis de su periodicidad y la determinación de sus frecuencias fundamentales.

#### b)

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

#### d)

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

#### f)

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


### Guía 2 — Ejercicio 15: transformada de Fourier de un tren de deltas

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
* **Reiniciar:** vuelve a la configuración inicial, con $T_0$=1.

La relación fundamental mostrada por el programa es:

```math
\widetilde{\delta}_{T_0}(t)
\longleftrightarrow
\frac{1}{T_0}\widetilde{\delta}_{1/T_0}(f)
```

Por lo tanto, al aumentar la separación entre las deltas en el tiempo, disminuye su separación en frecuencia, y viceversa.


### Guía 3 — Ejercicio 2: convolución continua

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
- elegir cuál de las dos señales se mantiene fija;
- observar la inversión y el desplazamiento respecto de la variable $\tau$;
- visualizar la zona de superposición;
- identificar los límites efectivos de integración;
- relacionar cada posición con el valor de la convolución $y(t)$.

## Requisitos

- Python 3.10 o posterior
- NumPy
- Matplotlib


## Controles

- **Valor de $t$:** desplaza la señal seleccionada.
- **Mover $g$ / Mover $x$:** permite elegir cuál de las señales se invierte y desplaza.
- **Reiniciar:** vuelve a la configuración inicial.

La conmutatividad de la convolución garantiza que ambas formas de representación producen el mismo resultado:

$$
x(t)*g(t)=g(t)*x(t).
$$
