"""DTFT y DFT de {3, 2, 3}: exploración del agregado de ceros.

Dependencias: numpy, matplotlib y tkinter (incluido en Python para Windows).
La frecuencia se expresa en ciclos por muestra. No se normaliza la DFT.
"""
import tkinter as tk
from tkinter import ttk

import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


ORIGINAL = np.array([3., 2., 3.])
COLOR = '#1769aa'
ORANGE = '#d97706'


def spectrum(n):
    """DFT de N puntos, completando con ceros a la derecha."""
    return np.fft.fft(ORIGINAL, n=n)


def dtft(f):
    return np.exp(-2j*np.pi*np.asarray(f)[..., None]*np.arange(3)) @ ORIGINAL


class App:
    def __init__(self, root):
        self.root = root
        root.title('DTFT y DFT · Agregado de ceros')
        root.geometry('1250x800')
        root.minsize(900, 620)
        controls = ttk.Frame(root, padding=(15, 10))
        controls.pack(fill='x')
        ttk.Label(controls, text='Ceros agregados:').pack(side='left')
        self.zeros = tk.StringVar(value='0')
        self.spin = ttk.Spinbox(controls, from_=0, to=100000, increment=1,
                               width=10, textvariable=self.zeros,
                               command=self.update)
        self.spin.pack(side='left', padx=8)
        self.spin.bind('<Return>', self.update)
        self.spin.bind('<FocusOut>', self.update)
        self.spin.bind('<KeyRelease>', self.schedule_update)
        self.pending = None
        self.info = ttk.Label(controls, font=('Arial', 12, 'bold'))
        self.info.pack(side='left', padx=15)
        self.error = ttk.Label(root, foreground='#b91c1c')
        self.error.pack(fill='x', padx=15)
        self.fig = Figure(figsize=(12, 6), constrained_layout=True)
        grid = self.fig.add_gridspec(2, 2, width_ratios=[1.45, 1])
        self.mag = self.fig.add_subplot(grid[0, 0])
        self.phase = self.fig.add_subplot(grid[1, 0], sharex=self.mag)
        self.time = self.fig.add_subplot(grid[:, 1])
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        NavigationToolbar2Tk(self.canvas, root)
        self.detail = ttk.Label(root, padding=(15, 7), font=('Arial', 11))
        self.detail.pack(fill='x')
        ttk.Label(root, padding=(15, 4), text=(
            'Hacé clic en módulo o fase para seleccionar la muestra DFT más cercana. '
            'Agregar ceros aumenta la densidad de muestras de la misma DTFT.')).pack(fill='x')
        self.canvas.mpl_connect('button_press_event', self.select)
        self.k = 0
        self.n = 3
        self.update()

    def schedule_update(self, event=None):
        if self.pending is not None:
            self.root.after_cancel(self.pending)
        self.pending = self.root.after(350, self.delayed_update)

    def delayed_update(self):
        self.pending = None
        self.update()

    def update(self, event=None):
        raw = self.zeros.get().strip()
        try:
            count = int(raw)
            if count < 0 or count > 100000:
                raise ValueError
        except ValueError:
            self.error.config(text='Ingresá un entero entre 0 y 100000 ceros.')
            return
        self.error.config(text='')
        old_f = self.k / self.n
        self.n = 3 + count
        self.k = min(round(old_f*self.n), self.n-1)
        self.values = spectrum(self.n)
        self.freq = np.arange(self.n)/self.n
        self.info.config(text=f'N = {self.n}     Δf = 1/{self.n} = {1/self.n:.6g} ciclos/muestra')
        self.draw()

    def draw(self):
        for ax in (self.mag, self.phase, self.time):
            ax.clear()
            ax.grid(alpha=.22)
        f = np.linspace(0, 1, 6001)
        continuous = dtft(f)
        phase = np.angle(continuous)
        # Interrumpir las líneas en los saltos: la fase no existe en los ceros.
        phase[np.abs(np.diff(phase, prepend=phase[0])) > 1] = np.nan
        for ax, curve, samples in (
            (self.mag, np.abs(continuous), np.abs(self.values)),
            (self.phase, phase, np.angle(self.values))):
            ax.plot(f, curve, color='0.5', lw=1.8, label='DTFT', zorder=2)
            stems = ax.stem(self.freq, samples, linefmt='-', markerfmt='o', basefmt=' ')
            stems.markerline.set_color(COLOR)
            stems.markerline.set_markersize(4 if self.n < 100 else 2)
            stems.stemlines.set_color(COLOR)
            stems.stemlines.set_linewidth(.9)
            stems.markerline.set_label('DFT')
            ax.set_xlim(-.02, 1.02)
            ax.legend(loc='upper right', fontsize=9)
        self.mag.set(title='Módulo: DTFT y DFT', ylabel='|X|', ylim=(-.35, 8.7))
        self.phase.set(title='Fase: DTFT y DFT', ylabel='Fase (rad)',
                       xlabel='f (ciclos por muestra)', ylim=(-3.4, 3.4))
        self.phase.set_yticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi],
                             ['−π', '−π/2', '0', 'π/2', 'π'])
        stems = self.time.stem(np.arange(3), ORIGINAL, linefmt='-', markerfmt='o', basefmt=' ')
        stems.markerline.set_color(COLOR)
        stems.stemlines.set_color(COLOR)
        stems.markerline.set_label('Valores originales')
        for i, value in enumerate(ORIGINAL):
            self.time.annotate(f'{value:g}', (i, value), xytext=(0, 9),
                               textcoords='offset points', ha='center', color=COLOR)
        if self.n > 3:
            self.time.plot(np.arange(3, self.n), np.zeros(self.n-3), 'o',
                           markerfacecolor='none', markeredgecolor=ORANGE,
                           markersize=5, label='Ceros agregados')
        self.time.axhline(0, color='0.3', lw=.8)
        self.time.set(title=f'Señal temporal · {self.n-3} ceros agregados',
                      xlabel='n (muestras)', ylabel='x[n]',
                      xlim=(-.65, max(3, self.n-1)+.65), ylim=(-.5, 4))
        if self.n <= 20:
            self.time.set_xticks(np.arange(self.n))
        self.time.legend(loc='upper right', fontsize=9)
        self.markers = []
        self.highlight()

    def select(self, event):
        if event.inaxes not in (self.mag, self.phase) or event.xdata is None:
            return
        if self.canvas.toolbar.mode:
            return
        self.k = int(np.clip(np.floor(event.xdata*self.n + .5), 0, self.n-1))
        self.highlight()

    def highlight(self):
        for artist in self.markers:
            artist.remove()
        self.markers = []
        f = self.freq[self.k]
        value = self.values[self.k]
        for ax, y in ((self.mag, abs(value)), (self.phase, np.angle(value))):
            self.markers.append(ax.axvline(f, color=ORANGE, ls='--', lw=1.1))
            self.markers.extend(ax.plot(f, y, 'o', color=ORANGE, ms=8, zorder=5))
        self.detail.config(text=(f'Muestra seleccionada: k = {self.k}    '
            f'fₖ = {self.k}/{self.n} = {f:.6g} ciclos/muestra    '
            f'|X[k]| = {abs(value):.6g}    '
            f'Fase = {np.angle(value):.6g} rad ({np.angle(value, deg=True):.3g}°)'))
        self.canvas.draw_idle()


if __name__ == '__main__':
    root = tk.Tk()
    App(root)
    root.mainloop()
