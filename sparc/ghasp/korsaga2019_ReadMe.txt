J/MNRAS/482/154 GHASP. spiral galaxies dark matter distribution (Korsaga+, 2019)
================================================================================
GHASP: an H {alpha} kinematics survey of spiral galaxies -
XII. Distribution of luminous and dark matter in spiral and irregular nearby
galaxies using R_c_-band photometry.
    Korsaga M., Amram P., Carignan C., Epinat B.
   <Mon. Not. R. Astron. Soc., 482, 154-174 (2019)>
   =2019MNRAS.482..154K    (SIMBAD/NED BibCode)
================================================================================
ADC_Keywords: Galaxies, photometry ; Models
Keywords: galaxies: dwarf - galaxies: haloes -
          galaxies: kinematics and dynamics -
          galaxies: spiral, dark matter

Abstract:
    Mass models of 100 nearby spiral and irregular galaxies, covering
    morphological types from Sa to Irr, are computed using H{alpha}
    rotation curves and R_c_-band surface brightness profiles. The
    kinematics was obtained using a scanning Fabry-Perot interferometer.
    One of the aims is to compare our results with those from Korsaga et
    al. 2018MNRAS.478...50K, which used mid-infrared (MIR) WISE
    (Wide-field Infrared Survey Explorer) W1 (3.4{mu}m) photometric data.
    For the analysis, the same tools were used for both bands.
    Pseudo-isothermal (ISO) core and Navarro-Frenk-White (NFW) cuspy
    models have been used. We test best-fitting models, maximum disc
    models, and models for which mass-to-light ratio (M/L) is fixed using
    the B-V colours. Similarly to what was found in the MIR 3.4{mu}m band,
    most of the observed rotation curves are better described by a central
    core density profile (ISO) than a cuspy one (NFW) when using the
    optical R_c_ band. In both bands, the dispersion in the (M/L) values
    is smaller for the fixed M/L fits. As for the W1 photometry, the
    derived dark matter halo' parameters depend on the morphological
    types. We find similar relations than those in the literature, only
    when we compare our results for the bulge-poor sub-sample because most
    of previous results were mainly based on late-type spirals. Because
    the dispersion in the model parameters is smaller and because stellar
    masses are better defined in that band, MIR photometry should be
    preferred, when possible, to the optical bands. It is shown that for
    high-z galaxies, sensible results can still be obtained without full
    profile decomposition.

Description:
    We use a sample of 100 spiral and irregular nearby galaxies with
    high-resolution H{alpha} rotational curves (RCS), derived from 2D
    velocity fields, and the optical R_c_-band photometry: 73 from surface
    brightness photometry obtained at the Observatoire de Haute Provence
    (OHP) (Barbosa et al. 2015MNRAS.453.2965B, Cat. J/MNRAS/453/2965) and
    27 from Sloan Digital Sky Survey (SDSS) DR7 (Abazajian et al.
    2009ApJS..182..543A, Cat. II/294) archival data.
    The RCs of this sample are selected from the GHASP survey, which
    contains 203 galaxies observed with the 1.93m telescope of the OHP
    using a Fabry-Perot interferometer scanning around the H{alpha}
    emission line with high spectral and spatial resolutions. The GHASP
    data have been published in several previous papers(Garrido et al.
    2002A&A...387..821G, 2003A&A...399...51G, 2005MNRAS.362..127G;
    Garrido, Marcelin & Amram 2004MNRAS.349..225G; Epinat et al.
    2008MNRAS.388..500E, Cat. J/MNRAS/388/500, 2008MNRAS.390..466E, Cat.
    J/MNRAS/390/466).
    First, we began with 124 galaxies, which have both H{alpha} RCs and
    optical R_c_-band photometric data. Secondly, we assigned a quality
    flag to the RC of each galaxy, ranging from 1 to 3: '1'for very high,
    '2' for high, and '3' for low quality. To construct mass models with
    good constraints, we therefore selected only galaxies with flag '1'
    and '2' that reduced the sample to 100 galaxies. The 124 galaxies with
    their global properties and quality flag are listed in Table A1.

File Summary:
--------------------------------------------------------------------------------
 FileName      Lrecl  Records   Explanations
--------------------------------------------------------------------------------
ReadMe            80        .   This file
tablea1.dat       89      124   Global properties
tablea2.dat      119      100   Parameters of mass models using the BFM and
                                fixed M/L techniques with the pseudo-isothermal
                                (ISO) model
tablea3.dat       76      100   Parameters of mass models using the MDM
                                technique with the pseudo-isothermal (ISO) model
tablea4.dat      127      100   Parameters of mass models using the BFM and
                                fixed M/L techniques with the NFW model
--------------------------------------------------------------------------------

