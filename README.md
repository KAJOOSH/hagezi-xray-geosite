# HaGeZi blocklists for Xray

Choose what to block and copy the matching rule. [فارسی](README.fa.md)

## Choose a package

**Start with TIF Medium** for everyday security. Add **TIF IPv4** to block listed IP addresses. Add **Multi Pro** if you also want to filter ads and trackers.

| Family | What it covers | When to use it |
| --- | --- | --- |
| **TIF Mini, Medium, Full** | Malware, phishing and command-and-control domains | Use Mini if memory is tight, Medium for everyday protection, or Full for wider coverage. Pick one size. |
| **TIF IPv4** | Listed threat IPv4 addresses | Add it when traffic can connect straight to an IP. A listed IP can be shared with legitimate services. |
| **Fake** | Scam sites and impersonation | Use it for targeted scam filtering. It overlaps with TIF. |
| **DynDNS, Badware Hoster, high-risk domain endings** | Infrastructure frequently abused for scams or malware | Use selectively. Broad rules can block legitimate sites on the same host or domain ending. |
| **Multi, device trackers, pop-ups, referrals** | Ads and tracking, plus some threat coverage in Multi | Use for privacy and ad filtering. Pick one Multi edition. |
| **NRD and DGA** | Newly registered domains. DGA is the narrower list. | Use for stricter filtering if you can allowlist legitimate new sites. Choose NRD or DGA. |
| **DNS, VPN and content lists** | DNS services, proxies and selected site categories | Use when you have a specific filtering policy. |

## Use a package

1. Download a file below and put it next to `geosite.dat` in Xray’s assets folder.
2. Add its rule to `routing.rules` before any catch-all rule. Separate entries with commas, save and reload Xray.

Use your blocking tag in place of `BLOCK`. If you need one, append `{"tag":"BLOCK","protocol":"blackhole"}` to `outbounds`.

For an exception, use your normal outbound in place of `DIRECT` if needed. Put the exception above its block rule and below unrelated security rules.

## Packages

<details>

<summary>Security</summary>

**TIF Medium** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-tif.dat)

```json
{"type": "field", "domain": ["ext:hagezi-tif.dat:tif-medium"], "outboundTag": "BLOCK"}
```

**TIF Full** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-tif-full.dat)

```json
{"type": "field", "domain": ["ext:hagezi-tif-full.dat:tif-full"], "outboundTag": "BLOCK"}
```

**TIF Mini** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-tif-mini.dat)

```json
{"type": "field", "domain": ["ext:hagezi-tif-mini.dat:tif-mini"], "outboundTag": "BLOCK"}
```

**TIF IPv4** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-tif-ipv4.dat)

```json
{"type": "field", "ip": ["ext:hagezi-tif-ipv4.dat:tif-ipv4"], "outboundTag": "BLOCK"}
```

**Fake sites and scams** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-fake.dat)

```json
{"type": "field", "domain": ["ext:hagezi-fake.dat:fake"], "outboundTag": "BLOCK"}
```

**Dynamic DNS services** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-dyndns.dat)

```json
{"type": "field", "domain": ["ext:hagezi-dyndns.dat:dyndns"], "outboundTag": "BLOCK"}
```

**Hosts frequently used to spread malware** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-badware-hoster.dat)

```json
{"type": "field", "domain": ["ext:hagezi-badware-hoster.dat:badware-hoster"], "outboundTag": "BLOCK"}
```

**High-risk domain endings** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-spam-tlds.dat)

```json
{"type": "field", "domain": ["ext:hagezi-spam-tlds.dat:spam-tlds"], "outboundTag": "BLOCK"}
```

**High-risk domain ending exceptions** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-spam-tlds-allow.dat)

```json
{"type": "field", "domain": ["ext:hagezi-spam-tlds-allow.dat:spam-tlds-allow"], "outboundTag": "DIRECT"}
```

</details>

<details>

<summary>Ads and tracking</summary>

Choose one Multi edition. The pop-up and referral lists can be used on their own.

**Multi Light** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-multi-light.dat)

```json
{"type": "field", "domain": ["ext:hagezi-multi-light.dat:multi-light"], "outboundTag": "BLOCK"}
```

**Multi Normal** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-multi-normal.dat)

```json
{"type": "field", "domain": ["ext:hagezi-multi-normal.dat:multi-normal"], "outboundTag": "BLOCK"}
```

**Multi Pro** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-multi-pro.dat)

```json
{"type": "field", "domain": ["ext:hagezi-multi-pro.dat:multi-pro"], "outboundTag": "BLOCK"}
```

