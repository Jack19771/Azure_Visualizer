import requests
import re
import time
from typing import List, Dict, Optional
from django.conf import settings
from django.core.cache import cache

class TerraformResourceFetcher:
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.repo = "hashicorp/terraform-provider-azurerm"
        self.token = getattr(settings, 'GITHUB_TOKEN', None)
        
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Azure-Terraform-Builder/1.0',
        }
        
        if self.token:
            self.headers['Authorization'] = f'token {self.token}'
        
        # Rate limiting
        self.max_requests_per_hour = 5000 if self.token else 60
        self.request_delay = 0.1 if self.token else 1.0  # seconds
    
    def get_terraform_resources(self) -> List[Dict]:
        """Pobierz wszystkie zasoby Terraform z GitHub"""
        
        # Sprawdź cache
        cached_resources = cache.get('github_terraform_resources_complete')
        if cached_resources:
            print(f"Using cached resources: {len(cached_resources)} items")
            return cached_resources
        
        try:
            print("Fetching all Terraform resources from GitHub...")
            
            # Pobierz wszystkie katalogi usług
            service_dirs = self._get_all_service_directories()
            if not service_dirs:
                print("No service directories found, using fallback")
                return self._get_fallback_resources()
            
            print(f"Found {len(service_dirs)} service directories")
            
            # Pobierz zasoby z każdego katalogu
            all_resources = []
            processed_count = 0
            
            for service_dir in service_dirs:
                service_name = service_dir['name']
                print(f"Processing service: {service_name} ({processed_count + 1}/{len(service_dirs)})")
                
                resources = self._get_resources_from_service(service_name)
                if resources:
                    all_resources.extend(resources)
                    print(f"  Found {len(resources)} resources")
                
                processed_count += 1
                
                # Rate limiting
                time.sleep(self.request_delay)
                
                # Zatrzymaj po 100 usługach jeśli bez tokena (limit API)
                if not self.token and processed_count >= 50:
                    print("Reached API limit without token, stopping...")
                    break
            
            print(f"Total resources found: {len(all_resources)}")
            
            if all_resources:
                # Cache na 2 godziny
                cache.set('github_terraform_resources_complete', all_resources, 7200)
                return all_resources
            else:
                return self._get_fallback_resources()
                
        except Exception as e:
            print(f"Error fetching from GitHub: {e}")
            return self._get_fallback_resources()
    
    def _get_all_service_directories(self) -> List[Dict]:
        """Pobierz wszystkie katalogi usług z GitHub"""
        
        url = f"{self.base_url}/repos/{self.repo}/contents/internal/services"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            
            if response.status_code != 200:
                print(f"GitHub API returned {response.status_code}")
                return []
            
            services = response.json()
            
            # Filtruj tylko katalogi
            service_dirs = [
                service for service in services 
                if service.get('type') == 'dir'
            ]
            
            return service_dirs
            
        except requests.RequestException as e:
            print(f"Error fetching service directories: {e}")
            return []
    
    def _get_resources_from_service(self, service_name: str) -> List[Dict]:
        """Pobierz zasoby z konkretnej usługi"""
        
        url = f"{self.base_url}/repos/{self.repo}/contents/internal/services/{service_name}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code != 200:
                return []
            
            service_files = response.json()
            resources = []
            
            # Debug - print first few files
            if service_name == "compute":
                print(f"Debug files in {service_name}:")
                for f in service_files[:5]:
                    print(f"  {f.get('name')} (type: {f.get('type')})")
            
            # Szukaj plików *_resource.go (główny pattern w GitHub)
            for file in service_files:
                filename = file.get('name', '')
                if (file.get('type') == 'file' and 
                    filename.endswith('_resource.go') and
                    not filename.endswith('_test.go')):
                    
                    resource_name = self._extract_resource_name_from_service_file(filename, service_name)
                    if resource_name:
                        display_name = self._generate_display_name(resource_name)
                        icon = self._get_resource_icon(resource_name, service_name)
                        category = self._normalize_category_name(service_name)
                        
                        resources.append({
                            'name': resource_name,
                            'display': display_name,
                            'icon': icon,
                            'category': category,
                            'service': service_name
                        })
            
            return resources
            
        except requests.RequestException:
            return []
    
    def _extract_resource_name_from_service_file(self, filename: str, service_name: str) -> Optional[str]:
        """Wyciągnij nazwę zasobu z pliku w formacie {nazwa}_resource.go"""
        # Przykład: availability_set_resource.go + service: compute -> azurerm_availability_set
        
        if filename.endswith('_resource.go'):
            # Usuń _resource.go z końca
            resource_part = filename[:-12]  # len('_resource.go') = 12
            
            # Zbuduj pełną nazwę zasobu
            return f"azurerm_{resource_part}"
        
        return None
    
    def _generate_display_name(self, resource_name: str) -> str:
        """Generuj czytelną nazwę zasobu"""
        # azurerm_virtual_machine -> Virtual Machine
        name_part = resource_name.replace('azurerm_', '').replace('_', ' ')
        return ' '.join(word.capitalize() for word in name_part.split())
    
    def _normalize_category_name(self, service_name: str) -> str:
        """Znormalizuj nazwę kategorii"""
        category_mapping = {
            # Direct mappings
            'compute': 'compute',
            'network': 'network',
            'storage': 'storage',
            'keyvault': 'security',
            'security': 'security',
            'securitycenter': 'security',
            'monitor': 'monitoring',
            'loganalytics': 'monitoring',
            'applicationinsights': 'monitoring',
            'containers': 'containers',
            'web': 'web',
            'appservice': 'web',
            
            # Databases
            'mssql': 'database',
            'mysql': 'database',
            'postgres': 'database',
            'cosmosdb': 'database',
            'cosmos': 'database',
            'redis': 'database',
            'redisenterprise': 'database',
            
            # AI/ML
            'cognitive': 'ai',
            'machinelearning': 'ai',
            'bot': 'ai',
            
            # Messaging
            'servicebus': 'messaging',
            'eventhub': 'messaging',
            'eventgrid': 'messaging',
            'notificationhub': 'messaging',
            'signalr': 'messaging',
            
            # Management
            'resource': 'management',
            'managementgroup': 'management',
            'policy': 'management',
            'authorization': 'management',
            'subscription': 'management',
            
            # Data & Analytics
            'datafactory': 'analytics',
            'databricks': 'analytics',
            'synapse': 'analytics',
            'streamanalytics': 'analytics',
            'hdinsight': 'analytics',
            'kusto': 'analytics',
            'purview': 'analytics',
            
            # Integration
            'logic': 'integration',
            'apimanagement': 'integration',
            'serviceconnector': 'integration',
            
            # DevOps
            'devtestlabs': 'devops',
            'automation': 'devops',
            
            # Networking (specific)
            'dns': 'network',
            'privatedns': 'network',
            'trafficmanager': 'network',
            'frontdoor': 'network',
            'firewall': 'network',
            'loadbalancer': 'network',
            
            # IoT
            'iothub': 'iot',
            'iotcentral': 'iot',
            'digitaltwins': 'iot',
            
            # Mixed Reality / Gaming
            'mixedreality': 'media',
            
            # Healthcare
            'healthcare': 'industry',
            
            # Communication
            'communication': 'communication'
        }
        
        # Mapuj lub użyj oryginalnej nazwy
        return category_mapping.get(service_name.lower(), 'other')
    
    def _get_resource_icon(self, resource_name: str, category: str) -> str:
        """Przypisz ikonę do zasobu"""
        
        # Specific resource icons
        specific_icons = {
            # Compute
            'azurerm_virtual_machine': '🖥️',
            'azurerm_linux_virtual_machine': '🐧',
            'azurerm_windows_virtual_machine': '🪟',
            'azurerm_virtual_machine_scale_set': '📊',
            'azurerm_availability_set': '🔄',
            'azurerm_managed_disk': '💿',
            'azurerm_snapshot': '📸',
            
            # Network
            'azurerm_virtual_network': '🌐',
            'azurerm_subnet': '🔗',
            'azurerm_public_ip': '🌍',
            'azurerm_load_balancer': '⚖️',
            'azurerm_application_gateway': '🚪',
            'azurerm_firewall': '🔥',
            'azurerm_network_security_group': '🛡️',
            'azurerm_route_table': '🗺️',
            'azurerm_virtual_network_gateway': '🔐',
            
            # Storage
            'azurerm_storage_account': '💾',
            'azurerm_storage_blob': '🗂️',
            'azurerm_storage_container': '📦',
            'azurerm_storage_queue': '📋',
            'azurerm_storage_table': '📊',
            
            # Database
            'azurerm_sql_server': '🗄️',
            'azurerm_postgresql_server': '🐘',
            'azurerm_mysql_server': '🐬',
            'azurerm_cosmosdb_account': '🌌',
            'azurerm_redis_cache': '⚡',
            
            # Security
            'azurerm_key_vault': '🔐',
            'azurerm_key_vault_secret': '🤐',
            'azurerm_key_vault_key': '🗝️',
            
            # Containers
            'azurerm_kubernetes_cluster': '☸️',
            'azurerm_container_registry': '📦',
            'azurerm_container_group': '🐳',
            
            # Web
            'azurerm_app_service': '🌍',
            'azurerm_function_app': '⚡',
            'azurerm_static_site': '📄',
            
            # AI
            'azurerm_cognitive_account': '🧠',
            'azurerm_bot_service': '🤖',
            'azurerm_machine_learning_workspace': '🔬',
            
            # Monitoring
            'azurerm_log_analytics_workspace': '📈',
            'azurerm_application_insights': '🔍',
            'azurerm_monitor_alert_rule': '🚨',
        }
        
        # Check specific icons first
        if resource_name in specific_icons:
            return specific_icons[resource_name]
        
        # Category-based icons
        category_icons = {
            'compute': '🖥️',
            'network': '🌐',
            'storage': '💾',
            'database': '🗄️',
            'security': '🔐',
            'containers': '📦',
            'web': '🌍',
            'monitoring': '📊',
            'messaging': '📨',
            'ai': '🧠',
            'analytics': '📊',
            'integration': '🔌',
            'devops': '⚙️',
            'iot': '📡',
            'media': '🎮',
            'industry': '🏥',
            'communication': '📞',
            'management': '📁',
            'other': '📋'
        }
        
        return category_icons.get(category, '📋')
    
    def _get_fallback_resources(self) -> List[Dict]:
        """Fallback do statycznej listy gdy GitHub API nie działa"""
        from .azure_resources import AzureResourcesProvider
        return AzureResourcesProvider.get_flat_list()
    
    def check_rate_limit(self) -> Dict:
        """Sprawdź limit API GitHub"""
        url = f"{self.base_url}/rate_limit"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'limit': data['resources']['core']['limit'],
                    'remaining': data['resources']['core']['remaining'],
                    'reset': data['resources']['core']['reset'],
                    'has_token': self.token is not None
                }
        except Exception:
            pass
        
        return {'error': 'Could not check rate limit'}
    
    def get_stats(self) -> Dict:
        """Zwróć statystyki fetcher'a"""
        return {
            'has_token': self.token is not None,
            'max_requests_per_hour': self.max_requests_per_hour,
            'request_delay': self.request_delay,
            'base_url': self.base_url,
            'repo': self.repo
        }