"""
Comprehensive list of Azure resources for Terraform Builder
Based on official Azure Resource Manager and Terraform AzureRM provider documentation
"""

class AzureResourcesProvider:
    
    @staticmethod
    def get_all_resources():
        """Returns comprehensive list of Azure resources organized by categories"""
        return {
            "management": [
                {"name": "azurerm_resource_group", "display": "Resource Group", "icon": "📁", "category": "management"},
                {"name": "azurerm_management_group", "display": "Management Group", "icon": "🏢", "category": "management"},
                {"name": "azurerm_subscription", "display": "Subscription", "icon": "📋", "category": "management"},
                {"name": "azurerm_policy_definition", "display": "Policy Definition", "icon": "📜", "category": "management"},
                {"name": "azurerm_role_assignment", "display": "Role Assignment", "icon": "👤", "category": "management"}
            ],
            
            "compute": [
                {"name": "azurerm_virtual_machine", "display": "Virtual Machine", "icon": "🖥️", "category": "compute"},
                {"name": "azurerm_linux_virtual_machine", "display": "Linux Virtual Machine", "icon": "🐧", "category": "compute"},
                {"name": "azurerm_windows_virtual_machine", "display": "Windows Virtual Machine", "icon": "🪟", "category": "compute"},
                {"name": "azurerm_virtual_machine_scale_set", "display": "VM Scale Set", "icon": "📊", "category": "compute"},
                {"name": "azurerm_availability_set", "display": "Availability Set", "icon": "🔄", "category": "compute"},
                {"name": "azurerm_disk_encryption_set", "display": "Disk Encryption Set", "icon": "🔒", "category": "compute"},
                {"name": "azurerm_managed_disk", "display": "Managed Disk", "icon": "💿", "category": "compute"},
                {"name": "azurerm_snapshot", "display": "Disk Snapshot", "icon": "📸", "category": "compute"}
            ],
            
            "network": [
                {"name": "azurerm_virtual_network", "display": "Virtual Network", "icon": "🌐", "category": "network"},
                {"name": "azurerm_subnet", "display": "Subnet", "icon": "🔗", "category": "network"},
                {"name": "azurerm_network_security_group", "display": "Network Security Group", "icon": "🛡️", "category": "network"},
                {"name": "azurerm_public_ip", "display": "Public IP", "icon": "🌍", "category": "network"},
                {"name": "azurerm_load_balancer", "display": "Load Balancer", "icon": "⚖️", "category": "network"},
                {"name": "azurerm_application_gateway", "display": "Application Gateway", "icon": "🚪", "category": "network"},
                {"name": "azurerm_virtual_network_gateway", "display": "VPN Gateway", "icon": "🔐", "category": "network"},
                {"name": "azurerm_firewall", "display": "Azure Firewall", "icon": "🔥", "category": "network"},
                {"name": "azurerm_network_interface", "display": "Network Interface", "icon": "📡", "category": "network"},
                {"name": "azurerm_route_table", "display": "Route Table", "icon": "🗺️", "category": "network"}
            ],
            
            "storage": [
                {"name": "azurerm_storage_account", "display": "Storage Account", "icon": "💾", "category": "storage"},
                {"name": "azurerm_storage_container", "display": "Blob Container", "icon": "📦", "category": "storage"},
                {"name": "azurerm_storage_blob", "display": "Storage Blob", "icon": "🗂️", "category": "storage"},
                {"name": "azurerm_storage_queue", "display": "Storage Queue", "icon": "📋", "category": "storage"},
                {"name": "azurerm_storage_table", "display": "Storage Table", "icon": "📊", "category": "storage"},
                {"name": "azurerm_storage_share", "display": "File Share", "icon": "📁", "category": "storage"}
            ],
            
            "database": [
                {"name": "azurerm_sql_server", "display": "SQL Server", "icon": "🗄️", "category": "database"},
                {"name": "azurerm_sql_database", "display": "SQL Database", "icon": "🗃️", "category": "database"},
                {"name": "azurerm_postgresql_server", "display": "PostgreSQL Server", "icon": "🐘", "category": "database"},
                {"name": "azurerm_mysql_server", "display": "MySQL Server", "icon": "🐬", "category": "database"},
                {"name": "azurerm_cosmosdb_account", "display": "Cosmos DB", "icon": "🌌", "category": "database"},
                {"name": "azurerm_redis_cache", "display": "Redis Cache", "icon": "⚡", "category": "database"},
                {"name": "azurerm_mariadb_server", "display": "MariaDB Server", "icon": "🦭", "category": "database"}
            ],
            
            "web": [
                {"name": "azurerm_app_service_plan", "display": "App Service Plan", "icon": "📋", "category": "web"},
                {"name": "azurerm_app_service", "display": "App Service", "icon": "🌍", "category": "web"},
                {"name": "azurerm_function_app", "display": "Function App", "icon": "⚡", "category": "web"},
                {"name": "azurerm_app_service_slot", "display": "Deployment Slot", "icon": "🔄", "category": "web"},
                {"name": "azurerm_static_site", "display": "Static Web App", "icon": "📄", "category": "web"}
            ],
            
            "containers": [
                {"name": "azurerm_container_registry", "display": "Container Registry", "icon": "📦", "category": "containers"},
                {"name": "azurerm_container_group", "display": "Container Instance", "icon": "🐳", "category": "containers"},
                {"name": "azurerm_kubernetes_cluster", "display": "AKS Cluster", "icon": "☸️", "category": "containers"},
                {"name": "azurerm_kubernetes_cluster_node_pool", "display": "AKS Node Pool", "icon": "🔗", "category": "containers"}
            ],
            
            "security": [
                {"name": "azurerm_key_vault", "display": "Key Vault", "icon": "🔐", "category": "security"},
                {"name": "azurerm_key_vault_secret", "display": "Key Vault Secret", "icon": "🤐", "category": "security"},
                {"name": "azurerm_key_vault_key", "display": "Key Vault Key", "icon": "🗝️", "category": "security"},
                {"name": "azurerm_key_vault_certificate", "display": "Key Vault Certificate", "icon": "📜", "category": "security"},
                {"name": "azurerm_security_center_contact", "display": "Security Center", "icon": "🛡️", "category": "security"}
            ],
            
            "monitoring": [
                {"name": "azurerm_monitor_workspace", "display": "Monitor Workspace", "icon": "📊", "category": "monitoring"},
                {"name": "azurerm_log_analytics_workspace", "display": "Log Analytics", "icon": "📈", "category": "monitoring"},
                {"name": "azurerm_application_insights", "display": "Application Insights", "icon": "🔍", "category": "monitoring"},
                {"name": "azurerm_monitor_alert_rule", "display": "Alert Rule", "icon": "🚨", "category": "monitoring"}
            ],
            
            "messaging": [
                {"name": "azurerm_servicebus_namespace", "display": "Service Bus", "icon": "📨", "category": "messaging"},
                {"name": "azurerm_servicebus_queue", "display": "Service Bus Queue", "icon": "📋", "category": "messaging"},
                {"name": "azurerm_servicebus_topic", "display": "Service Bus Topic", "icon": "📢", "category": "messaging"},
                {"name": "azurerm_eventhub_namespace", "display": "Event Hub", "icon": "📡", "category": "messaging"},
                {"name": "azurerm_notification_hub", "display": "Notification Hub", "icon": "🔔", "category": "messaging"}
            ],
            
            "ai": [
                {"name": "azurerm_cognitive_account", "display": "Cognitive Services", "icon": "🧠", "category": "ai"},
                {"name": "azurerm_bot_service", "display": "Bot Service", "icon": "🤖", "category": "ai"},
                {"name": "azurerm_machine_learning_workspace", "display": "ML Workspace", "icon": "🔬", "category": "ai"}
            ]
        }
    
    @staticmethod
    def get_flat_list():
        """Returns flat list of all resources"""
        all_resources = AzureResourcesProvider.get_all_resources()
        flat_list = []
        
        for category_resources in all_resources.values():
            flat_list.extend(category_resources)
            
        return flat_list
    
    @staticmethod
    def get_popular_resources():
        """Returns most commonly used Azure resources"""
        return [
            {"name": "azurerm_resource_group", "display": "Resource Group", "icon": "📁", "category": "management"},
            {"name": "azurerm_virtual_network", "display": "Virtual Network", "icon": "🌐", "category": "network"},
            {"name": "azurerm_subnet", "display": "Subnet", "icon": "🔗", "category": "network"},
            {"name": "azurerm_linux_virtual_machine", "display": "Linux Virtual Machine", "icon": "🐧", "category": "compute"},
            {"name": "azurerm_storage_account", "display": "Storage Account", "icon": "💾", "category": "storage"},
            {"name": "azurerm_app_service_plan", "display": "App Service Plan", "icon": "📋", "category": "web"},
            {"name": "azurerm_app_service", "display": "App Service", "icon": "🌍", "category": "web"},
            {"name": "azurerm_sql_server", "display": "SQL Server", "icon": "🗄️", "category": "database"},
            {"name": "azurerm_key_vault", "display": "Key Vault", "icon": "🔐", "category": "security"},
            {"name": "azurerm_kubernetes_cluster", "display": "AKS Cluster", "icon": "☸️", "category": "containers"}
        ]