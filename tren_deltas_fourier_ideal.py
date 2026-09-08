"""GUI didáctica: transformada de Fourier ideal de un tren de deltas.

Usamos la convención de transformada con frecuencia f medida en Hz:

    X(f) = integral x(t) * exp(-j*2*pi*f*t) dt

Con esta convención, el par de transformadas es:

    sum_k delta(t - k*T0)
        <---- Fourier ---->
    (1/T0) * sum_n delta(f - n/T0)

Las deltas se representan con flechas. No son pulsos de altura finita: la
altura de cada flecha indica su PESO (el coeficiente que multiplica a delta).

Dependencias:
    pip install numpy matplotlib

Ejecución:
    python tren_deltas_fourier_ideal.py
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider


# ---------------------------------------------------------------------------
# Parámetros de la visualización
# ---------------------------------------------------------------------------
T0_INICIAL = 1.0
LIMITE_TIEMPO = 6.0       # Se muestra el intervalo [-6, 6] segundos.
LIMITE_FRECUENCIA = 6.0   # Se muestra el intervalo [-6, 6] Hz.


def posiciones_del_tren(separacion, limite):
    """Devuelve los múltiplos de 'separacion' visibles en [-limite, limite].

    El pequeño margen numérico evita perder una delta que se encuentre
    exactamente sobre el borde del gráfico.
    """
    indice_maximo = int(np.floor(limite / separacion + 1e-12))
    indices = np.arange(-indice_maximo, indice_maximo + 1)
    return indices * separacion


def dibujar_deltas(ax, posiciones, peso, color):
    """Representa deltas ideales mediante flechas verticales.

    Una delta de Dirac no tiene una altura ordinaria. Por eso cada flecha debe
    interpretarse simbólicamente: su extremo marca el PESO de la delta.
    """
    for posicion in posiciones:
        ax.annotate(
            "",
            xy=(posicion, peso),
            xytext=(posicion, 0),
            arrowprops={
                "arrowstyle": "-|>",
                "color": color,
                "linewidth": 1.8,
                "mutation_scale": 11,
                "shrinkA": 0,
                "shrinkB": 0,
            },
        )


def configurar_eje(ax, titulo, etiqueta_x):
    """Configura el formato común de los dos gráficos."""
    ax.set_title(titulo, fontsize=13)
    ax.set_xlabel(etiqueta_x)
    ax.set_ylabel("Peso de la delta")
    ax.axhline(0, color="0.25", linewidth=0.9)
    ax.axvline(0, color="0.55", linewidth=0.8)
    ax.grid(True, axis="x", alpha=0.25)


def indicar_separacion(ax, separacion, altura, texto, color):
    """Dibuja una flecha horizontal entre las deltas ubicadas en 0 y separacion."""
    ax.annotate(
        "",
        xy=(separacion, altura),
        xytext=(0, altura),
        arrowprops={"arrowstyle": "<->", "color": color, "linewidth": 1.5},
    )
    ax.text(
        separacion / 2,
        altura * 1.04,
        texto,
        color=color,
        ha="center",
        va="bottom",
        fontsize=11,
    )


# ---------------------------------------------------------------------------
# Creación de la ventana
# ---------------------------------------------------------------------------
fig, (ax_tiempo, ax_frecuencia) = plt.subplots(2, 1, figsize=(12.5, 7.5))

# Dejamos espacio a la derecha para las ecuaciones y abajo para los controles.
plt.subplots_adjust(left=0.09, right=0.76, top=0.88, bottom=0.20, hspace=0.52)
fig.suptitle("Transformada de Fourier ideal de un tren de deltas", fontsize=16)


# La caja lateral se actualiza junto con el slider.
texto_resultado = fig.text(
    0.79,
    0.81,
    "",
    va="top",
    fontsize=11,
    bbox={"boxstyle": "round,pad=0.5", "facecolor": "whitesmoke", "alpha": 0.95},
)

# Mensaje conceptual permanente.
fig.text(
    0.79,
    0.42,
    "Relación inversa:\n\n"
    r"$T_0\uparrow\ \Rightarrow\ F_0\downarrow$" "\n\n"
    r"$T_0\downarrow\ \Rightarrow\ F_0\uparrow$" "\n\n"
    "Las flechas representan\ndeltas ideales; su altura\nindica el peso.",
    fontsize=11,
    va="top",
)


# ---------------------------------------------------------------------------
# Controles interactivos
# ---------------------------------------------------------------------------
ax_slider = fig.add_axes([0.14, 0.09, 0.48, 0.035])
slider_T0 = Slider(
    ax=ax_slider,
    # La explicación completa aparece en el gráfico; una etiqueta breve evita
    # que el texto quede recortado en ventanas angostas.
    label=r"$T_0$ [s]",
    valmin=0.25,
    valmax=2.5,
    valinit=T0_INICIAL,
    valstep=0.05,
)

ax_boton = fig.add_axes([0.65, 0.075, 0.10, 0.065])
boton_reiniciar = Button(ax_boton, "Reiniciar")


def actualizar(_=None):
    """Actualiza los dos trenes ideales cuando cambia T0."""
    T0 = slider_T0.val

    # La separación fundamental en frecuencia es la inversa de T0.
    F0 = 1.0 / T0

    # En tiempo, las deltas están en t = k*T0 y todas tienen peso 1.
    posiciones_t = posiciones_del_tren(T0, LIMITE_TIEMPO)
    peso_t = 1.0

    # En frecuencia, están en f = n/T0 = n*F0 y tienen peso 1/T0.
    posiciones_f = posiciones_del_tren(F0, LIMITE_FRECUENCIA)
    peso_f = 1.0 / T0

    # Limpiamos y reconstruimos los ejes. Esto simplifica la actualización del
    # número de deltas visibles, que cambia al mover el slider.
    ax_tiempo.clear()
    ax_frecuencia.clear()

    configurar_eje(
        ax_tiempo,
        r"Tiempo: $\widetilde{\delta}_{T_0}(t)=\sum_k\delta(t-kT_0)$",
        r"$t$ [s]",
    )
    configurar_eje(
        ax_frecuencia,
        r"Frecuencia: $X(f)=\dfrac{1}{T_0}\sum_n\delta(f-n/T_0)$",
        r"$f$ [Hz]",
    )

    dibujar_deltas(ax_tiempo, posiciones_t, peso_t, color="tab:blue")
    dibujar_deltas(ax_frecuencia, posiciones_f, peso_f, color="tab:purple")

    ax_tiempo.set_xlim(-LIMITE_TIEMPO, LIMITE_TIEMPO)
    ax_frecuencia.set_xlim(-LIMITE_FRECUENCIA, LIMITE_FRECUENCIA)
    ax_tiempo.set_ylim(-0.12, 1.38)
    ax_frecuencia.set_ylim(-0.12 * max(peso_f, 1), 1.38 * max(peso_f, 1))

    # Indicamos visualmente un período en cada dominio siempre que la segunda
    # delta se encuentre dentro del rango mostrado.
    if T0 <= LIMITE_TIEMPO:
        indicar_separacion(
            ax_tiempo,
            T0,
            altura=1.18,
            texto=rf"$T_0={T0:.2f}$ s",
            color="tab:blue",
        )

    if F0 <= LIMITE_FRECUENCIA:
        altura_flecha = 1.18 * peso_f
        indicar_separacion(
            ax_frecuencia,
            F0,
            altura=altura_flecha,
            texto=rf"$F_0=1/T_0={F0:.2f}$ Hz",
            color="tab:purple",
        )

    # La caja conecta el gráfico con el resultado analítico.
    texto_resultado.set_text(
        rf"$T_0={T0:.2f}$ s" "\n"
        rf"$F_0=\dfrac{{1}}{{T_0}}={F0:.2f}$ Hz" "\n\n"
        "En tiempo:" "\n"
        rf"$t=k\,({T0:.2f})$" "\n"
        r"peso $=1$" "\n\n"
        "En frecuencia:" "\n"
        rf"$f=n\,({F0:.2f})$" "\n"
        rf"peso $=\dfrac{{1}}{{T_0}}={peso_f:.2f}$"
    )

    # draw_idle evita redibujados innecesarios mientras se mueve el slider.
    fig.canvas.draw_idle()


def reiniciar(_event):
    """Recupera el caso sencillo T0=1 s."""
    slider_T0.reset()


# Conectamos el slider y el botón con sus respectivas funciones.
slider_T0.on_changed(actualizar)
boton_reiniciar.on_clicked(reiniciar)

# Dibujamos el estado inicial antes de abrir la ventana.
actualizar()


if __name__ == "__main__":
    plt.show()
