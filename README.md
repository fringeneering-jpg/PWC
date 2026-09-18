## Fluid Dynamics: Supersonic Wake Simulation

This section hosts the OpenFOAM numerical simulation case files (`PWC_Supersonic_Wake`) modeling supersonic flow characteristics, velocity profiles ($U$), pressure fields ($p$), temperature distributions ($T$), and density fields ($\rho$) across transient time steps.

<details>
<summary><b>📂 Case Directory Structure & Configuration Files</b></summary>

### System & Control Dictionaries (`/system`)
* `blockMeshDict` — Domain geometry and mesh generation parameters.
* `controlDict` — Time-step control, execution runtime, and function object definitions.
* `fvSchemes` & `fvSolution` — Numerical discretization schemes and linear solver controls.
* `topoSetDict`, `changeDictionaryDict`, & `setFieldsDict` — Cell set manipulation and initial field patching.

### Boundary Conditions & Initial Fields (`/0` & transient time directories)
* `0/U`, `0/p`, `0/T` — Initial boundary conditions for velocity, pressure, and temperature.
* Transient directories (`/0.501437` through `/4.99922797784`) — Full field data outputs across solved time steps containing:
  * `U` (Velocity vector field)
  * `p` (Kinematic/static pressure)
  * `T` (Temperature)
  * `rho` (Density)
  * `uniform/time` & `functionObjects/`

### Constant Properties & Mesh Topology (`/constant`)
* `thermophysicalProperties` — Thermodynamic and transport properties.
* `turbulenceProperties` — Turbulence modeling configuration.
* `polyMesh/` — Boundary definitions, face lists, point coordinates, and cell ownership files (including `obstacleCells`).

</details>

### Quick Execution Reference
To run or reconstruct the case locally using OpenFOAM:
```bash
# Verify mesh generation
blockMesh

# Run solver (or inspect pre-calculated time directories)
# log file saved as log.pwc_case_c
