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

Bu komut arayüz için gerekli ``streamlit`` kütüphanesini de kurar.
Unicode karakterleri içeren PDF çıktısı alınabilmesi için depo kökünde bulunan
``Fonts`` klasöründeki ``DejaVuSans.ttf`` dosyası kullanılır. Dosya mevcut
değilse sistemdeki ``/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf`` yolu
denenir.

Varsayılan olarak font aşağıdaki konumlarda aranır:

1. ``Fonts/DejaVuSans.ttf``
2. ``/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf``

## FONT_PATH Ortam Değişkeni

Uygulama PDF oluştururken varsayılan olarak yukarıdaki konumlardaki
``DejaVuSans.ttf`` dosyasını kullanır. Font bulunamazsa program hata verir.
Bu durumda ``FONT_PATH`` ortam değişkenini tanımlayarak farklı bir ``.ttf``
dosyası kullanabilirsiniz:

```bash
export FONT_PATH="/tam/yol/AlternatifFont.ttf"
```
Dosyayı indirdikten sonra bu değişkeni tanımlayıp uygulamayı
çalıştırmanız yeterlidir. Geçerli bir yol belirttiğinizde PDF işlemleri
bu font ile devam eder.
## OpenAI Anahtari

`LLMAnalyzer` sinifi OpenAI API'sini kullanir. Gercek bir sorgu icin
`OPENAI_API_KEY` ortam degiskenini asagidaki gibi tanimlayin veya ayni
isimli degiskeni `.env` dosyaniza ekleyin. Uygulama baslatildiginda dosya
varsa otomatik olarak yuklenir:

```bash
export OPENAI_API_KEY="sk-..."
```

Gecerli bir anahtar saglanmadiginda veya baglanti kurulamazsa analiz
sonuclari icin yer tutucu metinler dondurulur.

`OPENAI_MODEL` degiskenini `.env` dosyanizda ya da dogrudan ortamda
tanimlayarak kullanilacak model adini belirleyebilirsiniz. Deger
verilmezse varsayilan `gpt-3.5-turbo` kullanilir.

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

`8D_Guide.json` dosyasi uygulamaya gomulu varsayilan rehber verisiyle eslenmistir.
Bu dosyayi silerseniz `GuideManager.get_format("8D")` yine calisir ve dahili
veriyi kullanir. Diger rehber dosyalari gomulu olmadigindan yerinde kalmalidir;
ornegin `Guidelines/A3_Guide.json` dosyasi yoksa ayni fonksiyon
`GuideNotFoundError` hatasi verir.

## Prompts Klasoru

`Prompts/` klasorunde farkli rapor metodlari icin hazirlanmis JSON istem
sablonlari bulunur. Cogu dosya `*_Prompt.json` adini tasir ve iki ana bolum
icerir:

1. **system**: LLM'e gonderilecek genel sistem mesajini tanimlar.
2. **steps**: Her adim icin baslik ve kullanilacak metin sablonlarini icerir.

Bazi sablon dosyalari ise (ornegin `8D_Prompt.json`) her adim icin ayri
`system` ve `user_template` alanlari barindirir. Bu yapinin ornek bir parcasi
asagidaki gibidir:

```json
{
  "D1": { "system": "...", "user_template": "..." },
  "D2": { "system": "...", "user_template": "..." }
}
```

Uygulama icerisinde `PromptManager.get_template()` fonksiyonu metod adini
parametre olarak alir ve ilgili JSON dosyasini bu klasorden okuyup dondurur.
`LLMAnalyzer` sinifi bu sablonlari kullanarak her adim icin hazirlanan mesajlari
LLM'e iletir. `8D` metodunda ise bu adimlar atlanir ve tek seferde
`DEFAULT_8D_PROMPT` kullanilarak tam rapor uretilir. Bu durumda
`analyze` fonksiyonu `{"full_text": "..."}` biciminde sonuc dondurur.

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

## Streamlit Arayuzu

Bu arayuz icin `streamlit` kutuphanesi gereklidir ve `requirements.txt` dosyasinda yer alir.
Tarayici tabanli arayuzu calistirmak icin asagidaki komutu kullanabilirsiniz:

```bash
streamlit run UI/streamlit_app.py
```

Kok dizindeki ``run_app.py`` dosyasi ayni arayuzu kolayca ve uyarisiz sekilde acmanizi saglar:

```bash
python run_app.py
```

Bu komut arayuzu hicbir uyari gormeden baslatir.

Python kodu icinden `run_streamlit()` fonksiyonunu da cagirabilirsiniz:

```python
from UI import run_streamlit

run_streamlit()
```

## Minimal Ornek

Asagidaki kod ornegi girdi akisini nasil kullanabileceginizi gosterir:

```python
from GuideManager import GuideManager
from LLMAnalyzer import LLMAnalyzer
from ReportGenerator import ReportGenerator

text = "musteri sikayet metni"

guide = GuideManager()
guideline = guide.get_format("8D")

analyzer = LLMAnalyzer()
details = {"complaint": text}
analysis = analyzer.analyze(details, guideline)
result_text = analysis["full_text"]

reporter = ReportGenerator(guide)
info = {"customer": "ACME", "subject": "Issue", "part_code": "X"}
paths = reporter.generate(analysis, info, "raporlar")
print("PDF yolu:", paths["pdf"])
print("Excel yolu:", paths["excel"])
print(result_text)
```

## Cikti Formatlari

`ReportGenerator.generate` fonksiyonu olusturulan PDF ve Excel dosyalarinin yolunu dondurur.

Simdilik siniflar sadece taslak niteligindedir ve gercek islevler icermemektedir.

## Testler

Testler `fpdf`, `openpyxl` ve `python-dotenv` gibi ek paketlere baglidir.
Bu kutuphaneler `requirements.txt` dosyasinda listelenmistir.
Testleri calistirmadan once tum bagimliliklari kurdugunuzdan emin olun:

```bash
pip install -r requirements.txt
```

Bagimliliklari kurduktan sonra birim testlerini asagidaki komutla calistirabilirsiniz:

```bash
python -m unittest discover
```
