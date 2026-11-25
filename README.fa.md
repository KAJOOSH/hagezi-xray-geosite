# فهرست‌های HaGeZi برای Xray

انتخاب کنید چه چیزی مسدود شود و قانون همان بسته را کپی کنید. [English](README.md)

## انتخاب بسته

**برای شروع، TIF Medium را انتخاب کنید.** برای مسدود کردن آی‌پی‌های فهرست‌شده، **TIF IPv4** را اضافه کنید. اگر می‌خواهید تبلیغات و ردیاب‌ها را هم فیلتر کنید، **Multi Pro** را اضافه کنید.

| خانواده | پوشش | چه زمانی استفاده کنیم؟ |
| --- | --- | --- |
| **نسخه‌های Mini، Medium و Full از TIF** | دامنه‌های بدافزار، فیشینگ و سرورهای فرمان‌دهی | برای حافظهٔ محدود Mini، برای استفادهٔ روزمره Medium، و برای پوشش گسترده‌تر Full را انتخاب کنید. یکی کافی است. |
| **بستهٔ TIF IPv4** | نشانی‌های IPv4 ثبت‌شده در فهرست تهدید | برای اتصال مستقیم به آی‌پی اضافه کنید. بعضی از این نشانی‌ها با سرویس‌های سالم مشترک‌اند. |
| **بستهٔ Fake** | سایت‌های جعلی و کلاهبرداری | برای فیلتر متمرکز کلاهبرداری. بخشی از دامنه‌ها با TIF مشترک‌اند. |
| **بسته‌های DynDNS، Badware Hoster و پسوندهای پرریسک** | سرویس‌هایی که زیاد برای کلاهبرداری یا بدافزار به کار می‌روند | فقط در صورت نیاز. قواعد گسترده می‌توانند سایت‌های سالم روی همان میزبان یا پسوند را هم مسدود کنند. |
| **بسته‌های Multi، ردیاب دستگاه، پاپ‌آپ و لینک ارجاع** | تبلیغات و ردیابی، همراه با پوشش بخشی از تهدیدها در Multi | برای حریم خصوصی و فیلتر تبلیغات. یک نسخه از Multi انتخاب کنید. |
| **بسته‌های NRD و DGA** | دامنه‌های تازه‌ثبت‌شده. فهرست DGA محدودتر است. | برای فیلتر سخت‌گیرانه، اگر می‌توانید برای سایت‌های تازهٔ سالم استثنا بگذارید. یکی از NRD و DGA را انتخاب کنید. |
| **بسته‌های DNS، VPN و محتوا** | سرویس‌های DNS، پروکسی‌ها و دسته‌های مشخص سایت‌ها | وقتی سیاست مشخصی برای فیلتر دارید. |

## استفاده از یک بسته

۱. از فهرست زیر فایل دلخواه را بگیرید و آن را در پوشهٔ منابع Xray، کنار `geosite.dat` بگذارید.

۲. قانونش را در `routing.rules` پیش از هر قانون عمومی اضافه کنید. بین قانون‌ها ویرگول بگذارید، تنظیمات را ذخیره کنید و Xray را دوباره بارگذاری کنید.

تگ خروجی مسدودکنندهٔ خود را به‌جای `BLOCK` بگذارید. اگر چنین خروجی‌ای ندارید، `{"tag":"BLOCK","protocol":"blackhole"}` را به انتهای `outbounds` اضافه کنید.

در قانون استثنا، در صورت نیاز تگ خروجی معمول را جایگزین `DIRECT` کنید. استثنا را بالاتر از قانون مسدودکنندهٔ مربوط به خودش و پایین‌تر از سایر قواعد امنیتی بگذارید.

## بسته‌ها

<details>

<summary dir="rtl">امنیت</summary>

**نسخهٔ متوسط TIF** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-tif.dat)

```json
{"type": "field", "domain": ["ext:hagezi-tif.dat:tif-medium"], "outboundTag": "BLOCK"}
```

**نسخهٔ کامل TIF** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-tif-full.dat)

```json
{"type": "field", "domain": ["ext:hagezi-tif-full.dat:tif-full"], "outboundTag": "BLOCK"}
```

**نسخهٔ سبک TIF** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-tif-mini.dat)

