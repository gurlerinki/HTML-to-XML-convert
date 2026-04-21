# Domain Yetkili HTML -> PDF Dönüştürücü (C# / .NET Framework 4.8)

Bu proje, domain ortamında **sunucuda değil sadece kullanıcının kendi bilgisayarında** ve izinli tek kullanıcı hesabı ile toplu şekilde HTML dosyalarını PDF'e çevirmek için hazırlanmıştır.

## 1) Nasıl indireceğim?

### Seçenek A - ZIP indir
1. Repo sayfasında **Code > Download ZIP** seç.
2. ZIP'i hedef sunucuya çıkar (örn: `C:\Apps\DomainHtmlToPdfConverter`).

### Seçenek B - Git ile klonla
```powershell
git clone <REPO_URL>
cd HTML-to-XML-convert\csharp\DomainHtmlToPdfConverter
```

> `<REPO_URL>` yerine kendi Git URL'inizi yazın.

## 2) Gereksinimler

Kurulum yapılacak kullanıcı bilgisayarında (workstation) şunlar olmalı:
- Domain'e join edilmiş Windows workstation
- **.NET Framework 4.8 Runtime**
- `wkhtmltopdf.exe` (önerilen yol: `C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe`)

## 3) Nasıl kuracağım?

### A) `wkhtmltopdf` kurulumu
1. `wkhtmltopdf` kurulum paketini yükleyin.
2. `wkhtmltopdf.exe` dosyasının aşağıdaki yolda olduğunu doğrulayın:
   - `C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe`

### B) Uygulama ayarlarını yap
`App.config` içindeki anahtarları ortamınıza göre düzenleyin:
- `AllowedDomain`: Domain adı (örn: `CORP.LOCAL`)
- `AllowedUser`: Çalıştırmaya izinli **tek kullanıcı** (örn: `CORP\\svc_pdf_runner`)
- `AllowedComputer`: Kullanıcının kendi bilgisayar adı (örn: `USER-LAPTOP-01`)
- `WkhtmltopdfPath`: `wkhtmltopdf.exe` yolu
- `LogDirectory`: log klasörü

### C) Derleme (build)
Visual Studio Developer Command Prompt veya Build Tools terminalinde:
```bat
msbuild DomainHtmlToPdfConverter.csproj /t:Build /p:Configuration=Release
```

Çıktı dosyası:
- `bin\Release\DomainHtmlToPdfConverter.exe`

## 4) Nasıl çalıştıracağım?

Komut satırından:
```bat
DomainHtmlToPdfConverter.exe "C:\InputHtml" "C:\OutputPdf"
```

Örnek:
```bat
DomainHtmlToPdfConverter.exe "D:\TopluHtml" "D:\TopluPdf"
```

Uygulama:
1. İşletim sisteminin sunucu değil workstation olduğunu doğrular.
2. Bilgisayar adının `AllowedComputer` ile birebir eşleştiğini kontrol eder.
3. Makinenin domain bilgisini doğrular.
4. Oturum açmış kullanıcının `AllowedUser` ile birebir eşleştiğini kontrol eder.
5. Klasördeki `.html` ve `.htm` dosyalarını PDF'e dönüştürür.
6. Sonucu log dosyasına yazar.

## 5) Servis gibi otomatik çalıştırma (öneri)

Task Scheduler ile yalnızca yetkili kullanıcı altında çalıştırın:
1. **Create Task**
2. **Run whether user is logged on or not**
3. User hesabı: `AllowedUser` ile aynı hesap
4. Action:
   - Program/script: `DomainHtmlToPdfConverter.exe`
   - Arguments: `"C:\InputHtml" "C:\OutputPdf"`

## 6) Sık karşılaşılan sorunlar

- **Yetkisiz kullanıcı hatası**: `AllowedUser` değeri ile oturum açan kullanıcı aynı değil.
- **Bilgisayar yetkisi hatası**: `AllowedComputer` ile mevcut bilgisayar adı uyuşmuyor.
- **Sunucuda çalışmama durumu**: Uygulama sadece workstation (ProductType=1) sistemlerde çalışır.
- **Domain hatası**: Bilgisayar domain'e bağlı değil veya `AllowedDomain` yanlış.
- **PDF oluşmuyor**: `WkhtmltopdfPath` yanlış ya da `wkhtmltopdf` kurulu değil.
- **Boş çıktı**: Girdi klasöründe `.html/.htm` dosyası yok.

## Mimari Özeti

- **Program.cs**: Girdi/çıktı klasörü alır ve tüm akışı başlatır.
- **DomainAuthorizationService**: Workstation + bilgisayar adı + domain + tek kullanıcı yetkisini doğrular.
- **HtmlToPdfService**: `wkhtmltopdf.exe` ile tekil dönüşüm yapar.
- **BatchConversionService**: Toplu dönüşüm + loglama yapar.
