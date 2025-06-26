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

Anahtari ve sikayet kaydi Excel dosyasinin yolunu kolayca tanimlamak icin
`configure_env.py` betigini calistirabilirsiniz. Betik istenen bilgileri
sorarak `.env` dosyasina yazar.

```bash
python configure_env.py
```

Bu islemin ardindan `CLAIMS_FILE_PATH` degiskeni de `.env` dosyaniza eklenmis
olur ve uygulama muster sikayetlerini bu dosyadan okur.

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
- `ComplaintSearch`: Musteri sikayetlerini kaydeder ve arar.

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

`Prompts/` klasorunde her rapor metodu icin hazirlanmis duz metin sablonlari
bulunur. Bu dosyalar `*_Prompt.txt` adini tasir ve icerisinde buyuk dil
modeline gonderilecek tum metinler yer alir. Degiskenler cift suslu parantez
(`{{...}}`) seklinde belirtilir ve calisma sirasinda verilen bilgilerle
degistirilir.

Uygulamada `PromptManager.get_text_prompt("A3")` gibi bir cagriyla ilgili
sablon dosyasi okunur ve `LLMAnalyzer` tarafindan kullanilir. `8D` metodunda
ayni klasorden `8D_Prompt.txt` dosyasi dogrudan okunur.

### Sablonlari Ozellestirme

Sistemin urettigi ciktilari degistirmek icin bu metin dosyalarini dilediginiz
metin duzenleyiciyle acip icerigi guncelleyebilirsiniz. Gerekirse kendi metot
adinizla yeni bir `*_Prompt.txt` dosyasi ekleyip `PromptManager.get_text_prompt`
fonksiyonuna bu adi verebilirsiniz. Yer tutuculari korudugunuz surece metin
icerigini serbestce degistirerek rapor formatini ihtiyaciniza gore ozellestire
bilirsiniz.

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
 Arayuzun sol panelinden gecmis sikayetlerde anahtar kelime arayabilirsiniz.
 Tarayici tabanli arayuzu calistirmak icin asagidaki komutu kullanabilirsiniz:

```bash
streamlit run run_app.py
```
Bu komut **deponun kok dizininden** calistirildiginda gerekli paketleri
dogru sekilde bulur ve arayuzu acar. `UI/streamlit_app.py` dosyasini
daha sonra calistirmak isterseniz, `PYTHONPATH` degiskenini depo kokune
ayarlamaniz gerekir; aksi halde `ModuleNotFoundError: No module named
'GuideManager'` hatasiyla karsilasabilirsiniz.

```bash
export PYTHONPATH="$(pwd)"
streamlit run UI/streamlit_app.py
```

Kok dizindeki ``run_app.py`` dosyasini kullanarak arayuzu uyarisiz sekilde acabilirsiniz:

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
Katkida bulunacak gelistiriciler, testleri calistirmadan once asagidaki komutla tum bagimliliklari kurmalidir:

```bash
pip install -r requirements.txt
```

Bagimliliklari kurduktan sonra birim testlerini asagidaki komutla calistirabilirsiniz:

```bash
python -m unittest discover
```

## EXE Paketleme

Uygulamayı Windows üzerinde tek bir çalıştırılabilir dosya haline getirmek
için `PyInstaller` kullanılabilir. Önce paketi kurun:

```bash
pip install pyinstaller
```

Daha sonra aşağıdaki komutla gerekli veri dosyalarıyla birlikte paketleyin:

```bash
pyinstaller --onefile run_app.py \
  --copy-metadata streamlit \
  --add-data 'Guidelines/*:Guidelines' \
  --add-data 'Prompts/*:Prompts' \
  --add-data 'Fonts/*:Fonts' \
  --add-data 'Logo/*:Logo' \
  --add-data 'CC/*:CC'
```

Oluşan `dist/run_app.exe` dosyası müşteri bilgisayarında doğrudan
çalıştırılabilir.
