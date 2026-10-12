# The universal speed graph for the paper (2026-10-12)
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

c0 = 2.99792458e8
Y_bow = 5.93e26
rho_max = 1.304e15
rho_core = 2.3e17

def C_of_rho(rho):
    return np.minimum(c0, np.sqrt(2*Y_bow/rho))

rho = np.logspace(-27, 18, 600)
v = C_of_rho(rho)

fig, ax = plt.subplots(figsize=(7.5, 5))
ax.loglog(rho, v/1e3, "k-", lw=2, label=r"$C(\rho) = \min(c_0,\ \sqrt{2Y_{\mathrm{bow}}/\rho})$")

marks = [
    (8.74e-27, "the photon / the medium", "k"),
    (1.32e10, "the cap engages (0.9998 c0)", "b"),
    (1e11, "ladder anchor (0.363 c0)", "b"),
    (1e13, "ladder anchor (0.0363 c0)", "b"),
    (rho_max, "Max-P shell (954 km/s)", "r"),
    (rho_core, "bare neutron (72 km/s)", "r"),
]
for r, lab, col in marks:
    ax.plot(r, C_of_rho(r)/1e3, "o", color=col, ms=6)
    ax.annotate(lab, (r, C_of_rho(r)/1e3), xytext=(6, 6),
                textcoords="offset points", fontsize=8)

# observed objects (speeds read back densities)
ax.plot(0.775*rho_max, 1083, "s", color="g", ms=6)
ax.annotate("B1508+55: 1083 km/s\n(implied cap density = 0.775 rho_max)",
            (0.775*rho_max, 1083), xytext=(-8, 20), textcoords="offset points",
            fontsize=8, ha="right", va="bottom")
ax.plot(rho_max, 950, "D", color="purple", ms=7)
ax.annotate("RBH-1 (950 km/s\n= 0.996 of its C)", (rho_max, 950),
            xytext=(-8, -34), textcoords="offset points", fontsize=8,
            ha="right", va="top")

ax.set_xlabel(r"density $\rho$ (kg/m$^3$)")
ax.set_ylabel(r"maximum speed $C(\rho)$ (km/s)")
ax.set_title("The universal speed law: one medium, one yield, every object's own C")
ax.grid(True, which="both", ls=":", alpha=0.5)
ax.legend(loc="lower left", fontsize=9)
fig.tight_layout()
fig.savefig("speed_graph.png", dpi=200)
print("speed_graph.png written")
