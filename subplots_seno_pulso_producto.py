import numpy as np
import matplotlib.pyplot as plt


# Eje temporal
t = np.linspace(-1, 2, 3000)

# Señales
seno = np.sin(2 * np.pi * t)

# Pulso rectangular de amplitud 1 y ancho 1, centrado en t = 1/2.
# Por lo tanto, vale 1 entre t = 0 y t = 1, y 0 fuera de ese intervalo.
pulso = np.where((t >= 0) & (t <= 1), 1.0, 0.0)

producto = seno * pulso


# Tres subplots dispuestos verticalmente
fig, ax = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

ax[0].plot(t, seno, color="red", linewidth=2)
ax[0].set_title(r"Señal senoidal: $\sin(2\pi t)$")
ax[0].set_ylabel("Amplitud")

ax[1].plot(t, pulso, color="blue", linewidth=2)
ax[1].set_title(r"Pulso unitario centrado en $t=\frac{1}{2}$")
ax[1].set_ylabel("Amplitud")

ax[2].plot(t, producto, color="purple", linewidth=2)
ax[2].set_title("Producto entre ambas señales")
ax[2].set_xlabel("Tiempo t")
ax[2].set_ylabel("Amplitud")

# Formato común
for eje in ax:
    eje.axhline(0, color="black", linewidth=0.8)
    eje.axvline(0, color="black", linewidth=0.8)
    eje.grid(True, alpha=0.3)
    eje.set_xlim(-1, 2)

plt.tight_layout()
plt.show()