See also:
  J/MNRAS/388/500 : GHASP: H{alpha} data cubes for 108 galaxies
  J/MNRAS/401/2113 : GHASP: H{alpha} data cubes for 153 galaxies (Epinat+, 2010)
  J/MNRAS/453/2965 : Surface photometry of GHASP galaxies (Barbosa+, 2015)

Byte-by-byte Description of file: tablea1.dat
--------------------------------------------------------------------------------
   Bytes Format Units       Label   Explanations
--------------------------------------------------------------------------------
   1-  9  A9    ---         ID      Name of the galaxy in the UGC catalogue
                                     (UGC NNNNN)
      11  A1    ---       f_B-V     [*] * for galaxies with no B-V colour
                                     available in the RC3 catalogue, the value
                                     has been computed (1)
  13- 24  A12   ---         Type    Morphological type taken from the RC3
                                     catalogue (Third Reference Cat. of Bright
                                     Galaxies (RC3)
                                     de Vaucouleurs et al. 1991rc3..book.....D,
                                     Cat. VII/155) (2)
  26- 29  F4.1  mag         BMAG    Absolute B magnitude from Epinat et al.
                                     (2008MNRAS.388..500E, Cat. J/MNRAS/388/500)
  31- 34  F4.2  mag         B-V     (B-V) colours corrected for galactic and
                                     internal extinction from RC3 catalogue
                                     when available
  36- 39  F4.1  mag/arcsec2 mu0obs  Central surface brightness from the observed
                                     data
  41- 43  F3.1  ---         R25/h   Isophotal radius at the limiting surface
                                     brightness of 25mag/arcsec^2^ normalized by
                                     the disc scale length
  45- 48  F4.1  ---         Rlast/h The last radius of the RC normalized by the
                                     disc scale length
  50- 53  F4.1  mag/arcsec2 mu0     Central surface brightness of the disc
  55- 57  F3.1  kpc         h       Disc scale length of the disc component
  59- 64  F6.1  10+8Lsun    LD      Luminosity of the disc calculated at the
                                     isophotal radius
  66- 70  F5.2  mag/arcsec2 mue     ? Surface brightness of the bulge at the
                                     effective radius
  72- 75  F4.2  kpc         re      ? Effective radius of the bulge
  77- 80  F4.2  ---         n       ? Sersic index of the bulge
  82- 87  F6.2  10+8Lsun    LB      ? Luminosity of the bulge derived at the
                                     isophotal radius
      89  I1    ---       f_ID      [1/3] Classification flag of the inner
                                     galaxy rotation curves (RCs) (3)
--------------------------------------------------------------------------------
Note (1): Except for galaxies UGC 3521, 3708, 3915, 4393, 10652 for which the
          morphological types are taken from Epinat et al. (2008MNRAS.388..500E,
          Cat. J/MNRAS/388/500)
Note (2): The colour corrected for extinction (B-V) was taken directly from the
          RC3 catalogue for 62 galaxies of our sample and fitted for 38 galaxies
          using the relation (B-V)=(-0.032+/-0.004)t+(0.73+/-0.02)
Note (3): Flag as follows:
          1 = very high quality RCs
          2 = high-quality RCs
          3 = poor-quality RCs
--------------------------------------------------------------------------------

Byte-by-byte Description of file: tablea2.dat
--------------------------------------------------------------------------------
   Bytes Format Units          Label   Explanations
