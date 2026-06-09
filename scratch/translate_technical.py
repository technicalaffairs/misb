import os
import re
import time
import sys
from bs4 import BeautifulSoup, NavigableString
from deep_translator import GoogleTranslator

# Set output to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Folders definition
eng_dir = r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\appr_docs\ad_subst\ad_sub_tp"
ar_dir = r"c:\Users\sameh\OneDrive\المستندات\githup\mpis\misb\arabic_web\Ar_appr_docs\Ar_ad_subst\ad_ss_docs\new_translated"

# Ensure output directory exists
os.makedirs(ar_dir, exist_ok=True)

translator = GoogleTranslator(source='en', target='ar')

# High Voltage Electrical Engineering Dictionary (English -> Arabic) - Power Engineers Style
technical_dict = {
    # Headers & Metadata
    "Turns Ratio Test": "اختبار نسبة التحويل",
    "Turns Ratio Test For Two winding transformer": "اختبار نسبة التحويل للمحولات ثنائية الملفات",
    "Power Transformer": "محول القدرة",
    "Power Transformers": "محولات القدرة",
    "DC Winding Resistance Test": "اختبار مقاومة الملفات بالتيار المستمر",
    "D.C Winding Resistance Test (Two-Winding Transformer)": "اختبار مقاومة الملفات بالتيار المستمر (محول ثنائي الملفات)",
    "D.C Winding Resistance Test (Three-Winding Transformer)": "اختبار مقاومة الملفات بالتيار المستمر (محول ثلاثي الملفات)",
    "Three Winding Resistance Test Report": "تقرير اختبار مقاومة ملفات المحولات ثلاثية الملفات",
    "Three Winding Transformers Test": "اختبار محولات القدرة ثلاثية الملفات",
    "Two winding transformers": "محولات ثنائية الملفات",
    "Safety Precautions": "احتياطات السلامة والأمان",
    "Tools and Equipment": "الأجهزة والعدد المستخدمة",
    "Work to be Carried Out": "الإجراءات والخطوات المطلوب تنفيذها",
    "Technical Procedure": "إجراء فني معتمد",
    "Substations": "محطات المحولات",
    "Introduction": "مقدمة",
    "Equipment": "المعدة",
    "Procedure:": "الإجراء:",
    "Status:": "الموقف:",
    "Date Approved:": "تاريخ الاعتماد:",
    "Date to be Reviewed:": "تاريخ المراجعة التالية:",
    "Issued to:": "صادر إلى:",
    "Networks": "الشبكات",
    "APPROVED": "معتمد",
    "Test Sheet": "جدول القياسات والنتائج",
    "Tap Position": "وضع مغير الجهد (التاب)",
    "Current": "تيار القياس",
    "Phase": "الفازة",
    "Phase A": "الفازة R (أ)",
    "Phase B": "الفازة S (ب)",
    "Phase C": "الفازة T (ج)",
    "LV SIDE": "جهة الجهد المنخفض (LV)",
    "TERTIARY": "الملف الثالث (الترشيري)",
    "Location: Equipment code:": "الموقع: كود المعدة:",
    "Checked by: Date: Signature:": "راجع بمعرفة: التاريخ: التوقيع:",
    "Megger Tests": "اختبارات مقاومة العزل (الميجر)",
    "5000 V Megger Tests": "اختبارات مقاومة العزل بجهد 5000 فولت",
    "Megger test (5000V)": "اختبار الميجر (5000 فولت)",
    "Insulation tested": "العزل المختبر",
    "R60/R15": "معامل الاستقطاب R60/R15",
    "Resistance at 15 sec": "مقاومة العزل بعد 15 ثانية",
    "Resistance at 15 sec.": "مقاومة العزل بعد 15 ثانية",
    "Resistance at 60 sec": "مقاومة العزل بعد 60 ثانية",
    "Tan δ %": "عامل الفقد (تان دلتا %)",
    "Insulation Capacitance and Tan δ Dissipation Factor for Two Winding Transformer type CB 100 TEOF": "قياس سعة العزل وعامل الفقد (تان دلتا) لمحولات ثنائية الملفات طراز CB 100 TEOF",
    "High Voltage Tan δ testing (Results corrected to be at 20 ˚C": "اختبار تان دلتا للجهد العالي (النتائج مصححة عند 20 درجة مئوية)",
    "Test mode \" GST H-guard \" keep all pervious connections.": "وضع القياس (تأريض مع حماية العالي GST H-guard) مع الإبقاء على التوصيلات السابقة.",
    "Test mode \" GST L - Ground \"": "وضع القياس (تأريض مع حماية المنخفض GST L - Ground)",
    "Test mode \" GST l - Guard \" Keep all pervious connection.": "وضع القياس (تأريض مع حماية المنخفض GST l - Guard) مع الإبقاء على التوصيلات السابقة.",
    "Test mode \" GSTL- ground \" . Connect HV cable of the to S.C.. LV bushing": "وضع القياس (GSTL-ground) مع ربط كابل الجهد العالي لجهاز القياس بعوازل الجهد المنخفض المقصرة",
    "Test mode \" UST \" Keep all pervious connection.": "وضع القياس غير المؤرض (UST) مع الإبقاء على التوصيلات السابقة.",
    "Test mode \" UST-ground \" keep all pervious connections.": "وضع القياس غير المؤرض (UST-ground) مع الإبقاء على التوصيلات السابقة.",
    
    # Sentences & Instructions
    "A work order must be issued and the qualified test group": "يجب إصدار أمر شغل وأن تلتزم مجموعة الاختبار المؤهلة بتعليمات السلامة",
    "A work order permit must be issued,": "يجب إصدار تصريح وأمر شغل،",
    "A work order permit must be issued.": "يجب إصدار تصريح وأمر شغل.",
    "A word order permit must be issued.": "يجب إصدار تصريح وأمر شغل.",
    "A word order permit must be issued,": "يجب إصدار تصريح وأمر شغل،",
    "A word": "تصريح",
    "order": "أمر الشغل",
    "permit must be issued.": "يجب إصداره.",
    "All bushing must be clean otherwise errors reading could be happened": "يجب تنظيف جميع عوازل الاختراق (البوشينج) جيداً لتجنب حدوث أخطاء في القراءات",
    "All bushing should be cleaned otherwise errors reading could be occurred,": "يجب تنظيف جميع عوازل الاختراق (البوشينج) جيداً لتجنب حدوث أخطاء في القراءات،",
    "All bushings should be clean other wise errors reading could be happened": "يجب تنظيف جميع عوازل الاختراق (البوشينج) جيداً لتجنب حدوث أخطاء في القراءات",
    "Apply the + VE probe of megger to the S.C LV bushing. Apply the - VE probe of megger to the a S.C HV bushing.": "توصيل الطرف الموجب (+ VE) لجهاز الميجر بعوازل الجهد المنخفض المقصرة. وتوصيل الطرف السالب (- VE) بعوازل الجهد العالي المقصرة.",
    "Apply the + ve probe of megger to the S.C. HV bushing": "توصيل الطرف الموجب لجهاز الميجر بعوازل الجهد العالي المقصرة",
    "Apply the + ve probe of megger to the S.C. LV bushing": "توصيل الطرف الموجب لجهاز الميجر بعوازل الجهد المنخفض المقصرة",
    "Apply the + ve probe of megger to the S.C. LV& HV bushing": "توصيل الطرف الموجب لجهاز الميجر بعوازل الجهد المنخفض والجهد العالي المقصرة",
    "Apply the +ve probe of megger to S.C HV bushing and apply the -ve probe of megger to the earth point of the TR": "توصيل الطرف الموجب لجهاز الميجر بعوازل الجهد العالي المقصرة وتوصيل الطرف السالب بنقطة تأريض المحول",
    "Apply the +ve probe of megger to the S.C HV bushing.": "توصيل الطرف الموجب لجهاز الميجر بعوازل الجهد العالي المقصرة.",
    "Apply the +ve probe of megger to the S.C HV bushing. Apply the -ve probe of megger to the S.C LV bushing": "توصيل الطرف الموجب لجهاز الميجر بعوازل الجهد العالي المقصرة والطرف السالب بعوازل الجهد المنخفض المقصرة",
    "Apply the +ve probe of megger to the SH.C. Ter V bushing and apply the -ve probe of megger to the earth point of the TR": "توصيل الطرف الموجب لجهاز الميجر بعوازل الملف الثالث (الترشيري) المقصرة والطرف السالب بنقطة تأريض المحول",
    "Apply the - ve probe of megger to the S.C. HV bushing": "توصيل الطرف السالب لجهاز الميجر بعوازل الجهد العالي المقصرة",
    "Apply the - ve probe of megger to the S.C. LV bushing": "توصيل الطرف السالب لجهاز الميجر بعوازل الجهد المنخفض المقصرة",
    "Apply the -ve probe of megger to the S.C LV bushing.": "توصيل الطرف السالب لجهاز الميجر بعوازل الجهد المنخفض المقصرة.",
    "Apply the ve probe of megger to the earth point E": "توصيل الطرف السالب لجهاز الميجر بنقطة الأرضي E",
    "Be sure that the bushing connections are well cleaned before you apply the megger test cables": "تأكد من تنظيف أطراف عوازل الاختراق جيداً قبل توصيل كابلات اختبار الميجر",
    "Because of the amount of energy that can be stored in a magnetic field, precautions should be taken before disconnecting the test leads from the transformer that is under test.": "نظراً لكمية الطاقة الكبيرة التي يمكن تخزينها في المجال المغناطيسي للملفات، يجب اتخاذ الاحتياطات اللازمة وعدم فصل أطراف القياس حتى يتم تفريغ الشحنة تماماً.",
    "Changeover the switch to \" DF \" Positions .And select the range and dial to get balance of pointer.": "قم بتحويل المفتاح إلى وضع قياس عامل الفقد (DF)، ثم اختر المدى المناسب واضبط التدريج لتحقيق اتزان مؤشر القياس.",
    "Connect HV Cable to S.C. HV Bushing": "توصيل كابل الجهد العالي بعوازل الجهد العالي المقصرة",
    "Connect LV cable of the to S.C.. HV bushing.": "توصيل كابل الجهد المنخفض بعوازل الجهد العالي المقصرة.",
    "Connect LV cable to S.C. LV bushing": "توصيل كابل الجهد المنخفض بعوازل الجهد المنخفض المقصرة",
    "Connect the HV three-phase test leads (H1, H2, and H3) to the three phases HV bushings (R, S, T) of the transformer. Notice that Ho is neutral point with the neutral bushing.": "قم بتوصيل أطراف اختبار الجهد العالي الثلاثية (H1, H2, H3) بأطراف عوازل الجهد العالي الثلاثة (R, S, T) للمحول. مع ملاحظة أن Ho هي نقطة التعادل وتوصل بعازل التعادل (النيوترال).",
    "Connect the S.C H V bushing with S.C LV bushing with S.C Ter bushing": "قم بقصر وتوصيل عوازل الجهد العالي مع عوازل الجهد المنخفض مع عوازل الملف الثالث (الترشيري)",
    "Connect the S.C HV bushing with S.C LV bushing to the point of the earth of the TR.": "قم بتوصيل عوازل الجهد العالي المقصرة وعوازل الجهد المنخفض المقصرة بنقطة تأريض المحول.",
    "Connect the S.C HV bushing with the S.C.. LV bushing": "قم بتوصيل عوازل الجهد العالي المقصرة مع عوازل الجهد المنخفض المقصرة",
    "Connect the S.C HV bushing with the earth point E of the TR with S.C TER bushing.": "قم بتوصيل عوازل الجهد العالي المقصرة والملف الثالث (الترشيري) المقصر بنقطة تأريض المحول E.",
    "Connect the S.C LV bushing with the S.C TER bushing with the earth point of the TR E": "قم بتوصيل عوازل الجهد المنخفض المقصرة والملف الثالث (الترشيري) المقصر بنقطة تأريض المحول E",
    "Connect the S.C. HV bushing with the earth point E of the TR": "قم بتوصيل عوازل الجهد العالي المقصرة بنقطة تأريض المحول E",
    "Connect the S.C. LV bushing with the earth point of the TR": "قم بتوصيل عوازل الجهد المنخفض المقصرة بنقطة تأريض المحول",
    "Connect the bridles to the earth.": "قم بتوصيل موصلات خطوط الشبكة بالأرضي.",
    "Connect the earth of tester to common earth of Substation.": "قم بتوصيل أرضي جهاز الاختبار بشبكة التأريض العمومية بالمحطة.",
    "Connect the earth of tester to the common earth of substation.": "قم بتوصيل أرضي جهاز الاختبار بشبكة التأريض العمومية بالمحطة.",
    "Connect the earth of the transformer to the earth point of the tester": "قم بتوصيل أرضي المحول بنقطة الأرضي الخاصة بجهاز القياس",
    "Connect the power cable and switch the test equipment ON.": "قم بتوصيل كابل التغذية وتشغيل جهاز القياس (ON).",
    "Connect the voltage test leads inside the current test leads.": "قم بتوصيل أطراف قياس الجهد داخل أطراف قياس التيار.",
    "Correct the reading to be at 20 ˚C.": "تصحيح القراءة لتكون عند درجة حرارة 20 درجة مئوية.",
    "Depress the test switch and wait until the current indicator reaches the maximum and stop rising. The yellow ready lamp should be flashing.": "اضغط على مفتاح بدء الاختبار وانتظر حتى يستقر مؤشر تيار القياس عند القيمة القصوى. يجب أن تومض لمبة البيان الصفراء (جاهز - Ready).",
    "Disassemble HV and LV leads of the TR,": "فصل أطراف الجهد العالي والجهد المنخفض للمحول،",
    "Disassemble HV and LV leads of the TRA": "فصل أطراف الجهد العالي والجهد المنخفض للمحول",
    "Disassemble all clamp from bushings (Hi-voltage side, Low-voltage side and tertiary if exists)": "فك جميع روزتات عوازل الاختراق (البوشينج) من جهة الجهد العالي والجهد المنخفض والملف الثالث إن وجد",
    "Disassembly all clamps from bushings (High Voltage side, Low Voltage side & tertiary if exists)": "فك جميع روزتات عوازل الاختراق (البوشينج) من جهة الجهد العالي والجهد المنخفض والملف الثالث إن وجد",
    "Disconnect the transformer from bridles": "فصل المحول عن أطراف الشبكة",
    "Don't misapply the High leads and Low leads of the test equipment to the transformer bushings.": "احذر من عكس توصيل أطراف الجهد العالي والجهد المنخفض لجهاز القياس بعوازل المحول.",
    "Dont touch test leads during test be careful of applied voltage 5kv DC.": "لا تلمس أطراف الاختبار أثناء القياس، انتبه لجهد الاختبار المسلط وقيمته 5 كيلو فولت مستمر.",
    "Dont touch test leads during test, take care of the applied voltage 5kv dc": "لا تلمس أطراف الاختبار أثناء القياس، انتبه لجهد الاختبار المسلط وقيمته 5 كيلو فولت مستمر.",
    "Earth the test equipment with common earth of the substation.": "قم بتأريض جهاز الاختبار بربطه بالأرضي العمومي للمحطة.",
    "Ensure that test/dumb switch is in dump position (green color).": "تأكد من أن مفتاح الاختبار/التفريغ في وضع التفريغ (Dump) ذو اللون الأخضر.",
    "Follow the test procedures as the next drawing": "اتبع خطوات إجراء الاختبار كما هو موضح بالرسم التخطيطي التالي",
    "For all tests make short circuit onto the 3 bushings of HV side and LV side": "لجميع الاختبارات، قم بعمل قصر (شورت سريكت) على عوازل الجهد العالي وعوازل الجهد المنخفض الثلاثة",
    "For all tests make short circuit onto the 3 bushings of HV side and LV side be sure that the bushing connections are well cleaned before you apply the meager test cables.": "لكافة الاختبارات، يتم قصر عوازل الجهد العالي وعوازل الجهد المنخفض، مع التأكد من تنظيف أطراف العوازل جيداً قبل توصيل كابلات الميجر.",
    "In case of star connection, connect the current test leads to each phase between HV bushing to neutral, and in case of delta connection put them between the two HV bushings": "في حالة التوصيل النجمة، يتم توصيل أطراف اختبار التيار لكل فازة بين عازل الجهد العالي ونقطة التعادل، وفي حالة التوصيل الدلتا يتم توصيلها بين عازلين من عوازل الجهد العالي",
    "Isolate the transformer \" out of service \"": "فصل وعزل المحول خارج الخدمة تماماً",
    "Isolate the transformer from service and earthed": "فصل وعزل المحول من الخدمة وتأريضه",
    "Isolate the transformer from service and earthed,": "فصل وعزل المحول من الخدمة وتأريضه،",
    "Isolate the transformer out of service and earth": "فصل وعزل المحول من الخدمة وتأريضه",
    "Isolate the transformer out of service earthen": "فصل وعزل المحول من الخدمة وتأريضه",
    "Keep test leads apart from the buahings.": "أبق أطراف كابلات القياس بعيدة عن جسم عوازل الاختراق.",
    "Make short circuit SC for HV side and LV side bushings": "قم بعمل قصر (Short Circuit) على عوازل الجهد العالي والجهد المنخفض",
    "Never remove the leads during the testing process and always allow enough time (it may take several minuets) to completely discharge the transformer being tested.": "يمنع منعاً باتاً فصل كابلات القياس أثناء الاختبار، ويجب دائماً الانتظار لوقت كافٍ (قد يستغرق عدة دقائق) لتفريغ شحنة ملفات المحول بالكامل.",
    "Note that: Potential test leads must not touch the current leads": "ملاحظة هامة: يجب ألا تلامس أطراف قياس الجهد أطراف قياس التيار",
    "Note: Dont operate the tap-changer during the test otherwise the current will be disconnected.": "تنبيه: لا تقم بتشغيل مغير الجهد (التاب تشينجر) أثناء الاختبار وإلا سيتم قطع تيار القياس.",
    "Record the result In the Attached Test sheet": "سجل النتائج في جدول القياسات المرفق",
    "Record the result for each phase and neutral at each tap-changer position in case of tapchanger on the HV side.": "سجل النتيجة لكل فازة ونقطة التعادل عند كل وضع لمغير الجهد في حال كان مغير الجهد في جهة الجهد العالي.",
    "Record the results in the record sheet": "سجل القراءات في جدول القياسات",
    "Record the results in the record sheet.": "سجل القراءات في جدول القياسات.",
    "Record the results on the attached test sheet": "سجل القراءات في جدول القياس المرفق",
    "Record the results on the attached test sheet.": "سجل القراءات في جدول القياس المرفق.",
    "Remove any earth": "فك أي تأريض مؤقت",
    "Remove any earth.": "فك أي تأريض مؤقت.",
    "Repeat each step with each phase (R, S & T).": "كرر الخطوات السابقة مع كل فازة (R, S, T).",
    "Repeat steps 4, 5, 7 on the test #1.": "كرر الخطوات 4 و 5 و 7 في الاختبار رقم 1.",
    "Repeat steps 4,5,7 On the pervious test.": "كرر الخطوات 4 و 5 و 7 في الاختبار السابق.",
    "Run the test between each as the following steps:": "قم بإجراء الاختبار بين الأطراف وفق الخطوات التالية:",
    "Run the test with each": "قم بإجراء الاختبار على ملفات",
    "Safety fence (rope) with caution marks surrounding the work area,": "تسييج منطقة العمل بحبل وشريط تحذيري يحيط بالمنطقة لحماية طاقم العمل،",
    "To terminate the test, depress the dump switch, wait for the ready lamp to stop flashing.": "لإنهاء الاختبار، اضغط على مفتاح التفريغ (Dump)، وانتظر حتى تتوقف لمبة البيان الصفراء عن الوميض تماماً لتفريغ كامل الشحنة.",
    "Turn off megger and calculate the ratio (R60 / R15)": "أوقف تشغيل الميجر واحسب نسبة الاستقطاب (R60 / R15)",
    "Turn off megger and calculate the ratio R60/R15.": "أوقف تشغيل الميجر واحسب نسبة الاستقطاب R60/R15.",
    "Turn off megger and calculate the ratio.": "أوقف تشغيل الميجر واحسب نسبة الاستقطاب.",
    "Turn off megger and calculate the ratio.(R60/R15)": "أوقف تشغيل الميجر واحسب نسبة الاستقطاب (R60/R15)",
    "Turn on megger and record the reading after 15 sec ( R15 and anather reading after 60 sec R60 )": "شغل الميجر وسجل القراءة بعد 15 ثانية (R15) ثم قراءة أخرى بعد 60 ثانية (R60)",
    "Turn on megger and record the reading after 15 sec. (R15) and record anther reading after 60 sec. (R60)": "شغل الميجر وسجل القراءة بعد 15 ثانية (R15) وسجل القراءة الأخرى بعد 60 ثانية (R60)",
    "Turn on megger and record the reading after 15 sec. (R15) and record anther reading after 60 second (R60)": "شغل الميجر وسجل القراءة بعد 15 ثانية (R15) وسجل القراءة الأخرى بعد 60 ثانية (R60)",
    "Turn on megger and record the reading after 15 sec.(R15)": "شغل الميجر وسجل القراءة بعد 15 ثانية (R15)",
    "Turn on megger and record the reading after 15 sec.(R15) and record anther reading after 60 sec. (R60)": "شغل الميجر وسجل القراءة بعد 15 ثانية (R15) وسجل القراءة الأخرى بعد 60 ثانية (R60)",
    "Turn-on to C position and dial switches of the tester to get balance of pointer.": "قم بتحويل المفتاح إلى وضع قياس السعة C واضبط تدريج الجهاز للوصول لاتزان مؤشر القياس.",
    "current leads Must not be Disconnected while the lamp is flashing": "يجب عدم فصل أطراف تيار القياس نهائياً أثناء وميض لمبة البيان (خطورة عالية)",
    "is neutral point with the neutral bushing.": "هي نقطة التعادل وتوصل بعازل التعادل.",
    "winding and for each phase. In the same manner and the same precautions.": "الملفات ولكل فازة بنفس الأسلوب وبنفس الاحتياطات السابقة.",

    # Additional missing sentences & fragments
    "3B-Turns Ratio Test For Two winding transformer": "اختبار نسبة التحويل لمحولات ثنائية الملفات",
    "AVO - International, 4651 Single Westmorland TX 75237 - 1017 USA": "شركة AVO International, العنوان: 4651 Single Westmorland TX 75237 - 1017 USA",
    "Approved Date:": "تاريخ الاعتماد:",
    "CH + CHL": "سعة الملفات العالية + الملفات بين العالية والمنخفضة (CH + CHL)",
    "CHL": "السعة بين ملفات العالي والمنخفض (CHL)",
    "CHL (UST)": "السعة بين ملفات العالي والمنخفض في وضع القياس UST",
    "CHT (UST)": "السعة بين ملفات العالي والثالث في وضع القياس UST",
    "CL + CHL": "سعة الملفات المنخفضة + الملفات بين العالية والمنخفضة (CL + CHL)",
    "CLH": "السعة بين ملفات المنخفض والعالي (CLH)",
    "CLT": "السعة بين ملفات المنخفض والثالث (CLT)",
    "CT +CHT": "سعة الملف الثالث + الملفات بين العالية والثالث (CT + CHT)",
    "Calculated": "القيمة المحسوبة",
    "Connect the LV three phase test leads (": "قم بتوصيل أطراف اختبار الجهد المنخفض الثلاثية (",
    "Electrical Testing Instruments Scarbough, Ontario Canada M1V1E7": "شركة Electrical Testing Instruments, أونتاريو، كندا M1V1E7",
    "Feb": "فبراير",
    "Feb 2006": "فبراير 2006",
    "HV to (LV+T+E)": "الجهد العالي إلى (الجهد المنخفض + الملف الثالث + الأرضي)",
    "HV to LV": "الجهد العالي إلى الجهد المنخفض",
    "HV to LV +E": "الجهد العالي إلى (الجهد المنخفض + الأرضي)",
    "LV to (HV+T+E)": "الجهد المنخفض إلى (الجهد العالي + الملف الثالث + الأرضي)",
    "LV to HV": "الجهد المنخفض إلى الجهد العالي",
    "LV to HV +E": "الجهد المنخفض إلى (الجهد العالي + الأرضي)",
    "Megger 5000 V": "اختبار الميجر بجهد 5000 فولت",
    "Pfd Cap.": "السعة (pF)",
    "Ratio Test Results (for Three Winding Transformer)": "نتائج اختبار نسبة التحويل (محول ثلاثي الملفات)",
    "Ratio Test Results (for Two Winding Transformer)": "نتائج اختبار نسبة التحويل (محول ثنائي الملفات)",
    "Recocrd anther reading after 60 sec. (R60)": "سجل القراءة الأخرى بعد 60 ثانية (R60).",
    "Repeat the previous test procedure with rest phases H2, H": "كرر خطوات الاختبار السابقة مع بقية الفازات H2, H0",
    "Repeat the previous test procedure with rest phases H3, H1 ..... Press X": "كرر خطوات الاختبار السابقة مع بقية الفازات H3, H1 ..... ثم اضغط X",
    "Resistance at": "مقاومة العزل عند",
    "T to (H+L+E)": "الملف الثالث إلى (الجهد العالي + الجهد المنخفض + الأرضي)",
    "TAP": "التاب (مغير الجهد)",
    "TERTIARY": "الملف الثالث (الترشيري)",
    "TEST # 1 (C": "الاختبار رقم 1 (سعة",
    "Test # 1 HV -------- LV + E": "الاختبار رقم 1: الجهد العالي إلى الجهد المنخفض + الأرضي",
    "Test # 1 HV------> LV + Ter + E": "الاختبار رقم 1: الجهد العالي إلى الجهد المنخفض + الملف الثالث + الأرضي",
    "Test # 2 C": "الاختبار رقم 2: سعة",
    "Test # 2 LV -------- HV + E": "الاختبار رقم 2: الجهد المنخفض إلى الجهد العالي + الأرضي",
    "Test # 2 LV ------> HV + Ter + E": "الاختبار رقم 2: الجهد المنخفض إلى الجهد العالي + الملف الثالث + الأرضي",
    "Test # 3 C": "الاختبار رقم 3: سعة",
    "Test # 3 HV + LV": "الاختبار رقم 3: الجهد العالي + الجهد المنخفض",
    "Test # 3 Ter V ------> HV + LV + E": "الاختبار رقم 3: الملف الثالث إلى الجهد العالي + الجهد المنخفض + الأرضي",
    "Test # 4 C": "الاختبار رقم 4: سعة",
    "Test # 4 HV": "الاختبار رقم 4: الجهد العالي",
    "Test # 4 HV ------> LV": "الاختبار رقم 4: الجهد العالي إلى الجهد المنخفض",
    "Test # 5 C": "الاختبار رقم 5: سعة",
    "Test # 5 HV + LV + Ter ------>": "الاختبار رقم 5: الجهد العالي + الجهد المنخفض + الملف الثالث إلى",
    "Test # 6 C": "الاختبار رقم 6: سعة",
    "Test equipment type BM11 D": "جهاز اختبار طراز BM11 D",
    "Test equipment type BM11 D, The company address:": "جهاز اختبار طراز BM11 D، عنوان الشركة المصنعة:",
    "Test equipment type CB100-TEOF": "جهاز اختبار طراز CB100-TEOF",
    "Test equipment type DRX 2000, The company address: Electrical Testing Instruments Scarbough, Ontario Canada M1V1E7 telephone 416-292-8181, fax: 416-292-8188": "جهاز اختبار طراز DRX 2000، عنوان الشركة المصنعة: Electrical Testing Instruments Scarborough, Ontario Canada M1V1E7",
    "Test equipment type WRT100 The company address:": "جهاز اختبار طراز WRT100، عنوان الشركة المصنعة:",
    "The presence of current in load is signaled by flashing caution lamp and a display segment.": "يتم الاستدلال على مرور تيار الاختبار في الملفات (الحمل) عن طريق وميض لمبة البيان التحذيرية ومؤشر الشاشة.",
    "The qualified test grup staff should carry the suitable safety category": "يجب على طاقم الاختبار المؤهل الالتزام بمعايير وفئة السلامة والصحة المهنية المناسبة.",
    "The qualified test staff should carry the suitable safety category": "يجب على طاقم الاختبار المؤهل الالتزام بمعايير وفئة السلامة والصحة المهنية المناسبة.",
    "The qualified test staff should carry the suitable safety category,": "يجب على طاقم الاختبار المؤهل الالتزام بمعايير وفئة السلامة والصحة المهنية المناسبة،",
    "The test equipment is specifically designed for the measurement of dc resistance in high inductive alternator windings. It offers a choice of 4 full-scale resistance ranges in 2 channels.": "تم تصميم جهاز الاختبار خصيصاً لقياس مقاومة التيار المستمر للملفات ذات الحث العالي. ويوفر الجهاز 4 نطاقات قياس للمقاومة عبر قناتين.",
    "The yellow flashing ready lamp means current is flowing in the load": "وميض لمبة البيان الصفراء (جاهز - Ready) يعني مرور تيار القياس في الملفات (الحمل).",
    "This document lists the equipment Testing Procedure checklist, which must be performed for Power Transformers. According to each manufacturer Instructions.": "يحتوي هذا المستند على خطوات وإجراءات اختبار محولات القدرة الكهربائية طبقاً لتعليمات الشركة المصنعة.",
    "This document lists the equipment testing procedure checklist, which must be performed for power transformers according to each manufacturer Instructions.": "يحتوي هذا المستند على خطوات وإجراءات اختبار محولات القدرة الكهربائية طبقاً لتعليمات الشركة المصنعة.",
    "This document lists the equipment testing procedure checklist, which must be performed for power transformers. according to each manufacturer instructions.": "يحتوي هذا المستند على خطوات وإجراءات اختبار محولات القدرة الكهربائية طبقاً لتعليمات الشركة المصنعة.",
    "This document lists the steps for testing the turns ratio for the power transformers.": "يحتوي هذا المستند على خطوات وإجراءات اختبار نسبة التحويل (Turns Ratio) لمحولات القدرة.",
    "This will cause damage to the test equipment.": "قد يؤدي ذلك إلى حدوث تلف بجهاز الاختبار.",
    "Turn off megger and calculate the ratio.(R": "أوقف تشغيل جهاز الميجر واحسب نسبة الاستقطاب (R60/R15)",
    "Turn on megger and record the reading after 15 sec.(R15) and": "شغل الميجر وسجل القراءة بعد 15 ثانية (R15) وسجل القراءة الأخرى بعد 60 ثانية (R60)",
    "Turn on megger and record the reading after 15 sec.(R15)and record anther reading after 60 sec. (R60)": "شغل الميجر وسجل القراءة بعد 15 ثانية (R15) وسجل القراءة الأخرى بعد 60 ثانية (R60)",
    "You can change the range of the resistance to get accurate results, but it is not permitted to change the current setting while the current flow. If you need to change the current setting you should terminate the test.": "يمكن تغيير مدى المقاومة للحصول على قراءات دقيقة، ولكن يمنع منعاً باتاً تغيير قيمة تيار الاختبار أثناء مرور التيار. وإذا استدعى الأمر تغيير قيمة التيار، يجب إنهاء الاختبار أولاً.",
    "and record anther reading after 60 sec. (R60)": "وسجل القراءة الأخرى بعد 60 ثانية (R60).",
    "staff should carry the suitable safety category,": "يجب على طاقم العمل الالتزام بمعايير وفئة السلامة والصحة المهنية المناسبة،",
    "telephone 416-292-8181, fax: 416-292-8188": "هاتف: 416-292-8181، فاكس: 416-292-8188",
    "to be Reviewed:": "تاريخ المراجعة التالية:",
    "3) to the three phase LV bushing of the transformer notice that": "3) بأطراف عوازل الجهد المنخفض الثلاثة للمحول مع ملاحظة أن",
    
    # Extra terms observed in actual files
    "Apply the +ve probe of megger to the SH.C. Ter V bushing and apply the -ve probe of megger to the earth point E.": "توصيل الطرف الموجب (+ve) لجهاز الميجر بعوازل الملف الثالث (الترشيري) المقصرة، وتوصيل الطرف السالب (-ve) بنقطة تأريض المحول E.",
    "Apply the +ve probe of megger to the SH.C. Ter V bushing and apply the -ve probe of megger to the earth point E": "توصيل الطرف الموجب (+ve) لجهاز الميجر بعوازل الملف الثالث (الترشيري) المقصرة، وتوصيل الطرف السالب (-ve) بنقطة تأريض المحول E",
    "Apply the +ve probe of megger to the S.C HV bushing. Apply the -ve probe of megger to the S.C LV bushing": "توصيل الطرف الموجب (+ve) لجهاز الميجر بعوازل الجهد العالي المقصرة والطرف السالب (-ve) بعوازل الجهد المنخفض المقصرة",
    "is neutral point with the neutral bushing.": "هي نقطة التعادل وتوصل بعازل التعادل.",
    "Document No:": "رقم الوثيقة:",
    "Testing Procedure(s)": "إجراء (إجراءات) الاختبار",
    "05 Feb 2001": "05 فبراير 2001",
    "Date": "التاريخ",
    "Note :": "ملاحظة :",
    "60 sec.": "60 ثانية.",
    "(HV+LV+T) to E": "(الجهد العالي + الجهد المنخفض + الملف الثالث) إلى الأرضي",
    "Test #": "الاختبار رقم",
    "Notes": "ملاحظات",
    
    # New additions for the final 13 items
    "- Press X": "- اضغط على X",
    "- Press the test button Record the result.": "- اضغط على زر بدء الاختبار وسجل النتيجة.",
    "- Switch on the tester and press H": "- قم بتشغيل جهاز القياس واضغط على H",
    "..... Press X": "..... اضغط على X",
    "5000V": "5000 فولت",
    "Testing Procedures": "إجراءات الاختبار"
}