**Multi Pro Mini** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-multi-pro-mini.dat)

```json
{"type": "field", "domain": ["ext:hagezi-multi-pro-mini.dat:multi-pro-mini"], "outboundTag": "BLOCK"}
```

**Multi Pro++** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-multi-pro-plus.dat)

```json
{"type": "field", "domain": ["ext:hagezi-multi-pro-plus.dat:multi-pro-plus"], "outboundTag": "BLOCK"}
```

**Multi Pro++ Mini** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-multi-pro-plus-mini.dat)

```json
{"type": "field", "domain": ["ext:hagezi-multi-pro-plus-mini.dat:multi-pro-plus-mini"], "outboundTag": "BLOCK"}
```

**Multi Ultimate** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-multi-ultimate.dat)

```json
{"type": "field", "domain": ["ext:hagezi-multi-ultimate.dat:multi-ultimate"], "outboundTag": "BLOCK"}
```

**Multi Ultimate Mini** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-multi-ultimate-mini.dat)

```json
{"type": "field", "domain": ["ext:hagezi-multi-ultimate-mini.dat:multi-ultimate-mini"], "outboundTag": "BLOCK"}
```

**Pop-up ads** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-popupads.dat)

```json
{"type": "field", "domain": ["ext:hagezi-popupads.dat:popupads"], "outboundTag": "BLOCK"}
```

**Block referral links** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-referral-block.dat)

```json
{"type": "field", "domain": ["ext:hagezi-referral-block.dat:referral-block"], "outboundTag": "BLOCK"}
```

**Allow referral links** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-referral-allow.dat)

```json
{"type": "field", "domain": ["ext:hagezi-referral-allow.dat:referral-allow"], "outboundTag": "DIRECT"}
```

</details>

<details>

<summary>Device and app tracking</summary>

**Amazon trackers** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-native-amazon.dat)

```json
{"type": "field", "domain": ["ext:hagezi-native-amazon.dat:native-amazon"], "outboundTag": "BLOCK"}
```

**Apple trackers** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-native-apple.dat)

```json
{"type": "field", "domain": ["ext:hagezi-native-apple.dat:native-apple"], "outboundTag": "BLOCK"}
```

**Huawei trackers** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-native-huawei.dat)

```json
{"type": "field", "domain": ["ext:hagezi-native-huawei.dat:native-huawei"], "outboundTag": "BLOCK"}
```

**LG webOS trackers** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-native-lgwebos.dat)

```json
{"type": "field", "domain": ["ext:hagezi-native-lgwebos.dat:native-lgwebos"], "outboundTag": "BLOCK"}
```

**Oppo and Realme trackers** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-native-oppo-realme.dat)

```json
{"type": "field", "domain": ["ext:hagezi-native-oppo-realme.dat:native-oppo-realme"], "outboundTag": "BLOCK"}
```

**Roku trackers** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-native-roku.dat)

```json
{"type": "field", "domain": ["ext:hagezi-native-roku.dat:native-roku"], "outboundTag": "BLOCK"}
```

**Samsung trackers** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-native-samsung.dat)

```json
{"type": "field", "domain": ["ext:hagezi-native-samsung.dat:native-samsung"], "outboundTag": "BLOCK"}
```

**TikTok trackers** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-native-tiktok.dat)

```json
{"type": "field", "domain": ["ext:hagezi-native-tiktok.dat:native-tiktok"], "outboundTag": "BLOCK"}
```

**TikTok trackers, extended** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-native-tiktok-extended.dat)

```json
{"type": "field", "domain": ["ext:hagezi-native-tiktok-extended.dat:native-tiktok-extended"], "outboundTag": "BLOCK"}
```

**Vivo trackers** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-native-vivo.dat)

```json
{"type": "field", "domain": ["ext:hagezi-native-vivo.dat:native-vivo"], "outboundTag": "BLOCK"}
```

**Windows and Office trackers** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-native-winoffice.dat)

```json
{"type": "field", "domain": ["ext:hagezi-native-winoffice.dat:native-winoffice"], "outboundTag": "BLOCK"}
```

**Xiaomi trackers** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-native-xiaomi.dat)

```json
{"type": "field", "domain": ["ext:hagezi-native-xiaomi.dat:native-xiaomi"], "outboundTag": "BLOCK"}
```

</details>

<details>

<summary>DNS and other categories</summary>

The DoH and name server lists may block DNS services you use.

**Encrypted DNS domains** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-doh.dat)