```json
{"type": "field", "domain": ["ext:hagezi-tif-mini.dat:tif-mini"], "outboundTag": "BLOCK"}
```

**فهرست IPv4 تهدیدها** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-tif-ipv4.dat)

```json
{"type": "field", "ip": ["ext:hagezi-tif-ipv4.dat:tif-ipv4"], "outboundTag": "BLOCK"}
```

**سایت‌های جعلی و کلاهبرداری** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-fake.dat)

```json
{"type": "field", "domain": ["ext:hagezi-fake.dat:fake"], "outboundTag": "BLOCK"}
```

**سرویس‌های DNS پویا** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-dyndns.dat)

```json
{"type": "field", "domain": ["ext:hagezi-dyndns.dat:dyndns"], "outboundTag": "BLOCK"}
```

**میزبان‌های پرتکرار در انتشار بدافزار** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-badware-hoster.dat)

```json
{"type": "field", "domain": ["ext:hagezi-badware-hoster.dat:badware-hoster"], "outboundTag": "BLOCK"}
```

**پسوندهای پرریسک** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-spam-tlds.dat)

```json
{"type": "field", "domain": ["ext:hagezi-spam-tlds.dat:spam-tlds"], "outboundTag": "BLOCK"}
```

**استثناهای پسوندهای پرریسک** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-spam-tlds-allow.dat)

```json
{"type": "field", "domain": ["ext:hagezi-spam-tlds-allow.dat:spam-tlds-allow"], "outboundTag": "DIRECT"}
```

</details>

<details>

<summary dir="rtl">تبلیغات و ردیابی</summary>

یکی از نسخه‌های Multi را انتخاب کنید. فهرست‌های پاپ‌آپ و لینک ارجاع را می‌توانید جداگانه استفاده کنید.

**نسخهٔ Light از Multi** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-multi-light.dat)

```json
{"type": "field", "domain": ["ext:hagezi-multi-light.dat:multi-light"], "outboundTag": "BLOCK"}
```

**نسخهٔ Normal از Multi** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-multi-normal.dat)

```json
{"type": "field", "domain": ["ext:hagezi-multi-normal.dat:multi-normal"], "outboundTag": "BLOCK"}
```

**نسخهٔ Pro از Multi** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-multi-pro.dat)

```json
{"type": "field", "domain": ["ext:hagezi-multi-pro.dat:multi-pro"], "outboundTag": "BLOCK"}
```

**نسخهٔ کوچک Pro از Multi** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-multi-pro-mini.dat)

```json
{"type": "field", "domain": ["ext:hagezi-multi-pro-mini.dat:multi-pro-mini"], "outboundTag": "BLOCK"}
```

**نسخهٔ Pro++ از Multi** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-multi-pro-plus.dat)

```json
{"type": "field", "domain": ["ext:hagezi-multi-pro-plus.dat:multi-pro-plus"], "outboundTag": "BLOCK"}
```

**نسخهٔ کوچک Pro++ از Multi** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-multi-pro-plus-mini.dat)

```json
{"type": "field", "domain": ["ext:hagezi-multi-pro-plus-mini.dat:multi-pro-plus-mini"], "outboundTag": "BLOCK"}
```

**نسخهٔ Ultimate از Multi** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-multi-ultimate.dat)

```json
{"type": "field", "domain": ["ext:hagezi-multi-ultimate.dat:multi-ultimate"], "outboundTag": "BLOCK"}
```

**نسخهٔ کوچک Ultimate از Multi** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-multi-ultimate-mini.dat)

```json
{"type": "field", "domain": ["ext:hagezi-multi-ultimate-mini.dat:multi-ultimate-mini"], "outboundTag": "BLOCK"}
```

**تبلیغات پاپ‌آپ** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-popupads.dat)

```json
{"type": "field", "domain": ["ext:hagezi-popupads.dat:popupads"], "outboundTag": "BLOCK"}
```

**مسدودسازی لینک‌های ارجاع** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-referral-block.dat)

```json
{"type": "field", "domain": ["ext:hagezi-referral-block.dat:referral-block"], "outboundTag": "BLOCK"}
```

**بازگذاشتن لینک‌های ارجاع** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-referral-allow.dat)

```json
{"type": "field", "domain": ["ext:hagezi-referral-allow.dat:referral-allow"], "outboundTag": "DIRECT"}
```

</details>

