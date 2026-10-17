import os, glob
ROOT = os.path.dirname(os.path.abspath(__file__))

def replace_in_file(rel_path, replacements):
    path = os.path.join(ROOT, rel_path)
    if not os.path.exists(path):
        print(f"[MISS] {rel_path}"); return
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    orig = text
    for old, new in replacements:
        if old in text:
            text = text.replace(old, new)
    if text != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[REPAIRED] {rel_path}")
    else:
        print(f"[UNCHANGED] {rel_path}")

# 1. the \r typo across all md files
for path in glob.glob(os.path.join(ROOT, "**", "*.md"), recursive=True):
    with open(path, "r", encoding="utf-8") as f:
        t = f.read()
    u = (t.replace("Drivers: \run_parallel_knots.py", "Drivers: run_parallel_knots.py")
         .replace("Drivers: \nun_parallel_knots.py", "Drivers: run_parallel_knots.py")
         .replace("Drivers: un_parallel_knots.py", "Drivers: run_parallel_knots.py"))
    if u != t:
        with open(path, "w", encoding="utf-8") as f:
            f.write(u)
        print(f"[FIXED typo] {os.path.relpath(path, ROOT)}")

# 2. the print-string sync in the_ladder.py + the unified
OLD_PRINT = 'print("\\nSTEP 5: the rotation formula (s_shared = 0.2264 derived, nothing fitted)")'
NEW_PRINT = ('print(\n    "\\nSTEP 5: rotation formula "\n    "(this run uses fitted s_shared = 0.2264; "\n    "framework-derived value = 0.2250)"\n)')
replace_in_file("scripts/the_ladder.py", [(OLD_PRINT, NEW_PRINT)])
replace_in_file("PHASE_WAVE_COSMOLOGY_UNIFIED.md", [(OLD_PRINT, NEW_PRINT)])

# 3. the neutron status updates (the surgical version, preserving the physics)
replace_in_file("papers_extra/NEUTRON_LIFETIME.md", [
    ("plausible, unchecked, unwritten", "proposed, open to refinement - see the closed fold below"),
    ("**Status: candidate.**", "**Status: proposed, open to refinement (`scripts/neutron_fold_closed.py`, `scripts/k_final_19_18.py`).**"),
])

# 4. the superseded sentence in the stacked blocks
OLD_NEUTRON_OPEN = ("The open item, named: derive k from the winding count - the 720 deg / 9 deg "
"tolerance ratio squared (6.4e3) sits in the right decade. The form is the "
"mechanism's; the coefficient is the last receipt.")
NEW_NEUTRON_OPEN = ("The tariff k is derived below via the winding tolerance and the k-H0 bridge "
"(`scripts/neutron_fold_closed.py`, `scripts/k_final_19_18.py`), with the "
"run-matched beam spectrum named as the remaining refinement.")
for md in ["PHASE_WAVE_COSMOLOGY_UNIFIED.md", "PHASE_WAVE_COSMOLOGY_DERIVATIONS.md",
           "subsectors/SUBATOMIC_PARTICLES.md", "clay/LODGEMENT_2_YANG_MILLS_MASS_GAP.md"]:
    replace_in_file(md, [(OLD_NEUTRON_OPEN, NEW_NEUTRON_OPEN)])

# 5. the scope note + the redshift open-verification flags
OLD_SUB = "## The strict subtraction ledger and the rate-limit friction (2026-10-17)\n\n"
NEW_SUB = ("## The strict subtraction ledger and the rate-limit friction (2026-10-17)\n\n"
"**Scope - bidirectional field tension and the wake:** in the magnetically held electromagnetic "
"field substrate, two opposite processes coexist: **tying** compacts extended medium into matter "
"(shrinking the field, dropping ambient field tension, and raising internal pressure in the "
"compacted knot), while **untying** returns matter to extended medium (expanding the field and "
"raising its tension); neither local mechanism alone predetermines which process dominates the net "
"global evolution. The rejection of \"springs, cycles, and thermal engines\" below is scoped strictly "
"to the local SMBH wake - ruling out an artificial local ring oscillator behind the moving black "
"hole - and does not repeal matter-medium untying elsewhere in the framework.\n\n")
replace_in_file("PHASE_WAVE_COSMOLOGY_UNIFIED.md", [(OLD_SUB, NEW_SUB)])
replace_in_file("subsectors/COSMOLOGY_ASTROPHYSICS.md", [(OLD_SUB, NEW_SUB)])

OLD_RED = "the tired light rejoins the 2.7255 K bath (the CMB is the graveyard of worn-out photons)."
NEW_RED = (OLD_RED + " **Open verification item:** the exact mathematical relationship between the quantitative "
"lattice-density redshift law (1+z) = (rho_emit/rho_obs)^(1/3) and this unpaired-wave wear-out "
"description is marked OPEN for formal verification.")
replace_in_file("subsectors/COSMOLOGY_ASTROPHYSICS.md", [(OLD_RED, NEW_RED)])
replace_in_file("PHASE_WAVE_COSMOLOGY_UNIFIED.md", [
    ("the CMB is the graveyard of the worn-out photons (the redshift is the luminous wearing out - the unpaired wave, not the knot).",
     "the CMB is the graveyard of the worn-out photons (the redshift is the luminous wearing out - the unpaired wave, not the knot; the exact mathematical relationship between this unpaired-wave wear-out description and the quantitative density law (1+z) = (rho_emit/rho_obs)^(1/3) is marked OPEN for formal verification).")
])

# 6. the D9 dual-evaluation note
OLD_D9 = "**Match.** G at +0.04%; the bridge 42.75 vs 42.7416"
NEW_D9 = ("**Match.** G at +0.04% (the measured-R_p evaluation, R_p = 0.8414 fm, run in `scripts/final_G_lock.py` and `scripts/the_ladder.py`); "
"the bridge 42.75 vs 42.7416")
replace_in_file("PHASE_WAVE_COSMOLOGY_DERIVATIONS.md", [(OLD_D9, NEW_D9)])