# Words/abbreviations that must remain in English
SKIP_WORDS = {
    "CH", "CL", "HL", "CHL", "CHT", "CLH", "CLT", "CT", "E", "HV", "LV", "T", "C", "DF", 
    "R15", "R60", "R60/R15", "BM11 D", "WRT100", "DRX 2000", "CB100-TEOF", "AVO",
    "H1", "H2", "H3", "H0", "X1", "X2", "X3", "X0", "Y1", "Y2", "Y3", "Y1-Y2", "Y2-Y3", "Y3-Y1",
    "X1-X0", "X2-X0", "X3-X0", "H1-H0", "H2-H0", "H3-H0", "H1-H2", "H2-H3", "H3-H1",
    "An-an", "Bn-bn", "Cn-cn", "ESts", "inding", "RANSFORMER", "TR"
}

# Regex to detect text that shouldn't be translated (like terminal names, numbers, or document codes)
CODE_PATTERNS = [
    r'^[H|X|Y]\d+-[H|X|Y]\d+$',
    r'^[H|X|Y]\d+$',
    r'^[T|CB|BB|B|Ch|FS|PT|CT|TC|TD|TB]-\d+-[r|R]\d+[a-z]?$',
    r'^\d+$',
    r'^[A-Z]$',
    r'^[R|S|T]$',
    r'^[H|L]V$',
    r'^D\.?C\.?$',
    r'^A\.?C\.?$',
    r'^Vacuum$',
    r'^MR$',
    r'^WRT100$',
    r'^Programa$',
    r'^TM\s*\d+$'
]

