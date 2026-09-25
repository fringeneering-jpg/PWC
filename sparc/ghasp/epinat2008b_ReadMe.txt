J/MNRAS/390/466     GHASP: H{alpha} data cubes for 97 galaxies   (Epinat+, 2008)
================================================================================
GHASP: an H{alpha} kinematic survey of 203 spiral and irregular galaxies.
VII. Revisiting the analysis of H{alpha} data cubes for 97 galaxies.
    Epinat B., Amram P., Marcelin M.
   <Mon. Not. R. Astron. Soc., 390, 466-504 (2008)>
   =2008MNRAS.390..466E
================================================================================
ADC_Keywords: Galaxy catalogs ; Radial velocities ; Morphology
Keywords: galaxies: dwarf - galaxies: irregular -
          galaxies: kinematics and dynamics - galaxies: spiral

Abstract:
    The Gassendi HAlpha survey of SPirals survey (GHASP) consists of 3D
    H{alpha} data cubes for 203 spiral and irregular galaxies, covering 
    a large range in morphological types and absolute magnitudes, for
    kinematics analysis. It is the largest sample of Fabry-Perot data
    published up to now. In order to provide an homogenous sample, reduced
    and analysed using the same procedure, we present in this paper the
    new reduction and analysis for a set of 97 galaxies already published
    in previous papers but now using the new data reduction procedure
    adopted for the whole sample. The GHASP survey is now achieved and the
    whole sample is reduced using the adaptive binning techniques based on
    Voronoi tessellations. We have derived H{alpha} data cubes from which
    are computed H{alpha} maps, radial velocity fields as well as residual
    velocity fields, position-velocity diagrams, rotation curves and
    kinematical parameters for almost all galaxies. The rotation curves,
    the kinematical parameters and their uncertainties are computed
    homogeneously using the new method based on the power spectrum of the
    residual velocity field. This paper provides the kinematical
    parameters for the whole sample. For the first time, the integrated
    H{alpha} profiles have been computed and are presented for the whole
    sample. The total H{alpha} fluxes deduced from these profiles have
    been used in order to provide a flux calibration for the 203 GHASP
    galaxies. This paper confirms the conclusions already drawn from half
    the sample concerning (i) the increased accuracy of position angles
    measurements using kinematical data, (ii) the difficulty to have
    robust determinations of both morphological and kinematical
    inclinations in particular for low-inclination galaxies and (iii) the
    very good agreement between the Tully-Fisher relationship derived
    from our data and previous determinations found in the literature.