<details>

<summary dir="rtl">ردیابی در دستگاه‌ها و برنامه‌ها</summary>

**ردیاب‌های آمازون** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-native-amazon.dat)

```json
{"type": "field", "domain": ["ext:hagezi-native-amazon.dat:native-amazon"], "outboundTag": "BLOCK"}
```

**ردیاب‌های اپل** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-native-apple.dat)

```json
{"type": "field", "domain": ["ext:hagezi-native-apple.dat:native-apple"], "outboundTag": "BLOCK"}
```

**ردیاب‌های هواوی** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-native-huawei.dat)

```json
{"type": "field", "domain": ["ext:hagezi-native-huawei.dat:native-huawei"], "outboundTag": "BLOCK"}
```

**ردیاب‌های LG webOS** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-native-lgwebos.dat)

```json
{"type": "field", "domain": ["ext:hagezi-native-lgwebos.dat:native-lgwebos"], "outboundTag": "BLOCK"}
```

**ردیاب‌های Oppo و Realme** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-native-oppo-realme.dat)

```json
{"type": "field", "domain": ["ext:hagezi-native-oppo-realme.dat:native-oppo-realme"], "outboundTag": "BLOCK"}
```

**ردیاب‌های Roku** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-native-roku.dat)

```json
{"type": "field", "domain": ["ext:hagezi-native-roku.dat:native-roku"], "outboundTag": "BLOCK"}
```

**ردیاب‌های سامسونگ** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-native-samsung.dat)

```json
{"type": "field", "domain": ["ext:hagezi-native-samsung.dat:native-samsung"], "outboundTag": "BLOCK"}
```

**ردیاب‌های تیک‌تاک** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-native-tiktok.dat)

```json
{"type": "field", "domain": ["ext:hagezi-native-tiktok.dat:native-tiktok"], "outboundTag": "BLOCK"}
```

**ردیاب‌های تیک‌تاک، نسخهٔ گسترده** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-native-tiktok-extended.dat)

```json
{"type": "field", "domain": ["ext:hagezi-native-tiktok-extended.dat:native-tiktok-extended"], "outboundTag": "BLOCK"}
```

**ردیاب‌های Vivo** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-native-vivo.dat)

```json
{"type": "field", "domain": ["ext:hagezi-native-vivo.dat:native-vivo"], "outboundTag": "BLOCK"}
```

**ردیاب‌های ویندوز و آفیس** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-native-winoffice.dat)

```json
{"type": "field", "domain": ["ext:hagezi-native-winoffice.dat:native-winoffice"], "outboundTag": "BLOCK"}
```

**ردیاب‌های شیائومی** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-native-xiaomi.dat)

```json
{"type": "field", "domain": ["ext:hagezi-native-xiaomi.dat:native-xiaomi"], "outboundTag": "BLOCK"}
```

</details>

<details>

<summary dir="rtl">سرویس‌های DNS و دسته‌های دیگر</summary>

فهرست‌های DoH و سرورهای نام ممکن است سرویس DNS مورد استفاده‌تان را هم مسدود کنند.

**دامنه‌های DNS رمزگذاری‌شده** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-doh.dat)

```json
{"type": "field", "domain": ["ext:hagezi-doh.dat:doh"], "outboundTag": "BLOCK"}
```

**نشانی‌های IPv4 سرویس‌های DNS رمزگذاری‌شده** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-doh-ipv4.dat)

```json
{"type": "field", "ip": ["ext:hagezi-doh-ipv4.dat:doh-ipv4"], "outboundTag": "BLOCK"}
```

**دامنه‌های DNS رمزگذاری‌شده، VPN، Tor و پروکسی** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-doh-vpn-proxy-bypass.dat)

```json
{"type": "field", "domain": ["ext:hagezi-doh-vpn-proxy-bypass.dat:doh-vpn-proxy-bypass"], "outboundTag": "BLOCK"}
```

**نشانی‌های IP سرورهای نام** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-nameserver-ip.dat)

```json
{"type": "field", "ip": ["ext:hagezi-nameserver-ip.dat:nameserver-ip"], "outboundTag": "BLOCK"}
```

**موتورهای جست‌وجوی بدون پشتیبانی از SafeSearch** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-nosafesearch.dat)

