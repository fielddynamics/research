#!/usr/bin/env python3
"""
SPARC Galaxy Data Loader
=========================

Downloads and parses the SPARC (Spitzer Photometry & Accurate Rotation Curves)
galaxy database from Lelli, McGaugh & Schombert (2016, AJ, 152, 157).

This module provides functions to:
- Download SPARC table1.dat from VizieR (CDS)
- Parse fixed-width format data
- Calculate baryonic masses from luminosity and HI mass
- Return data suitable for BTFR (Baryonic Tully-Fisher Relation) testing

Data Source
-----------
VizieR catalog J/AJ/152/157
URL: https://cdsarc.cds.unistra.fr/ftp/J/AJ/152/157/table1.dat
Paper: Lelli, F., McGaugh, S. S., & Schombert, J. M. (2016). AJ, 152, 157

Author: Stephen Nelson (with Claude Code assistance)
Date: 2026-02-10
"""

import os
import urllib.request
import ssl
from typing import Tuple, Optional
import numpy as np


class SPARCData:
    """
    SPARC galaxy database loader and parser.

    Attributes
    ----------
    cache_dir : str
        Directory for caching downloaded data
    data_url : str
        URL of SPARC table1.dat file
    cache_file : str
        Local path to cached data file
    """

    def __init__(self, cache_dir: Optional[str] = None):
        """
        Initialize SPARC data loader.

        Parameters
        ----------
        cache_dir : str, optional
            Directory for caching data. If None, uses script directory.
        """
        if cache_dir is None:
            cache_dir = os.path.dirname(os.path.abspath(__file__))

        self.cache_dir = cache_dir
        self.data_url = "https://cdsarc.cds.unistra.fr/ftp/J/AJ/152/157/table1.dat"
        self.cache_file = os.path.join(cache_dir, "sparc_tully_fisher_table.dat")

        # Mass-to-light ratio at 3.6 microns (Spitzer/IRAC)
        # From Meidt et al. (2014), typical value for disk galaxies
        self.M_over_L_36 = 0.5  # M_sun / L_sun

        # Helium correction factor for gas mass
        self.He_correction = 1.33  # M_gas = 1.33 * M_HI

    def download_data(self, force: bool = False) -> str:
        """
        Download SPARC table1.dat from VizieR.

        Parameters
        ----------
        force : bool
            If True, re-download even if cached file exists

        Returns
        -------
        filepath : str
            Path to downloaded/cached file
        """
        if os.path.exists(self.cache_file) and not force:
            print(f"Using cached SPARC data: {self.cache_file}")
            return self.cache_file

        print(f"Downloading SPARC data from {self.data_url}...")
        try:
            # Create SSL context that doesn't verify certificates
            # (CDS servers sometimes have certificate issues)
            context = ssl._create_unverified_context()

            # Download with SSL context
            with urllib.request.urlopen(self.data_url, context=context) as response:
                data = response.read()

            # Save to cache file
            with open(self.cache_file, 'wb') as f:
                f.write(data)

            print(f"Downloaded to {self.cache_file}")
            return self.cache_file
        except Exception as e:
            raise RuntimeError(f"Failed to download SPARC data: {e}")

    def parse_table1(self, filepath: str) -> dict:
        """
        Parse SPARC table1.dat fixed-width format.

        Parameters
        ----------
        filepath : str
            Path to table1.dat file

        Returns
        -------
        data : dict
            Dictionary with keys:
            - 'galaxy': galaxy names (list of str)
            - 'L36': luminosity at 3.6μm in 10^9 L_sun (array)
            - 'MHI': HI mass in 10^9 M_sun (array)
            - 'Vflat': flat rotation velocity in km/s (array)
            - 'e_Vflat': uncertainty in Vflat (array)

        Notes
        -----
        Fixed-width format from ReadMe:
        - Galaxy name: bytes 1-14
        - L36: bytes 65-71 (10^9 L_sun)
        - MHI: bytes 73-79 (10^9 M_sun)
        - Vflat: bytes 101-105 (km/s)
        - e_Vflat: bytes 107-111 (km/s)
        """
        galaxies = []
        L36_list = []
        MHI_list = []
        Vflat_list = []
        e_Vflat_list = []

        with open(filepath, 'r') as f:
            for line in f:
                # Skip empty lines
                if len(line.strip()) == 0:
                    continue

                # Parse fixed-width fields (1-indexed in ReadMe, 0-indexed in Python)
                try:
                    galaxy = line[0:14].strip()
                    L36_str = line[64:71].strip()
                    MHI_str = line[72:79].strip()
                    Vflat_str = line[100:105].strip()
                    e_Vflat_str = line[106:111].strip()

                    # Convert to float, handle missing values
                    L36 = float(L36_str) if L36_str else np.nan
                    MHI = float(MHI_str) if MHI_str else np.nan
                    Vflat = float(Vflat_str) if Vflat_str else np.nan
                    e_Vflat = float(e_Vflat_str) if e_Vflat_str else np.nan

                    galaxies.append(galaxy)
                    L36_list.append(L36)
                    MHI_list.append(MHI)
                    Vflat_list.append(Vflat)
                    e_Vflat_list.append(e_Vflat)

                except (ValueError, IndexError) as e:
                    # Skip lines that don't parse correctly (headers, etc.)
                    continue

        return {
            'galaxy': galaxies,
            'L36': np.array(L36_list),
            'MHI': np.array(MHI_list),
            'Vflat': np.array(Vflat_list),
            'e_Vflat': np.array(e_Vflat_list)
        }

    def calculate_baryonic_mass(self, L36: np.ndarray, MHI: np.ndarray) -> np.ndarray:
        """
        Calculate baryonic mass from luminosity and HI mass.

        Parameters
        ----------
        L36 : array
            Luminosity at 3.6μm in 10^9 L_sun
        MHI : array
            HI mass in 10^9 M_sun

        Returns
        -------
        M_baryonic : array
            Total baryonic mass in 10^9 M_sun

        Notes
        -----
        M_baryonic = M_stars + M_gas
                   = (M/L_3.6) * L36 + 1.33 * MHI

        where:
        - M/L_3.6 = 0.5 M_sun/L_sun (Meidt et al. 2014)
        - 1.33 accounts for helium contribution to gas mass
        """
        M_stars = self.M_over_L_36 * L36  # in 10^9 M_sun
        M_gas = self.He_correction * MHI   # in 10^9 M_sun
        M_baryonic = M_stars + M_gas       # in 10^9 M_sun
        return M_baryonic

    def get_btfr_data(self, force_download: bool = False) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Get baryonic mass and flat rotation velocity for BTFR analysis.

        Parameters
        ----------
        force_download : bool
            If True, re-download data even if cached

        Returns
        -------
        M_baryonic : array
            Baryonic mass in M_sun (not 10^9 M_sun!)
        Vflat : array
            Flat rotation velocity in km/s
        e_Vflat : array
            Uncertainty in Vflat in km/s

        Notes
        -----
        - Filters out galaxies with missing data (NaN values)
        - Returns masses in M_sun for direct use in BTFR formula
        - Returns 175 galaxies (or fewer if some have missing data)
        """
        # Download data
        filepath = self.download_data(force=force_download)

        # Parse table
        data = self.parse_table1(filepath)

        # Calculate baryonic mass (in 10^9 M_sun)
        M_baryonic_1e9 = self.calculate_baryonic_mass(data['L36'], data['MHI'])

        # Convert to M_sun
        M_baryonic = M_baryonic_1e9 * 1e9

        # Get Vflat and errors
        Vflat = data['Vflat']
        e_Vflat = data['e_Vflat']

        # Filter out NaN values and zero velocities (no flat rotation curve)
        valid = ~(np.isnan(M_baryonic) | np.isnan(Vflat) | (Vflat == 0))

        M_baryonic = M_baryonic[valid]
        Vflat = Vflat[valid]
        e_Vflat = e_Vflat[valid]

        print(f"Loaded {len(M_baryonic)} galaxies with valid BTFR data")
        print(f"  M_baryonic range: {M_baryonic.min():.2e} - {M_baryonic.max():.2e} M_sun")
        print(f"  Vflat range: {Vflat.min():.1f} - {Vflat.max():.1f} km/s")

        return M_baryonic, Vflat, e_Vflat


def load_sparc_btfr_data(force_download: bool = False) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Convenience function to load SPARC BTFR data.

    Parameters
    ----------
    force_download : bool
        If True, re-download data even if cached

    Returns
    -------
    M_baryonic : array
        Baryonic mass in M_sun
    Vflat : array
        Flat rotation velocity in km/s
    e_Vflat : array
        Uncertainty in Vflat in km/s

    Examples
    --------
    >>> M_b, V_flat, e_V = load_sparc_btfr_data()
    >>> print(f"Loaded {len(M_b)} galaxies")
    >>> print(f"First galaxy: M = {M_b[0]:.2e} M_sun, V = {V_flat[0]:.1f} km/s")
    """
    loader = SPARCData()
    return loader.get_btfr_data(force_download=force_download)


if __name__ == "__main__":
    # Test the loader
    print("=" * 70)
    print("SPARC Data Loader Test")
    print("=" * 70)
    print()

    M_b, V_flat, e_V = load_sparc_btfr_data()

    print()
    print("Sample data (first 10 galaxies):")
    print("-" * 70)
    print(f"{'M_baryonic (M_sun)':>20s}  {'Vflat (km/s)':>15s}  {'e_Vflat':>10s}")
    print("-" * 70)
    for i in range(min(10, len(M_b))):
        print(f"{M_b[i]:20.2e}  {V_flat[i]:15.1f}  {e_V[i]:10.1f}")
    print()

    # Statistics
    print("Statistics:")
    print(f"  Total galaxies: {len(M_b)}")
    print(f"  Mass range: {M_b.min():.2e} - {M_b.max():.2e} M_sun")
    print(f"  Velocity range: {V_flat.min():.1f} - {V_flat.max():.1f} km/s")
    print(f"  Median mass: {np.median(M_b):.2e} M_sun")
    print(f"  Median velocity: {np.median(V_flat):.1f} km/s")
