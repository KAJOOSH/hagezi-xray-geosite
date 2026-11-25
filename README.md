# فهرست‌های HaGeZi برای Xray

بسته‌های HaGeZi برای Xray به‌صورت فایل‌های مستقل در دسترس‌اند. از [راهنمای بسته‌ها](docs/PACKAGES.md) فقط فایل‌های موردنیازتان را انتخاب کنید. مراحل زیر برای بستهٔ امنیتی TIF Medium است.

## دانلود و استفاده

۱. از [بخش Releases](https://github.com/KAJOOSH/hagezi-xray-geosite/releases) نسخهٔ دلخواه را انتخاب کنید یا [آخرین فایل `hagezi-tif.dat`](https://github.com/KAJOOSH/hagezi-xray-geosite/releases/latest/download/hagezi-tif.dat) را مستقیم بگیرید.

۲. فایل را کنار `geoip.dat` و `geosite.dat` در پوشهٔ منابع Xray بگذارید. اگر مرزبان چند نود دارد، فایل را پیش از اعمال کانفیگ روی همهٔ نودهای مشمول قرار دهید. در Docker، فایل باید داخل کانتینر در دسترس باشد.

۳. قانون زیر را به ابتدای `routing.rules` اضافه کنید. اگر خروجی مسدودکنندهٔ `blackhole` در کانفیگ شما نام دیگری دارد، آن نام را به‌جای `BLOCK` بگذارید. اگر چنین خروجی‌ای ندارید، `{"tag":"BLOCK","protocol":"blackhole"}` را به انتهای `outbounds` اضافه کنید. سپس کانفیگ را دوباره بارگذاری کنید. [مستندات Routing در Xray](https://xtls.github.io/en/config/routing.html)

```json
{
  "type": "field",
  "domain": ["ext:hagezi-tif.dat:tif-medium"],
  "outboundTag": "BLOCK"
}
```

برای نسخه‌های Xray که از `geodata` پشتیبانی می‌کنند، [نمونهٔ به‌روزرسانی خودکار فایل](examples/xray-geodata.json) آماده است.

این فهرست روی دامنه‌هایی عمل می‌کند که Xray هنگام مسیریابی می‌بیند. برای مسدود کردن اتصال مستقیم به IP بدون نام قابل‌تشخیص، از قانون IP استفاده کنید.
