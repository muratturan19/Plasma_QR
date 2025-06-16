# Quality_Reporter

Otomatik kalite raporlama ve analizi icin gelistirilen Python paketi. 8D, A3,
Ishikawa, 5N1K ve DMAIC rapor metodlarindan birini secerek calisabilir.

## Kurulum

1. Bu depoyu klonlayin.
2. Opsiyonel olarak bir sanal ortam olusturun ve etkinlestirin:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Bagimliliklari kurmak icin asagidaki komutu calistirin:

```bash
pip install -r requirements.txt
```

## Modul Yapisi

Proje asagidaki paketleri icermektedir:

- `UI`: Kullanici arayuzu islemlerini yonetir.
- `GuideManager`: secilen rapor metodunun rehberini ve verilerini yonetir.
- `LLMAnalyzer`: Metinleri buyuk dil modeli kullanarak analiz eder.
- `Review`: Olusturulan rapor ya da analiz sonucunu gozden gecirir.
- `Comparison`: Iki veri kumesini veya raporu karsilastirir.
- `ReportGenerator`: Analiz sonucundan secilen metod icin rapor uretir.

Her paket icerisinde beklenen davranisi aciklayan siniflar yer almaktadir.

## Guidelines Klasoru

`Guidelines/` klasorunde 8D, A3, Ishikawa, 5N1K ve DMAIC metodlari icin
hazirlanmis JSON rehber dosyalari bulunur. `GuideManager.load_guide` fonksiyonuna
bu dosyalardan birinin yolunu vererek calismak istediginiz metodu secersiniz.
Ornegin `Guidelines/A3_Guide.json` yolunu kullanarak A3 metodunu secebilirsiniz.

## Kullanici Girdisi Akisi

Kullanicidan alinan veriler uygulama icinde asagidaki yollari izler:

1. **UI** kullanicidan metin veya dosya konumunu toplar.
2. **GuideManager** bu veriyi secilen metodun adimlariyla iliskilendirir.
3. **LLMAnalyzer** metni buyuk dil modeli araciligiyla yorumlar.
4. **Review** veya **Comparison** ihtiyaca gore analizi gozden gecirir.
5. **ReportGenerator** son raporu olusturarak diske yazar.

Bu surec asagidaki sekilde gosterilebilir:

```
[User] -> [UI] -> [GuideManager] -> [LLMAnalyzer] -> [ReportGenerator] -> PDF/Excel
```

## Ornek Kullanim

Paketleri kendi uygulamaniza dahil ederek asagidaki gibi kullanabilirsiniz:

```python
from UI import UI

ui = UI()
ui.start()
```

## Minimal Ornek

Asagidaki kod ornegi girdi akisini nasil kullanabileceginizi gosterir:

```python
from GuideManager import GuideManager
from LLMAnalyzer import LLMAnalyzer
from ReportGenerator import ReportGenerator

text = "musteri sikayet metni"

guide = GuideManager()
guide.load_guide("Guidelines/8D_Guide.json")

analyzer = LLMAnalyzer()
analysis = analyzer.analyze(text)

reporter = ReportGenerator(guide)
info = {"customer": "ACME", "subject": "Issue", "part_code": "X"}
paths = reporter.generate(analysis, info, "raporlar")
print("PDF yolu:", paths["pdf"])
print("Excel yolu:", paths["excel"])
```

## Cikti Formatlari

`ReportGenerator.generate` fonksiyonu olusturulan PDF ve Excel dosyalarinin yolunu dondurur.

Simdilik siniflar sadece taslak niteligindedir ve gercek islevler icermemektedir.
