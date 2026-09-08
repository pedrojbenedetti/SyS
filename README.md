# Señales y Sistemas

Repositorio de scripts, visualizaciones y recursos interactivos para acompañar las guías de ejercicios de la materia **16.68 - Señales y Sistemas** del **ITBA**.

El objetivo es facilitar la interpretación gráfica de los conceptos teóricos y complementar la resolución analítica de los ejercicios.

## Contenido

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
