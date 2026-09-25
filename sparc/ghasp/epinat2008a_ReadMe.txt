J/MNRAS/388/500    GHASP: H{alpha} data cubes for 108 galaxies   (Epinat+, 2008)
================================================================================
GHASP: an H{alpha} kinematic survey of spiral and irregular galaxies.
VI. New H{alpha} data cubes for 108 galaxies.
    Epinat B., Amram P., Marcelin M., Balkowski C., Daigle O., Hernandez O.,
    Chemin L., Carignan C., Gach J.-L., Balard P.
   <Mon. Not. R. Astron. Soc., 388, 500-550 (2008)>
   =2008MNRAS.388..500E
================================================================================
ADC_Keywords: Galaxy catalogs ; Radial velocities ; Morphology
Keywords: galaxies: dwarf - galaxies: irregular -
          galaxies: kinematics and dynamics - galaxies: spiral

Abstract:
    We present the Fabry-Perot observations obtained for a new set of 
    108 galaxies in the frame of the Gassendi H{alpha} survey of SPirals
    (GHASP). The GHASP survey consists of 3D H{alpha} data cubes for 203
    spiral and irregular galaxies, covering a large range in morphological
    types and absolute magnitudes, for kinematics analysis. The new set of
    data presented here completes the survey. The GHASP sample is by now
    the largest sample of Fabry-Perot data ever published. The analysis of
    the whole GHASP sample will be done in forthcoming papers. Using
    adaptive binning techniques based on Voronoi tessellations, we have
    derived H{alpha} data cubes from which are computed H{alpha} maps,
    radial velocity fields as well as residual velocity fields,
    position-velocity diagrams, rotation curves and the kinematical
    parameters for almost all galaxies.

