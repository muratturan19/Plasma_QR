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

## Ornek Kullanim

Paketleri kendi uygulamaniza dahil ederek asagidaki gibi kullanabilirsiniz:

```python
from UI import UI

ui = UI()
ui.start()
```

Simdilik siniflar sadece taslak niteligindedir ve gercek islevler icermemektedir.
