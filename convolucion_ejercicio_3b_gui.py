"""Convolución del ejercicio 3b, con dos paneles y controles interactivos.

x(t) = Pi((t-2)/4); h(t) = exp(-3t)u(t) + 2 delta(t-1).
Se adopta Pi(+/-1/2)=1/2. La delta es una flecha simbólica de peso 2;
no se aproxima por un pico numérico ni se integra mediante una grilla.
Dependencias: numpy, matplotlib. Ejecutar el archivo abre la ventana.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, TextBox, RadioButtons, Button

AZUL = '#1565C0'
NARANJA = '#EF6C00'
VERDE = '#2E7D32'
VIOLETA = '#6A1B9A'
ROJO = '#C62828'
T_MIN, T_MAX = -1.0, 7.0


def pulso(t):
    """Pulso entre 0 y 4; valor 1/2 exactamente en sus extremos."""
    t = np.asarray(t, dtype=float)
    valor = np.where((t > 0) & (t < 4), 1.0, 0.0)
    valor = np.where((t == 0) | (t == 4), 0.5, valor)
    return float(valor) if valor.ndim == 0 else valor


def exponencial(t):
    t = np.asarray(t, dtype=float)
    return np.exp(-3 * np.maximum(t, 0)) * (t >= 0)


def y_exponencial(t):
    """Integral exacta, escrita de manera estable para tiempos negativos."""
    t = np.asarray(t, dtype=float)
    valor = -np.expm1(-3 * np.clip(t, 0, 4)) / 3
    valor *= np.exp(-3 * np.maximum(t - 4, 0))
    return float(valor) if valor.ndim == 0 else valor


def y_delta(t):
    return 2 * pulso(np.asarray(t) - 1)


def salida(t):
    return y_exponencial(t) + y_delta(t)


def limites(t, mover_h=True):
    return (0.0, min(4.0, t)) if mover_h else (max(0.0, t - 4), t)


def dibujar_salidas(ax):
    """Evita unir los saltos con segmentos oblicuos ficticios."""
    tiempos = np.linspace(T_MIN, T_MAX, 1601)
    ax.plot(tiempos, y_exponencial(tiempos), color=VERDE, ls='--', lw=1.8,
            label=r'$y_e(t)$: exponencial')
    for k, (a, b, peso) in enumerate([(T_MIN, 1, 0), (1, 5, 2), (5, T_MAX, 0)]):
        tt = np.linspace(a, b, 601)
        ax.plot(tt, np.full_like(tt, peso), color=NARANJA, ls=':', lw=2,
                label=r'$y_\delta(t)=2x(t-1)$' if k == 0 else None)
        ax.plot(tt, y_exponencial(tt) + peso, color=VIOLETA, lw=2.5,
                label=r'$y(t)=y_e(t)+y_\delta(t)$' if k == 0 else None)
    for borde in (1.0, 5.0):
        base = y_exponencial(borde)
        ax.plot([borde, borde], [base, base + 2], ':', color=VIOLETA, alpha=0.45)
        ax.plot([borde, borde], [base, base + 2], 'o', color=VIOLETA, mfc='white', ms=5)
        ax.plot(borde, base + 1, 'o', color=VIOLETA, ms=4)
        ax.plot(borde, 1, 'o', color=NARANJA, ms=4)
    for borde in (0, 1, 4, 5):
        ax.axvline(borde, color='0.65', ls=':', lw=0.8)
    ax.set(xlim=(T_MIN, T_MAX), ylim=(-0.13, 3.05), xlabel='Tiempo t [s]', ylabel='Salida',
           title='2. Salida: área exponencial + contribución de la delta')
    ax.grid(alpha=0.18)
    ax.legend(loc='upper left', fontsize=9, ncol=3)


class ConvolucionGUI:
    def __init__(self):
        self.mover_h = True
        self.animando = False
        self.sincronizando = False
        self.fig = plt.figure(figsize=(14, 8.5))
        self.fig.suptitle('Ejercicio 3b · Convolución continua', fontsize=17, weight='bold', y=0.97)
        self.fig.text(0.5, 0.92,
                      r'$x(t)=\Pi((t-2)/4),\qquad h(t)=e^{-3t}u(t)+2\delta(t-1)$',
                      ha='center', fontsize=14)
        rejilla = self.fig.add_gridspec(2, 1, left=0.065, right=0.73, bottom=0.25,
                                         top=0.85, hspace=0.40)
        self.ax_arriba = self.fig.add_subplot(rejilla[0])
        self.ax_abajo = self.fig.add_subplot(rejilla[1])
        dibujar_salidas(self.ax_abajo)
        self.cursor = self.ax_abajo.axvline(0.5, color=ROJO, ls='--', lw=1.4)
        self.punto, = self.ax_abajo.plot([], [], 'o', color=ROJO, ms=8, zorder=7)
        self.info = self.fig.text(0.76, 0.83, '', va='top', fontsize=11, linespacing=1.65)
        self.fig.text(0.76, 0.285, 'Delta: flecha simbólica de peso 2.\nConvención: Π(±1/2) = 1/2.\nEn t = 1 y t = 5: aporte delta = 1.',
                      fontsize=10, va='top', color='0.3', linespacing=1.5)

        self.slider = Slider(self.fig.add_axes([0.40, 0.145, 0.48, 0.032]),
                             'Tiempo t [s]', T_MIN, T_MAX, valinit=0.5,
                             valstep=0.01, valfmt='%1.2f', color=VIOLETA)
        self.entrada = TextBox(self.fig.add_axes([0.40, 0.075, 0.11, 0.042]), 't [s]: ', initial='0.5')
        self.selector = RadioButtons(self.fig.add_axes([0.065, 0.065, 0.245, 0.11]),
                                     ('Mover h: h(t − τ)', 'Mover x: x(t − τ)'), activecolor=VIOLETA)
        self.boton_play = Button(self.fig.add_axes([0.55, 0.075, 0.10, 0.042]), 'Animar')
        self.boton_reset = Button(self.fig.add_axes([0.68, 0.075, 0.10, 0.042]), 'Reiniciar')
        self.estado = self.fig.text(0.40, 0.035, 'Escribí t y presioná Enter, o mové el deslizador.', fontsize=10)
        self.slider.on_changed(self.actualizar)
        self.entrada.on_submit(self.ingresar_t)
        self.selector.on_clicked(self.cambiar_movil)
        self.boton_play.on_clicked(self.alternar_animacion)
        self.boton_reset.on_clicked(self.reiniciar)
        self.timer = self.fig.canvas.new_timer(interval=60)
        self.timer.add_callback(self.avanzar)
        self.fig.canvas.mpl_connect('close_event', lambda event: self.timer.stop())
        self.actualizar(0.5)

    def actualizar(self, t):
        t = float(t)
        if not self.sincronizando:
            self.sincronizando = True
            self.entrada.set_val(f'{t:.4g}')
            self.sincronizando = False
        ax = self.ax_arriba
        ax.clear()
        # Se agregan los quiebres a la grilla para representar bien los soportes.
        tau = np.unique(np.r_[np.linspace(-5.2, 8, 2401), 0, 4, t, t-4, t-1, 1])
        tau = tau[(tau >= -5.2) & (tau <= 8)]
        if self.mover_h:
            ax.plot([0, 0, 4, 4], [0, 1, 1, 0], color=AZUL, lw=2.2, label=r'$x(\tau)$ fija')
            ax.plot(tau, exponencial(t-tau), color=NARANJA, lw=2, ls='--',
                    label=r'$e^{-3(t-\tau)}u(t-\tau)$')
            posicion_delta = t - 1
            ecuacion = r'$\int_0^{\min(4,t)}e^{-3(t-\tau)}\,d\tau$'
            soportes = 'Pulso fijo: [0, 4]\nExponencial: τ ≤ t\nDelta móvil: τ = t − 1'
        else:
            ax.plot(tau, exponencial(tau), color=NARANJA, lw=2, label=r'$e^{-3\tau}u(\tau)$ fija')
            ax.plot([t-4, t-4, t, t], [0, 1, 1, 0], color=AZUL, lw=2.2, ls='--',
                    label=r'$x(t-\tau)$ móvil')
            posicion_delta = 1
            ecuacion = r'$\int_{\max(0,t-4)}^t e^{-3\tau}\,d\tau$'
            soportes = 'Pulso móvil: [t − 4, t]\nExponencial: τ ≥ 0\nDelta fija: τ = 1'

        a, b = limites(t, self.mover_h)
        if b > a:
            intervalo = np.linspace(a, b, 501)
            integrando = np.exp(-3*(t-intervalo)) if self.mover_h else np.exp(-3*intervalo)
            ax.fill_between(intervalo, 0, integrando, color=VERDE, alpha=0.3,
                            label=r'Área = $y_e(t)$')
            for extremo in (a, b):
                ax.axvline(extremo, color=VERDE, ls=':', lw=1)
        ax.annotate('', xy=(posicion_delta, 1.4), xytext=(posicion_delta, 0),
                    arrowprops=dict(arrowstyle='->', color=NARANJA, lw=2.3))
        ax.annotate('δ: peso 2', (posicion_delta, 1.4), xytext=(5, 0),
                    textcoords='offset points', color=NARANJA, fontsize=10)
        ax.axhline(0, color='0.3', lw=0.7)
        ax.set(xlim=(-5.2, 8), ylim=(-0.08, 1.65), xlabel=r'Variable de integración $\tau$ [s]',
               ylabel='Amplitud (parte regular)', title='1. Señal fija y señal invertida/desplazada')
        ax.grid(alpha=0.15)
        ax.legend(loc='upper left', fontsize=9)

        ye, yd = y_exponencial(t), y_delta(t)
        if t < 0:
            tramo = 't < 0: no hay solapamiento.'
        elif t < 1:
            tramo = '0 ≤ t < 1: crece el área.'
        elif t < 4:
            tramo = '1 ≤ t < 4: área + pulso retrasado.'
        elif t < 5:
            tramo = '4 ≤ t < 5: decae el área + pulso.'
        else:
            tramo = 't ≥ 5: queda la cola exponencial.'
        integral = ecuacion if b > a else r'$y_e(t)=0$'
        borde = '\nDelta en el borde: toma x = 1/2.' if t in (1, 5) else ''
        self.info.set_text(
            f't = {t:.3f} s\n\n{soportes}\n\n'
            + ('Límites de integración:\n' + f'a = {a:.3f}, b = {b:.3f}\n' if b > a else 'Sin área de solapamiento.\n')
            + integral + '\n\n'
            + f'Área exponencial = {ye:.5f}\n'
            + r'$y_\delta(t)=2x(t-1)$' + f' = {yd:.3f}\n'
            + f'Salida total = {ye+yd:.5f}\n\n{tramo}{borde}')
        self.cursor.set_xdata([t, t])
        self.punto.set_data([t], [ye+yd])
        self.fig.canvas.draw_idle()

    def ingresar_t(self, texto):
        if self.sincronizando:
            return
        try:
            t = float(texto.strip().replace(',', '.'))
            if not np.isfinite(t) or not T_MIN <= t <= T_MAX:
                raise ValueError
        except ValueError:
            self.estado.set_text(f'Ingresá un número entre {T_MIN:g} y {T_MAX:g} s.')
            self.estado.set_color(ROJO)
            self.fig.canvas.draw_idle()
            return
        self.estado.set_text('Escribí t y presioná Enter, o mové el deslizador.')
        self.estado.set_color('0.2')
        self.slider.set_val(t)

    def cambiar_movil(self, etiqueta):
        self.mover_h = etiqueta.startswith('Mover h')
        self.actualizar(self.slider.val)

    def alternar_animacion(self, event=None):
        self.animando = not self.animando
        self.boton_play.label.set_text('Pausar' if self.animando else 'Animar')
        if self.animando:
            if self.slider.val >= T_MAX:
                self.slider.set_val(T_MIN)
            self.timer.start()
        else:
            self.timer.stop()
        self.fig.canvas.draw_idle()

    def avanzar(self):
        if self.slider.val >= T_MAX:
            self.animando = False
            self.timer.stop()
            self.boton_play.label.set_text('Animar')
            self.fig.canvas.draw_idle()
            return
        self.slider.set_val(min(T_MAX, round(self.slider.val + 0.04, 6)))

    def reiniciar(self, event=None):
        self.animando = False
        self.timer.stop()
        self.boton_play.label.set_text('Animar')
        self.slider.set_val(T_MIN)


if __name__ == '__main__':
    app = ConvolucionGUI()
    plt.show()
