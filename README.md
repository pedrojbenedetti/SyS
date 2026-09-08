# Señales y Sistemas

Repositorio de scripts, visualizaciones y recursos interactivos para acompañar las guías de ejercicios de la materia **16.68 - Señales y Sistemas** del **ITBA**.

El objetivo es facilitar la interpretación gráfica de los conceptos teóricos y complementar la resolución analítica de los ejercicios.

Consultas: pbenedetti@itba.edu.ar

## Contenido
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

Para ejecutar el script:

```bash
python tren_deltas_fourier_ideal.py
```

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

Las dependencias pueden instalarse con:

```bash
python -m pip install numpy matplotlib
```

## Ejecución

Descargar o clonar el repositorio y ejecutar:

```bash
python convolucion_interactiva.py
```

## Controles

- **Valor de $t$:** desplaza la señal seleccionada.
- **Mover $g$ / Mover $x$:** permite elegir cuál de las señales se invierte y desplaza.
- **Reiniciar:** vuelve a la configuración inicial.

La conmutatividad de la convolución garantiza que ambas formas de representación producen el mismo resultado:

$$
x(t)*g(t)=g(t)*x(t).
$$
