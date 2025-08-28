"""
Static hierarchical Azure resources for Terraform Builder
Organized by categories and subcategories
"""

class StaticResourceProvider:
    
    @staticmethod
    def get_hierarchical_resources():
        """Returns organized Azure resources with subcategories"""
        return {
            "Virtual Machines": {
                "icon": "🖥️",
                "subcategories": {
                    "Windows": [
                        {"name": "azurerm_windows_virtual_machine", "display": "Windows Server 2022", "icon": "🪟", "category": "compute"},
                        {"name": "azurerm_windows_virtual_machine", "display": "Windows Server 2019", "icon": "🪟", "category": "compute"},
                        {"name": "azurerm_windows_virtual_machine", "display": "Windows 11 Enterprise", "icon": "🪟", "category": "compute"},
                        {"name": "azurerm_virtual_machine_scale_set", "display": "Windows VM Scale Set", "icon": "📊", "category": "compute"}
                    ],
                    "Linux": [
                        {"name": "azurerm_linux_virtual_machine", "display": "Ubuntu Server 22.04", "icon": "🐧", "category": "compute"},
                        {"name": "azurerm_linux_virtual_machine", "display": "Red Hat Enterprise Linux", "icon": "🎩", "category": "compute"},
                        {"name": "azurerm_linux_virtual_machine", "display": "CentOS 8", "icon": "🐧", "category": "compute"},
                        {"name": "azurerm_linux_virtual_machine", "display": "SUSE Linux Enterprise", "icon": "🦎", "category": "compute"},
                        {"name": "azurerm_virtual_machine_scale_set", "display": "Linux VM Scale Set", "icon": "📊", "category": "compute"}
                    ],
                    "Specialized": [
                        {"name": "azurerm_availability_set", "display": "Availability Set", "icon": "🔄", "category": "compute"},
                        {"name": "azurerm_managed_disk", "display": "Managed Disk", "icon": "💿", "category": "compute"},
                        {"name": "azurerm_snapshot", "display": "VM Snapshot", "icon": "📸", "category": "compute"}
                    ]
                }
            },
            
            "Databases": {
                "icon": "🗄️",
                "subcategories": {
                    "SQL Databases": [
                        {"name": "azurerm_mssql_server", "display": "SQL Server", "icon": "🗄️", "category": "database"},
                        {"name": "azurerm_mssql_database", "display": "SQL Database", "icon": "🗃️", "category": "database"},
                        {"name": "azurerm_mssql_managed_instance", "display": "SQL Managed Instance", "icon": "🏢", "category": "database"}
                    ],
                    "Open Source": [
                        {"name": "azurerm_postgresql_server", "display": "PostgreSQL Server", "icon": "🐘", "category": "database"},
                        {"name": "azurerm_postgresql_flexible_server", "display": "PostgreSQL Flexible Server", "icon": "🐘", "category": "database"},
                        {"name": "azurerm_mysql_server", "display": "MySQL Server", "icon": "🐬", "category": "database"},
                        {"name": "azurerm_mysql_flexible_server", "display": "MySQL Flexible Server", "icon": "🐬", "category": "database"}
                    ],
                    "NoSQL": [
                        {"name": "azurerm_cosmosdb_account", "display": "Cosmos DB", "icon": "🌌", "category": "database"},
                        {"name": "azurerm_redis_cache", "display": "Redis Cache", "icon": "⚡", "category": "database"},
                        {"name": "azurerm_redis_enterprise_cluster", "display": "Redis Enterprise", "icon": "⚡", "category": "database"}
                    ]
                }
            },
            
            "Networking": {
                "icon": "🌐",
                "subcategories": {
                    "Core Networking": [
                        {"name": "azurerm_virtual_network", "display": "Virtual Network", "icon": "🌐", "category": "network"},
                        {"name": "azurerm_subnet", "display": "Subnet", "icon": "🔗", "category": "network"},
                        {"name": "azurerm_public_ip", "display": "Public IP", "icon": "🌍", "category": "network"},
                        {"name": "azurerm_network_interface", "display": "Network Interface", "icon": "📡", "category": "network"}
                    ],
                    "Security": [
                        {"name": "azurerm_network_security_group", "display": "Network Security Group", "icon": "🛡️", "category": "network"},
                        {"name": "azurerm_firewall", "display": "Azure Firewall", "icon": "🔥", "category": "network"},
                        {"name": "azurerm_firewall_policy", "display": "Firewall Policy", "icon": "📋", "category": "network"},
                        {"name": "azurerm_application_security_group", "display": "Application Security Group", "icon": "🛡️", "category": "network"}
                    ],
                    "Load Balancing": [
                        {"name": "azurerm_lb", "display": "Load Balancer", "icon": "⚖️", "category": "network"},
                        {"name": "azurerm_application_gateway", "display": "Application Gateway", "icon": "🚪", "category": "network"},
                        {"name": "azurerm_traffic_manager_profile", "display": "Traffic Manager", "icon": "🚦", "category": "network"}
                    ],
                    "Connectivity": [
                        {"name": "azurerm_virtual_network_gateway", "display": "VPN Gateway", "icon": "🔐", "category": "network"},
                        {"name": "azurerm_express_route_circuit", "display": "ExpressRoute", "icon": "🔗", "category": "network"},
                        {"name": "azurerm_route_table", "display": "Route Table", "icon": "🗺️", "category": "network"}
                    ]
                }
            },
            
            "Storage": {
                "icon": "💾",
                "subcategories": {
                    "Storage Accounts": [
                        {"name": "azurerm_storage_account", "display": "Storage Account (General Purpose)", "icon": "💾", "category": "storage"},
                        {"name": "azurerm_storage_account", "display": "Blob Storage", "icon": "🗂️", "category": "storage"},
                        {"name": "azurerm_storage_account", "display": "Data Lake Storage", "icon": "🏞️", "category": "storage"}
                    ],
                    "File Services": [
                        {"name": "azurerm_storage_share", "display": "File Share", "icon": "📁", "category": "storage"},
                        {"name": "azurerm_netapp_account", "display": "NetApp Files", "icon": "📂", "category": "storage"},
                        {"name": "azurerm_storage_sync", "display": "Azure File Sync", "icon": "🔄", "category": "storage"}
                    ],
                    "Backup & Archive": [
                        {"name": "azurerm_recovery_services_vault", "display": "Recovery Services Vault", "icon": "🔐", "category": "storage"},
                        {"name": "azurerm_backup_policy_vm", "display": "VM Backup Policy", "icon": "💾", "category": "storage"}
                    ]
                }
            },
            
            "Web & Mobile": {
                "icon": "🌍",
                "subcategories": {
                    "App Services": [
                        {"name": "azurerm_service_plan", "display": "App Service Plan", "icon": "📋", "category": "web"},
                        {"name": "azurerm_linux_web_app", "display": "Linux Web App", "icon": "🐧", "category": "web"},
                        {"name": "azurerm_windows_web_app", "display": "Windows Web App", "icon": "🪟", "category": "web"},
                        {"name": "azurerm_linux_function_app", "display": "Function App (Linux)", "icon": "⚡", "category": "web"}
                    ],
                    "Static & CDN": [
                        {"name": "azurerm_static_site", "display": "Static Web App", "icon": "📄", "category": "web"},
                        {"name": "azurerm_cdn_profile", "display": "CDN Profile", "icon": "🌐", "category": "web"},
                        {"name": "azurerm_frontdoor", "display": "Front Door", "icon": "🚪", "category": "web"}
                    ]
                }
            },
            
            "Security": {
                "icon": "🔐",
                "subcategories": {
                    "Key Management": [
                        {"name": "azurerm_key_vault", "display": "Key Vault", "icon": "🔐", "category": "security"},
                        {"name": "azurerm_key_vault_secret", "display": "Key Vault Secret", "icon": "🤐", "category": "security"},
                        {"name": "azurerm_key_vault_key", "display": "Key Vault Key", "icon": "🗝️", "category": "security"},
                        {"name": "azurerm_key_vault_certificate", "display": "Key Vault Certificate", "icon": "📜", "category": "security"}
                    ],
                    "Identity": [
                        {"name": "azurerm_user_assigned_identity", "display": "Managed Identity", "icon": "👤", "category": "security"},
                        {"name": "azurerm_role_assignment", "display": "Role Assignment", "icon": "👥", "category": "security"}
                    ]
                }
            }
        }
    
    @staticmethod
    def get_flat_list():
        """Returns flat list of all resources for backward compatibility"""
        hierarchical = StaticResourceProvider.get_hierarchical_resources()
        flat_list = []
        
        for category_name, category_data in hierarchical.items():
            for subcategory_name, resources in category_data["subcategories"].items():
                for resource in resources:
                    # Add subcategory info to resource
                    resource_copy = resource.copy()
                    resource_copy["parent_category"] = category_name
                    resource_copy["subcategory"] = subcategory_name
                    flat_list.append(resource_copy)
        
        return flat_list