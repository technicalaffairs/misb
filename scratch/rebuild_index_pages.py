"""
سكريبت إعادة بناء صفحات الفهرس المرجعية بالعربية الاحترافية
يقرأ الملف الأصلي ويستبدل النص العربي المفقود (بسبب windows-1256) بنص عربي صحيح
"""
import re, os, shutil

BASE = r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_appr_docs\Ar_ad_subst"

# ===== إعادة بناء Ar_ad_Trafo.htm =====
trafo_html = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html dir="rtl" lang="ar">
<head>
<link href="../../../style.css" rel="stylesheet"/>
<title>MPIS - محولات القدرة</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<meta content="Microsoft FrontPage 5.0" name="GENERATOR"/>
<style>
<!--
div.Section1 {page:Section1;}
span.MsoHyperlink {color:blue; text-decoration:underline;}
-->
</style>
</head>
<body dir="rtl" background="../../../images/sand.gif" bgcolor="#ffffff" text="#000000" link="#0033CC" vlink="#666633">

<p dir="rtl" style="font-family: Traditional Arabic; font-size: 22pt; font-weight: bold; color: #0033CC; text-align: right; margin-bottom: 5px;">
نظام معلومات إجراءات الصيانة — محطات المحولات
</p>
<p dir="rtl" style="font-family: Traditional Arabic; font-size: 18pt; font-weight: bold; color: #003399; text-align: right; border-bottom: 2px solid #003399; margin-bottom: 10px;">
محولات القدرة — سجل الوثائق المعتمدة
</p>

<table border="1" cellpadding="6" cellspacing="0" width="100%" style="border-collapse:collapse; font-family: Traditional Arabic; font-size: 14pt;" dir="rtl">
<thead>
  <tr style="background-color: #003399; color: white;">
    <th dir="rtl">رقم الوثيقة</th>
    <th dir="rtl">وصف المحول / الموقع</th>
    <th dir="rtl">الجهة المصنعة</th>
    <th dir="rtl">الجهد / القدرة</th>
    <th dir="rtl">تاريخ الاعتماد</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td dir="ltr"><a href="ad_ss_docs/T-001-r1a.htm">T-001-r1a</a></td>
    <td dir="rtl">محول القدرة الرئيسي — صيانة وفحص دوري</td>
    <td dir="rtl">متعدد</td>
    <td dir="rtl">11/220/500 ك.ف — 150 م.ف.أ</td>
    <td dir="rtl">يناير 2001</td>
  </tr>
  <tr style="background-color: #f0f4ff;">
    <td dir="ltr"><a href="ad_ss_docs/T-002-r1a.htm">T-002-r1a</a></td>
    <td dir="rtl">محول القدرة — 11/66 ك.ف</td>
    <td dir="rtl">متعدد</td>
    <td dir="rtl">11/66 ك.ف — 25 م.ف.أ</td>
    <td dir="rtl">يونيو 1999</td>
  </tr>
  <tr>
    <td dir="ltr"><a href="ad_ss_docs/T-003-r0a.htm">T-003-r0a</a></td>
    <td dir="rtl">محول I1-Y1 — 125 م.ف.أ — اختبار وفحص</td>
    <td dir="rtl">TU</td>
    <td dir="rtl">66/11 ك.ف — 125 م.ف.أ</td>
    <td dir="rtl">يونيو 1999</td>
  </tr>
  <tr style="background-color: #f0f4ff;">
    <td dir="ltr"><a href="ad_ss_docs/T-003-r1a.htm">T-003-r1a</a></td>
    <td dir="rtl">محول I1-Y1 — 125 م.ف.أ (مراجعة 1)</td>
    <td dir="rtl">Fuji</td>
    <td dir="rtl">66/11 ك.ف — 125 م.ف.أ</td>
    <td dir="rtl">يونيو 1999</td>
  </tr>
  <tr>
    <td dir="ltr"><a href="ad_ss_docs/T-004-r1a.htm">T-004-r1a</a></td>
    <td dir="rtl">محول (I1-Y1) — 125 م.ف.أ (مراجعة 1)</td>
    <td dir="rtl">Fuji</td>
    <td dir="rtl">66/11 ك.ف — 125 م.ف.أ</td>
    <td dir="rtl">يونيو 1999</td>
  </tr>
  <tr style="background-color: #f0f4ff;">
    <td dir="ltr"><a href="ad_ss_docs/T-005-r0a.htm">T-005-r0a</a></td>
    <td dir="rtl">محول القدرة — فحص وصيانة (مراجعة 0)</td>
    <td dir="rtl">Fuji</td>
    <td dir="rtl">66/11 ك.ف — 125 م.ف.أ</td>
    <td dir="rtl">يونيو 1999</td>
  </tr>
  <tr>
    <td dir="ltr"><a href="ad_ss_docs/T-005-r1a.htm">T-005-r1a</a></td>
    <td dir="rtl">محول القدرة — فحص وصيانة (مراجعة 1)</td>
    <td dir="rtl">Fuji</td>
    <td dir="rtl">66/11 ك.ف — 125 م.ف.أ</td>
    <td dir="rtl">مارس 2002</td>
  </tr>
  <tr style="background-color: #f0f4ff;">
    <td dir="ltr"><a href="ad_ss_docs/T-032-r0a.htm">T-032-r0a</a></td>
    <td dir="rtl">محول القدرة — اختبارات صيانة دورية</td>
    <td dir="rtl">—</td>
    <td dir="rtl">66/11 ك.ف</td>
    <td dir="rtl">سبتمبر 2002</td>
  </tr>
  <tr>
    <td dir="ltr"><a href="ad_ss_docs/T-033-r0a.htm">T-033-r0a</a></td>
    <td dir="rtl">محول I2-Y1 — اختبارات صيانة دورية</td>
    <td dir="rtl">—</td>
    <td dir="rtl">66/11 ك.ف — 25 م.ف.أ</td>
    <td dir="rtl">أكتوبر 2002</td>
  </tr>
  <tr style="background-color: #f0f4ff;">
    <td dir="ltr"><a href="ad_ss_docs/T-041-r0a.htm">T-041-r0a</a></td>
    <td dir="rtl">محول القدرة — 66/11 ك.ف</td>
    <td dir="rtl">ABB</td>
    <td dir="rtl">66/11 ك.ف — 25 م.ف.أ</td>
    <td dir="rtl">أكتوبر 2002</td>
  </tr>
  <tr>
    <td dir="ltr"><a href="ad_ss_docs/T-042-r0a.htm">T-042-r0a</a></td>
    <td dir="rtl">محول القدرة — صيانة وفحص</td>
    <td dir="rtl">—</td>
    <td dir="rtl">—</td>
    <td dir="rtl">—</td>
  </tr>
  <tr style="background-color: #f0f4ff;">
    <td dir="ltr"><a href="ad_ss_docs/T-043-r0a.htm">T-043-r0a</a></td>
    <td dir="rtl">محول القدرة ABB — 66/11 ك.ف</td>
    <td dir="rtl">ABB</td>
    <td dir="rtl">66/11 ك.ف — 25 م.ف.أ</td>
    <td dir="rtl">—</td>
  </tr>