--------------------------------------------------------------------------------
   1-  9  A9    ---            ID      Name of the galaxy in the UGC catalogue
                                        (UGC NNNNN)
      11  A1    ---          f_ID      [*] Flag on ID * : galaxies for which the
                                        presence of dark matter is not necessary
  13- 16  F4.2  Msun/Lsun      M/LdBFM M/L of the disc from the best-fitting
                                        model (BFM) for pseudo-isothermal (ISO)
                                        core model (1)
  18- 21  F4.2  Msun/Lsun    E_M/LdBFM Upper error on M/LDBFM (1)
  23- 26  F4.2  Msun/Lsun    e_M/LdBFM Lower error on M/LDBFM (1)
  28- 32  F5.2  Msun/Lsun      M/LbBFM ? M/L of the bulge from the best-fitting
                                        model (BFM) for pseudo-isothermal (ISO)
                                        core model (1)
  34- 37  F4.2  Msun/Lsun    E_M/LbBFM ? Upper error on M/LBBFM (1)
  39- 43  F5.2  Msun/Lsun    e_M/LbBFM ? Lower error on M/LBBFM (1)
      45  A1    ---          l_r0BFM   ? Lower limit flag on r0BFM (1)
  47- 51  F5.1  kpc            r0BFM   Core radius of the dark matter halo from
                                        the best-fitting model (BFM) for
                                        pseudo-isothermal (ISO) core model (1)
  53- 57  F5.1  kpc          E_r0BFM   ? Upper error on r0BFM (1)
  59- 62  F4.1  kpc          e_r0BFM   ? Lower error on r0BFM (1)
  64- 66  I3    10-3Msun/pc3   rho0BFM Central density of the dark matter halo
                                        from the best-fitting model (BFM) for
                                        pseudo-isothermal (ISO) core model (1)
  68- 70  I3    10-3Msun/pc3 E_rho0BFM Upper error on rho0BFM (1)
  72- 74  I3    10-3Msun/pc3 e_rho0BFM Lower error on rho0BFM (1)
  76- 79  F4.1  ---            Chi2BFM Reduced chi-squared from the best-fitting
                                        model (BFM) for pseudo-isothermal (ISO)
                                        core model (1)
  81- 84  F4.2  Msun/Lsun      M/LfML  M/L derived using the B-V colour (2)
  86- 89  F4.1  kpc            r0fML   Core radius of the dark matter halo from
                                        pseudo-isothermal (ISO) core model with
                                        fixed M/L (3)
  91- 95  F5.1  kpc          E_r0fML   Upper error on r0fML (3)
  97-100  F4.1  kpc          e_r0fML   Lower error on r0fML (3)
 102-104  I3    10-3Msun/pc3   rho0fML Central density of the dark matter halo
                                        from pseudo-isothermal (ISO) core model
                                        with fixed M/L (3)
 106-108  I3    10-3Msun/pc3 E_rho0fML Upper error on rho0fML (3)
 110-112  I3    10-3Msun/pc3 e_rho0fML Lower error on rho0fML (3)
 114-119  F6.1  ---            Chi2fML Reduced chi-squared from
                                        pseudo-isothermal (ISO) core model with
                                        fixed M/L (3)
--------------------------------------------------------------------------------
Note (1): Values taken from the best fit for the pseudo-isothermal (ISO) core
          model (Begeman 1987PhDT.......199B)
Note (2): The relation between the M/L in the Rc band and the (B-V) colour
          (Bell & de Jong 2001ApJ...550..212B) is given by
          log(M/L_R_)=-0.660+1.222(B-V)
Note (3): Values taken from the pseudo-isothermal (ISO) core model fitting with
          fixed M/L, derived from the (B-V) colour
--------------------------------------------------------------------------------

Byte-by-byte Description of file: tablea3.dat
--------------------------------------------------------------------------------
   Bytes Format Units          Label   Explanations
--------------------------------------------------------------------------------
   1-  9  A9    ---            ID      Name of the galaxy in the UGC catalogue
                                        (UGC NNNNN)
  11- 15  F5.2  Msun/Lsun      M/LdMDM M/L of the disc from the
                                        pseudo-isothermal maximum disc model
                                        (MDM) (1)
  17- 20  F4.2  Msun/Lsun    E_M/LdMDM Upper error on M/LdMDM (1)
  22- 26  F5.2  Msun/Lsun    e_M/LdMDM Lower error on M/LdMDM (1)
  28- 32  F5.2  Msun/Lsun      M/LbMDM ? M/L of the disc from the
                                        pseudo-isothermal maximum disc model
                                        (MDM) (1)
  34- 38  F5.2  Msun/Lsun    E_M/LbMDM ? Upper error on M/LbMDM (1)
  40- 44  F5.2  Msun/Lsun    e_M/LbMDM ? Lower error on M/LbMDM (1)
  46- 49  F4.1  kpc            r0MDM   Core radius of the dark matter halo
                                        from the pseudo-isothermal maximum disc
                                        model (MDM) (1)
  51- 54  F4.1  kpc          E_r0MDM   Upper error on r0MDM (1)
  56- 59  F4.1  kpc          e_r0MDM   Lower error on r0MDM (1)
  61- 63  I3    10-3Msun/pc3   rho0MDM Central density of the dark matter halo
                                        from the pseudo-isothermal maximum disc
                                        model (MDM) (1)
  65- 67  I3    10-3Msun/pc3 E_rho0MDM Upper error on rho0MDM (1)
  69- 71  I3    10-3Msun/pc3 e_rho0MDM Lower error on rho0MDM (1)
  73- 76  F4.1  ---            Chi2MDM Reduced chi-squared from the
                                        pseudo-isothermal maximum disc model
                                        (MDM) (1)
--------------------------------------------------------------------------------
Note (1): Values taken from the pseudo-isothermal maximum disc fit (MDM) that
          minimizes the halo contribution by maximizing the stellar disc (and
          bulge when present) contribution.
--------------------------------------------------------------------------------

Byte-by-byte Description of file: tablea4.dat
--------------------------------------------------------------------------------
   Bytes Format Units       Label       Explanations
