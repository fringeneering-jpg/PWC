import numpy as np

# New mechanism: light travels at constant c0 (matches GW170817). The (1+z) stretch
# instead comes from the SOURCE event itself running slower when the medium was denser.
# observed_duration / intrinsic_duration = (rho(t_emit)/rho_today)^m = (1+z)^(n*m)
# where n is the density-history exponent (rho ~ (1+z)^n) and m is how strongly the
# reaction rate is throttled by density. Need (1+z)^(n*m) = (1+z)^1 exactly, i.e. n*m = 1.

z_vals = np.array([0.1, 0.5, 1.0, 1.5])

density_histories = {
    "matter (n=3)": 3.0,
    "radiation (n=4)": 4.0,
    "1/r^2, matches gravity (n=2)": 2.0,
}

print("Required throttling exponent m for exact (1+z) match, per density history:")
print(f"{'history':>32} {'n':>4} {'required m = 1/n':>18}")
for name, n in density_histories.items():
    m_required = 1.0/n
    print(f"{name:>32} {n:4.1f} {m_required:18.4f}")

print()
print("Sanity check: if m=1 (simplest possible 'rate throttled linearly by density') and n=1")
print("(density scales linearly as (1+z), NOT matter/radiation/1/r^2), that's the only way")
print("to get n*m=1 with BOTH m and n at the simplest possible values (m=1, n=1):")
n, m = 1.0, 1.0
predicted = (1+z_vals)**(n*m)
for z, p in zip(z_vals, predicted):
    print(f"  z={z:.1f}: predicted stretch = {p:.3f}, required = {1+z:.3f}, ratio = {p/(1+z):.4f}")
