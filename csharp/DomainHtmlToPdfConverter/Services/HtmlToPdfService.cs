using System;
using System.Diagnostics;
using System.IO;

namespace DomainHtmlToPdfConverter.Services
{
    internal class HtmlToPdfService
    {
        private readonly string _wkhtmltopdfPath;

        public HtmlToPdfService(string wkhtmltopdfPath)
        {
            _wkhtmltopdfPath = wkhtmltopdfPath;
        }

        public void Convert(string htmlFilePath, string outputPdfPath)
        {
            if (!File.Exists(_wkhtmltopdfPath))
            {
                throw new FileNotFoundException("wkhtmltopdf bulunamadı.", _wkhtmltopdfPath);
            }

            var processStartInfo = new ProcessStartInfo
            {
                FileName = _wkhtmltopdfPath,
                Arguments = string.Format("--enable-local-file-access \"{0}\" \"{1}\"", htmlFilePath, outputPdfPath),
                UseShellExecute = false,
                RedirectStandardError = true,
                RedirectStandardOutput = true,
                CreateNoWindow = true
            };

            using (var process = Process.Start(processStartInfo))
            {
                if (process == null)
                {
                    throw new InvalidOperationException("wkhtmltopdf işlemi başlatılamadı.");
                }

                process.WaitForExit();
                if (process.ExitCode != 0)
                {
                    var error = process.StandardError.ReadToEnd();
                    throw new InvalidOperationException("PDF üretimi başarısız: " + error);
                }
            }
        }
    }
}