Description:
    The GHASP survey was originally selected to be a subsample
    complementing the radio survey Westerbork survey of HI in SPirals
    galaxies (WHISP) providing HI distribution and velocity maps for about
    400 galaxies (http://www.astro.rug.nl/whisp). The first set of GHASP
    galaxies was selected from the first WHISP website list but some of
    them have never been observed by WHISP.

File Summary:
--------------------------------------------------------------------------------
 FileName   Lrecl  Records   Explanations
--------------------------------------------------------------------------------
ReadMe         80        .   This file
tableb1.dat    76      203   Calibration parameters
tableb2.dat    97      203   Model parameters
tableb3.dat    97      203   Galaxy parameters
tablef.dat     43     4208   Rotation curves for 82 galaxies
--------------------------------------------------------------------------------

See also:
   J/MNRAS/388/500 : GHASP: H{alpha} data cubes for 108 galaxies (Epinat+, 2008)

Byte-by-byte Description of file: tableb1.dat
--------------------------------------------------------------------------------
  Bytes Format Units      Label    Explanations
--------------------------------------------------------------------------------
  1-  9  A9    ---        Name     Galaxy name
 11- 15  I5    ---        UGC      ? UGC number
     16  A1    ---      m_UGC      [c] Multiplicity index on UGC
 18- 21  I4    ---        NGC      ? NGC number
     22  A1    ---      m_NGC      [A] Multiplicity index on NGC
 24- 25  I2    h          RAh      Right ascension (J2000) (1)
 27- 28  I2    min        RAm      Right ascension (J2000) (1)
 30- 33  F4.1  s          RAs      Right ascension (J2000) (1)
     35  A1    ---        DE-      Declination sign (J2000) (1)
 36- 37  I2    deg        DEd      Declination (J2000) (1)
 39- 40  I2    arcmin     DEm      Declination (J2000) (1)
 42- 43  I2    arcsec     DEs      Declination (J2000) (1)
 45- 49  I5    s          ExpTime  Exposure time
 51- 54  F4.2  arcsec     Scale    Pixel scale (arcsec/pix)
 56- 57  A2    ---      l_Flux     [>= ] Limit flag on  Flux
 58- 62  F5.1 10-16W/m2   Flux     ? Integrated H{alpha} flux deduced from the
                                     comparison with James et al. (2004, 
                                     Cat. J/A+A/414/23) data (2)
 64- 67  F4.1 10-16W/m2 e_Flux     ? rms uncertainty on Flux
 69- 76  A8    ---        Pap      Publication papers
--------------------------------------------------------------------------------
Note (1): Coordinates of the centre of the galaxy used for the kinematic study.
Note (2): When the galaxy is larger than the field of view (see tableb3.dat),
     we only have a lower limit on the integrated H{alpha} flux.
--------------------------------------------------------------------------------

Byte-by-byte Description of file: tableb2.dat
--------------------------------------------------------------------------------
   Bytes Format Units   Label   Explanations
--------------------------------------------------------------------------------
   1-  9  A9    ---     Name    Galaxy name
  11- 14  I4    km/s    VsysL   Systemic velocity found in HyperLeda data base
  16- 17  I2    km/s  e_VsysL   rms uncertainty on VsysL
  19- 22  I4    km/s    Vsys    ?=- Systemic velocity deduced from our
                                    velocity field analysis
  24- 26  I3    km/s  e_Vsys    ?=- rms uncertainty on Vsys
  28- 29  I2    deg     iM      Morphological inclination from HyperLeda
                                 (Paturel et al., 1997, Cat. VII/237)
  31- 32  I2    deg   e_iM      rms uncertainty on iM
  34- 35  I2    deg     iK      ?=- Inclination deduced from the analysis of
                                    our velocity field
  37- 38  I2    deg   e_iK      ?=- rms uncertainty on iK
      39  A1    ---   n_iK      [*] * for fixed value (3)
  42- 44  I3    deg     PA1     ? Morphological position angle
      45  A1    ---   r_PA1     [M] Reference for PA1 (4)
      46  A1    ---     ---     [/]
  47- 48  I2    deg     PA2     ? Morphological position angle
  49- 50  A2    ---   r_PA2     [Ha ] Reference for PA2 (4)
      51  A1    ---     ---     [/]
  52- 54  I3    deg     PA3     ? Morphological position angle
  55- 56  A2    ---   r_PA3     [M Pa Va] Reference for PA3 (4)
      57  A1    ---     ---     [/]
  58- 60  I3    deg     PA4     ? Morphological position angle
  61- 62  A2    ---   r_PA4     [Ha M Ni Pa] Reference for PA4 (4)
      63  A1    ---     ---     [/]
  64- 66  I3    deg     PA      ? Morphological position angle
  67- 68  A2    ---   r_PA      [Ha M Ni Pa A Sp] Reference for PA (4)
  70- 71  I2    deg   e_PA      ?=- rms uncertainty on PA
  73- 75  I3    deg     PA-FP   ? Position angle deduced from our velocity field
      76  A1    ---   n_PA-FP   [a] a indicates that the position angle refers
                                    to the approaching side
  78- 79  I2    deg   e_PA-FP   ? rms uncertainty on PA-FP
      80  A1    ---   f_PA-FP   [*] * for PA that have been fixed equal to
                                    morphological value
      82  A1    ---   l_Vres    Limit flag on Vres
  83- 89  F7.1   m/s    Vres    ? Mean residual velocity on the whole velocity
                                  field
  91- 92  I2    km/s    sigres  ? Residual velocity dispersion on the whole
                                  velocity field
  94- 97  F4.1  ---     chi2    ? Reduced {chi}^2^ of the model
--------------------------------------------------------------------------------
Note (3): Those marked with an asterisk (*) have been fixed equal to
     morphological value from HyperLeda, except UGC 9649, UGC 10359,
     UGC 10470 for which we used morphological inclinations from NED, and
     UGC 508, UGC 2023, UGC 2034, UGC 2455, UGC 4499, UGC 6118, UGC 6628,
     UGC 9013, UGC 9363, UGC 10791 and UGC 12632 for which we used
     inclinations determined from HI data (see tableb3.dat).
Note (4): Morphological position angle from HyperLeda, except for those
     marked as follows:
      Ha = Haynes et al., 1999AJ....117.1668H
      Ni = Nilson, 1973, Cat. VII/26
      Pa = Paturel et al., 2000A&AS..146...19P
      S  = 2006 Sloan Digital Sky Survey, DR5, http://www.sdss.org
      Sp = Springob et al., 2007, Cat. J/ApJS/172/599
      M  = Two-Micron All-Sky Survey team 2003,
            2MASS extended objects, Cat. VII/233
      Va = Vauglin et al., 1999, Cat. J/A+AS/135/133
--------------------------------------------------------------------------------

Byte-by-byte Description of file: tableb3.dat
--------------------------------------------------------------------------------
   Bytes Format Units    Label   Explanations
--------------------------------------------------------------------------------
   1-  9  A9    ---      Name    Galaxy name
  11- 14  F4.1  ---      T       Morphological type from the de Vaucouleurs
                                 classification (de Vaucouleurs 1979, VII/155)
                                 in HyperLeda data base
  16- 18  F3.1  ---    e_T       rms uncertainty on T Type
  20- 30  A11   ---      MType   Morphological type from HyperLeda data base
  32- 36  F5.1  Mpc      Dist    Distance (5)
  37- 38  A2    ---    r_Dist    Reference for Distance (6)
  40- 44  F5.1  mag      BMAG    ? Absolute B magnitude from Dist and apparent
                                   corrected B magnitude (HyperLeda)
  46- 49  F4.2  ---      b/a     Axis ratio from HyperLeda
  51- 54  F4.2  ---    e_b/a     rms uncertainty on b/a
  56- 57  I2    deg      i       Inclination derived from the axis ratio
                                  (arccos(b/a))
  59- 60  I2    deg    e_i       rms uncertainty on i
  62- 65  I4    arcsec   D25     Isophotal radius at the limiting surface
                                  brightness of 25 Bmag/arcsec^2^, in arcsec (7)
  67- 68  I2    arcsec e_D25     rms uncertainty on D25
      69  A1    ---     ---      [/]
  70- 73  F4.1  kpc      D25kpc  Isophotal radius at the limiting surface
                                  brightness of 25 Bmag/arcsec^2^, in kpc (7)
  75- 77  F3.1  kpc    e_D25kpc  rms uncertainty on D25kpc
      78  A1    ---    r_D25     [*] an asterisk (*) indicates that the galaxy
                                     is larger than GHASP field of view
  80- 83  I4    km/s     Vmax    ? Maximum velocity
  85- 87  I3    km/s   e_Vmax    ? rms uncertainty on Vmax
  88- 89  A2    ---    n_Vmax    [PV ] PV = Vmax from Position-Velocity diagram
                                       (from fit of velocity field otherwise)
      91  I1    ---    f_Vmax    [1/4]? Vmax reached (8)
      93  A1    ---      HI      [VW] VLA or WHISP data
  95- 97  A3    ---    r_HI      References for aperture synthesis HI data (9)
--------------------------------------------------------------------------------
Note (5): Distance, deduced from the systemic velocity taken in NED corrected
     from Virgo infall, assuming H_0_=75km/s/Mpc, except for those marked
Note (6): References for systemic velocity as follows:
     Ja = James et al., 2004, Cat. J/A+A/414/23
     Ka = Karachentsev et al., 2004, Cat. J/AJ/127/2031
     Ko = Koopmann, Haynes & Catinella, 2006, Cat. J/AJ/131/716
     Mo = Moustakas & Kennicutt, 2006, Cat. J/ApJS/164/8
     Oc = O'Connell, Gallagher & Hunter, 1994ApJ...433...65O
     Sa = Saha et al., 2006ApJS..165..108S
     Sh = Shapley, Fabbiano & Eskridge, 2001ApJS..137..139S
     Tu = Tully et al., 1996, Cat. J/AJ/112/2471
Note (7): From HyperLeda (Paturel et al., 1991A&A...243..319P, Cat. VII/237)
     adopting the distance given in column Dist
Note (8): this indicates whether Vax is:
      1 = reached
      2 = probably reached
      3 = probably not reached
      4 = not reached
Note (9): References for aperture synthesis HI data as follows:
     S02 = Swaters et al., 2002A&A...390..829S
     N05 = Noordermeer et al., 2005, Cat. J/A+A/442/137,
           http://www.astro.rug.nl/whisp
     I94 = Irwin, 1994ApJ...429..618I
     R94 = Rownd, Dickey & Helou, 1994AJ....108.1638R
     S96 = Schulman et al., 1996AJ....112..960S
     L98 = Laine & Gottesman, 1998MNRAS.297.1041L
     K00 = Kornreich et al., 2000AJ....120..139K
     W01 = Wilcots, Turnbull & Brinks, 2001ApJ...560..110W
     W02 = Williams, Yun & Verdes-Montenegro, 2002AJ....123.2417W
     W04 = Wilcots & Prescott, 2004AJ....127.1900W
--------------------------------------------------------------------------------

Byte-by-byte Description of file: tablef.dat
--------------------------------------------------------------------------------
   Bytes Format Units     Label  Explanations
--------------------------------------------------------------------------------
   1-  8  A8    ---       Name   Galaxy name
  10- 14  F5.2  kpc       r      Galactic radius, in kpc
  16- 19  F4.2  kpc     e_r      Dispersion around the galactic radius in kpc
  21- 25  F5.1  arcsec    r2     Galactic radius, in arcsec
  27- 30  F4.1  arcsec  e_r2     Dispersion around the galactic radius in arcsec
  32- 34  I3    km/s      Vrot   Rotation velocity
  36- 38  I3    km/s    e_Vrot   Dispersion on the rotation velocity
  40- 41  I2    ---       Nbins  Number of velocity bins
      43  A1    ---       Side   [ar] Receding - r - or approaching - a - side
--------------------------------------------------------------------------------

History:
    From electronic version of the journal

References:
    Garrido et al., Paper I          2002A&A...387..821G
    Garrido et al., Paper II         2003A&A...399...51G
    Garrido et al., Paper III        2004MNRAS.349..225G
    Garrido et al., Paper IV         2005MNRAS.362..127G
    Spano et al.,   Paper V          2008MNRAS.383..297S
    Epinat et al.,  Paper VI         2008MNRAS.388..500E, Cat. J/MNRAS/388/50
================================================================================
(End)                                      Patricia Vannier [CDS]    22-Mar-2010
