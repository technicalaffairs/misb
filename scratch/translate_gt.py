import os, re

filepath = r'c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_gen_docs\Ar_Gas Turbines_docs Page.htm'
with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

replacements = {
    "Nubaria CCPS": "محطة النوبارية (دورة مركبة)",
    "Port Said GT": "محطة بورسعيد الغازية",
    "El-Shabab GT": "محطة الشباب الغازية",
    "Talkha GT": "محطة طلخا الغازية",
    "Nubaria PS": "محطة النوبارية",
    "Mahmoudia PS": "محطة المحمودية",
    "Demiatta GT": "محطة دمياط الغازية",
    "Wady Hof": "محطة وادي حوف",
    "Talkha 750": "محطة طلخا 750",
    "Kafr El Dawar": "محطة كفر الدوار",
    
    "Air Intake, Kafeer, W1": "مأخذ الهواء، كافير، فحص أسبوعي W1",
    "Air Intake, Kafeer, H \n      4000": "مأخذ الهواء، كافير، فحص 4000 ساعة",
    "Air Intake, Kafeer, H \n      8000": "مأخذ الهواء، كافير، فحص 8000 ساعة",
    "Fuel Oil Flow \n      Distributor, type 4, Roper Pump Co., Y1": "موزع تدفق زيت الوقود، النوع 4، شركة Roper للطلمبات، فحص سنوي Y1",
    "Gas Turbine GT9DUAL Brown Boveri &amp; Co. \n    Ltd Switzerland GT, OH 20000": "التوربينة الغازية GT9DUAL، شركة Brown Boveri &amp; Co. Ltd سويسرا، عَمرة 20000 ساعة",
    "Combustion Chamber of Gas \n      Turbine GT94.2A3, Siemens, H8000": "غرفة الاحتراق للتوربينة الغازية GT94.2A3، سيمنز، فحص 8000 ساعة",
    "Turbine &amp; Compressor, \n      V94-3A, Siemens Germany, Y1": "التوربينة والضاغط، V94-3A، سيمنز ألمانيا، فحص سنوي Y1",
    "Gas turbine frame 5 Series \n\t\t5001 General Electric\n\t\t,Lub. oil cooler": "التوربينة الغازية فريم 5 سلسلة 5001 جنرال إلكتريك، مبرد زيت التزييت",
    "Gas turbine frame 5 Series \n\t\t5001 General Electric ,according differential pressure": "التوربينة الغازية فريم 5 سلسلة 5001 جنرال إلكتريك، وفقاً للضغط التفاضلي",
    "Combustion Chamber Tiles, BBC Switzerland, \n    H 2000": "بلاطات غرفة الاحتراق، BBC سويسرا، فحص 2000 ساعة",
    "Hot Gas Casing, BBC Switzerland, H 2000": "غلاف الغاز الساخن، BBC سويسرا، فحص 2000 ساعة",
    "High \n    Pressure Sight Glass of Flame Monitor, \n    \n    BBC Switzerland, H 2000": "زجاجة المراقبة ذات الضغط العالي لمراقب اللهب، BBC سويسرا، فحص 2000 ساعة",
    "Gas \n    Turbine 135MW, \n     V 94.2, \n     Siemens \n    Germany, EOH 8000": "التوربينة الغازية 135 ميجاوات، V 94.2، سيمنز ألمانيا، 8000 ساعة تشغيل مكافئة",
    "Over Speed Governor, \n      R2201, BBC, every 4000 EOH Service": "حاكم السرعة الزائدة، R2201، BBC، صيانة كل 4000 ساعة تشغيل مكافئة",
    "Fuel Gas Piping, GT Frame IV, GE, H12000": "مواسير غاز الوقود، التوربينة الغازية فريم 4، جنرال إلكتريك، فحص 12000 ساعة",
    "Heat Exchanger of Closed \n\t\tCooling Water System": "المبادل الحراري لنظام مياه التبريد المغلق",
    "Heat Exchanger for High \n        Pressure Heater System, (I2-8000 h)": "المبادل الحراري لنظام سخانات الضغط العالي، (فحص I2 - 8000 ساعة)",
    "Heat Exchanger for Low \n        Pressure Heater System, (I2-8000 h)": "المبادل الحراري لنظام سخانات الضغط المنخفض، (فحص I2 - 8000 ساعة)",
    "Ratchet \n        Turning Gear, GE, M6": "جهاز التدوير ذو السقاطة، جنرال إلكتريك، فحص 6 شهور M6",
    "Water/Air Cooler, EK V23/11-4R, LUWA, M6": "مبرد الماء/الهواء، EK V23/11-4R، LUWA، فحص 6 شهور M6",
    "Gas turbine frame 5 Series \n\t\t5001 General Electric \n\t\t,Lub. oil cooler": "التوربينة الغازية فريم 5 سلسلة 5001 جنرال إلكتريك، مبرد زيت التزييت",
}

for eng, ar in replacements.items():
    text = text.replace(eng, ar)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print("Translation completed.")