</tbody>
</table>

<p dir="rtl" style="margin-top: 20px; font-family: Simplified Arabic; font-size: 11pt; color: #666;">
<b>ملاحظة:</b> جميع الوثائق المدرجة معتمدة وفق متطلبات نظام MPIS.
يُشترط الرجوع إلى النسخة المعتمدة قبل تنفيذ أي إجراء صيانة.
</p>

</body>
</html>
"""

# ===== إعادة بناء Ar_ad_Batteries.htm =====
batteries_html = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html dir="rtl" lang="ar">
<head>
<link href="../../../style.css" rel="stylesheet"/>
<title>MPIS - بطاريات المحطة</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<style><!--
div.Section1 {page:Section1;}
span.MsoHyperlink {color:blue; text-decoration:underline;}
--></style>
</head>
<body dir="rtl" background="../../../images/sand.gif" bgcolor="#ffffff" text="#000000" link="#0033CC" vlink="#666633">

<p dir="rtl" style="font-family: Traditional Arabic; font-size: 22pt; font-weight: bold; color: #0033CC; text-align: right; margin-bottom: 5px;">
نظام معلومات إجراءات الصيانة — محطات المحولات
</p>
<p dir="rtl" style="font-family: Traditional Arabic; font-size: 18pt; font-weight: bold; color: #003399; text-align: right; border-bottom: 2px solid #003399; margin-bottom: 10px;">
البطاريات وشواحن البطاريات — سجل الوثائق المعتمدة
</p>

<table border="1" cellpadding="6" cellspacing="0" width="100%" style="border-collapse:collapse; font-family: Traditional Arabic; font-size: 14pt;" dir="rtl">
<thead>
  <tr style="background-color: #003399; color: white;">
    <th dir="rtl">رقم الوثيقة</th>
    <th dir="rtl">الموقع / الوصف</th>
    <th dir="rtl">الشركة المصنعة</th>
    <th dir="rtl">النوع</th>
    <th dir="rtl">تاريخ الاعتماد</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td dir="ltr"><a href="ad_ss_docs/B-016-r0a.htm">B-016-r0a</a></td>
    <td dir="rtl">بطارية المحطة — (I1-Y1)</td>
    <td dir="rtl">Czech Ferak</td>
    <td dir="rtl">5KPM250P</td>
    <td dir="rtl">يوليو 2002</td>
  </tr>
  <tr style="background-color: #f0f4ff;">
    <td dir="ltr"><a href="ad_ss_docs/B-017-r0a.htm">B-017-r0a</a></td>
    <td dir="rtl">بطارية المحطة — (I2-Y2)</td>
    <td dir="rtl">Czech Ferak</td>
    <td dir="rtl">5KPM250P</td>
    <td dir="rtl">يوليو 2002</td>
  </tr>
  <tr>
    <td dir="ltr"><a href="ad_ss_docs/B-018-r0a.htm">B-018-r0a</a></td>
    <td dir="rtl">بطارية 175 أمبير/ساعة — (I3-Y3)</td>
    <td dir="rtl">FERAK - CZECHOSLOVAKIA</td>
    <td dir="rtl">E5KPM250P</td>
    <td dir="rtl">يوليو 2002</td>
  </tr>
  <tr style="background-color: #f0f4ff;">
    <td dir="ltr"><a href="ad_ss_docs/B-027-r0a.htm">B-027-r0a</a></td>
    <td dir="rtl">بطارية المحطة — صيانة دورية</td>
    <td dir="rtl">—</td>
    <td dir="rtl">—</td>
    <td dir="rtl">يناير 2005</td>
  </tr>
  <tr>
    <td dir="ltr"><a href="ad_ss_docs/B-031-r0a.htm">B-031-r0a</a></td>
    <td dir="rtl">بطارية المحطة — فحص وصيانة</td>
    <td dir="rtl">—</td>
    <td dir="rtl">—</td>
    <td dir="rtl">يناير 2004</td>
  </tr>
  <tr style="background-color: #f0f4ff;">
    <td dir="ltr"><a href="ad_ss_docs/Ch-010-r0a.htm">Ch-010-r0a</a></td>
    <td dir="rtl">شاحن البطارية — (I2-M1)</td>
    <td dir="rtl">CHLORIDE</td>
    <td dir="rtl">C3PF-2-60</td>
    <td dir="rtl">يوليو 2002</td>
  </tr>
  <tr>
    <td dir="ltr"><a href="ad_ss_docs/Ch-011-r0a.htm">Ch-011-r0a</a></td>
    <td dir="rtl">شاحن البطارية — (I3-M3)</td>
    <td dir="rtl">CHLORIDE</td>
    <td dir="rtl">C3PF-2-60</td>
    <td dir="rtl">يوليو 2002</td>
  </tr>
  <tr style="background-color: #f0f4ff;">
    <td dir="ltr"><a href="ad_ss_docs/Ch-012-r0a.htm">Ch-012-r0a</a></td>
    <td dir="rtl">شاحن البطارية — (I3-Y1)</td>
    <td dir="rtl">CHLORIDE</td>
    <td dir="rtl">C3PF-2-60</td>
    <td dir="rtl">يوليو 2002</td>
  </tr>
</tbody>
</table>
</body>
</html>
"""

