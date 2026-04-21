using System;
using System.DirectoryServices.ActiveDirectory;
using System.Security.Principal;

namespace DomainHtmlToPdfConverter.Services
{
    internal class DomainAuthorizationService
    {
        private readonly string _allowedDomain;
        private readonly string _allowedUser;

        public DomainAuthorizationService(string allowedDomain, string allowedUser)
        {
            _allowedDomain = allowedDomain ?? string.Empty;
            _allowedUser = allowedUser ?? string.Empty;
        }

        public bool IsAuthorized()
        {
            if (!IsMachineInAllowedDomain())
            {
                return false;
            }

            return IsAllowedUser();
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
