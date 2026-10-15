# HEAT HATES PRESSURE - the speed-up law, written (2026-10-12)
import math
s = 1.0/19.0
c0 = 2.99792458e8

print("=" * 78)
print("THE DERIVATION: HEAT HATES PRESSURE -> the untie's tempo")
print("=" * 78)
print("""
1. THE RULE (the flux law).
   Heat is a transfer, not an energy. Its only direction law: away from pressure,
   toward relief. The flux follows the pressure's own gradient:
        u_heat = -(1/rho) grad P    x    (the medium's conductance kappa)
   The untying front is the relief valve; the heat converges on it.

2. THE SET RATE (the throttle).
   The medium unties at its OWN rate - the melt's tempo H(t) - independent of the
   heat. The untie's volumetric growth dilutes the pressure:
        d(ln P)/dt = -3 H(t)      (the expansion's own press)

3. THE GRIP (the debt's share).
   The pressure's grip on the heat is the debt's tension: the retained share s
   of the balance - the negative-pressure draw, the 615x margin. The grip sets
   how strongly the pressure SHEPHERDS the heat toward the front.

4. THE TIGHTENING (the front's own dynamics).
   As the front eats the wall, the boundary shrinks and the drop deepens:
        d(ln |grad P|)/dt = + (the growth's press) x (the grip) x (1 + the
        boundary's shrinkage)  -  the "tighter" is the drop concentrating.

5. THE SPEED-UP LAW (the balance's time derivative).
        (1/u)(du/dt) = s x 3H x (1 + T)
   where s = 1/19 (the grip), H = the growth's press, T = the tightening factor
   (the boundary's shrinkage + the drop's deepening). The heat accelerates
   exactly as the pressure lets go - slower through the wall (the squeeze),
   faster down the relief (the flight). Early: slow unties, streams, hot
   boundaries (T small). Late: the spread pushes the heat off the boundary,
   the tightening forces it into the untie zones (T grows). The speed-up is the
   history's own acceleration.

6. THE PEAK'S PIN.
   The demanded tempo at the LSS: 1/258 kyr = 1.47 x (1/380 kyr, the age's own).
        s x (1 + T) = 1.47   ->   T = 1.47 x 19 - 1 = 26.9
   The tightening factor T ~ 27 is the named coefficient - the boundary's
   shrinkage + the drop's deepening, to be read from the web's observed choke
   zones (the wall thickness, the contrast). The derivation is closed IN FORM:
   the speed-up law = the grip x the press x the tightening, three locked
   quantities, one named coefficient.
""")
print("the three locked pieces: s = 1/19 (the grip), H (the press), and the rule")
print("(the flux follows -grad P). The one named coefficient: the tightening T.")
print("Status: the derivation's FORM is written from the rule; T awaits the web's")
print("observed choke zones - the thermal web's own data, which the framework holds.")
