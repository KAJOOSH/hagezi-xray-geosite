# بسته‌های HaGeZi برای Xray

از جدول‌ها فایل موردنیازتان را بگیرید. هر لینک به همان فایل در آخرین انتشار اشاره می‌کند. نسخه‌های قبلی در [Releases](https://github.com/KAJOOSH/hagezi-xray-geosite/releases) در دسترس‌اند.

## فعال کردن یک بسته

فایل انتخابی را در پوشهٔ منابع Xray بگذارید و قانونش را پیش از قوانین عمومی `DIRECT` در `routing.rules` اضافه کنید. اگر مرزبان کانفیگ را بین چند نود توزیع می‌کند، ابتدا فایل را روی تمام نودهای مشمول بگذارید. برای بستهٔ دامنه از `domain` و برای بستهٔ IP از `ip` استفاده کنید. در هر قانون فقط نوع مربوط به همان بسته را بگذارید.

برای مثال، بستهٔ **Fake** را این‌طور فعال کنید.

```json
{
  "type": "field",
  "domain": ["ext:hagezi-fake.dat:fake"],
  "outboundTag": "BLOCK"
}
```

قانون بستهٔ **TIF IPv4** به این شکل است.

```json
{
  "type": "field",
  "ip": ["ext:hagezi-tif-ipv4.dat:tif-ipv4"],
  "outboundTag": "BLOCK"
}
```

نام فایل و تگ را از جدول بردارید. اگر خروجی مسدودکنندهٔ شما نام دیگری دارد، آن نام را جایگزین کنید. فهرست دامنه به دیدن نام مقصد توسط Xray وابسته است. [راهنمای قوانین Xray](https://xtls.github.io/en/config/routing.html)

### استفاده از بسته‌های استثنا

بسته‌های `spam-tlds-allow` و `referral-allow` را به خروجی معمول همان ترافیک بفرستید. قانون استثنا باید پیش از قانون مسدودکننده‌ای باشد که قرار است از آن استثنا بگیرد. قواعد مستقل امنیتی را بالاتر نگه دارید تا استثنا آن‌ها را دور نزند. Xray اولین قانون منطبق را اعمال می‌کند. [ترتیب قوانین Xray](https://xtls.github.io/en/config/routing.html)

## امنیت و نشانی‌های تهدید

یکی از سه اندازهٔ TIF را انتخاب کنید. بستهٔ IPv4 را می‌توان در کنار بستهٔ دامنه استفاده کرد.

| کاربرد | فایل دانلود | تگ Xray | نوع |
| --- | --- | --- | --- |
| تهدیدهای مهم با اندازهٔ متوسط | [`hagezi-tif.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-tif.dat) | `tif-medium` | دامنه |
| پوشش گسترده‌تر تهدیدها | [`hagezi-tif-full.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-tif-full.dat) | `tif-full` | دامنه |
| فهرست سبک‌تر برای نود کم‌حافظه | [`hagezi-tif-mini.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-tif-mini.dat) | `tif-mini` | دامنه |
| نشانی‌های IPv4 تهدید | [`hagezi-tif-ipv4.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-tif-ipv4.dat) | `tif-ipv4` | آدرس IP |
| سایت‌های جعلی و کلاهبرداری | [`hagezi-fake.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-fake.dat) | `fake` | دامنه |
| سرویس‌های DNS پویا | [`hagezi-dyndns.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-dyndns.dat) | `dyndns` | دامنه |
| دامنهٔ میزبان‌هایی که مکرراً برای انتشار بدافزار استفاده می‌شوند | [`hagezi-badware-hoster.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-badware-hoster.dat) | `badware-hoster` | دامنه |
| پسوندهای پرریسک، همراه با فایل استثنا | [`hagezi-spam-tlds.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-spam-tlds.dat) | `spam-tlds` | دامنه |
| استثناهای فهرست پسوندها | [`hagezi-spam-tlds-allow.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-spam-tlds-allow.dat) | `spam-tlds-allow` | استثنا |

## تبلیغات و ردیابی

یکی از نسخه‌های Multi را انتخاب کنید. بسته‌های دیگر این بخش جداگانه فعال می‌شوند.

| کاربرد | فایل دانلود | تگ Xray | نوع |
| --- | --- | --- | --- |
| نسخهٔ سبک | [`hagezi-multi-light.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-multi-light.dat) | `multi-light` | دامنه |
| پوشش معمول | [`hagezi-multi-normal.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-multi-normal.dat) | `multi-normal` | دامنه |
| پوشش بیشتر | [`hagezi-multi-pro.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-multi-pro.dat) | `multi-pro` | دامنه |
| نسخهٔ کم‌حجم Pro | [`hagezi-multi-pro-mini.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-multi-pro-mini.dat) | `multi-pro-mini` | دامنه |
| نسخهٔ سخت‌گیرانهٔ Pro++ | [`hagezi-multi-pro-plus.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-multi-pro-plus.dat) | `multi-pro-plus` | دامنه |
| نسخهٔ کم‌حجم Pro++ | [`hagezi-multi-pro-plus-mini.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-multi-pro-plus-mini.dat) | `multi-pro-plus-mini` | دامنه |
| سخت‌گیرانه‌ترین نسخه | [`hagezi-multi-ultimate.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-multi-ultimate.dat) | `multi-ultimate` | دامنه |
| نسخهٔ کم‌حجم Ultimate | [`hagezi-multi-ultimate-mini.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-multi-ultimate-mini.dat) | `multi-ultimate-mini` | دامنه |
| دامنه‌های تبلیغات پاپ‌آپ | [`hagezi-popupads.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-popupads.dat) | `popupads` | دامنه |
| مسدودسازی لینک‌های ارجاع و وابسته | [`hagezi-referral-block.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-referral-block.dat) | `referral-block` | دامنه |
| بازگذاشتن لینک‌های ارجاع و وابسته | [`hagezi-referral-allow.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-referral-allow.dat) | `referral-allow` | استثنا |

## ردیاب‌های دستگاه‌ها و سرویس‌ها

| کاربرد | فایل دانلود | تگ Xray | نوع |
| --- | --- | --- | --- |
| آمازون | [`hagezi-native-amazon.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-native-amazon.dat) | `native-amazon` | دامنه |
| اپل | [`hagezi-native-apple.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-native-apple.dat) | `native-apple` | دامنه |
| هواوی | [`hagezi-native-huawei.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-native-huawei.dat) | `native-huawei` | دامنه |
| تلویزیون‌های LG webOS | [`hagezi-native-lgwebos.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-native-lgwebos.dat) | `native-lgwebos` | دامنه |
| گوشی‌های Oppo و Realme | [`hagezi-native-oppo-realme.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-native-oppo-realme.dat) | `native-oppo-realme` | دامنه |
| دستگاه‌های Roku | [`hagezi-native-roku.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-native-roku.dat) | `native-roku` | دامنه |
| سامسونگ | [`hagezi-native-samsung.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-native-samsung.dat) | `native-samsung` | دامنه |
| تیک‌تاک | [`hagezi-native-tiktok.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-native-tiktok.dat) | `native-tiktok` | دامنه |
| نسخهٔ سخت‌گیرانه‌تر تیک‌تاک | [`hagezi-native-tiktok-extended.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-native-tiktok-extended.dat) | `native-tiktok-extended` | دامنه |
| گوشی‌های Vivo | [`hagezi-native-vivo.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-native-vivo.dat) | `native-vivo` | دامنه |
| ویندوز، آفیس و سرویس‌های مایکروسافت | [`hagezi-native-winoffice.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-native-winoffice.dat) | `native-winoffice` | دامنه |
| شیائومی | [`hagezi-native-xiaomi.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-native-xiaomi.dat) | `native-xiaomi` | دامنه |

## سرویس‌های DNS و دسته‌های دیگر

فعال کردن بسته‌های DoH یا سرور نام ممکن است DNS مورد استفادهٔ کاربران را محدود کند.

| کاربرد | فایل دانلود | تگ Xray | نوع |
| --- | --- | --- | --- |
| دامنه‌های DNS رمزگذاری‌شده | [`hagezi-doh.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-doh.dat) | `doh` | دامنه |
| نشانی‌های IPv4 سرویس‌های DNS رمزگذاری‌شده | [`hagezi-doh-ipv4.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-doh-ipv4.dat) | `doh-ipv4` | آدرس IP |
| فهرست گسترده‌تر شامل DNS رمزگذاری‌شده، VPN، Tor و پروکسی | [`hagezi-doh-vpn-proxy-bypass.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-doh-vpn-proxy-bypass.dat) | `doh-vpn-proxy-bypass` | دامنه |
| نشانی‌های IP سرورهای نام | [`hagezi-nameserver-ip.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-nameserver-ip.dat) | `nameserver-ip` | آدرس IP |
| موتورهای جست‌وجوی بدون پشتیبانی از SafeSearch | [`hagezi-nosafesearch.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-nosafesearch.dat) | `nosafesearch` | دامنه |
| سرویس‌های کوتاه‌کنندهٔ لینک | [`hagezi-urlshortener.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-urlshortener.dat) | `urlshortener` | دامنه |
| دامنه‌های توزیع محتوای ناقض حق نشر | [`hagezi-anti-piracy.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-anti-piracy.dat) | `anti-piracy` | دامنه |
| دامنه‌های مرتبط با قمار | [`hagezi-gambling.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-gambling.dat) | `gambling` | دامنه |
| نسخهٔ متوسط فهرست قمار | [`hagezi-gambling-medium.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-gambling-medium.dat) | `gambling-medium` | دامنه |
| نسخهٔ کوچک فهرست قمار | [`hagezi-gambling-mini.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-gambling-mini.dat) | `gambling-mini` | دامنه |
| شبکه‌های اجتماعی | [`hagezi-social.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-social.dat) | `social` | دامنه |
| سایت‌های محتوای بزرگسالان | [`hagezi-nsfw.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-nsfw.dat) | `nsfw` | دامنه |

## دامنه‌های تازه‌ثبت‌شده

این فایل‌ها بزرگ‌اند و می‌توانند دامنه‌های تازهٔ سالم را هم مسدود کنند. پنج بازهٔ NRD مستقل‌اند و برای پوشش بیشتر کنار هم قرار می‌گیرند. برای DGA یک بازهٔ زمانی انتخاب کنید.

| کاربرد | فایل دانلود | تگ Xray | نوع |
| --- | --- | --- | --- |
| از ۷ روز پیش تا دیروز | [`hagezi-nrd7.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-nrd7.dat) | `nrd7` | دامنه |
| از ۱۴ تا ۸ روز پیش | [`hagezi-nrd14-8.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-nrd14-8.dat) | `nrd14-8` | دامنه |
| از ۲۱ تا ۱۵ روز پیش | [`hagezi-nrd21-15.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-nrd21-15.dat) | `nrd21-15` | دامنه |
| از ۲۸ تا ۲۲ روز پیش | [`hagezi-nrd28-22.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-nrd28-22.dat) | `nrd28-22` | دامنه |
| از ۳۵ تا ۲۹ روز پیش | [`hagezi-nrd35-29.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-nrd35-29.dat) | `nrd35-29` | دامنه |
| دامنه‌های تازهٔ با آنتروپی بالا در ۷ روز گذشته | [`hagezi-dga7.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-dga7.dat) | `dga7` | دامنه |
| دامنه‌های تازهٔ با آنتروپی بالا در ۱۴ روز گذشته | [`hagezi-dga14.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-dga14.dat) | `dga14` | دامنه |
| دامنه‌های تازهٔ با آنتروپی بالا در ۳۰ روز گذشته | [`hagezi-dga30.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-dga30.dat) | `dga30` | دامنه |

## قاعده‌های مخصوص DNS

بستهٔ DNS Rebind پاسخ resolver را بررسی می‌کند و قالب مستقل قابل‌معادل‌سازی برای مسیریابی Xray ندارد. قالب‌های AdGuard، DNSMasq و RPZ از همان بسته‌های اصلی نیز خروجی‌های جایگزین برای ابزارهای دیگرند. [فهرست قالب‌ها و بسته‌های HaGeZi](https://github.com/hagezi/dns-blocklists#tif)
