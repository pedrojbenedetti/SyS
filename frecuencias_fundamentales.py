import numpy as np
import matplotlib.pyplot as plt


def configurar_eje(eje, xlabel=False):
    """Aplica un formato común a todos los subplots."""
    eje.axhline(0, color="black", linewidth=0.8)
    eje.axvline(0, color="black", linewidth=0.8)
    eje.grid(True, alpha=0.3)
    eje.set_ylabel("Amplitud")
    if xlabel:
        eje.set_xlabel("Tiempo t [s]")


# -----------------------------------------------------------------------------
# b) x(t) = 3 sen(19*pi*t - pi/3) + 2 cos(10*pi*t + pi/6)
# -----------------------------------------------------------------------------
t_b = np.linspace(-0.1, 2.1, 12000)

seno_b = 3 * np.sin(19 * np.pi * t_b - np.pi / 3)
coseno_b = 2 * np.cos(10 * np.pi * t_b + np.pi / 6)
suma_b = seno_b + coseno_b

fig_b, ax_b = plt.subplots(3, 1, figsize=(11, 8), sharex=True)
fig_b.suptitle("Ejercicio b", fontsize=15)

ax_b[0].plot(t_b, seno_b, color="red", linewidth=1.8)
ax_b[0].set_title(r"$3\sin(19\pi t-\pi/3)$")

ax_b[1].plot(t_b, coseno_b, color="blue", linewidth=1.8)
ax_b[1].set_title(r"$2\cos(10\pi t+\pi/6)$")

# En el último subplot, la suma es continua y sus componentes son punteadas.
ax_b[2].plot(t_b, suma_b, color="purple", linewidth=2.2, label="Suma")
ax_b[2].plot(
    t_b,
    seno_b,
    color="red",
    linestyle="--",
    linewidth=1.2,
    alpha=0.75,
    label="Seno",
)
ax_b[2].plot(
    t_b,
    coseno_b,
    color="blue",
    linestyle="--",
    linewidth=1.2,
    alpha=0.75,
    label="Coseno",
)
ax_b[2].set_title("Suma y componentes")
ax_b[2].legend(loc="upper right")

for i, eje in enumerate(ax_b):
    configurar_eje(eje, xlabel=(i == 2))
    eje.set_xlim(t_b[0], t_b[-1])

fig_b.tight_layout()


# -----------------------------------------------------------------------------
# d) según lo pedido: coseno y 1/2 del coseno al cuadrado.
# En la imagen, esta expresión está rotulada como ejercicio e).
# x(t) = 1/2 [cos(2t - pi/4)]^2
# -----------------------------------------------------------------------------
t_d = np.linspace(-np.pi, 2 * np.pi, 6000)

coseno_d = np.cos(2 * t_d - np.pi / 4)
coseno_cuadrado_d = 0.5 * coseno_d**2

fig_d, ax_d = plt.subplots(2, 1, figsize=(11, 6), sharex=True)
fig_d.suptitle("Ejercicio d: coseno al cuadrado", fontsize=15)

ax_d[0].plot(t_d, coseno_d, color="blue", linewidth=2)
ax_d[0].set_title(r"$\cos(2t-\pi/4)$")

ax_d[1].plot(t_d, coseno_cuadrado_d, color="purple", linewidth=2)
ax_d[1].set_title(r"$\frac{1}{2}[\cos(2t-\pi/4)]^2$")

for i, eje in enumerate(ax_d):
    configurar_eje(eje, xlabel=(i == 1))
    eje.set_xlim(t_d[0], t_d[-1])

fig_d.tight_layout()


# -----------------------------------------------------------------------------
# f) x(t) = sen(5*pi*t) / sen(pi*t)
# -----------------------------------------------------------------------------
t_f = np.linspace(-2, 2, 8001)

numerador_f = np.sin(5 * np.pi * t_f)
denominador_f = np.sin(np.pi * t_f)

# El cociente da 0/0 en los enteros. Para dibujar su forma sin errores
# numéricos usamos su extensión continua equivalente:
# sen(5x)/sen(x) = 16 cos^4(x) - 12 cos^2(x) + 1.
cociente_extendido_f = (
    16 * np.cos(np.pi * t_f) ** 4
    - 12 * np.cos(np.pi * t_f) ** 2
    + 1
)

fig_f, ax_f = plt.subplots(3, 1, figsize=(11, 8), sharex=True)
fig_f.suptitle("Ejercicio f", fontsize=15)

ax_f[0].plot(t_f, numerador_f, color="red", linewidth=1.8)
ax_f[0].set_title(r"Numerador: $\sin(5\pi t)$")

ax_f[1].plot(t_f, denominador_f, color="blue", linewidth=1.8)
ax_f[1].set_title(r"Denominador: $\sin(\pi t)$")

ax_f[2].plot(
    t_f,
    cociente_extendido_f,
    color="purple",
    linewidth=2.2,
    label="Cociente",
)
ax_f[2].plot(
    t_f,
    numerador_f,
    color="red",
    linestyle="--",
    linewidth=1.2,
    alpha=0.75,
    label="Numerador",
)
ax_f[2].plot(
    t_f,
    denominador_f,
    color="blue",
    linestyle="--",
    linewidth=1.2,
    alpha=0.75,
    label="Denominador",
)

# Los círculos abiertos señalan los puntos enteros donde el cociente original
# no está definido, aunque su límite vale 5.
enteros = np.arange(np.ceil(t_f[0]), np.floor(t_f[-1]) + 1)
ax_f[2].scatter(
    enteros,
    np.full_like(enteros, 5, dtype=float),
    facecolors="white",
    edgecolors="purple",
    linewidths=1.5,
    s=50,
    zorder=5,
    label="Puntos no definidos",
)
ax_f[2].set_title("Cociente y señales del numerador y denominador")
ax_f[2].legend(loc="lower right")

for i, eje in enumerate(ax_f):
    configurar_eje(eje, xlabel=(i == 2))
    eje.set_xlim(t_f[0], t_f[-1])

fig_f.tight_layout()


plt.show()
