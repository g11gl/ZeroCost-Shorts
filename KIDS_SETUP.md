# قناة Shorts التعليمية للأطفال (6–9 سنوات)

الإعداد المختار: **عربي فصيح بسيط**، **حروف وأرقام وألوان**، **صور كرتونية ثلاثية الأبعاد**، وصوت سعودي نسائي `ar-SA-ZariyahNeural`.

## قواعد الأمان قبل النشر العام

- كل فيديو من إعداد `kids_learning` يُرسل إلى YouTube مع `selfDeclaredMadeForKids: true` وفئة التعليم `27`.
- الرفع التلقائي مجدول الساعة **20:17 بتوقيت السعودية** (17:17 UTC) ويكون **Private** فقط. قد يتأخر موعد تشغيل GitHub Actions قليلًا.
- تشغيل `Run workflow` يدويًا يبدأ باختبار إعداد فقط (`smoke_test_only = true`) من دون أي مفاتيح. بعد إضافة `GROQ_API_KEY` و`DEAPI_TOKEN` يمكن إلغاء هذا الخيار لتوليد MP4 والاحتفاظ به في Artifacts. يمكن تحديد `upload_to_youtube` لرفع نسخة **خاصة** بعد إكمال OAuth.
- يمنع أمر `--privacy public` لمحتوى الأطفال ما لم تضف `--allow-public-kids` صراحة بعد مراجعة الفيديو. لا يوجد هذا الخيار في التشغيل المجدول.
- جرى تعطيل تشغيل ملفي `daily_facts.yml` و`daily_myth.yml` القديمين (بلا جدول زمني ومع `if: false`) حتى لا ينشرا فيديوهات غير موجهة للأطفال عند تفعيل GitHub Actions.
- راجع الحروف والنطق، صحة عدد العناصر والألوان في صور AI، وضوح النصوص العربية، مدة الصوت، حقوق الملكية، وأي معلومة غير مناسبة قبل التفكير في النشر العام.
- لأن جميع فيديوهات هذه القناة للأطفال، يُستحسن أيضًا ضبط جمهور القناة من **YouTube Studio → Settings → Channel → Advanced settings → Audience → Yes, set this channel as made for kids**. لا يحل هذا محل ضبط كل فيديو الذي يتولاه الكود.

## خدمات مطلوبة (تُضاف كـ GitHub Actions Secrets)

من مستودع GitHub: **Settings → Secrets and variables → Actions → New repository secret**.

| الاسم | الخدمة | الغرض |
| --- | --- | --- |
| `GROQ_API_KEY` | [Groq](https://console.groq.com/keys) | نص الدرس بالعربية |
| `DEAPI_TOKEN` | [deAPI](https://deapi.ai/) | إنشاء الرسوم ثلاثية الأبعاد |
| `YT_CLIENT_ID` | Google Cloud OAuth Desktop app | رفع الفيديو إلى قناتك |
| `YT_CLIENT_SECRET_VALUE` | Google Cloud OAuth Desktop app | رفع الفيديو إلى قناتك |
| `YT_REFRESH_TOKEN` | حساب قناة YouTube الموافق على OAuth | رفع الفيديو إلى قناتك |

خدمات الصور والنصوص قد تكون لها حدود مجانية أو تكاليف؛ راجع حسابك قبل تفعيل التشغيل اليومي. **لا تُرسل المفاتيح أو رموز OAuth في المحادثة ولا تضعها في ملفات GitHub العامة.**

لإعداد OAuth على جهازك فقط: فعّل [YouTube Data API v3](https://console.cloud.google.com/apis/library/youtube.googleapis.com) ثم أنشئ OAuth Client ID لنوع **Desktop app**، وضع الملف الذي نزلته في `secrets/client_secret.json`، وشغّل `python scripts/youtube_auth.py` بعد تثبيت `requirements.txt`. انسخ القيم الثلاث المطلوبة إلى Secrets. انتبه أن تطبيقات OAuth التي لا تزال في وضع Testing قد تحتاج إعادة تفويض لاحقًا.

## الاختبار قبل النشر

1. من قسم **Actions** فعّل Workflows إن كان GitHub يطلب ذلك للـ fork.
2. افتح **Daily YouTube Short → Run workflow**، واترك `smoke_test_only` محددًا لأول اختبار بلا مفاتيح. يجب أن تنجح الاختبارات الثلاثة.
3. بعد إضافة مفاتيح توليد النص والصور، كرر التشغيل وألغِ `smoke_test_only` واكتب موضوعًا مثل `الحرف أ: أرنب وأسد`، واترك `upload_to_youtube` غير محدد. بعد نجاحه حمّل **kids-review-...** من قسم Artifacts وراجع الفيديو.
4. راجع جودة الفيديو. إذا كان مناسبًا، كرر التشغيل مع تحديد `upload_to_youtube` بعد إكمال OAuth، وسيكون الفيديو **Private**.
5. من YouTube Studio تحقق من أن جمهور الفيديو **Made for Kids** وأن مستوى الخصوصية **Private**؛ ثم قرر يدويًا متى يصبح النشر العام مناسبًا. لا يُفعّل الكود النشر العام تلقائيًا.

## الاختبارات المحلية دون مفاتيح

```bash
python -m unittest discover -s tests -v
python -m compileall -q pipeline scripts tests
```

لتوليد عينة بدون رفع (تحتاج `GROQ_API_KEY` و`DEAPI_TOKEN`):

```bash
python scripts/run_short.py --channel kids_learning --topic "اللون الأحمر: التفاح والفراولة"
```

المخرجات: `output/runs/kids_learning_*/short.mp4`.
