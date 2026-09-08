"""Visualización didáctica de una convolución continua por definición.

Se estudian las señales

    x(t) = 1,       -1 <= t <= 1
    g(t) = t / 3,    0 <= t <= 3

El control deslizante cambia el parámetro t. Los botones permiten elegir si
se deja fija x(tau) y se mueve g(t-tau), o si se deja fija g(tau) y se mueve
x(t-tau). En ambos casos se obtiene la misma convolución.

Requisitos:
    pip install numpy matplotlib

Ejecución:
    python convolucion_interactiva.py
"""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons, Slider


# Colores constantes: cada señal conserva su color aun cuando se transforma.
COLOR_X = "#1565C0"
COLOR_G = "#EF6C00"
COLOR_PRODUCTO = "#2E7D32"
COLOR_LIMITES = "#C62828"
COLOR_CONVOLUCION = "#6A1B9A"


def x(s: np.ndarray) -> np.ndarray:
    """Pulso rectangular unitario con soporte [-1, 1]."""
    return np.where((-1.0 <= s) & (s <= 1.0), 1.0, 0.0)


def g(s: np.ndarray) -> np.ndarray:
    """Rampa truncada g(s)=s/3 con soporte [0, 3]."""
    return np.where((0.0 <= s) & (s <= 3.0), s / 3.0, 0.0)


def limites_efectivos(t: float, mover: str) -> tuple[float, float]:
    """Devuelve la intersección de los soportes para la opción elegida."""
    if mover == "g":
        # [-1, 1] intersección [t-3, t]
        return max(-1.0, t - 3.0), min(1.0, t)

    # [0, 3] intersección [t-1, t+1]
    return max(0.0, t - 1.0), min(3.0, t + 1.0)


def convolucion_exacta(t: np.ndarray | float) -> np.ndarray | float:
    """Resultado analítico de (x*g)(t)."""
    valores = np.asarray(t, dtype=float)
    resultado = np.zeros_like(valores)

    tramo_1 = (-1.0 < valores) & (valores < 1.0)
    tramo_2 = (1.0 <= valores) & (valores <= 2.0)
    tramo_3 = (2.0 < valores) & (valores < 4.0)

    resultado[tramo_1] = (valores[tramo_1] + 1.0) ** 2 / 6.0
    resultado[tramo_2] = 2.0 * valores[tramo_2] / 3.0
    resultado[tramo_3] = (
        -valores[tramo_3] ** 2 + 2.0 * valores[tramo_3] + 8.0
    ) / 6.0

    if np.isscalar(t):
        return float(resultado)
    return resultado


def formato_numero(valor: float) -> str:
    """Formato corto para los límites y el valor de la integral."""
    if np.isclose(valor, round(valor), atol=1e-9):
        return str(int(round(valor)))
    return f"{valor:.2f}"


def configurar_ejes(ax: plt.Axes, xlim: tuple[float, float]) -> None:
    """Agrega ejes cartesianos, grilla y límites comunes."""
    ax.axhline(0, color="0.2", linewidth=0.9)
    ax.axvline(0, color="0.2", linewidth=0.9)
    ax.set_xlim(*xlim)
    ax.grid(alpha=0.18)


