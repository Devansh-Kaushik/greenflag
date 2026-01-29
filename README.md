# ETA Deflection Performance Test Suite

Production-grade Locust test suite for the Green Flag `gfdtv-platform-ms-eta-deflection-update` service.

## Configuration
- **Domain**: Defaults to `si.mycro.cloud` (configurable via `BASE_DOMAIN`).
- **Auth**: Reads from `token.txt` automatically.
- **Data**: Reads from `phones.csv`.

## Quick Start (No long commands needed)
1. Ensure your active token is in `token.txt`.
2. Ensure `phones.csv` has valid test data.
3. Run:
   ```bash
   locust -f locustfile.py --headless -u 1 -r 1 -t 1m --html report.html
   ```

## Traffic Profile
- **80% Valid**: Checks Strict Business Logic (Future/Past/Present).
- **10% Invalid**: Fuzz testing.
- **10% Auth Failure**: Security testing.

## Files
- `config.py`: Configuration loader.
- `data.py`: CSV loader & invalid generator.
- `utils.py`: strict `etaTense` validation logic.
- `locustfile.py`: Main scenario definitions.
