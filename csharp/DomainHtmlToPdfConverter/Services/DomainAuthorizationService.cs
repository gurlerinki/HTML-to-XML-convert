using System;
using System.DirectoryServices.ActiveDirectory;
using System.Management;
using System.Security.Principal;

namespace DomainHtmlToPdfConverter.Services
{
    internal class DomainAuthorizationService
    {
        private readonly string _allowedDomain;
        private readonly string _allowedUser;
        private readonly string _allowedComputer;

        public DomainAuthorizationService(string allowedDomain, string allowedUser, string allowedComputer)
        {
            _allowedDomain = allowedDomain ?? string.Empty;
            _allowedUser = allowedUser ?? string.Empty;
            _allowedComputer = allowedComputer ?? string.Empty;
        }

        public bool IsAuthorized()
        {
            if (!IsWorkstationOs())
            {
                return false;
            }

            if (!IsAllowedComputer())
            {
                return false;
            }

            if (!IsMachineInAllowedDomain())
            {
                return false;
            }

            return IsAllowedUser();
        }

        private static bool IsWorkstationOs()
        {
            try
            {
                using (var searcher = new ManagementObjectSearcher("SELECT ProductType FROM Win32_OperatingSystem"))
                {
                    foreach (ManagementObject os in searcher.Get())
                    {
                        var productType = Convert.ToInt32(os["ProductType"]);
                        return productType == 1;
                    }
                }
            }
            catch
            {
                return false;
            }

            return false;
        }

        private bool IsAllowedComputer()
        {
            return Environment.MachineName.Equals(_allowedComputer, StringComparison.OrdinalIgnoreCase);
        }

        private bool IsMachineInAllowedDomain()
        {
            try
            {
                var machineDomain = Domain.GetComputerDomain().Name;
                return machineDomain.Equals(_allowedDomain, StringComparison.OrdinalIgnoreCase);
            }
            catch
            {
                return false;
            }
        }

        private bool IsAllowedUser()
        {
            var identity = WindowsIdentity.GetCurrent();
            if (identity == null || string.IsNullOrWhiteSpace(identity.Name))
            {
                return false;
            }

            return identity.Name.Equals(_allowedUser, StringComparison.OrdinalIgnoreCase);
        }
    }
}
