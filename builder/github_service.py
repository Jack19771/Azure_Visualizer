import requests

class GitHubAzureResourceFetcher:
    def __init__(self):
        self.base_url = "https://api.github.com/repos/hashicorp/terraform-provider-azurerm"
    
    def get_resource_list(self):
        """Pobierz listę zasobów Azure z GitHub"""
        try:
            # Pobierz listę usług z /internal/services
            url = f"{self.base_url}/contents/internal/services"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                services = response.json()
                resources = []
                
                # Przykład parsowania - uproszczony
                known_resources = [
                    {"name": "azurerm_virtual_machine", "display": "Virtual Machine", "icon": "🖥️", "category": "compute"},
                    {"name": "azurerm_storage_account", "display": "Storage Account", "icon": "💾", "category": "storage"},
                    {"name": "azurerm_postgresql_server", "display": "PostgreSQL Database", "icon": "🗄️", "category": "database"},
                    {"name": "azurerm_virtual_network", "display": "Virtual Network", "icon": "🌐", "category": "network"},
                    {"name": "azurerm_resource_group", "display": "Resource Group", "icon": "📦", "category": "management"}
                ]
                
                return known_resources
            else:
                # Fallback do statycznej listy
                return self._get_static_resources()
                
        except Exception as e:
            print(f"GitHub API error: {e}")
            return self._get_static_resources()
    
    def _get_static_resources(self):
        return [
            {"name": "azurerm_virtual_machine", "display": "Virtual Machine", "icon": "🖥️", "category": "compute"},
            {"name": "azurerm_storage_account", "display": "Storage Account", "icon": "💾", "category": "storage"},
            {"name": "azurerm_postgresql_server", "display": "PostgreSQL Database", "icon": "🗄️", "category": "database"}
        ]