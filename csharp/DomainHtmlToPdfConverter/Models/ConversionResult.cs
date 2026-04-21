namespace DomainHtmlToPdfConverter.Models
{
    internal class ConversionResult
    {
        public int TotalCount { get; set; }

        public int SuccessCount { get; set; }

        public int FailureCount { get; set; }
    }
}