# ===== إعادة بناء Ar_ad_tap_changers.htm =====
tapchanger_html = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html dir="rtl" lang="ar">
<head>
<link href="../../../style.css" rel="stylesheet"/>
<title>MPIS - مغيرات التفريعات</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<style><!-- div.Section1 {page:Section1;} span.MsoHyperlink {color:blue; text-decoration:underline;} --></style>
</head>
<body dir="rtl" background="../../../images/sand.gif" bgcolor="#ffffff" text="#000000" link="#0033CC" vlink="#666633">

<p dir="rtl" style="font-family: Traditional Arabic; font-size: 22pt; font-weight: bold; color: #0033CC; text-align: right; margin-bottom: 5px;">
نظام معلومات إجراءات الصيانة — محطات المحولات
</p>
<p dir="rtl" style="font-family: Traditional Arabic; font-size: 18pt; font-weight: bold; color: #003399; text-align: right; border-bottom: 2px solid #003399; margin-bottom: 10px;">
مغيرات التفريعات — سجل الوثائق المعتمدة
</p>

<table border="1" cellpadding="6" cellspacing="0" width="100%" style="border-collapse:collapse; font-family: Traditional Arabic; font-size: 14pt;" dir="rtl">
<thead>
  <tr style="background-color: #003399; color: white;">
    <th dir="rtl">رقم الوثيقة</th>
    <th dir="rtl">الموقع / الوصف</th>
    <th dir="rtl">الشركة المصنعة</th>
    <th dir="rtl">النوع</th>
    <th dir="rtl">تاريخ الاعتماد</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td dir="ltr"><a href="ad_ss_docs/TC-001-r0a.htm">TC-001-r0a</a></td>
    <td dir="rtl">مغير التفريعات — محول 66 ك.ف</td>
    <td dir="rtl">MR</td>
    <td dir="rtl">MR-5 (66 ك.ف)</td>
    <td dir="rtl">ديسمبر 2005</td>
  </tr>
  <tr style="background-color: #f0f4ff;">
    <td dir="ltr"><a href="ad_ss_docs/TC-004-r0a.htm">TC-004-r0a</a></td>
    <td dir="rtl">مغير التفريعات — محول 66 ك.ف (مراجعة 0)</td>
    <td dir="rtl">—</td>
    <td dir="rtl">—</td>
    <td dir="rtl">ديسمبر 2005</td>
  </tr>
  <tr>
    <td dir="ltr"><a href="ad_ss_docs/TC-005-r0a.htm">TC-005-r0a</a></td>
    <td dir="rtl">مغير التفريعات — محول 220 ك.ف (Trafo-union P1)</td>
    <td dir="rtl">Trafo-union</td>
    <td dir="rtl">CRNGS 230-2/533-521/40-16</td>
    <td dir="rtl">ديسمبر 2005</td>
  </tr>
