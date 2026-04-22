# HTML Converter Tools (Offline)

Bu depo artık iki farklı araç içerir:

1. **HTML → XML (XHTML) toplu dönüştürücü (CLI)**
2. **HTML → PDF toplu dönüştürücü (Masaüstü arayüz / GUI)**

Her iki araç da internet bağlantısı olmadan çalışır.

---

## 1) HTML → XML (CLI)

`html_to_xml_batch_no_lxml.py` bozuk HTML dosyalarını `html5lib` ile parse ederek iyi-biçimli XML (XHTML benzeri) çıktısı üretir.

### Kurulum

```bash
python -m pip install -r requirements.txt
```

### Kullanım

```bash
python html_to_xml_batch_no_lxml.py "C:\input_klasoru" -o "C:\output_klasoru"
```

Opsiyonlar:

- `--flat`: klasör yapısını korumadan tüm XML dosyalarını tek klasöre yazar.
- `--no-pretty`: girintileme (pretty-print) kapatılır.

---

## 2) HTML → PDF (GUI)

`html_to_pdf_gui.py`, kullanıcıya arayüz üzerinden:

- birden fazla HTML dosyası seçme,
- klasörden toplu HTML ekleme,
- PDF kayıt klasörü seçme,
- tek tıkla toplu PDF dönüştürme

imkânı verir.

### Çalıştırma (Geliştirici ortamı)

```bash
python html_to_pdf_gui.py
```

---

## Son kullanıcıda Python kurulu olmadan kullanım (EXE)

Aşağıdaki adımlarla Windows için tek dosya EXE üretebilirsiniz:

1. Gerekli paketleri kurun:

```bash
python -m pip install -r requirements.txt pyinstaller
```

2. EXE derleyin:

```bash
pyinstaller --noconfirm --onefile --windowed --name html-to-pdf-batch html_to_pdf_gui.py
```

3. Üretilen dosya:

- `dist/html-to-pdf-batch.exe`

Bu EXE son kullanıcı bilgisayarında **Python kurulu olmadan** çalışır.

---

## Notlar

- PDF kalitesi/uyumu HTML içeriğine bağlıdır.
- Çok karmaşık CSS/JS içeren sayfalarda sadeleştirme gerekebilir.
- Araçlar tamamen offline kullanım için uygundur.
