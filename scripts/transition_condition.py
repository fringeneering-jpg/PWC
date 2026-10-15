# The medium->matter transition condition (2026-10-08, Jaden's order)
import math
c0 = 2.99792458e8
c0sq = c0**2
rho_max = 1.304e15
rho0 = 8.74e-27
hbar = 1.05457e-34
mp = 1.6726e-27
me = 9.1094e-31
Rp = 0.8414e-15

print("== 1. The proton/electron inventory (Identity B) ==")
Vp = mp/rho_max
Rp_ball = (3*Vp/(4*math.pi))**(1/3)
print(f"proton inventory ball: V = m_p/rho_max = {Vp:.4e} m^3 -> R_ball = {Rp_ball/1e-15:.2f} fm = "
      f"{Rp_ball/Rp:.1f} R_p")
Ve = me/rho_max
Re_ball = (3*Ve/(4*math.pi))**(1/3)
print(f"electron inventory ball: R = {Re_ball/1e-15:.3f} fm (V = {Ve:.3e} m^3)")
print(f"plateau work per kg: P* dv = rho_max c0^2 x (1/rho_max) = {rho_max*c0sq/rho_max/c0sq:.6f} c0^2")

print("\n== 2. The T2 gate (blockage) ==")
lam = (mp/7.475e16)**(1/3)
print(f"gate density m_p/lambda^3 = 7.475e16 -> lambda = {lam/1e-15:.2f} fm = {lam/Rp:.1f} R_p")
print(f"(only compact cores / Max-P walls block the medium; stars and planets are transparent)")

print("\n== 3. The keystone ramp end (alignment = absence of heat) ==")
H0_floor = 32.371*c0sq
print(f"H0 floor = 32.371 c0^2 = {H0_floor:.3e} J/kg; at rho_max: S = 1, heat fully expelled.")
print(f"the tied state is the HEAT-VOID state; the untie suction is the heat seeking to refill it.")

print("\n== 4. The quantization (proton/electron) ==")
print(f"m_p R_p c0 = {mp*Rp*c0/hbar:.3f} hbar = 4 hbar  (Identity A)")
print(f"electron: 4 EM waves on the 720-degree loop (Jaden, 2026-10-07)")

print("\n== 5. The stagnation column (hold) ==")
col = 3*3.23e11/(4*math.pi*6.6743e-11)
print(f"gravity-hold column rho*R >= {col:.4e} kg/m^2 (medium chunks);")
print(f"the KNOT's own column: rho_max x R_ball = {rho_max*Rp_ball:.2f} kg/m^2 - gravity is nothing")
print(f"there; matter holds by TOPOLOGY (the 720-degree lock), not by gravity.")

print("\n== THE TRANSITION CONDITION (five gates, all needed) ==")
print("1. BLOCKAGE: rho > m_p/lambda^3 = 7.475e16 (the T2 gate) - only compact cores / Max-P walls.")
print("2. FOLD: compression to rho_max/2 -> rho_max (P = P* = rho_max c0^2); the gas-branch squeeze")
print("   expels 31.371 c0^2/kg of heat (self-financed: H_local >= 32.371 c0^2).")
print("3. PLATEAU WORK: m*c0^2 per kg tied - the demand function m = dP*dV/c0^2 at dP = P*.")
print("4. QUANTIZATION: the heat-expelled waves lock on the 720-degree loop, m R c0 = 4 hbar")
print("   (S = 1: alignment is the absence of heat - the keystone ramp end).")
print("5. HOLD: the knot holds by topology (not by the 1.155e21 column - that is for MEDIUM chunks).")
print()
print("The RSMBH wake runs gates 1-4 at the closing walls (blocked, fold, P* slam, heat expelled);")
print("the natural recombination product is hydrogen - the easiest knot (locked ruling).")
print("The gravity wave (free displacement, sub-column) never reaches gate 2 - it re-pairs into")
print("ordered medium, never ties.")
print()
print("Counter-intuition, in numbers: the TIE fights both - expels c0^2/kg of heat AND compresses")
print("against the negative pressure. The UNTIE runs with both: the negative pressure (1.75% of the")
print("bill, the trigger) and the heat suction (98.25%) pull in the SAME direction - the heat seeks")
print("the heatless knot and the field's stretch opens it. Matter is counter-intuitive for both,")
print("exactly as stated.")
