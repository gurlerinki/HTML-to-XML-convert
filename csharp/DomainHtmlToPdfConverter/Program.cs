using System;
using System.Collections.Generic;
using System.Configuration;
using System.IO;
using System.Linq;
using DomainHtmlToPdfConverter.Services;

namespace DomainHtmlToPdfConverter
{
    internal static class Program
    {
        private static int Main(string[] args)
        {
            if (args.Length < 2)
            {
                Console.WriteLine("Kullanım: DomainHtmlToPdfConverter.exe <html_klasoru> <pdf_klasoru>");
                return 1;
            }

            var inputFolder = args[0];
            var outputFolder = args[1];

            if (!Directory.Exists(inputFolder))
            {
                Console.WriteLine("HTML klasörü bulunamadı: " + inputFolder);
                return 1;
            }

            Directory.CreateDirectory(outputFolder);

            var authorizationService = new DomainAuthorizationService(
                ConfigurationManager.AppSettings["AllowedDomain"],
                ConfigurationManager.AppSettings["AllowedUser"],
                ConfigurationManager.AppSettings["AllowedComputer"]);

            if (!authorizationService.IsAuthorized())
            {
                Console.WriteLine("Bu bilgisayar veya kullanıcı etki alanı politikasına göre yetkili değil.");
                return 2;
            }

            var htmlFiles = Directory.GetFiles(inputFolder, "*.html", SearchOption.TopDirectoryOnly)
                                     .Concat(Directory.GetFiles(inputFolder, "*.htm", SearchOption.TopDirectoryOnly))
                                     .Distinct(StringComparer.OrdinalIgnoreCase)
                                     .ToList();

            if (!htmlFiles.Any())
            {
                Console.WriteLine("Dönüştürülecek HTML dosyası bulunamadı.");
                return 0;
            }

            var converter = new HtmlToPdfService(ConfigurationManager.AppSettings["WkhtmltopdfPath"]);
            var batchService = new BatchConversionService(converter, ConfigurationManager.AppSettings["LogDirectory"]);

            var summary = batchService.Convert(htmlFiles, outputFolder);

            Console.WriteLine("Toplam: {0}, Başarılı: {1}, Hatalı: {2}",
                summary.TotalCount,
                summary.SuccessCount,
                summary.FailureCount);

            return summary.FailureCount == 0 ? 0 : 3;
        }
    }
}
