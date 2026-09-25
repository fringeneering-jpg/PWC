"""First-pass BH held-medium profile: hydrostatic atmospheres with trial stiff EOS (FAILED; see predictions/bh_flow_profile.md).
Also restates the k-rule as a universal column density. Run 2026-09-25."""
import numpy as np
G=6.6743e-11;c=299792458.0;Ms=1.98892e30;RN=2.3e17;RM=1.304e15;k=0.868899
for C in [10,50,1e3,4.3e6]:
    Rc=(3*C*Ms/(4*np.pi*RN))**(1/3); Mm=k*C**(2/3)*Ms
    print(f"C={C:>9.0f} Msun  R_c={Rc/1e3:8.1f} km  held medium {k*C**(2/3):9.1f} Msun  Sigma = {Mm/(4*np.pi*Rc**2):.3e} kg/m^2")
def held(C,w,rs_frac):   # P = w c^2 (rho - rho_s), capped at rho_max, Newtonian hydrostatics from the core surface
    Rc=(3*C*Ms/(4*np.pi*RN))**(1/3); r=Rc; rho=RM; M=C*Ms; dr=Rc*1e-4; Mmed=0; cs2=w*c*c; rs=rs_frac*RM
    while rho>rs and r<1e4*Rc:
        drho=-rho*G*M/(r*r)/cs2*dr; dm=4*np.pi*r*r*rho*dr; rho+=drho; M+=dm; Mmed+=dm; r+=dr
        dr=min(Rc*1e-3, 0.01*cs2*r*r/(G*M))
    return Mmed/Ms
for w in [1/3,1.0]:
    for f in [0.5,0.1,1e-3]:
        Cs=np.array([10,100,1e3,1e4]); m=np.array([held(C,w,f) for C in Cs])
        print(f"w={w:.2f}, surface at {f}*rho_max: held {m.round(3)} Msun; scales as C^{np.polyfit(np.log10(Cs),np.log10(m),1)[0]:.2f} (target 0.67)")