def main() -> None:
    tau = np.linspace(-5.5, 6.5, 6001)
    t_convolucion = np.linspace(-2.0, 5.0, 1401)
    y_convolucion = convolucion_exacta(t_convolucion)

    figura = plt.figure(figsize=(14, 6.5))
    rejilla = figura.add_gridspec(
        2,
        left=0.07,
        right=0.97,
        bottom=0.25,
        top=0.87,
        hspace=0.46,
    )

    ax_superposicion = figura.add_subplot(rejilla[0])
    ax_resultado = figura.add_subplot(rejilla[1])

    figura.suptitle("Convolución continua por definición", fontsize=17, weight="bold")

    # Panel 4: resultado completo; el punto rojo sigue al slider.
    ax_resultado.plot(
        t_convolucion,
        y_convolucion,
        color=COLOR_CONVOLUCION,
        linewidth=2.7,
        label=r"$y(t)=(x*g)(t)$",
    )
    tramo_recorrido, = ax_resultado.plot([], [], color=COLOR_CONVOLUCION, linewidth=5, alpha=0.25)
    punto_actual, = ax_resultado.plot([], [], "o", color=COLOR_LIMITES, markersize=8, zorder=5)
    linea_t = ax_resultado.axvline(-2.0, color=COLOR_LIMITES, linestyle="--", linewidth=1.4)
    texto_resultado = ax_resultado.text(
        0.03,
        0.95,
        "",
        transform=ax_resultado.transAxes,
        va="top",
        fontsize=11,
        bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor="0.75", alpha=0.95),
    )
    ax_resultado.set_title("4. Resultado de la convolución")
    ax_resultado.set_xlabel(r"$t$")
    ax_resultado.set_ylabel(r"$y(t)$")
    ax_resultado.set_ylim(-0.08, 1.55)
    configurar_ejes(ax_resultado, (-2.0, 5.0))
    ax_resultado.legend(loc="upper right")

    # Controles.
    ax_slider = figura.add_axes((0.39, 0.12, 0.48, 0.04))
    slider_t = Slider(
        ax=ax_slider,
        label=r"Valor de $t$",
        valmin=-2.0,
        valmax=5.0,
        valinit=-2.0,
        valstep=0.01,
        color=COLOR_CONVOLUCION,
    )

    ax_selector = figura.add_axes((0.075, 0.045, 0.23, 0.125), facecolor="#F5F5F5")
    selector = RadioButtons(
        ax_selector,
        (r"Mover $g$:  $g(t-\tau)$", r"Mover $x$:  $x(t-\tau)$"),
        active=0,
        activecolor=COLOR_CONVOLUCION,
    )
    ax_selector.set_title("Elegir la señal móvil", fontsize=10, pad=5)

    ax_reiniciar = figura.add_axes((0.89, 0.045, 0.075, 0.043))
    boton_reiniciar = Button(ax_reiniciar, "Reiniciar", hovercolor="#E0E0E0")

    estado = {"mover": "g"}

    def actualizar(_: float | str | None = None) -> None:
        t_actual = float(slider_t.val)
        mover = estado["mover"]
        limite_inferior, limite_superior = limites_efectivos(t_actual, mover)
        hay_superposicion = limite_inferior < limite_superior
        valor_y = convolucion_exacta(t_actual)

        ax_superposicion.clear()

        if mover == "g":
            fija = x(tau)
            movil = g(t_actual - tau)
            producto = fija * movil
            etiqueta_fija = r"$x(\tau)$ fija"
            etiqueta_movil = r"$g(t-\tau)$ móvil"
            color_fija = COLOR_X
            color_movil = COLOR_G
            descripcion_soportes = (
                "Señal fija: " + r"$x(\tau),\quad \tau\in[-1,1]$" + "\n"
                + "Señal móvil: " + r"$g(t-\tau),\quad \tau\in[t-3,t]$"
            )
        else:
            fija = g(tau)
            movil = x(t_actual - tau)
            producto = fija * movil
            etiqueta_fija = r"$g(\tau)$ fija"
            etiqueta_movil = r"$x(t-\tau)$ móvil"
            color_fija = COLOR_G
            color_movil = COLOR_X
            descripcion_soportes = (
                "Señal fija: " + r"$g(\tau),\quad \tau\in[0,3]$" + "\n"
                + "Señal móvil: " + r"$x(t-\tau),\quad \tau\in[t-1,t+1]$"
            )

        # Panel 2: señal fija, señal invertida/desplazada y zona común.
        ax_superposicion.plot(tau, fija, color=color_fija, linewidth=2.5, label=etiqueta_fija)
        ax_superposicion.plot(
            tau,
            movil,
            color=color_movil,
            linewidth=2.5,
            linestyle="--",
            label=etiqueta_movil,
        )
        ax_superposicion.fill_between(
            tau,
            0,
            producto,
            where=producto > 0,
            color=COLOR_PRODUCTO,
            alpha=0.30,
            label="Zona de superposición",
        )
        ax_superposicion.text(
            0.02,
            0.96,
            descripcion_soportes,
            transform=ax_superposicion.transAxes,
            va="top",
            fontsize=10,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="0.8", alpha=0.92),
        )

        if hay_superposicion:
            ax_superposicion.axvline(
                limite_inferior,
                color=COLOR_LIMITES,
                linestyle=":",
                linewidth=1.8,
            )
            ax_superposicion.axvline(
                limite_superior,
                color=COLOR_LIMITES,
                linestyle=":",
                linewidth=1.8,
            )

            a_texto = formato_numero(limite_inferior)
            b_texto = formato_numero(limite_superior)
            intervalo = "Superposición: " + rf"$\tau\in[{a_texto},{b_texto}]$"

            if mover == "g":
                definicion = (
                    r"$y(t)=\int_{\tau_{\mathrm{min}}}^{\tau_{\mathrm{max}}}"
                    r"x(\tau)\,g(t-\tau)\,d\tau$"
                )
                evaluacion = (
                    rf"$y({t_actual:.2f})="
                    rf"\int_{{{a_texto}}}^{{{b_texto}}}"
                    rf"\frac{{{t_actual:.2f}-\tau}}{{3}}\,d\tau"
                    rf"={valor_y:.4f}$"
                )
            else:
                definicion = (
                    r"$y(t)=\int_{\tau_{\mathrm{min}}}^{\tau_{\mathrm{max}}}"
                    r"g(\tau)\,x(t-\tau)\,d\tau$"
                )
                evaluacion = (
                    rf"$y({t_actual:.2f})="
                    rf"\int_{{{a_texto}}}^{{{b_texto}}}"
                    r"\frac{\tau}{3}\,d\tau"
                    rf"={valor_y:.4f}$"
                )

            texto_integral = intervalo + "\n" + definicion + "\n" + evaluacion
        else:
            texto_integral = (
                "Superposición: " + r"$\varnothing$" + "\n"
                + rf"$y({t_actual:.2f})=0$"
            )

        ax_superposicion.text(
            0.02,
            0.03,
            texto_integral,
            transform=ax_superposicion.transAxes,
            va="bottom",
            fontsize=10.5,
            bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor="0.75", alpha=0.95),
        )

        ax_superposicion.set_title(rf"2. Inversión y desplazamiento para $t={t_actual:.2f}$")
        ax_superposicion.set_xlabel(r"$\tau$")
        ax_superposicion.set_ylabel("Amplitud")
        ax_superposicion.set_ylim(-0.08, 1.25)
        configurar_ejes(ax_superposicion, (-5.5, 6.5))
        ax_superposicion.legend(loc="upper right", fontsize=9)

        mascara_recorrida = t_convolucion <= t_actual
        tramo_recorrido.set_data(
            t_convolucion[mascara_recorrida],
            y_convolucion[mascara_recorrida],
        )
        punto_actual.set_data([t_actual], [valor_y])
        linea_t.set_xdata([t_actual, t_actual])
        texto_resultado.set_text(rf"$t={t_actual:.2f}$" + "\n" + rf"$y(t)={valor_y:.4f}$")

        figura.canvas.draw_idle()

    def cambiar_senal_movil(etiqueta: str) -> None:
        estado["mover"] = "g" if "Mover $g$" in etiqueta else "x"
        actualizar()

    def reiniciar(_: object) -> None:
        selector.set_active(0)
        slider_t.reset()

    slider_t.on_changed(actualizar)
    selector.on_clicked(cambiar_senal_movil)
    boton_reiniciar.on_clicked(reiniciar)

    actualizar()
    plt.show()


if __name__ == "__main__":
    main()
