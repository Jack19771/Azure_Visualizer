#!/usr/bin/env python3
"""
Azure Icon Mapper - Final Version
Mapuje zasoby z azure_resources_formatted.json na ikony z folderów
Dodaje pole 'icon' do każdego zasobu w JSON
"""

import json
import os
import re
from pathlib import Path
from difflib import SequenceMatcher
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
import logging

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class IconFile:
    filename: str
    full_path: str
    relative_path: str  # ścieżka relatywna od folderu icons
    folder_category: str
    normalized_name: str
    service_keywords: List[str]

class AzureIconMapper:
    def __init__(self, json_path="azure_resources_formatted.json", icons_path="icons", output_path="azure_resources_with_icons.json"):
        self.json_path = Path(json_path)
        self.icons_path = Path(icons_path)
        self.output_path = Path(output_path)
        self.icons_cache = []
        
        # Specjalne mapowania dla dokładnych dopasowań
        self.exact_mappings = {
            # Identity
            'azurerm_aadb2c_directory': 'identity/',  # szukaj B2C w identity
            'azurerm_active_directory_domain_service': 'identity/',  # szukaj Domain Service w identity
            
            # Storage
            'azurerm_storage_account': 'storage/10086-icon-service-Storage-Accounts.svg',
            'azurerm_storage_blob': 'storage/',
            'azurerm_storage_container': 'storage/',
            'azurerm_storage_queue': 'storage/',
            
            # Networking
            'azurerm_virtual_network': 'networking/',  # szukaj Virtual Network
            'azurerm_subnet': 'networking/',  # szukaj Subnet
            'azurerm_network_security_group': 'networking/',
            'azurerm_public_ip': 'networking/',
            'azurerm_load_balancer': 'networking/',
            'azurerm_application_gateway': 'networking/',
            
            # Compute
            'azurerm_virtual_machine': 'compute/',
            'azurerm_linux_virtual_machine': 'compute/',
            'azurerm_windows_virtual_machine': 'compute/',
            'azurerm_availability_set': 'compute/',
            
            # Security
            'azurerm_key_vault': 'security/',
            'azurerm_key_vault_secret': 'security/',
            'azurerm_advanced_threat_protection': 'security/',
            
            # Databases
            'azurerm_sql_database': 'databases/',
            'azurerm_sql_server': 'databases/',
            'azurerm_cosmosdb_account': 'databases/',
            'azurerm_postgresql_server': 'databases/',
            'azurerm_mysql_server': 'databases/',
            
            # AI + ML
            'azurerm_ai_services': 'ai + machine learning/',
            'azurerm_cognitive_account': 'ai + machine learning/',
            
            # Analytics
            'azurerm_analysis_services_server': 'analytics/',
            'azurerm_data_factory': 'analytics/',
            'azurerm_stream_analytics_job': 'analytics/',
            
            # Integration
            'azurerm_api_management': 'integration/',
            'azurerm_logic_app_workflow': 'integration/',
            'azurerm_servicebus_namespace': 'integration/',
            'azurerm_eventhub_namespace': 'analytics/',  # Event Hub jest w analytics
            
            # Web
            'azurerm_app_service': 'app services/',
            'azurerm_app_service_plan': 'app services/',
            'azurerm_function_app': 'app services/',
            
            # Management
            'azurerm_resource_group': 'general/',
            'azurerm_management_group': 'general/',
        }
        
    def normalize_name(self, name: str) -> str:
        """Normalizuje nazwę do porównywania"""
        if not name:
            return ""
        
        # Usuń prefix azurerm_ 
        name = re.sub(r'^azurerm_', '', name)
        
        # Zamień podkreślenia na spacje
        name = name.replace('_', ' ')
        
        # Usuń znaki specjalne
        name = re.sub(r'[^\w\s]', ' ', name)
        
        # Usuń wielokrotne spacje
        name = re.sub(r'\s+', ' ', name)
        
        return name.lower().strip()
    
    def extract_service_name_from_icon(self, filename: str) -> str:
        """Wyciąga nazwę usługi z nazwy pliku ikony"""
        # Format: NUMER-icon-service-NAZWA-USLUGI.svg
        match = re.match(r'^\d+-icon-service-(.+)\.svg$', filename, re.IGNORECASE)
        if match:
            service_part = match.group(1)
            # Zamień myślniki na spacje i normalizuj
            service_name = service_part.replace('-', ' ')
            return self.normalize_name(service_name)
        return self.normalize_name(filename.replace('.svg', ''))
    
    def extract_keywords_from_resource_name(self, resource_name: str) -> List[str]:
        """Wyciąga kluczowe słowa z nazwy zasobu Terraform"""
        normalized = self.normalize_name(resource_name)
        words = normalized.split()
        
        # Dodaj też oryginalne słowa przed normalizacją
        original_words = resource_name.replace('azurerm_', '').split('_')
        
        all_words = list(set(words + original_words))
        
        # Usuń bardzo krótkie słowa i popularne stopwords
        filtered_words = [w for w in all_words if len(w) > 2 and w not in ['the', 'and', 'for', 'with']]
        
        return filtered_words
    
    def scan_icons(self) -> List[IconFile]:
        """Skanuje wszystkie ikony i tworzy cache"""
        logger.info("Skanowanie ikon...")
        icons = []
        
        for folder in self.icons_path.iterdir():
            if not folder.is_dir():
                continue
                
            folder_name = folder.name
            logger.info(f"Skanowanie folderu: {folder_name}")
            
            for svg_file in folder.glob("*.svg"):
                relative_path = f"{folder_name}/{svg_file.name}"
                
                icon = IconFile(
                    filename=svg_file.name,
                    full_path=str(svg_file.absolute()),
                    relative_path=relative_path,
                    folder_category=folder_name,
                    normalized_name=self.extract_service_name_from_icon(svg_file.name),
                    service_keywords=self.extract_service_name_from_icon(svg_file.name).split()
                )
                icons.append(icon)
        
        logger.info(f"Znaleziono {len(icons)} ikon")
        return icons
    
    def calculate_similarity(self, str1: str, str2: str) -> float:
        """Oblicza podobieństwo między stringami (0-1)"""
        if not str1 or not str2:
            return 0.0
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()
    
    def find_icon_by_exact_mapping(self, resource_name: str) -> Optional[IconFile]:
        """Szuka ikony przez dokładne mapowanie"""
        if resource_name in self.exact_mappings:
            mapping = self.exact_mappings[resource_name]
            
            # Jeśli to pełna ścieżka do pliku
            if mapping.endswith('.svg'):
                for icon in self.icons_cache:
                    if icon.relative_path == mapping:
                        return icon
            
            # Jeśli to tylko folder - szukaj najlepszego dopasowania w tym folderze
            else:
                folder_name = mapping.rstrip('/')
                resource_keywords = self.extract_keywords_from_resource_name(resource_name)
                
                best_match = None
                best_score = 0
                
                for icon in self.icons_cache:
                    if icon.folder_category == folder_name:
                        # Sprawdź podobieństwo na poziomie słów kluczowych
                        score = 0
                        for keyword in resource_keywords:
                            if keyword in icon.normalized_name:
                                score += 1
                        
                        # Dodaj podobieństwo tekstowe
                        text_similarity = self.calculate_similarity(
                            ' '.join(resource_keywords), 
                            icon.normalized_name
                        )
                        score += text_similarity
                        
                        if score > best_score:
                            best_score = score
                            best_match = icon
                
                return best_match
        
        return None
    
    def find_icon_by_fuzzy_search(self, resource_name: str) -> Optional[Tuple[IconFile, float]]:
        """Szuka ikony przez wyszukiwanie rozmyte"""
        resource_keywords = self.extract_keywords_from_resource_name(resource_name)
        resource_text = ' '.join(resource_keywords)
        
        best_match = None
        best_score = 0
        
        for icon in self.icons_cache:
            # Metoda 1: Keyword matching
            keyword_matches = 0
            for keyword in resource_keywords:
                if keyword in icon.normalized_name:
                    keyword_matches += 1
            
            keyword_score = keyword_matches / max(len(resource_keywords), 1)
            
            # Metoda 2: Text similarity
            text_score = self.calculate_similarity(resource_text, icon.normalized_name)
            
            # Metoda 3: Sprawdź czy nazwa zasobu jest w nazwie ikony
            partial_score = 0
            for keyword in resource_keywords:
                if len(keyword) > 3:  # tylko dłuższe słowa
                    if keyword in icon.normalized_name:
                        partial_score += 0.3
            
            # Kombinowany wynik
            combined_score = (keyword_score * 0.5) + (text_score * 0.3) + (partial_score * 0.2)
            
            if combined_score > best_score:
                best_score = combined_score
                best_match = icon
        
        return (best_match, best_score) if best_match and best_score > 0.1 else None
    
    def find_icon_for_resource(self, resource_name: str) -> Dict[str, any]:
        """Znajduje najlepszą ikonę dla zasobu"""
        # Metoda 1: Exact mapping
        exact_match = self.find_icon_by_exact_mapping(resource_name)
        if exact_match:
            return {
                'icon_path': exact_match.relative_path,
                'icon_filename': exact_match.filename,
                'confidence': 1.0,
                'method': 'exact_mapping'
            }
        
        # Metoda 2: Fuzzy search
        fuzzy_result = self.find_icon_by_fuzzy_search(resource_name)
        if fuzzy_result:
            icon, score = fuzzy_result
            return {
                'icon_path': icon.relative_path,
                'icon_filename': icon.filename,
                'confidence': score,
                'method': 'fuzzy_search'
            }
        
        # Brak dopasowania
        return {
            'icon_path': None,
            'icon_filename': None,
            'confidence': 0.0,
            'method': 'no_match'
        }
    
    def process_resources(self, use_sample=False) -> Dict:
        """Przetwarza zasoby i dodaje ikony"""
        # Wybierz plik do przetwarzania
        input_file = "sample_azure_resources.json" if use_sample else self.json_path
        
        logger.info(f"Ładowanie zasobów z {input_file}")
        
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            logger.error(f"Błąd przy ładowaniu JSON: {e}")
            return {}
        
        if 'resources' not in data:
            logger.error("Brak klucza 'resources' w JSON")
            return {}
        
        resources = data['resources']
        logger.info(f"Przetwarzanie {len(resources)} zasobów...")
        
        # Statystyki
        stats = {
            'total': len(resources),
            'mapped': 0,
            'unmapped': 0,
            'high_confidence': 0,
            'exact_mappings': 0,
            'fuzzy_mappings': 0
        }
        
        # Przetwarzanie każdego zasobu
        for resource_name, resource_data in resources.items():
            icon_info = self.find_icon_for_resource(resource_name)
            
            # Dodaj informacje o ikonie do zasobu
            resource_data['icon'] = {
                'path': icon_info['icon_path'],
                'filename': icon_info['icon_filename'],
                'confidence': icon_info['confidence'],
                'mapping_method': icon_info['method']
            }
            
            # Aktualizuj statystyki
            if icon_info['icon_path']:
                stats['mapped'] += 1
                if icon_info['confidence'] >= 0.7:
                    stats['high_confidence'] += 1
                if icon_info['method'] == 'exact_mapping':
                    stats['exact_mappings'] += 1
                elif icon_info['method'] == 'fuzzy_search':
                    stats['fuzzy_mappings'] += 1
            else:
                stats['unmapped'] += 1
        
        # Dodaj statystyki do metadanych
        data['icon_mapping_stats'] = stats
        
        logger.info("=== STATYSTYKI MAPOWANIA ===")
        logger.info(f"Łącznie zasobów: {stats['total']}")
        logger.info(f"Zmapowanych: {stats['mapped']} ({stats['mapped']/stats['total']*100:.1f}%)")
        logger.info(f"Nie zmapowanych: {stats['unmapped']} ({stats['unmapped']/stats['total']*100:.1f}%)")
        logger.info(f"Wysokie zaufanie (≥70%): {stats['high_confidence']} ({stats['high_confidence']/stats['total']*100:.1f}%)")
        logger.info(f"Dokładne mapowania: {stats['exact_mappings']}")
        logger.info(f"Rozmyte mapowania: {stats['fuzzy_mappings']}")
        
        return data
    
    def save_results(self, data: Dict, suffix=""):
        """Zapisuje wyniki do pliku JSON"""
        output_file = self.output_path
        if suffix:
            output_file = output_file.with_name(f"{output_file.stem}_{suffix}{output_file.suffix}")
        
        logger.info(f"Zapisywanie wyników do {output_file}")
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ Zapisano pomyślnie: {output_file}")
            return str(output_file)
            
        except Exception as e:
            logger.error(f"Błąd przy zapisywaniu: {e}")
            return None
    
    def generate_mapping_report(self, data: Dict, output_file="mapping_report.txt"):
        """Generuje raport mapowania"""
        stats = data.get('icon_mapping_stats', {})
        resources = data.get('resources', {})
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=== RAPORT MAPOWANIA IKON AZURE ===\n\n")
            
            f.write("STATYSTYKI OGÓLNE:\n")
            f.write(f"Łącznie zasobów: {stats.get('total', 0)}\n")
            f.write(f"Zmapowanych: {stats.get('mapped', 0)}\n")
            f.write(f"Nie zmapowanych: {stats.get('unmapped', 0)}\n")
            f.write(f"Wysokie zaufanie: {stats.get('high_confidence', 0)}\n")
            f.write(f"Dokładne mapowania: {stats.get('exact_mappings', 0)}\n")
            f.write(f"Rozmyte mapowania: {stats.get('fuzzy_mappings', 0)}\n\n")
            
            f.write("ZASOBY BEZ IKON:\n")
            unmapped_count = 0
            for resource_name, resource_data in resources.items():
                icon_info = resource_data.get('icon', {})
                if not icon_info.get('path'):
                    f.write(f"- {resource_name}\n")
                    unmapped_count += 1
                    if unmapped_count >= 20:  # Ogranicz do pierwszych 20
                        f.write("... (i więcej)\n")
                        break
            
            f.write(f"\nZASOBY Z NISKIM ZAUFANIEM (<70%):\n")
            low_confidence_count = 0
            for resource_name, resource_data in resources.items():
                icon_info = resource_data.get('icon', {})
                confidence = icon_info.get('confidence', 0)
                if icon_info.get('path') and confidence < 0.7:
                    f.write(f"- {resource_name}: {icon_info['filename']} ({confidence:.2f})\n")
                    low_confidence_count += 1
                    if low_confidence_count >= 20:
                        f.write("... (i więcej)\n")
                        break
        
        logger.info(f"Wygenerowano raport: {output_file}")
    
    def run(self, use_sample=False):
        """Główna funkcja uruchamiająca mapowanie"""
        logger.info("=== ROZPOCZYNANIE MAPOWANIA IKON ===")
        
        # Skanuj ikony
        self.icons_cache = self.scan_icons()
        if not self.icons_cache:
            logger.error("Nie znaleziono ikon!")
            return
        
        # Przetwórz zasoby
        processed_data = self.process_resources(use_sample=use_sample)
        if not processed_data:
            logger.error("Nie udało się przetworzyć zasobów!")
            return
        
        # Zapisz wyniki
        suffix = "sample" if use_sample else ""
        output_file = self.save_results(processed_data, suffix)
        
        # Wygeneruj raport
        if output_file:
            report_file = f"mapping_report{'_sample' if use_sample else ''}.txt"
            self.generate_mapping_report(processed_data, report_file)
        
        logger.info("=== MAPOWANIE ZAKOŃCZONE ===")
        
        return output_file

def main():
    """Główna funkcja"""
    mapper = AzureIconMapper()
    
    # Sprawdź czy pliki istnieją
    if not mapper.json_path.exists():
        logger.error(f"Nie znaleziono pliku: {mapper.json_path}")
        return
    
    if not mapper.icons_path.exists():
        logger.error(f"Nie znaleziono folderu: {mapper.icons_path}")
        return
    
    print("Wybierz opcję:")
    print("1. Test na próbce (10 zasobów)")
    print("2. Pełne mapowanie (1108 zasobów)")
    
    choice = input("Wybór (1 lub 2): ").strip()
    
    if choice == "1":
        logger.info("Uruchamianie testu na próbce...")
        result = mapper.run(use_sample=True)
    elif choice == "2":
        logger.info("Uruchamianie pełnego mapowania...")
        result = mapper.run(use_sample=False)
    else:
        print("Nieprawidłowy wybór")
        return
    
    if result:
        print(f"\n✅ Mapowanie zakończone!")
        print(f"📄 Wynik zapisano w: {result}")
        print(f"📊 Raport dostępny w pliku tekstowym")
    else:
        print("❌ Mapowanie nie powiodło się")

if __name__ == "__main__":
    main()