</tbody>
</table>
</body>
</html>
"""

# ===== إعادة بناء Ar_ad_CT_PT_LA.htm =====
ct_pt_html = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html dir="rtl" lang="ar">
<head>
<link href="../../../style.css" rel="stylesheet"/>
<title>MPIS - محولات القياس وبارق الصواعق</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<style><!-- div.Section1 {page:Section1;} span.MsoHyperlink {color:blue; text-decoration:underline;} --></style>
</head>
<body dir="rtl" background="../../../images/sand.gif" bgcolor="#ffffff" text="#000000" link="#0033CC" vlink="#666633">

<p dir="rtl" style="font-family: Traditional Arabic; font-size: 22pt; font-weight: bold; color: #0033CC; text-align: right; margin-bottom: 5px;">
نظام معلومات إجراءات الصيانة — محطات المحولات
</p>
<p dir="rtl" style="font-family: Traditional Arabic; font-size: 18pt; font-weight: bold; color: #003399; text-align: right; border-bottom: 2px solid #003399; margin-bottom: 10px;">
محولات التيار / الجهد وبارق الصواعق — سجل الوثائق المعتمدة
</p>

<table border="1" cellpadding="6" cellspacing="0" width="100%" style="border-collapse:collapse; font-family: Traditional Arabic; font-size: 14pt;" dir="rtl">
<thead>
  <tr style="background-color: #003399; color: white;">
    <th dir="rtl">رقم الوثيقة</th>
    <th dir="rtl">الموقع / الوصف</th>
    <th dir="rtl">الشركة المصنعة</th>
    <th dir="rtl">النوع</th>
    <th dir="rtl">تاريخ الاعتماد</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td dir="ltr"><a href="ad_ss_docs/CT-014-r0a.htm">CT-014-r0a</a></td>
    <td dir="rtl">محولات التيار — (I1-Y1)</td>
    <td dir="rtl">ALSTHOM</td>
    <td dir="rtl">CTH 550 / CTH 420 / QDR-245 (500/400/220 ك.ف)</td>
    <td dir="rtl">مارس 2005</td>
  </tr>
  <tr style="background-color: #f0f4ff;">
    <td dir="ltr"><a href="ad_ss_docs/PT-009-r0a.htm">PT-009-r0a</a></td>
    <td dir="rtl">محولات الجهد (أحادية / ثلاثية الطور) — (I1-Y1)</td>
    <td dir="rtl">ALSTHOM</td>
    <td dir="rtl">متعدد (500/400/220 ك.ف)</td>
    <td dir="rtl">مارس 2005</td>
  </tr>
</tbody>
</table>
</body>
</html>
"""

