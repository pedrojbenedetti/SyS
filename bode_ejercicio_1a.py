"""Bode del ejercicio 1a: módulo exacto/asintótico y fase exacta en grados.

Dependencias: numpy y matplotlib.
Las frecuencias del eje se expresan en Hz; H(s) usa rad/s.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox


# Parámetros del enunciado
F1 = 10.0       # Hz: quiebre del pasaaltos
F2 = 500.0      # Hz: frecuencia natural del pasabajos
XI = 0.4       # amortiguamiento
F_MIN = 0.1     # Hz
F_MAX = 10000.0 # Hz


def graficar_bode():
    """Construye la figura y la devuelve para permitir guardarla."""
    if not (0 < F_MIN < F1 < F2 < F_MAX and XI > 0):
        raise ValueError("Se requiere 0 < F_MIN < F1 < F2 < F_MAX y XI > 0.")

    f = np.sort(np.unique(np.r_[np.logspace(np.log10(F_MIN),
                                             np.log10(F_MAX), 3000), F1, F2]))
    w1, w2 = 2 * np.pi * F1, 2 * np.pi * F2
    s = 1j * 2 * np.pi * f

    h1 = s / (s + w1)
    h2 = w2**2 / (s**2 + 2 * XI * w2 * s + w2**2)
    h = h1 * h2

    # En decibeles, el producto de los módulos se convierte en suma.
    db_total = 20 * np.log10(np.abs(h))
    asintota1 = np.where(f < F1, 20 * np.log10(f / F1), 0.0)
    asintota2 = np.where(f > F2, -40 * np.log10(f / F2), 0.0)
    asintota_total = asintota1 + asintota2

    # angle calcula el argumento; unwrap evita saltos artificiales de 360 grados.
    fase = np.degrees(np.unwrap(np.angle(h)))

    fig, axes = plt.subplots(2, 1, figsize=(11, 8),
                             sharex=True)
    fig.subplots_adjust(left=0.09, right=0.97, top=0.93, bottom=0.22, hspace=0.26)
    ax = axes[0]
    ax.semilogx(f, db_total, color="tab:blue", lw=2.3, label="Módulo exacto")
    ax.semilogx(f, asintota_total, color="tab:orange", ls="--", lw=2.3,
                label="Módulo asintótico")
    ax.plot([F1, F2], [0, 0], "o", color="tab:orange", ms=5)
    ax.set_title("Ejercicio 1a · Bode de módulo del filtro pasabanda", fontsize=14)
    ax.set_ylim(min(asintota_total.min(), db_total.min()) - 5,
                max(9, db_total.max() + 5))

    for posicion, texto in [(np.sqrt(F_MIN * F1), "+20 dB/década"),
                             (np.sqrt(F1 * F2), "0 dB/década"),
                             (np.sqrt(F2 * F_MAX), "−40 dB/década")]:
        valor = np.interp(np.log10(posicion), np.log10(f), asintota_total)
        ax.annotate(texto, (posicion, valor), xytext=(0, 18),
                    textcoords="offset points", ha="center", fontsize=10,
                    bbox=dict(facecolor="white", edgecolor="none", alpha=0.85))

    ax.set_ylabel("Módulo [dB]")
    ax_fase = axes[1]
    ax_fase.semilogx(f, fase, color="tab:purple", lw=2.3, label="Fase exacta")
    ax_fase.set_title("Fase del filtro")
    ax_fase.set_ylabel("Fase [grados]")
    ax_fase.set_ylim(-190, 100)
    ax_fase.set_yticks(np.arange(-180, 91, 45))

    for eje in axes:
        eje.axhline(0, color="gray", lw=0.7, zorder=0)
        for fc in (F1, F2):
            eje.axvline(fc, color="gray", ls=":", lw=1)
        eje.set_xlim(F_MIN, F_MAX)
        eje.grid(True, which="major", alpha=0.3)
        eje.grid(True, which="minor", alpha=0.12)
        eje.legend(loc="lower left", fontsize=9)

    axes[-1].set_xlabel("Frecuencia f [Hz] · escala logarítmica")
    ticks = np.unique(np.r_[10.0 ** np.arange(np.ceil(np.log10(F_MIN)),
                                              np.floor(np.log10(F_MAX)) + 1), F1, F2])
    axes[-1].set_xticks(ticks)
    axes[-1].set_xticklabels([f"{valor:g}" for valor in ticks])

    # Una misma frecuencia seleccionada en los dos paneles.
    seleccion = [eje.axvline(F1, color="crimson", lw=1.4, ls="-.") for eje in axes]
    punto_modulo, = ax.plot([], [], "o", color="tab:blue", ms=7, zorder=6)
    punto_asintota, = ax.plot([], [], "s", color="tab:orange", ms=6, zorder=6)
    punto_fase, = ax_fase.plot([], [], "o", color="tab:purple", ms=7, zorder=6)
    estilo = dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor="crimson", alpha=0.95)
    etiqueta_modulo = ax.text(0.02, 0.97, "", transform=ax.transAxes,
                             va="top", fontsize=9, bbox=estilo, zorder=10)
    etiqueta_fase = ax_fase.text(0.98, 0.97, "", transform=ax_fase.transAxes,
                               ha="right", va="top", fontsize=10, bbox=estilo, zorder=10)

    entrada_ax = fig.add_axes([0.22, 0.105, 0.18, 0.045])
    entrada = TextBox(entrada_ax, "Frecuencia [Hz]: ", initial="120")
    estado = fig.text(0.44, 0.12, "", fontsize=9, va="center")

    def actualizar(texto):
        try:
            frecuencia = float(texto.strip().replace(",", "."))
            if not np.isfinite(frecuencia) or not F_MIN <= frecuencia <= F_MAX:
                raise ValueError
        except ValueError:
            estado.set_text(f"Ingresá un número entre {F_MIN:g} y {F_MAX:g} Hz.")
            estado.set_color("crimson")
            fig.canvas.draw_idle()
            return

        # Evaluación directa: no se aproxima al punto más cercano de la grilla.
        ss = 1j * 2 * np.pi * frecuencia
        hh = ss / (ss + w1) * w2**2 / (ss**2 + 2 * XI * w2 * ss + w2**2)
        modulo = abs(hh)
        modulo_db = 20 * np.log10(modulo)
        asintotico_db = (20 * np.log10(frecuencia / F1) if frecuencia < F1 else 0.0)
        asintotico_db += (-40 * np.log10(frecuencia / F2) if frecuencia > F2 else 0.0)
        fase_rad = np.angle(hh)
        fase_grados = np.degrees(fase_rad)

        for linea in seleccion:
            linea.set_xdata([frecuencia, frecuencia])
        punto_modulo.set_data([frecuencia], [modulo_db])
        punto_asintota.set_data([frecuencia], [asintotico_db])
        punto_fase.set_data([frecuencia], [fase_grados])
        etiqueta_modulo.set_text(
            f"f = {frecuencia:g} Hz\n"
            f"Exacto: {modulo_db:.3f} dB   |H| = {modulo:.5f}\n"
            f"Asintótico: {asintotico_db:.3f} dB")
        etiqueta_fase.set_text(
            f"f = {frecuencia:g} Hz\n"
            f"Fase: {fase_grados:.3f}°  ({fase_rad:.5f} rad)")
        estado.set_text("Presioná Enter para actualizar.")
        estado.set_color("0.3")
        fig.canvas.draw_idle()

    entrada.on_submit(actualizar)
    # Mantener la referencia al widget permite que siga respondiendo.
    fig.entrada_frecuencia = entrada
    actualizar(entrada.text)
    return fig


if __name__ == "__main__":
    figura = graficar_bode()
    # Para exportar la figura, descomentá esta línea:
    # figura.savefig("bode_ejercicio_1a.png", dpi=200, bbox_inches="tight")
    plt.show()