Description:
    The GHASP survey was originally selected to be a subsample
    complementing the radio survey Westerbork survey of HI in SPirals
    galaxies (WHISP) providing HI distribution and velocity maps for
    about 400 galaxies (http://www.astro.rug.nl/whisp). The first set of
    GHASP galaxies was selected from the first WHISP website list but some
    of them have never been observed by WHISP.

File Summary:
--------------------------------------------------------------------------------
 FileName   Lrecl  Records   Explanations
--------------------------------------------------------------------------------
ReadMe         80        .   This file
tablec1.dat    70      120   Log of the observations
tablec2.dat    95      108   Model parameters
tablec3.dat    94      108   Galaxy parameters
tablef.dat     44     5505   Rotation curves for 93 galaxies
--------------------------------------------------------------------------------

See also:
  J/A+AS/137/495 : Halpha Catalogue of HCG Galaxies (Severgnini+, 1999)
  J/ApJ/704/1657 : Halpha rotation curves for 10 spiral galaxies (Fathi+, 2009)

Byte-by-byte Description of file: tablec1.dat
--------------------------------------------------------------------------------
   Bytes Format Units      Label     Explanations
--------------------------------------------------------------------------------
   1-  9  A9    ---        Name      Name of the galaxy
  11- 15  A5    ---        NGC       ? Name in the NGC catalogue when available
  17- 18  I2    h          RAh       Right ascension (J2000) (1)
  20- 21  I2    min        RAm       Right ascension (J2000) (1)
  23- 26  F4.1  s          RAs       Right ascension (J2000) (1)
      28  A1    ---        DE-       Declination sign (J2000) (1)
  29- 30  I2    deg        DEd       Declination (J2000) (1)
  32- 33  I2    arcmin     DEm       Declination (J2000) (1)
  35- 36  I2    arcsec     DEs       Declination (J2000) (1)
      37  A1    ---        H         [H] H when position from HyperLeda
  39- 44  F6.1  0.1nm      lamc      Central wavelength of the interference
                                      filter used
  46- 49  F4.1  0.1nm      FWHM      FWHM of the interference filter
  51- 60  A10 "YYYY/MM/DD" Date      Date of the observations
  62- 66  I5    s          ExpTime   Total exposure time
  68- 70  F3.1  arcsec     Seeing    Seeing
--------------------------------------------------------------------------------
Note (1): Position of the centre of the galaxy used for the kinematic study
     except for those with r_Pos=H (taken from HyperLeda).
--------------------------------------------------------------------------------

Byte-by-byte Description of file: tablec2.dat
--------------------------------------------------------------------------------
   Bytes Format Units   Label     Explanations
--------------------------------------------------------------------------------
   1-  9  A9    ---     Name      Name
  11- 14  I4    km/s    Vsys-L    Systemic velocity found in HyperLeda data base
  16- 17  I2    km/s  e_Vsys-L    rms uncertainty on Vsys-LEDA
  19- 22  I4    km/s    Vsys-FP   ? Systemic velocity deduced from our velocity
                                    field analysis
  24- 25  I2    km/s  e_Vsys-FP   ? rms uncertainty on Vsys-FP
  27- 28  I2    deg     i-L       Morphological inclination from HyperLeda
  30- 31  I2    deg   e_i-L       ? rms uncertainty on Imorph
  33- 34  I2    deg     i-FP      ? Inclination deduced from the analysis of our
                                    velocity field
  36- 37  I2    deg   e_i-FP      ? rms uncertainty on I-FP
      38  A1    ---   n_i-FP      [*c] Inclination not from optical data (1)
  40- 42  I3    deg     PA-L      ? Morphological position angle from LEDA
                                    except for those marked
  43- 44  A2    ---   r_PA-L      Reference for PA (2)
      45  A1    ---     ---       [/]
  46- 48  I3    deg     PA2       ? Morphological position angle
  49- 50  A2    ---   r_PA2       Reference for PA2 (2)
      51  A1    ---     ---       [/]
  52- 54  I3    deg     PA3       ? Morphological position angle
  55- 56  A2    ---   r_PA3       Reference for PA3 (2)
      57  A1    ---     ---       [/]
  58- 60  I3    deg     PA4       ? Morphological position angle
  61- 62  A2    ---   r_PA4       Reference for PA4 (2)
      63  A1    ---     ---       [/]
  64- 65  I2    deg     PA5       ? Morphological position angle
      66  A1    ---   r_PA5       Reference for PA5 (2)
  68- 69  I2    deg   e_PA5       ? rms uncertainty on PAmorph
  71- 73  I3    deg     PA-FP     ? Kinematical major axis position angle,
                                    deduced from our velocity field
      74  A1    ---   f_PA-FP     [s] s when PA refers to the approaching side
  76- 77  I2    deg   e_PA-FP     ? rms uncertainty on PA-FP
      78  A1    ---   n_PA-FP     [*] * for fixed PA
      80  A1    ---   l_Vres      Limit flag on Vres
  81- 87  F7.1  m/s     Vres      ? Mean residual velocity in the whole
                                    velocity field
  89- 90  I2    km/s    sigres    ? Residual velocity dispersion in the whole
                                    velocity field
  92- 95  F4.1  ---     chi2      ? Reduced {chi}^2^ of the model
--------------------------------------------------------------------------------
Note (1): Note as follows:
      * = inclinations have been fixed equal to morphological value
      c = inclinations determined from HI data (see Table C3)
Note (2): References for Morphological position angle as follows:
     Ha = Haynes et al., 1999AJ....117.1668H
     Ni = Nilson, 1973, Cat. <VII/26>
     PA = Paturel et al., 2000A&AS..146...19P
     S  = SDSS, 2006, http://www.sdss.org
     M  = 2MASS team 2003, 2MASS extended objects
     Va = Vauglin et al., 1999, Cat. <J/A+AS/135/133>
--------------------------------------------------------------------------------

Byte-by-byte Description of file: tablec3.dat
--------------------------------------------------------------------------------
   Bytes Format Units     Label  Explanations
--------------------------------------------------------------------------------
   1-  9  A9    ---       Name   Name
  11- 14  F4.1  ---       T      RC3 morphological type from HyperLeda data base
  16- 18  F3.1  ---     e_T      rms uncertainty on  T
  20- 30  A11   ---       MType  Morphological type from the HyperLeda data base
  32- 36  F5.1  Mpc       Dist   Distance (1)
  37- 38  A2    ---     r_Dist   Distance reference (2)
  40- 44  F5.1  mag       BMAG   ? Absolute B magnitude
  46- 49  F4.2  ---       b/a    Axial ratio from HyperLeda
  51- 54  F4.2  ---     e_b/a    rms uncertainty on b/a
  56- 57  I2    deg       i      Inclination derived from the axial ratio,
                                  arccos(b/a)
  59- 60  I2    deg     e_i      rms uncertainty on i
  62- 64  I3   arcsec     D25    Isophotal radius at the limiting surface
                                 brightness of 25Bmag/arcsec^2^
  66- 67  I2   arcsec   e_D25    rms uncertainty on D25
      68  A1    ---     ---      [/]
  69- 72  F4.1  kpc       D25kpc D25 Isophotal radius in kpc
  74- 76  F3.1  kpc     e_D25kpc rms uncertainty on D25kpc
      77  A1    ---     n_D25kpc [*] * when galaxy is larger than GHASP
                                     field-of-view
  79- 81  I3    km/s      Vmax   ? Maximum velocity (3)
  83- 85  I3    km/s    e_Vmax   ? rms uncertainty on Vmax
  86- 87  A2    ---     n_Vmax   [PV] Vmax from position-velocity diagram (3)
      89  I1    ---     q_Vmax   [1/4]? Quality flag on Vmax (5)
  91- 94  A4    ---       HIdata Aperture synthesis HI data references (4)
--------------------------------------------------------------------------------
Note (1): Deduced from the systemic velocity taken in NED corrected from
     Virgo infall, assuming H0=75km/s/Mpc, except for those marked
Note (2): Distance references as follow:
     Ja = James et al., 2004, Cat. <J/A+A/414/23>
     Ka = Karachentsev et al., 2004, Cat. <J/AJ/127/2031>
     Ko = Koopmann, Haynes & Catinella, 2006, Cat. <J/AJ/131/716>
     Mo = Moustakas & Kennicutt, 2006, Cat. <J/ApJS/164/81>
     Oc = O'Connell, Gallagher & Hunter, 1994ApJ...433...65O
     Sh = Shapley, Fabbiano & Eskridge, 2001ApJS..137..139S
Note (3): derived from the fit of the velocity field discussed in 
     Section 3.2, or from the position-velocity diagram, if n_Vmax=PV
Note (4): References as follows:
   WS02 = W for WHISP data, Swaters et al., 2002A&A...390..829S
   WN05 = W for WHISP data, Noordermeer et al. 2005, Cat. <J/A+A/442/137>
   WWeb = W for WHISP data, http://www.astro.rug.nl/whisp
   VI94 = V for VLA data, Irwin, 1994ApJ...429..618I
   VR94 = V for VLA data, Rownd et al., 1994AJ....108.1638R
   VS96 = V for VLA data, Schulman et al., 1996AJ....112..960S
   VK00 = V for VLA data, Kornreich et al., 2000AJ....120..139K
   VW01 = V for VLA data, Wilcots et al., 2001ApJ...560..110W
   VW04 = V for VLA data, Wilcots & Prescott, 2004AJ....127.1900W
Note (5): Quality value indicates the following:
      1 = reached,
      2 = probably reached, 
      3 = probably not reached
      4 = not reached
--------------------------------------------------------------------------------

Byte-by-byte Description of file: tablef.dat
--------------------------------------------------------------------------------
   Bytes Format Units    Label  Explanations
--------------------------------------------------------------------------------
   1-  9  A9    ---      Name   Name of the galaxy
  11- 15  F5.2  kpc      r      Galactic radius in kpc
  17- 20  F4.2  kpc    e_r      Dispersion around the galactic radius in kpc
  22- 26  F5.1  arcsec   r2     Galactic radius in arcsec
  28- 31  F4.1  arcsec e_r2     Dispersion around the galactic radius in arcsec
  33- 35  I3    km/s     Vrot   Rotation velocity
  37- 39  I3    km/s   e_Vrot   Dispersion on the rotation velocity
  41- 42  I2    ---      NBins  Number of velocity bins
      44  A1    ---      Side   [ar] Receding - r - or approaching - a - side
--------------------------------------------------------------------------------

History:
    From electronic version of the journal

References:
    Garrido et al., Paper I           2002A&A...387..821G
    Garrido et al., Paper II          2003A&A...399...51G
    Garrido et al., Paper III         2004MNRAS.349..225G
    Garrido et al., Paper IV          2005MNRAS.362..127G
    Spano et al.,   Paper V           2008MNRAS.383..297S
    Epinat et al.,  Paper VII         2008MNRAS.390..466E
================================================================================
(End)                                      Patricia Vannier [CDS]    30-Nov-2009
