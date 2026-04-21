using System;
using System.Collections.Generic;
using System.IO;
using DomainHtmlToPdfConverter.Models;

namespace DomainHtmlToPdfConverter.Services
{
    internal class BatchConversionService
    {
        private readonly HtmlToPdfService _converter;
        private readonly string _logDirectory;

        public BatchConversionService(HtmlToPdfService converter, string logDirectory)
        {
            _converter = converter;
            _logDirectory = logDirectory;
        }

        public ConversionResult Convert(IReadOnlyList<string> htmlFiles, string outputFolder)
        {
            Directory.CreateDirectory(_logDirectory);
            var logPath = Path.Combine(_logDirectory, "conversion-" + DateTime.Now.ToString("yyyyMMdd-HHmmss") + ".log");

            var result = new ConversionResult { TotalCount = htmlFiles.Count };

            using (var writer = new StreamWriter(logPath, false))
            {
                foreach (var htmlFile in htmlFiles)
                {
                    var pdfName = Path.GetFileNameWithoutExtension(htmlFile) + ".pdf";
                    var outputPdf = Path.Combine(outputFolder, pdfName);

                    try
                    {
                        _converter.Convert(htmlFile, outputPdf);
                        result.SuccessCount++;
                        writer.WriteLine("OK | " + htmlFile + " -> " + outputPdf);
                    }
                    catch (Exception ex)
                    {
                        result.FailureCount++;
                        writer.WriteLine("ERR | " + htmlFile + " | " + ex.Message);
                    }
                }
            }

            return result;
        }
    }
}
