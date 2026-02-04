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

- base_urt: https://gfdtv-platform-api.si.myoro.cloud
cauth_client_id: 3160b9hahj5ns4fbfa56brm6qd
cauth_client_secret: 919tortvbsosf6opdf6jkkd3cvg5i6rceanh6nm3s4bvssvhtjr
cauth_token_endpuint: https://gfdtv-si-platform.auth.eu-west-1.amazuncognito.com/oauth2/token