def should_skip(text):
    text = text.strip()
    if not text:
        return True
    
    # Skip if only punctuation or mathematical expressions
    if re.match(r'^[^\w\s]+$', text):
        return True
        
    # Remove leading/trailing parentheses and check
    text_clean = re.sub(r'^[()\[\]{}]+|[()\[\]{}]+$', '', text).strip()
    
    # If the clean text matches standard code patterns
    for p in CODE_PATTERNS:
        if re.match(p, text_clean, re.IGNORECASE):
            return True
            
    # Check if the clean text is in our skip words list
    if text_clean.upper() in SKIP_WORDS or text_clean in SKIP_WORDS:
        return True
        
    # Skip vector connection fragments like "An-an (X", "Bn-bn (Y", "Cn-cn (X", etc.
    # Also skip "/" symbol or formulas like ")/(X"
    if re.search(r'(An-an|Bn-bn|Cn-cn|X|Y|H|L|E|T|C|DF|R15|R60|sec)', text_clean, re.IGNORECASE):
        # If it looks like a formula or a split fragment:
        if len(text_clean) <= 12 and any(c in text_clean for c in "()[]/+-><="):
            return True
        if text_clean.startswith(')') or text_clean.endswith('('):
            return True
        if '/' in text_clean and len(text_clean) <= 6:
            return True
            
    # Skip standard mathematical combinations like "CH + CHL", "+ C", etc.
    expr_parts = re.split(r'[\s+\-*/()_&]+', text_clean)
    expr_parts = [p.strip() for p in expr_parts if p.strip()]
    if expr_parts and all(p.upper() in SKIP_WORDS or re.match(r'^\d+$', p) for p in expr_parts):
        return True
        
    return False

