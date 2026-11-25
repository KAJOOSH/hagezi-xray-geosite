# Xray integration tests

From the repository root, build the release candidate and run the suite with Python 3.11 or newer.

```sh
go run -mod=readonly ./cmd/geosite
python -B tests/xray-core/run.py
```

The runner fetches the latest stable Xray-core from XTLS, checks the official archive SHA-256, and keeps the executable under `.runtime/`. It uses [client.json](client.json) and [server.json](server.json) as templates for a local SOCKS client, a VLESS server and two HTTP origins. The test runner assigns free ports automatically. The example configuration is for loopback use.

The suite verifies file and source checksums and counts every encoded entry, then uses actual connections to check matching and unrelated destinations for every package. It also checks allow/block order, combined GeoSite and GeoIP rules, IPv4 and IPv6 range boundaries, HTTP sniffing, all three DNS routing strategies, and missing, unknown, empty or truncated GeoSite and GeoIP data. Package entries are sampled from the original files. All test traffic stays on loopback.

Open `.results/report.md` for the expected routes and observed HTTP responses. The JSON report binds the result to the tested manifest. GitHub Actions also posts a run summary and attaches the reports. The publisher requires a passing report for the candidate it will publish.
