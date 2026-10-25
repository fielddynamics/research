# Galaxy Catalog

> **Note:** this page documents the separate Field Dynamics web API at `api.fielddynamics.org`. It is kept for reference; the service may be offline, and it is not part of the documentation app.

The SPARC data endpoints provide access to the full catalog of 175 galaxies from the Spitzer Photometry and Accurate Rotation Curves database (Lelli, McGaugh, Schombert 2016).

## Single Galaxy

**GET** `/v1/sparc/{name}`

Returns the full rotation curve data and metadata for a single galaxy. This is the primary data retrieval endpoint: pass a galaxy name and receive all tabulated columns from the SPARC database.

```python
import requests

resp = requests.get(
    "https://api.fielddynamics.org/v1/sparc/NGC3198"
)
galaxy = resp.json()

# galaxy["name"]                    -> "NGC3198"
# galaxy["distance_mpc"]            -> 13.8
# galaxy["luminosity_3_6um"]        -> 38.279
# galaxy["disk_scale_length_kpc"]   -> 3.14
# galaxy["data"]["radius_kpc"]      -> [0.32, 0.64, ...]
# galaxy["data"]["v_obs_km_s"]      -> [51.0, 84.0, ...]
```

### Response fields

| Field | Description |
|-------|-------------|
| `name` | Galaxy identifier |
| `distance_mpc` | Distance in megaparsecs |
| `inclination_deg` | Disk inclination angle |
| `luminosity_3_6um` | Spitzer 3.6 micron luminosity (10^9 L_sun) |
| `disk_scale_length_kpc` | Exponential disk scale length |
| `hi_mass_1e9_msun` | Neutral hydrogen mass (10^9 M_sun) |
| `quality` | Data quality flag (1 = best) |
| `points` | Number of rotation curve measurements |
| `data.radius_kpc` | Galactocentric radii |
| `data.v_obs_km_s` | Observed circular velocities |
| `data.e_v_obs_km_s` | Velocity measurement errors |
| `data.v_gas_km_s` | Gas contribution to rotation curve |
| `data.v_disk_km_s` | Disk contribution to rotation curve |
| `data.v_bul_km_s` | Bulge contribution to rotation curve |

## Catalog

**GET** `/v1/sparc/catalog`

Returns summary metadata for all 175 galaxies. Use this to browse the database or filter by quality or Hubble type before fetching individual galaxies.

```python
import requests

resp = requests.get(
    "https://api.fielddynamics.org/v1/sparc/catalog"
)
catalog = resp.json()

# catalog["galaxies"]  -> list of 175 galaxy metadata objects
# catalog["count"]     -> 175
```

### Optional query parameters

| Parameter | Description |
|-----------|-------------|
| `quality` | Filter by quality flag (1, 2, or 3) |
| `hubble_type` | Filter by Hubble type code |