def translate_phrase(text):
    # Preserve original leading/trailing whitespace
    leading = text[:len(text) - len(text.lstrip())]
    trailing = text[len(text.rstrip()):] if len(text.rstrip()) < len(text) else ""
    
    text_stripped = " ".join(text.strip().split())
    if should_skip(text_stripped):
        return text
        
    # Check technical dictionary first (exact match)
    if text_stripped in technical_dict:
        return leading + technical_dict[text_stripped] + trailing
        
    # Partial matching check
    for eng_phrase, ar_phrase in technical_dict.items():
        if eng_phrase.lower() == text_stripped.lower():
            return leading + ar_phrase + trailing
            
    # Fallback to Google Translate for unseen text
    print(f"[FALLBACK] Unseen text, translating via Google Translate: '{text_stripped}'", flush=True)
    try:
        translated = translator.translate(text_stripped)
        print(f"[FALLBACK] Result: '{translated}'", flush=True)
        time.sleep(0.2)
        return leading + translated + trailing
    except Exception as e:
        print(f"[FALLBACK] Error: {e}", flush=True)
        return text

def translate_html_tree(node):
    if isinstance(node, NavigableString):
        if node.parent.name not in ['script', 'style', 'title']:
            translated = translate_phrase(str(node))
            node.replace_with(translated)
        return
        
    for child in list(node.children):
        translate_html_tree(child)