--------------------------------------------------------------------------------
   1-  9  A9    ---         ID          Name of the galaxy in the UGC catalogue
                                         (UGC NNNNN)
  11- 14  F4.2  Msun/Lsun   M/LdNFWBFM  M/L of the disc from the best-fitting
                                         model (BFM) for lambda-CDM cuspy
                                         density profile (1)
  16- 19  F4.2  Msun/Lsun E_M/LdNFWBFM  Upper error on M/LdNFWBFM (1)
  21- 24  F4.2  Msun/Lsun e_M/LdNFWBFM  Lower error on M/LdNFWBFM (1)
  26- 30  F5.2  Msun/Lsun   M/LbNFWBFM  ? M/L of the bulge from the best-fitting
                                         model (BFM) for lambda-CDM cuspy
                                         density profile (1)
  32- 36  F5.2  Msun/Lsun E_M/LbNFWBFM  ? Upper error on M/LbNFWBFM (1)
  38- 42  F5.2  Msun/Lsun e_M/LbNFWBFM  ? Lower error on M/LbNFWBFM (1)
  44- 47  F4.1  ---         cNFWBFM     Central halo concentration index
                                         from the best-fitting model (BFM) for
                                         lambda-CDM cuspy density profile (1)
  49- 52  F4.1  ---       E_cNFWBFM     Upper error on cNFWBFM (1)
  54- 57  F4.1  ---       e_cNFWBFM     Lower error on cNFWBFM (1)
  59- 63  F5.1  km/s        VNFWBFM     Halo velocity from the best-fitting
                                         model (BFM) for lambda-CDM cuspy
                                         density profile (1)
  65- 69  F5.1  km/s      E_VNFWBFM     Upper error on VNFWBFM (1)
  71- 75  F5.1  km/s      e_VNFWBFM     Lower error on VNFWBFM (1)
  77- 80  F4.1  ---         Chi2VNFWBFM Reduced chi-squared from the
                                         best-fitting model (BFM) for
                                         lambda-CDM cuspy density profile (1)
  82- 85  F4.2  Msun/Lsun   M/LNFWfML   M/L derived using the B-V colour (2)
  87- 91  F5.1  ---         cNFWfML     Central halo concentration index from
                                         lambda-CDM cuspy density profile
                                         fitting with fixed M/L (3)
  93- 97  F5.1  ---       E_cNFWfML     Upper error on cNFWfML (3)
  99-102  F4.1  ---       e_cNFWfML     Lower error on cNFWfML (3)
 104-108  F5.1  km/s        VNFWfML     Halo velocity from lambda-CDM cuspy
                                         density profile fitting with fixed
                                         M/L (3)
 110-114  F5.1  km/s      E_VNFWfML     Upper error on VNFWfML (3)
 116-120  F5.1  km/s      e_VNFWfML     Lower error on VNFWfML (3)
 122-127  F6.1  ---         Chi2NFWfML  Reduced chi-squared from lambda-CDM
                                         cuspy density profile fitting with
                                         fixed M/L (3)
--------------------------------------------------------------------------------
Note (1): Values taken from the best fit for the Navarro-Frenk-White (NFW)
          lambda-CDM cuspy density profile model
          (Navarro et al. 1996ApJ...462..563N)
Note (2): The relation between the M/L in the Rc band and the (B-V) colour
          (Bell & de Jong 2001ApJ...550..212B) is given by
          log(M/L_R_)=-0.660+1.222(B-V)
Note (3): Values taken from the Navarro-Frenk-White (NFW)
          lambda-CDM cuspy density profile model with fixed M/L, derived from
          the (B-V) colour
--------------------------------------------------------------------------------

History:
    From electronic version of the journal

References:
  Garrido et al.,       Paper I     2002A&A...387..821G
  Garrido et al.,       Paper II    2003A&A...399...51G
  Garrido et al.,       Paper III   2004MNRAS.349..225G
  Garrido et al.,       Paper IV    2005MNRAS.362..127G
  Spano et al.,         Paper V     2008MNRAS.383..297S
  Epinat et al.,        Paper VI    2008MNRAS.388..500E, Cat. J/MNRAS/388/500
  Epinat et al.,        Paper VII   2008MNRAS.390..466E, Cat. J/MNRAS/390/466
  Epinat et al.,        Paper VIII  2010MNRAS.401.2113E, Cat. J/MNRAS/401/2113
  Torres-Flores et al., Paper IX    2011MNRAS.416.1936T
  Barbosa et al.,       Paper X     2015MNRAS.453.2965B, Cat. J/MNRAS/453/2965
  Korsaga et al.,       Paper XI    2018MNRAS.478...50K
  Korsaga et al.,       Paper XIII  2019MNRAS.490.2977K

================================================================================
(End)                                           Ana Fiallos [CDS]    20-Jun-2022