# ===== إعادة بناء Ar_ad_DS_ES.htm =====
ds_es_html = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html dir="rtl" lang="ar">
<head>
<link href="../../../style.css" rel="stylesheet"/>
<title>MPIS - مفاتيح العزل والتأريض</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<style><!-- div.Section1 {page:Section1;} span.MsoHyperlink {color:blue; text-decoration:underline;} --></style>
</head>
<body dir="rtl" background="../../../images/sand.gif" bgcolor="#ffffff" text="#000000" link="#0033CC" vlink="#666633">

<p dir="rtl" style="font-family: Traditional Arabic; font-size: 22pt; font-weight: bold; color: #0033CC; text-align: right; margin-bottom: 5px;">
نظام معلومات إجراءات الصيانة — محطات المحولات
</p>
<p dir="rtl" style="font-family: Traditional Arabic; font-size: 18pt; font-weight: bold; color: #003399; text-align: right; border-bottom: 2px solid #003399; margin-bottom: 10px;">
مفاتيح العزل ومفاتيح التأريض — سجل الوثائق المعتمدة
</p>

<table border="1" cellpadding="6" cellspacing="0" width="100%" style="border-collapse:collapse; font-family: Traditional Arabic; font-size: 14pt;" dir="rtl">
<thead>
  <tr style="background-color: #003399; color: white;">
    <th dir="rtl">رقم الوثيقة</th>
    <th dir="rtl">الموقع / الوصف</th>
    <th dir="rtl">الشركة المصنعة</th>
    <th dir="rtl">النوع</th>
    <th dir="rtl">تاريخ الاعتماد</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td dir="ltr"><a href="ad_ss_docs/DS-010-r0a.htm">DS-010-r0a</a></td>
    <td dir="rtl">مفتاح عزل 66 ك.ف</td>
    <td dir="rtl">Elbrom Turbo (بلغاريا)</td>
    <td dir="rtl">RT-MM</td>
    <td dir="rtl">يوليو 2002</td>
  </tr>
  <tr style="background-color: #f0f4ff;">
    <td dir="ltr"><a href="ad_ss_docs/DS-030-r0a.htm">DS-030-r0a</a></td>
    <td dir="rtl">مفتاح عزل 220 ك.ف</td>
    <td dir="rtl">AEG</td>
    <td dir="rtl">VIS 300</td>
    <td dir="rtl">ديسمبر 2002</td>
  </tr>
  <tr>
    <td dir="ltr"><a href="ad_ss_docs/DS-035-r0a.htm">DS-035-r0a</a></td>
    <td dir="rtl">مفاتيح عزل ثلاثية الأقطاب — 66 ك.ف</td>
    <td dir="rtl">ABB-ARAB</td>
    <td dir="rtl">SGF 72.5</td>
    <td dir="rtl">يوليو 2002</td>
  </tr>
  <tr style="background-color: #f0f4ff;">
    <td dir="ltr"><a href="ad_ss_docs/DS-036-r0a.htm">DS-036-r0a</a></td>
    <td dir="rtl">مفاتيح عزل أحادية القطب — 66 ك.ف</td>
    <td dir="rtl">ABB-ARAB</td>
    <td dir="rtl">SGF 72.5</td>
    <td dir="rtl">يوليو 2002</td>
  </tr>
  <tr>
    <td dir="ltr"><a href="ad_ss_docs/DS-037-r0a.htm">DS-037-r0a</a></td>
    <td dir="rtl">مفاتيح عزل ثلاثية الأقطاب — 66 ك.ف</td>
    <td dir="rtl">Elbrom Turbo (بلغاريا)</td>
    <td dir="rtl">RT-MM</td>
    <td dir="rtl">يوليو 2002</td>
  </tr>
  <tr style="background-color: #f0f4ff;">
    <td dir="ltr"><a href="ad_ss_docs/DS-043-r0a.htm">DS-043-r0a</a></td>
    <td dir="rtl">مفاتيح العزل والتأريض — (I1-Y1) — 1000 أمبير</td>
    <td dir="rtl">ALSTHOM</td>
    <td dir="rtl">S2DA-L / S2DAT-L (500/400/220 ك.ف)</td>
    <td dir="rtl">مارس 2005</td>
  </tr>
