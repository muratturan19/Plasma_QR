# 8D_Reporter

Otomatik 8D raporlama ve analizi icin gelistirilen Python paketi.

## Kurulum

1. Bu depoyu klonlayin.
2. Opsiyonel olarak bir sanal ortam olusturun ve etkinlestirin:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Gerekli bagimliliklari kurun (simdilik harici bagimlilik yoktur):

```bash
pip install -r requirements.txt
```

## Modul Yapisi

Proje asagidaki paketleri icermektedir:

- `UI`: Kullanici arayuzu islemlerini yonetir.
- `GuideManager`: 8D rehberi ve verileriyle ilgili islemleri saglar.
- `LLMAnalyzer`: Metinleri buyuk dil modeli kullanarak analiz eder.
- `Review`: Olusturulan rapor ya da analiz sonucunu gozden gecirir.
- `Comparison`: Iki veri kumesini veya raporu karsilastirir.
- `ReportGenerator`: Analiz sonucundan 8D raporu uretir.

Her paket icerisinde beklenen davranisi aciklayan siniflar yer almaktadir.

## Kullanici Girdisi Akisi

Kullanicidan alinan veriler uygulama icinde asagidaki yollari izler:

1. **UI** kullanicidan metin veya dosya konumunu toplar.
2. **GuideManager** bu veriyi 8D adimlariyla iliskilendirir.
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
guide.load_guide("guide.xlsx")

analyzer = LLMAnalyzer()
analysis = analyzer.analyze(text)

reporter = ReportGenerator()
pdf_path, excel_path = reporter.generate(analysis)
print("PDF kaydedildi:", pdf_path)
print("Excel kaydedildi:", excel_path)
```

## Cikti Formatlari

`ReportGenerator.generate` fonksiyonunun PDF ve Excel dosya yollarini dondurmesi beklenir.
Raporlar varsayilan olarak calisma dizininde `rapor.pdf` ve `rapor.xlsx` adiyla olusur.

Simdilik siniflar sadece taslak niteligindedir ve gercek islevler icermemektedir.
