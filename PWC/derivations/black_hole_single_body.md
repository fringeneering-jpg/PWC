# The single black hole — mechanics as Jaden stated and corrected them (2026-10-02)

Registry: `DERIVATIONS.md` row 16. The mechanics are his; the numbers are arithmetic on them. Verbatim statements and the full run log are in the local capture folder (not in git).

## Structure
1. **Core.** Every black hole has a neutron-density core (ρ_core ≈ 2.3×10¹⁷ kg/m³, just holding off beta decay). The core stacks like the medium does: more mass adds layers at the density ceiling, never density; no beta-decay wall. Gravity is 1/r² measured from the centre. The interior of a big core keeps pulling but has no effect outside the core's boundary, so it is removed from the core's pulling capacity. There is **no cap** on the surface pull: pull beyond what holds ρ_max just stacks the shell thicker.
2. **Shell.** The core drags the medium in; the medium cannot be crushed past ρ_max = 1.304×10¹⁵, so it stacks into a layer around the core, thicker, not denser, while the pull stays above the yield 3.23×10¹¹ N/kg. **"Shell" means only this ρ_max layer** (it starts where max-P starts). The black hole = core + shell. A larger core has more layers physically but a thinner shell in proportion. How much medium the shell holds goes with the core's surface area (k·C^(2/3), row 11); the shell's outer radial edge is the optical/density boundary, not the capacity.
3. **Outside the shell.** The medium falls off by its own pull on itself (same for every hole). It is heavy medium, the "starting attractor" (name not final), and is not part of the black hole.
4. **The edge seen.** The sonic choke r_s = 2GM/c₀², where matter being pulled in reaches c (the limit on how fast gravity can drive matter); gives Hawking's temperature exactly (`PWC.md` §8). The medium does not flow.
5. **Merger.** Rows 11–13: cores push through each other's ρ_max layers, volumes add, the joined core has less max pull and storage, and the dropped mass is min(motion energy at contact, storage lost). Bow waves: a body whose ρ_max shell exceeds the medium's limit (954 km/s) forms a new ρ_max front (RBH-1; supernova and merger are the same event at higher speeds): row 15.

## Numbers (arithmetic on the above; per-hole tables are in the local capture folder)
- Core radius (whole mass at ρ_core) and Max-P edge = reach √(GM/a_max): GW150914 core 47–50 km, edge 159.6 km; Sgr A* core 2,071 km, reach 42,039 km; M87* core 23,760 km, reach 1.63×10⁶ km; RBH-1 scale (10⁷ M☉) core 2,743 km, edge 64,109 km.
- With the area-law shell (row 11) heavy cores are almost all the mass and the shell thickness tends to a constant ≈ 640 km; the reach picture gives shells tens of thousands of km thick. The two pictures disagree for heavy holes and are not reconciled.

## Open items (stated honestly)
- **Decompression law**: density of the medium outside the shell from its own pull on itself — mechanism stated (his ruling), no equation solved.
- **Mass bookkeeping for heavy holes**: ρ_max filling the reach holds more mass than the catalog mass above ≈ 1,900 M☉ (2.1× at 8,200 M☉, 47× for Sgr A*). Whether and how shell medium counts toward the catalog mass is not settled.
- **Core density vs mass** (row 12) is only supported over merger masses 14–238 M☉; the supermassive end is an untested extrapolation (a power-law extrapolation would make the Sgr A* core 73–323 km, not 2,071 km).
- **Black-hole shadow (EHT)** — undefined in PWC. The flowing-medium (river-model) calculation gave GR's 3√3/2 r_s and is **withdrawn**: the medium does not flow.
- The yield 3.23×10¹¹ and 159.6 km come from GW150914's edge, first computed from that event's Kerr horizon (a GR number); the shell scale carries that one calibration.
- The sealed light-bending, speed-limit and merger results are in rows 13–15; none of them has been derived from a medium equation of state `P(ρ, s)` (still OPEN).

## Withdrawn along the way (do not revive)
The capped-core run (g_cap = 5.38×10¹², edge = 4.08× core); a "fixed-thickness pulling layer" and "finite maximum surface pull" (his correction: interior has no effect, no cap); Gemini's all-mass-core "decompression size" tables and mean-density "fits" (Schwarzschild-volume identities); "sliding" densities beyond the merger range; all heat-based merger accounts.