</tbody>
</table>
</body>
</html>
"""

# ===== إعادة بناء Ar_ad_Busbars.htm =====
busbars_html = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html dir="rtl" lang="ar">
<head>
<link href="../../../style.css" rel="stylesheet"/>
<title>MPIS - قضبان التوصيل</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<style><!-- div.Section1 {page:Section1;} span.MsoHyperlink {color:blue; text-decoration:underline;} --></style>
</head>
<body dir="rtl" background="../../../images/sand.gif" bgcolor="#ffffff" text="#000000" link="#0033CC" vlink="#666633">

<p dir="rtl" style="font-family: Traditional Arabic; font-size: 22pt; font-weight: bold; color: #0033CC; text-align: right; margin-bottom: 5px;">
نظام معلومات إجراءات الصيانة — محطات المحولات
</p>
<p dir="rtl" style="font-family: Traditional Arabic; font-size: 18pt; font-weight: bold; color: #003399; text-align: right; border-bottom: 2px solid #003399; margin-bottom: 10px;">
قضبان التوصيل (العملة) — سجل الوثائق المعتمدة
</p>

<table border="1" cellpadding="6" cellspacing="0" width="100%" style="border-collapse:collapse; font-family: Traditional Arabic; font-size: 14pt;" dir="rtl">
<thead>
  <tr style="background-color: #003399; color: white;">
    <th dir="rtl">رقم الوثيقة</th>
    <th dir="rtl">الموقع / الوصف</th>
    <th dir="rtl">الشركة المصنعة</th>
    <th dir="rtl">الجهد</th>
    <th dir="rtl">تاريخ الاعتماد</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td dir="ltr"><a href="ad_ss_docs/BB-001-r0a.htm">BB-001-r0a</a></td>
    <td dir="rtl">قضبان التوصيل الرئيسية</td>
    <td dir="rtl">AEG</td>
    <td dir="rtl">11 ك.ف</td>
    <td dir="rtl">مارس 2003</td>
  </tr>
  <tr style="background-color: #f0f4ff;">
    <td dir="ltr"><a href="ad_ss_docs/BB-002-r0a.htm">BB-002-r0a</a></td>
    <td dir="rtl">قضبان التوصيل الثانوية</td>
    <td dir="rtl">ABB</td>
    <td dir="rtl">22 ك.ف</td>
    <td dir="rtl">مارس 2003</td>
  </tr>
  <tr>
    <td dir="ltr"><a href="ad_ss_docs/BB-003-r0a.htm">BB-003-r0a</a></td>
    <td dir="rtl">قضبان التوصيل — فحص بجهاز Hipotronics</td>
    <td dir="rtl">Hipotronics</td>
    <td dir="rtl">11 ك.ف</td>
    <td dir="rtl">نوفمبر 2004</td>
  </tr>
</tbody>
</table>
</body>
</html>
"""

# ===== إعادة بناء Ar_ad_condensers.htm =====
condensers_html = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html dir="rtl" lang="ar">
<head>
<link href="../../../style.css" rel="stylesheet"/>
<title>MPIS - مكثفات تحسين معامل الاستطاعة</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<style><!-- div.Section1 {page:Section1;} span.MsoHyperlink {color:blue; text-decoration:underline;} --></style>
</head>
<body dir="rtl" background="../../../images/sand.gif" bgcolor="#ffffff" text="#000000" link="#0033CC" vlink="#666633">

<p dir="rtl" style="font-family: Traditional Arabic; font-size: 22pt; font-weight: bold; color: #0033CC; text-align: right; margin-bottom: 5px;">
نظام معلومات إجراءات الصيانة — محطات المحولات
</p>
<p dir="rtl" style="font-family: Traditional Arabic; font-size: 18pt; font-weight: bold; color: #003399; text-align: right; border-bottom: 2px solid #003399; margin-bottom: 10px;">
مكثفات تحسين معامل الاستطاعة — سجل الوثائق المعتمدة
</p>

