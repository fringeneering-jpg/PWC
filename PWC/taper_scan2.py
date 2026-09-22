exec(open('taper_model.py').read().split("print(\"scanning")[0])
print("fine scan near the crossing...")
for lg in np.arange(8.10, 8.45, 0.02):
    try:
        r = calib_residual(lg)
        print(f"  log10(c_s)={lg:.2f}  c_s/c={10**lg/2.998e8:.4f}  residual={r:+.5f} Msun")
    except Exception as e:
        print(f"  log10(c_s)={lg:.2f}  FAILED: {e}")
