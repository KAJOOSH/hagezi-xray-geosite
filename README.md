# فهرست HaGeZi TIF Medium برای Xray

این پروژه هر روز فهرست دامنه‌های مرتبط با بدافزار، فیشینگ و سرورهای فرمان‌دهی را از HaGeZi می‌گیرد و برای Xray به فایل `hagezi-tif.dat` تبدیل می‌کند.

## راه‌اندازی در گیت‌هاب

۱. فایل‌های پروژه، از جمله پوشهٔ `.github`، را در شاخهٔ پیش‌فرض مخزن عمومی `hagezi-xray-geosite` در گیت‌هاب قرار دهید.

۲. در بخش **Actions**، گردش‌کار **Update GeoSite** را باز کنید و برای اجرای دستی در هر زمان، شاخهٔ پیش‌فرض را انتخاب کنید و **Run workflow** را بزنید.

۳. فایل آماده را از شاخهٔ `generated` دانلود کنید. به‌روزرسانی هر روز حدود ساعت ۰۶:۴۷ به وقت تهران اجرا می‌شود. اگر خوراک تغییری نکرده باشد، نسخهٔ تکراری ذخیره نمی‌شود.

```text
https://raw.githubusercontent.com/KAJOOSH/hagezi-xray-geosite/generated/hagezi-tif.dat
```

کنار فایل، هش `SHA-256`، نسخهٔ منبع و متن اصلی HaGeZi هم ذخیره می‌شود. اگر گیت‌هاب زمان‌بندی را به‌دلیل غیرفعال‌بودن مخزن متوقف کرد، آن را در **Actions** دوباره فعال کنید. [راهنمای زمان‌بندی گیت‌هاب](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)

## استفاده در Xray یا مرزبان

۱. فایل `hagezi-tif.dat` را در پوشهٔ منابع Xray، کنار `geoip.dat` و `geosite.dat`، بگذارید. در مرزبان نود، مسیر را با `XRAY_ASSETS_PATH` بررسی کنید. اگر از Docker استفاده می‌کنید، فایل باید داخل کانتینر در دسترس باشد. پیش از اعمال کانفیگ مشترک، فایل را روی تمام نودهایی بگذارید که آن را می‌گیرند. [مستندات مرزبان نود](https://gozargah.github.io/marzban/en/docs/marzban-node#configuration)

۲. قانون زیر را به ابتدای `routing.rules`، پیش از قوانین `DIRECT`، اضافه کنید. در کانفیگ باید خروجی `BLOCK` از نوع `blackhole` وجود داشته باشد. اگر خروجی مسدودکنندهٔ شما نام دیگری دارد، همان نام را جایگزین کنید. [مستندات Routing در Xray](https://xtls.github.io/en/config/routing.html)

```json
{
  "type": "field",
  "domain": ["ext:hagezi-tif.dat:tif-medium"],
  "outboundTag": "BLOCK"
}
```

۳. کانفیگ را ابتدا روی یک نود اعمال کنید. اگر نسخهٔ Xray از `geodata` پشتیبانی می‌کند، با [نمونهٔ به‌روزرسانی نود](examples/xray-geodata.json) می‌توانید نسخه‌های بعدی را خودکار بارگیری و اعمال کنید. زمان را بر اساس منطقهٔ زمانی نود، بعد از انتشار گیت‌هاب بگذارید. [مستندات به‌روزرسانی GeoData در Xray](https://xtls.github.io/en/config/geodata.html)

فیلتر روی دامنه‌هایی عمل می‌کند که Xray هنگام مسیریابی می‌بیند. اتصال مستقیم به IP بدون نام قابل‌تشخیص، به قانون IP جداگانه نیاز دارد.

## منبع و مجوز

کد پروژه و فایل تبدیل‌شده با مجوز `GPL-3.0-only` منتشر می‌شوند. متن اصلی فهرست و مشخصات نسخهٔ آن کنار خروجی در شاخهٔ `generated` در دسترس است. [پروژهٔ HaGeZi](https://github.com/hagezi/dns-blocklists#tif) · [مجوز](LICENSE)