<table border="1" cellpadding="6" cellspacing="0" width="100%" style="border-collapse:collapse; font-family: Traditional Arabic; font-size: 14pt;" dir="rtl">
<thead>
  <tr style="background-color: #003399; color: white;">
    <th dir="rtl">رقم الوثيقة</th>
    <th dir="rtl">الموقع / الوصف</th>
    <th dir="rtl">الشركة المصنعة</th>
    <th dir="rtl">الجهد</th>
    <th dir="rtl">تاريخ الاعتماد</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td dir="ltr"><a href="ad_ss_docs/C-001-r0a.htm">C-001-r0a</a></td>
    <td dir="rtl">مكثف تحسين معامل الاستطاعة — (I1-M6)</td>
    <td dir="rtl">NOKIA</td>
    <td dir="rtl">11 ك.ف</td>
    <td dir="rtl">مارس 2005</td>
  </tr>
</tbody>
</table>
</body>
</html>
"""

# ===== إعادة بناء Ar_ad_compressors.htm =====
compressors_html = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html dir="rtl" lang="ar">
<head>
<link href="../../../style.css" rel="stylesheet"/>
<title>MPIS - ضاغطات الهواء</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<style><!-- div.Section1 {page:Section1;} span.MsoHyperlink {color:blue; text-decoration:underline;} --></style>
</head>
<body dir="rtl" background="../../../images/sand.gif" bgcolor="#ffffff" text="#000000" link="#0033CC" vlink="#666633">

<p dir="rtl" style="font-family: Traditional Arabic; font-size: 22pt; font-weight: bold; color: #0033CC; text-align: right; margin-bottom: 5px;">
نظام معلومات إجراءات الصيانة — محطات المحولات
</p>
<p dir="rtl" style="font-family: Traditional Arabic; font-size: 18pt; font-weight: bold; color: #003399; text-align: right; border-bottom: 2px solid #003399; margin-bottom: 10px;">
ضاغطات الهواء — سجل الوثائق المعتمدة
</p>

<p dir="rtl" style="font-family: Traditional Arabic; font-size: 14pt; color: #666; text-align: right; margin-top: 20px;">
لا توجد وثائق معتمدة مسجلة حالياً لضاغطات الهواء في هذا القسم.
يرجى التواصل مع المهندس المسؤول لمعرفة آخر المستجدات.
</p>
</body>
</html>
"""

# ===== إعادة بناء Ar_Distrib_Board.htm =====
distrib_html = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html dir="rtl" lang="ar">
<head>
<link href="../../../style.css" rel="stylesheet"/>
<title>MPIS - لوحة التوزيع الرئيسية</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
<style><!-- div.Section1 {page:Section1;} span.MsoHyperlink {color:blue; text-decoration:underline;} --></style>
</head>
<body dir="rtl" background="../../../images/sand.gif" bgcolor="#ffffff" text="#000000" link="#0033CC" vlink="#666633">

<p dir="rtl" style="font-family: Traditional Arabic; font-size: 22pt; font-weight: bold; color: #0033CC; text-align: right; margin-bottom: 5px;">
نظام معلومات إجراءات الصيانة — محطات المحولات
</p>
<p dir="rtl" style="font-family: Traditional Arabic; font-size: 18pt; font-weight: bold; color: #003399; text-align: right; border-bottom: 2px solid #003399; margin-bottom: 10px;">
لوحة التوزيع الرئيسية — سجل الوثائق المعتمدة
</p>

<p dir="rtl" style="font-family: Traditional Arabic; font-size: 14pt; color: #666; text-align: right; margin-top: 20px;">
لا توجد وثائق معتمدة مسجلة حالياً للوحة التوزيع الرئيسية في هذا القسم.
يرجى التواصل مع المهندس المسؤول لمعرفة آخر المستجدات.
</p>
</body>
</html>
"""

# ===== كتابة الملفات =====
to_write = {
    "Ar_ad_Trafo.htm": trafo_html,
    "Ar_ad_Batteries.htm": batteries_html,
    "Ar_ad_tap_changers.htm": tapchanger_html,
    "Ar_ad_CT_PT_LA.htm": ct_pt_html,
    "Ar_ad_DS_ES.htm": ds_es_html,
    "Ar_ad_Busbars.htm": busbars_html,
    "Ar_ad_compressors.htm": compressors_html,
    "Ar_ad_condensers.htm": condensers_html,
    "Ar_Distrib_Board.htm": distrib_html,
}

for fname, html_content in to_write.items():
    fp = os.path.join(BASE, fname)
    # Backup original
    backup = fp + ".bak"
    if not os.path.exists(backup):
        shutil.copy2(fp, backup)
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"OK Written: {fname}")

print("\nDone. All 9 index reference files rebuilt in Arabic.")
