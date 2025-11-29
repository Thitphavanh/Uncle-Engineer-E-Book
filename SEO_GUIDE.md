# คู่มือ SEO สำหรับ Uncle EBook

## สิ่งที่ได้ทำไปแล้ว ✅

### 1. Meta Tags พื้นฐาน
- ✅ Title Tag ที่เหมาะสม
- ✅ Meta Description
- ✅ Meta Keywords
- ✅ Meta Author
- ✅ Meta Robots (index, follow)
- ✅ Canonical URLs

### 2. Open Graph Tags (Facebook, LINE)
- ✅ og:title
- ✅ og:description
- ✅ og:type
- ✅ og:url
- ✅ og:image
- ✅ og:site_name
- ✅ og:locale

### 3. Twitter Card Tags
- ✅ twitter:card
- ✅ twitter:title
- ✅ twitter:description
- ✅ twitter:image

### 4. Structured Data (Schema.org JSON-LD)
- ✅ WebSite Schema
- ✅ Organization Schema
- ✅ SearchAction Schema

### 5. Sitemap และ Robots
- ✅ sitemap.xml (Dynamic sitemap)
- ✅ robots.txt
- ✅ แยก sitemap เป็น 3 ส่วน: Static Pages, EBooks, Categories

### 6. Technical SEO
- ✅ Semantic HTML
- ✅ Mobile-Responsive Design
- ✅ Fast Loading (Tailwind CDN)
- ✅ Clean URLs (slug-based)

---

## วิธีใช้งาน SEO ในแต่ละหน้า

### ตัวอย่างการ Override Meta Tags ในแต่ละหน้า:

```django
{% extends 'base.html' %}

{% block title %}ชื่อหน้าของคุณ - Uncle EBook{% endblock %}

{% block description %}คำอธิบายหน้าของคุณที่น่าสนใจและมี keyword{% endblock %}

{% block keywords %}keyword1, keyword2, keyword3, Uncle EBook{% endblock %}

{% block og_title %}ชื่อสำหรับ Social Media{% endblock %}

{% block og_description %}คำอธิบายสำหรับ Social Media{% endblock %}

{% block og_image %}{{ request.scheme }}://{{ request.get_host }}{{ ebook.cover_image.url }}{% endblock %}

{% block canonical %}{{ request.scheme }}://{{ request.get_host }}{% url 'ebook_detail' ebook.slug %}{% endblock %}

{% block content %}
<!-- เนื้อหาของคุณ -->
{% endblock %}
```

---

## ตัวอย่างการเพิ่ม Structured Data สำหรับหน้าหนังสือ

ใน `ebook_detail.html` เพิ่ม:

```django
{% block structured_data %}
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "Book",
    "name": "{{ ebook.title }}",
    "author": {
        "@type": "Person",
        "name": "{{ ebook.author }}"
    },
    "description": "{{ ebook.descriptions|truncatewords:30 }}",
    "image": "{{ request.scheme }}://{{ request.get_host }}{{ ebook.cover_image.url }}",
    "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "4.5",
        "reviewCount": "100"
    },
    "offers": {
        "@type": "Offer",
        "price": "{{ ebook.price }}",
        "priceCurrency": "THB",
        "availability": "https://schema.org/InStock"
    }
}
</script>
{% endblock %}
```

---

## การตรวจสอบ SEO

### 1. Google Search Console
1. ไปที่ https://search.google.com/search-console
2. เพิ่มเว็บไซต์ของคุณ
3. ส่ง sitemap: `https://uncle-ebook.com/sitemap.xml`

### 2. Bing Webmaster Tools
1. ไปที่ https://www.bing.com/webmasters
2. เพิ่มเว็บไซต์
3. ส่ง sitemap

### 3. เครื่องมือตรวจสอบ SEO