def process_file(filename):
    eng_path = os.path.join(eng_dir, filename)
    ar_filename = filename.replace("-r0.htm", "-r0a.htm").replace("-r1.htm", "-r1a.htm").replace("-r0.html", "-r0a.htm").replace("-r1.html", "-r1a.htm")
    ar_path = os.path.join(ar_dir, ar_filename)
    
    print(f"\n[TECHNICAL TRANSLATOR] Processing: {filename} -> {ar_filename}", flush=True)
    
    with open(eng_path, "r", encoding="windows-1252", errors="ignore") as f:
        html_content = f.read()
        
    soup = BeautifulSoup(html_content, "html.parser")
    
    # 1. Set RTL and lang tags
    html_tag = soup.find("html")
    if html_tag:
        html_tag["dir"] = "rtl"
        html_tag["lang"] = "ar"
        
    # Flip direction and alignment attributes from LTR to RTL
    for el in soup.find_all(dir=True):
        if el["dir"].lower() == "ltr":
            el["dir"] = "rtl"
            
    for el in soup.find_all(align=True):
        if el["align"].lower() == "left":
            el["align"] = "right"
            
    for el in soup.find_all(style=True):
        style = el["style"]
        style = re.sub(r'text-align\s*:\s*left', 'text-align: right', style, flags=re.IGNORECASE)
        style = re.sub(r'direction\s*:\s*ltr', 'direction: rtl', style, flags=re.IGNORECASE)
        el["style"] = style
        
    # Set proper encoding meta tag to UTF-8
    meta_charset = soup.find("meta", attrs={"http-equiv": "Content-Type"})
    if meta_charset:
        meta_charset["content"] = "text/html; charset=utf-8"
    else:
        meta_c = soup.find("meta", charset=True)
        if meta_c:
            meta_c["charset"] = "utf-8"
        else:
            new_meta = soup.new_tag("meta", attrs={"http-equiv": "Content-Type", "content": "text/html; charset=utf-8"})
            if soup.head:
                soup.head.insert(0, new_meta)
        
    # 2. Update relative paths to depth 5 (since they are in ad_ss_docs/new_translated/)
    for link in soup.find_all("link", rel="stylesheet"):
        href = link.get("href", "")
        if "style.css" in href:
            link["href"] = "../../../../../style.css"
            
    for body in soup.find_all("body"):
        if body.get("background"):
            body["background"] = body["background"].replace("../../../images/", "../../../../../images/")
            
    for img in soup.find_all("img"):
        src = img.get("src", "")
        if src:
            if "../../../images/" in src:
                img["src"] = src.replace("../../../images/", "../../../../../images/")
            elif "graphics/" in src:
                img["src"] = "../../../../../appr_docs/ad_subst/ad_sub_tp/" + src
            
    # Update title tag
    title_tag = soup.find("title")
    if title_tag:
        cleaned_title = " ".join(title_tag.string.split())
        title_tag.string = cleaned_title.replace("-r0", "-r0a").replace("-r1", "-r1a") + " معتمد (APPROVED)"

    # 3. Translate all HTML text nodes recursively
    translate_html_tree(soup)
    
    # 4. Save in isolated directory
    with open(ar_path, "w", encoding="utf-8") as out_f:
        out_f.write(str(soup))
        
    print(f"Generated Technical Arabic page: {ar_filename}", flush=True)

files_to_translate = [
    "T-022-r0.htm",
    "T-024-r0.htm",
    "T-025-r0.htm",
    "T-026-r0.htm",
    "T-027-r0.htm"
]

if __name__ == "__main__":
    for f in files_to_translate:
        process_file(f)
    print("\nTechnical translation pipeline complete! Files saved in new_translated/ folder.", flush=True)