```json
{"type": "field", "domain": ["ext:hagezi-doh.dat:doh"], "outboundTag": "BLOCK"}
```

**Encrypted DNS IPv4 addresses** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-doh-ipv4.dat)

```json
{"type": "field", "ip": ["ext:hagezi-doh-ipv4.dat:doh-ipv4"], "outboundTag": "BLOCK"}
```

**Encrypted DNS, VPN, Tor and proxy domains** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-doh-vpn-proxy-bypass.dat)

```json
{"type": "field", "domain": ["ext:hagezi-doh-vpn-proxy-bypass.dat:doh-vpn-proxy-bypass"], "outboundTag": "BLOCK"}
```

**Name server IP addresses** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-nameserver-ip.dat)

```json
{"type": "field", "ip": ["ext:hagezi-nameserver-ip.dat:nameserver-ip"], "outboundTag": "BLOCK"}
```

**Search engines without SafeSearch support** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-nosafesearch.dat)

```json
{"type": "field", "domain": ["ext:hagezi-nosafesearch.dat:nosafesearch"], "outboundTag": "BLOCK"}
```

**Link shorteners** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-urlshortener.dat)

```json
{"type": "field", "domain": ["ext:hagezi-urlshortener.dat:urlshortener"], "outboundTag": "BLOCK"}
```

**Piracy sites** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-anti-piracy.dat)

```json
{"type": "field", "domain": ["ext:hagezi-anti-piracy.dat:anti-piracy"], "outboundTag": "BLOCK"}
```

**Gambling** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-gambling.dat)

```json
{"type": "field", "domain": ["ext:hagezi-gambling.dat:gambling"], "outboundTag": "BLOCK"}
```

**Gambling Medium** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-gambling-medium.dat)

```json
{"type": "field", "domain": ["ext:hagezi-gambling-medium.dat:gambling-medium"], "outboundTag": "BLOCK"}
```

**Gambling Mini** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-gambling-mini.dat)

```json
{"type": "field", "domain": ["ext:hagezi-gambling-mini.dat:gambling-mini"], "outboundTag": "BLOCK"}
```

**Social networks** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-social.dat)

```json
{"type": "field", "domain": ["ext:hagezi-social.dat:social"], "outboundTag": "BLOCK"}
```

**Adult content** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-nsfw.dat)

```json
{"type": "field", "domain": ["ext:hagezi-nsfw.dat:nsfw"], "outboundTag": "BLOCK"}
```

</details>

<details>

<summary>Newly registered domains</summary>

These lists are large and can include legitimate new sites. Combine NRD ranges if you need more days. For DGA, choose one time window.

**NRD, 1–7 days ago** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-nrd7.dat)

```json
{"type": "field", "domain": ["ext:hagezi-nrd7.dat:nrd7"], "outboundTag": "BLOCK"}
```

**NRD, 8–14 days ago** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-nrd14-8.dat)

```json
{"type": "field", "domain": ["ext:hagezi-nrd14-8.dat:nrd14-8"], "outboundTag": "BLOCK"}
```

**NRD, 15–21 days ago** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-nrd21-15.dat)

```json
{"type": "field", "domain": ["ext:hagezi-nrd21-15.dat:nrd21-15"], "outboundTag": "BLOCK"}
```

**NRD, 22–28 days ago** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-nrd28-22.dat)

```json
{"type": "field", "domain": ["ext:hagezi-nrd28-22.dat:nrd28-22"], "outboundTag": "BLOCK"}
```

**NRD, 29–35 days ago** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-nrd35-29.dat)

```json
{"type": "field", "domain": ["ext:hagezi-nrd35-29.dat:nrd35-29"], "outboundTag": "BLOCK"}
```

**DGA, past 7 days** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-dga7.dat)

```json
{"type": "field", "domain": ["ext:hagezi-dga7.dat:dga7"], "outboundTag": "BLOCK"}
```

**DGA, past 14 days** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-dga14.dat)

```json
{"type": "field", "domain": ["ext:hagezi-dga14.dat:dga14"], "outboundTag": "BLOCK"}
```

**DGA, past 30 days** · [Download](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-dga30.dat)

```json
{"type": "field", "domain": ["ext:hagezi-dga30.dat:dga30"], "outboundTag": "BLOCK"}
```

</details>

Domain lists work when Xray can see the destination name. DNS rebinding protection is handled by the DNS resolver.

Lists by [HaGeZi](https://github.com/hagezi/dns-blocklists) · [GPL-3.0](LICENSE)