#### ตรวจสอบ Meta Tags:
- [Meta Tags Checker](https://metatags.io/)
- ใส่ URL และดูว่า meta tags ทั้งหมดแสดงถูกต้องหรือไม่

#### ตรวจสอบ Structured Data:
- [Google Rich Results Test](https://search.google.com/test/rich-results)
- ใส่ URL หรือ code เพื่อทดสอบ structured data

#### ตรวจสอบ Open Graph:
- [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/)
- ดูว่าแชร์บน Facebook จะแสดงอย่างไร

#### ตรวจสอบ Twitter Card:
- [Twitter Card Validator](https://cards-dev.twitter.com/validator)

#### ตรวจสอบความเร็วเว็บไซต์:
- [Google PageSpeed Insights](https://pagespeed.web.dev/)
- [GTmetrix](https://gtmetrix.com/)

#### ตรวจสอบ Mobile-Friendly:
- [Google Mobile-Friendly Test](https://search.google.com/test/mobile-friendly)

---

## สิ่งที่ต้องทำเพิ่มเติม 📋

### 1. เพิ่มรูป OG Image (สำคัญมาก!)
สร้างรูป og-image.jpg ขนาด 1200x630 px และใส่ที่:
```
static/images/og-image.jpg
```

### 2. เพิ่ม Favicon
```html
<link rel="icon" type="image/png" href="{{ STATIC_URL }}images/favicon.png">
<link rel="apple-touch-icon" href="{{ STATIC_URL }}images/apple-touch-icon.png">
```

### 3. เพิ่ม Google Analytics
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

### 4. เพิ่ม Google Tag Manager (GTM)
```html
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-XXXXXXX');</script>
```

### 5. ปรับปรุง Content
- ✍️ เขียน title และ description ที่ unique สำหรับทุกหน้า
- 📝 เพิ่ม alt text ให้รูปภาพทั้งหมด
- 🔗 สร้าง internal links ระหว่างหน้า
- 📊 เพิ่ม breadcrumbs

### 6. เพิ่ม SSL Certificate (HTTPS)
- ใช้ Let's Encrypt (ฟรี)
- ตั้งค่าใน nginx/apache

### 7. ปรับปรุง Performance
- Enable Gzip compression
- Minify CSS/JS
- Optimize images
- Use CDN
- Enable browser caching

---

## Keywords แนะนำสำหรับแต่ละหน้า

### หน้าแรก (index):
```
อีบุ๊ค, หนังสืออิเล็กทรอนิกส์, หนังสือดิจิทัล, Uncle EBook,
ebook Thailand, หนังสือออนไลน์, อ่านหนังสือออนไลน์,
แพลตฟอร์มอีบุ๊คไทย
```

### หน้าหนังสือ (ebooks):
```
หนังสืออีบุ๊ค, รายการหนังสือ, ebook list,
หนังสือแนะนำ, หนังสือมาใหม่, หนังสือขายดี
```

### หน้าหมวดหมู่ (categories):
```
หมวดหมู่หนังสือ, ประเภทหนังสือ, category books,
หนังสือแยกประเภท
```

### หน้ารายละเอียดหนังสือ:
```
[ชื่อหนังสือ], [ชื่อผู้แต่ง], [หมวดหมู่],
รีวิวหนังสือ, ซื้อหนังสือออนไลน์
```

---

## เทคนิค SEO เพิ่มเติม

### 1. Schema.org สำหรับหนังสือ
เพิ่มใน template ของหน้าหนังสือ:
- Book Schema
- Author Schema
- Rating Schema
- Offer Schema

### 2. Breadcrumbs
เพิ่ม breadcrumbs navigation และ Schema:
```
หน้าแรก > หมวดหมู่ > ชื่อหนังสือ
```

### 3. Pagination SEO
สำหรับหน้าที่มี pagination เพิ่ม:
```html
<link rel="prev" href="...">
<link rel="next" href="...">
```

### 4. Image Optimization
- ใช้ format WebP
- Lazy loading
- เพิ่ม alt text ทุกรูป
- ขนาดรูปที่เหมาะสม

### 5. Internal Linking
- Link ระหว่างหนังสือที่เกี่ยวข้อง
- Link จาก category ไปยังหนังสือ
- Link จากหน้าแรกไปยังหนังสือแนะนำ

---

## การวัดผล SEO

### KPIs ที่ควรติดตาม:
1. **Organic Traffic** - จำนวนผู้เข้าชมจาก Google
2. **Keyword Rankings** - อันดับของ keywords
3. **Click-Through Rate (CTR)** - อัตราการคลิกจาก search results
4. **Bounce Rate** - อัตราการออกจากเว็บทันที
5. **Average Session Duration** - ระยะเวลาเฉลี่ยที่อยู่ในเว็บ
6. **Pages per Session** - จำนวนหน้าที่เข้าชมต่อครั้ง
7. **Conversion Rate** - อัตราการซื้อหนังสือ

### เครื่องมือวิเคราะห์:
- Google Analytics 4
- Google Search Console
- Bing Webmaster Tools
- Ahrefs / SEMrush (เสียเงิน)

---

## การตั้งค่า Site Domain สำหรับ Production

**สำคัญมาก!** ก่อนเปิด production ต้องอัพเดต domain ของเว็บไซต์:

```bash
python manage.py shell
```

```python
from django.contrib.sites.models import Site
site = Site.objects.get(id=1)
site.domain = 'uncle-ebook.com'  # เปลี่ยนเป็น domain จริงของคุณ
site.name = 'Uncle EBook'
site.save()
print(f"✅ Site updated: {site.domain}")
exit()
```

หรือใช้คำสั่งเดียว:
```bash
python manage.py shell -c "from django.contrib.sites.models import Site; site = Site.objects.get(id=1); site.domain = 'uncle-ebook.com'; site.name = 'Uncle EBook'; site.save(); print('✅ Site updated')"
```

---

## Checklist ก่อน Launch

- [ ] **อัพเดต Site Domain เป็น production domain** (ตามขั้นตอนด้านบน)
- [ ] ตรวจสอบ sitemap.xml ทำงาน
- [ ] ตรวจสอบ robots.txt ถูกต้อง
- [ ] ทุกหน้ามี unique title และ description
- [ ] มี og:image สำหรับทุกหน้าสำคัญ
- [ ] Structured data ผ่าน Rich Results Test
- [ ] Mobile-Friendly ผ่าน Google Test
- [ ] Page Speed > 80 (Mobile & Desktop)
- [ ] SSL Certificate ติดตั้งแล้ว (HTTPS)
- [ ] Google Analytics ทำงาน
- [ ] Google Search Console ลงทะเบียนแล้ว
- [ ] ส่ง sitemap ไปยัง Google และ Bing

---

## Tips สำหรับ SEO ภาษาไทย

1. **ใช้ภาษาไทยที่เป็นธรรมชาติ** - อย่ายัด keywords
2. **เขียน meta description ให้น่าสนใจ** - เพิ่ม CTA
3. **ใช้ชื่อไฟล์รูปเป็นภาษาไทย** - หรือภาษาอังกฤษที่เกี่ยวข้อง
4. **สร้าง content ที่มีคุณภาพ** - Google ชอบ content ที่ดี
5. **Update content เป็นประจำ** - Google ชอบเว็บที่ active
6. **สร้าง backlinks** - รับ link จากเว็บอื่นที่มีคุณภาพ
7. **ใช้ Social Media** - แชร์บน Facebook, Twitter, LINE

---

## ติดต่อและความช่วยเหลือ

หากมีคำถามเกี่ยวกับ SEO:
- Email: support@uncle-ebook.com
- LINE: @uncleebook

สร้างโดย: Claude AI Assistant
วันที่: 13 พฤศจิกายน 2568