```json
{"type": "field", "domain": ["ext:hagezi-nosafesearch.dat:nosafesearch"], "outboundTag": "BLOCK"}
```

**سرویس‌های کوتاه‌کنندهٔ لینک** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-urlshortener.dat)

```json
{"type": "field", "domain": ["ext:hagezi-urlshortener.dat:urlshortener"], "outboundTag": "BLOCK"}
```

**سایت‌های توزیع محتوای ناقض حق نشر** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-anti-piracy.dat)

```json
{"type": "field", "domain": ["ext:hagezi-anti-piracy.dat:anti-piracy"], "outboundTag": "BLOCK"}
```

**سایت‌های قمار** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-gambling.dat)

```json
{"type": "field", "domain": ["ext:hagezi-gambling.dat:gambling"], "outboundTag": "BLOCK"}
```

**نسخهٔ متوسط فهرست قمار** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-gambling-medium.dat)

```json
{"type": "field", "domain": ["ext:hagezi-gambling-medium.dat:gambling-medium"], "outboundTag": "BLOCK"}
```

**نسخهٔ کوچک فهرست قمار** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-gambling-mini.dat)

```json
{"type": "field", "domain": ["ext:hagezi-gambling-mini.dat:gambling-mini"], "outboundTag": "BLOCK"}
```

**شبکه‌های اجتماعی** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-social.dat)

```json
{"type": "field", "domain": ["ext:hagezi-social.dat:social"], "outboundTag": "BLOCK"}
```

**سایت‌های محتوای بزرگسالان** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-nsfw.dat)

```json
{"type": "field", "domain": ["ext:hagezi-nsfw.dat:nsfw"], "outboundTag": "BLOCK"}
```

</details>

<details>

<summary dir="rtl">دامنه‌های تازه‌ثبت‌شده</summary>

این فهرست‌ها بزرگ‌اند و ممکن است سایت‌های تازهٔ سالم را هم دربر بگیرند. برای پوشش روزهای بیشتر، بازه‌های NRD را کنار هم بگذارید. برای DGA یک بازه انتخاب کنید.

**فهرست NRD از ۱ تا ۷ روز پیش** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-nrd7.dat)

```json
{"type": "field", "domain": ["ext:hagezi-nrd7.dat:nrd7"], "outboundTag": "BLOCK"}
```

**فهرست NRD از ۸ تا ۱۴ روز پیش** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-nrd14-8.dat)

```json
{"type": "field", "domain": ["ext:hagezi-nrd14-8.dat:nrd14-8"], "outboundTag": "BLOCK"}
```

**فهرست NRD از ۱۵ تا ۲۱ روز پیش** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-nrd21-15.dat)

```json
{"type": "field", "domain": ["ext:hagezi-nrd21-15.dat:nrd21-15"], "outboundTag": "BLOCK"}
```

**فهرست NRD از ۲۲ تا ۲۸ روز پیش** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-nrd28-22.dat)

```json
{"type": "field", "domain": ["ext:hagezi-nrd28-22.dat:nrd28-22"], "outboundTag": "BLOCK"}
```

**فهرست NRD از ۲۹ تا ۳۵ روز پیش** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-nrd35-29.dat)

```json
{"type": "field", "domain": ["ext:hagezi-nrd35-29.dat:nrd35-29"], "outboundTag": "BLOCK"}
```

**فهرست DGA در ۷ روز گذشته** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-dga7.dat)

```json
{"type": "field", "domain": ["ext:hagezi-dga7.dat:dga7"], "outboundTag": "BLOCK"}
```

**فهرست DGA در ۱۴ روز گذشته** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-dga14.dat)

```json
{"type": "field", "domain": ["ext:hagezi-dga14.dat:dga14"], "outboundTag": "BLOCK"}
```

**فهرست DGA در ۳۰ روز گذشته** · [دانلود](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-dga30.dat)

```json
{"type": "field", "domain": ["ext:hagezi-dga30.dat:dga30"], "outboundTag": "BLOCK"}
```

</details>

فهرست‌های دامنه زمانی اعمال می‌شوند که Xray نام مقصد را ببیند. محافظت در برابر DNS Rebind در سرویس DNS انجام می‌شود.

فهرست‌ها از [HaGeZi](https://github.com/hagezi/dns-blocklists) · [مجوز `GPL-3.0`](LICENSE)
