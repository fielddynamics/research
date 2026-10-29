# Reference data: sources

`atomic_reference.csv` collects every reference value used by the baseline comparison. The values are those already used by the test suites in this folder, now in one auditable file, with a column of independent empirical radii added.

| Column | Quantity | Source |
|---|---|---|
| `n` | Principal quantum number of the outermost occupied shell | Ground-state electron configuration |
| `zeff_clementi` | Effective nuclear charge of the outermost orbital | Clementi, E. and Raimondi, D. L. (1963), *J. Chem. Phys.* 38, 2686; Clementi, E., Raimondi, D. L. and Reinhardt, W. P. (1967), *J. Chem. Phys.* 47, 1300 |
| `r_clementi_pm` | Calculated atomic radius: radius of maximum radial density of the outermost orbital, from SCF functions | Clementi, Raimondi and Reinhardt (1967) |
| `r_covalent_cordero_pm` | Covalent radius from crystallographic bond lengths (an independent, empirical radius) | Cordero, B. et al. (2008), Covalent radii revisited, *Dalton Trans.* 2832, doi:10.1039/b801115j |
| `alpha_A3` | Static electric dipole polarisability (Å³) | CRC Handbook of Chemistry and Physics; cf. Schwerdtfeger, P. and Nagle, J. K. (2019), 2018 Table of static dipole polarizabilities of the neutral elements, *Mol. Phys.* 117, 1200 |
| `ie_eV` | First ionisation energy | NIST Atomic Spectra Database |
| `ea_eV` | Electron affinity (positive = energy released) | CRC Handbook; NIST |
| `en_pauling` | Pauling electronegativity (blank for He, Ne, Ar) | Pauling scale, CRC Handbook |

Uncertainties are not yet recorded per value. For polarisabilities the 2018 table quotes uncertainties of a few per cent for most light elements; aluminium is a known case where older handbook values (6.8 Å³) differ from the recommended value (57.8 a.u. = 8.57 Å³).
