from django.shortcuts import render
from django.http import JsonResponse
from .static_resources import StaticResourceProvider
import time

def home(request):
    return render(request, 'index.html')

def get_resources(request):
    """API endpoint zwracający hierarchiczne zasoby Azure"""
    
    # Sprawdź format odpowiedzi
    format_type = request.GET.get('format', 'hierarchical')  # hierarchical lub flat
    
    if format_type == 'hierarchical':
        resources = StaticResourceProvider.get_hierarchical_resources()
        return JsonResponse({
            'resources': resources,
            'format': 'hierarchical',
            'total_categories': len(resources),
            'source': 'static_hierarchical',
            'timestamp': time.time()
        })
    else:
        # Flat format for backward compatibility
        resources = StaticResourceProvider.get_flat_list()
        return JsonResponse({
            'resources': resources,
            'total_count': len(resources),
            'format': 'flat',
            'source': 'static_flat',
            'timestamp': time.time()
        })

def get_resource_templates(request):
    """Zwróć gotowe szablony infrastruktury"""
    templates = [
        {
            'name': 'web_app_basic',
            'display': 'Web App + Database',
            'description': 'Simple web application with PostgreSQL database',
            'icon': '🌐',
            'resources': [
                'azurerm_resource_group',
                'azurerm_service_plan',
                'azurerm_linux_web_app',
                'azurerm_postgresql_server',
                'azurerm_postgresql_database'
            ]
        },
        {
            'name': 'vm_with_network',
            'display': 'Virtual Machine Setup',
            'description': 'Windows VM with complete networking setup',
            'icon': '🖥️',
            'resources': [
                'azurerm_resource_group',
                'azurerm_virtual_network',
                'azurerm_subnet',
                'azurerm_network_security_group',
                'azurerm_public_ip',
                'azurerm_network_interface',
                'azurerm_windows_virtual_machine'
            ]
        },
        {
            'name': 'secure_storage',
            'display': 'Secure Storage Solution',
            'description': 'Storage account with backup and security',
            'icon': '💾',
            'resources': [
                'azurerm_resource_group',
                'azurerm_storage_account',
                'azurerm_key_vault',
                'azurerm_recovery_services_vault'
            ]
        }
    ]
    
    return JsonResponse({'templates': templates})