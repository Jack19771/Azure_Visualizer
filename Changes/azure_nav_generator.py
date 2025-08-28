#!/usr/bin/env python3
"""
Azure Navigation Generator
Przetwarza azyre.csv na hierarchiczny JSON z ikonami
Output: Nav.json - struktura nawigacyjna
"""

import csv
import json
import re
from pathlib import Path
from difflib import SequenceMatcher
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Dict, Optional
import logging

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class IconFile:
    filename: str
    relative_path: str
    folder_category: str
    normalized_name: str

@dataclass
class AzureService:
    resource_type: str
    service_category: str
    service_name: str
    resource_count: int = 1

class AzureNavigationGenerator:
    def __init__(self, csv_path="azyre.csv", icons_path="icons", output_path="Nav.json"):
        self.csv_path = Path(csv_path)
        self.icons_path = Path(icons_path)
        self.output_path = Path(output_path)
        self.icons_cache = []
        
    def normalize_name(self, name: str) -> str:
        """Normalizuje nazwę do porównywania"""
        if not name:
            return ""
        
        # Usuń prefix "Azure" jeśli jest
        name = re.sub(r'^azure\s+', '', name, flags=re.IGNORECASE)
        
        # Usuń znaki specjalne i zamień na spacje
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
    
    def scan_icons(self) -> List[IconFile]:
        """Skanuje wszystkie ikony"""
        logger.info("Skanowanie ikon...")
        icons = []
        
        if not self.icons_path.exists():
            logger.error(f"Folder ikon nie istnieje: {self.icons_path}")
            return icons
        
        for folder in self.icons_path.iterdir():
            if not folder.is_dir():
                continue
                
            folder_name = folder.name
            
            for svg_file in folder.glob("*.svg"):
                relative_path = f"{folder_name}/{svg_file.name}"
                
                icon = IconFile(
                    filename=svg_file.name,
                    relative_path=relative_path,
                    folder_category=folder_name,
                    normalized_name=self.extract_service_name_from_icon(svg_file.name)
                )
                icons.append(icon)
        
        logger.info(f"Znaleziono {len(icons)} ikon w {len(set(icon.folder_category for icon in icons))} folderach")
        return icons
    
    def load_services_from_csv(self) -> List[AzureService]:
        """Ładuje usługi z CSV i grupuje je"""
        logger.info(f"Ładowanie usług z {self.csv_path}")
        services = []
        
        if not self.csv_path.exists():
            logger.error(f"Plik CSV nie istnieje: {self.csv_path}")
            return services
        
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                # Grupowanie usług - liczymy wystąpienia
                service_groups = defaultdict(list)
                
                for row in reader:
                    resource_type = row.get('resource_type', '').strip()
                    service_category = row.get('service_category', '').strip()
                    service_name = row.get('service_name', '').strip()
                    
                    if not all([resource_type, service_category, service_name]):
                        continue
                    
                    key = (service_category, service_name)
                    service_groups[key].append(resource_type)
                
                # Tworzenie unikalnych usług z liczbą zasobów
                for (category, name), resources in service_groups.items():
                    service = AzureService(
                        resource_type=resources[0],  # Pierwszy zasób jako reprezentant
                        service_category=category,
                        service_name=name,
                        resource_count=len(resources)
                    )
                    services.append(service)
            
            logger.info(f"Załadowano {len(services)} unikalnych usług")
            
            # Statystyki kategorii
            category_counts = defaultdict(int)
            for service in services:
                category_counts[service.service_category] += 1
            
            logger.info("Kategorie usług:")
            for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
                logger.info(f"  {category}: {count} usług")
            
            return services
            
        except Exception as e:
            logger.error(f"Błąd przy ładowaniu CSV: {e}")
            return []
    
    def calculate_similarity(self, str1: str, str2: str) -> float:
        """Oblicza podobieństwo między stringami (0-1)"""
        if not str1 or not str2:
            return 0.0
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()
    
    def find_icon_for_service(self, service: AzureService) -> Optional[Dict[str, any]]:
        """Znajduje najlepszą ikonę dla usługi"""
        service_normalized = self.normalize_name(service.service_name)
        
        best_match = None
        best_score = 0.0
        best_method = ""
        
        # Metoda 1: Exact match w nazwie ikony
        for icon in self.icons_cache:
            if service_normalized in icon.normalized_name:
                score = self.calculate_similarity(service_normalized, icon.normalized_name)
                if score > best_score:
                    best_match = icon
                    best_score = score
                    best_method = "exact_name_match"
        
        # Metoda 2: Fuzzy match z wysokim progiem
        if best_score < 0.8:
            for icon in self.icons_cache:
                score = self.calculate_similarity(service_normalized, icon.normalized_name)
                if score > best_score and score > 0.6:
                    best_match = icon
                    best_score = score
                    best_method = "fuzzy_match"
        
        # Metoda 3: Keyword matching - szukaj kluczowych słów
        if best_score < 0.6:
            service_words = set(service_normalized.split())
            for icon in self.icons_cache:
                if icon.normalized_name:
                    icon_words = set(icon.normalized_name.split())
                    common_words = service_words.intersection(icon_words)
                    
                    # Dodatkowe punkty za długie słowa
                    score = 0
                    for word in common_words:
                        if len(word) > 3:  # Długie słowa są bardziej znaczące
                            score += len(word) / 10
                        else:
                            score += 0.1
                    
                    # Normalizuj wynik
                    if len(service_words) > 0:
                        score = score / len(service_words)
                    
                    if score > best_score:
                        best_match = icon
                        best_score = score
                        best_method = "keyword_match"
        
        if best_match and best_score > 0.3:  # Minimalny próg akceptacji
            return {
                'path': best_match.relative_path,
                'filename': best_match.filename,
                'confidence': best_score,
                'method': best_method
            }
        
        return None
    
    def create_navigation_structure(self, services: List[AzureService]) -> Dict:
        """Tworzy hierarchiczną strukturę nawigacji"""
        logger.info("Tworzenie struktury nawigacji...")
        
        # Grupowanie usług według kategorii
        categories = defaultdict(list)
        
        for service in services:
            categories[service.service_category].append(service)
        
        # Tworzenie struktury JSON
        navigation = {
            "metadata": {
                "generated_at": "2025-08-28",
                "total_categories": len(categories),
                "total_services": len(services),
                "total_resources": sum(service.resource_count for service in services)
            },
            "categories": {}
        }
        
        # Statystyki mapowania
        mapping_stats = {
            "total_services": len(services),
            "mapped_services": 0,
            "unmapped_services": 0,
            "high_confidence": 0,
            "medium_confidence": 0,
            "low_confidence": 0
        }
        
        # Przetwarzanie każdej kategorii
        for category_name, category_services in categories.items():
            logger.info(f"Przetwarzanie kategorii: {category_name} ({len(category_services)} usług)")
            
            services_list = []
            
            for service in category_services:
                # Znajdź ikonę dla usługi
                icon_info = self.find_icon_for_service(service)
                
                service_data = {
                    "name": service.service_name,
                    "resource_type": service.resource_type,
                    "resource_count": service.resource_count,
                    "icon": None
                }
                
                if icon_info:
                    service_data["icon"] = {
                        "path": icon_info['path'],
                        "filename": icon_info['filename'],
                        "confidence": round(icon_info['confidence'], 3),
                        "mapping_method": icon_info['method']
                    }
                    
                    # Aktualizuj statystyki
                    mapping_stats["mapped_services"] += 1
                    if icon_info['confidence'] >= 0.8:
                        mapping_stats["high_confidence"] += 1
                    elif icon_info['confidence'] >= 0.6:
                        mapping_stats["medium_confidence"] += 1
                    else:
                        mapping_stats["low_confidence"] += 1
                else:
                    mapping_stats["unmapped_services"] += 1
                
                services_list.append(service_data)
            
            # Sortuj usługi według nazwy
            services_list.sort(key=lambda x: x['name'])
            
            # Znajdź reprezentatywną ikonę dla kategorii (najczęstsza ikona w tej kategorii)
            category_icons = defaultdict(int)
            for service_data in services_list:
                if service_data['icon']:
                    folder = service_data['icon']['path'].split('/')[0]
                    category_icons[folder] += 1
            
            category_icon_folder = max(category_icons.items(), key=lambda x: x[1])[0] if category_icons else None
            
            navigation["categories"][category_name] = {
                "name": category_name,
                "services_count": len(services_list),
                "total_resources": sum(service['resource_count'] for service in services_list),
                "category_icon_folder": category_icon_folder,
                "services": services_list
            }
        
        # Dodaj statystyki mapowania
        navigation["mapping_stats"] = mapping_stats
        
        # Sortuj kategorie według nazwy
        navigation["categories"] = dict(sorted(navigation["categories"].items()))
        
        logger.info("=== STATYSTYKI MAPOWANIA ===")
        logger.info(f"Łącznie usług: {mapping_stats['total_services']}")
        logger.info(f"Zmapowanych: {mapping_stats['mapped_services']} ({mapping_stats['mapped_services']/mapping_stats['total_services']*100:.1f}%)")
        logger.info(f"Nie zmapowanych: {mapping_stats['unmapped_services']} ({mapping_stats['unmapped_services']/mapping_stats['total_services']*100:.1f}%)")
        logger.info(f"Wysokie zaufanie (≥80%): {mapping_stats['high_confidence']}")
        logger.info(f"Średnie zaufanie (60-80%): {mapping_stats['medium_confidence']}")
        logger.info(f"Niskie zaufanie (<60%): {mapping_stats['low_confidence']}")
        
        return navigation
    
    def save_navigation(self, navigation: Dict) -> str:
        """Zapisuje nawigację do pliku JSON"""
        logger.info(f"Zapisywanie nawigacji do {self.output_path}")
        
        try:
            with open(self.output_path, 'w', encoding='utf-8') as f:
                json.dump(navigation, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ Zapisano nawigację: {self.output_path}")
            return str(self.output_path)
            
        except Exception as e:
            logger.error(f"Błąd przy zapisywaniu: {e}")
            return None
    
    def generate_navigation_report(self, navigation: Dict) -> str:
        """Generuje raport nawigacji"""
        report_path = "navigation_report.txt"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("=== RAPORT NAWIGACJI AZURE ===\n\n")
            
            metadata = navigation.get('metadata', {})
            mapping_stats = navigation.get('mapping_stats', {})
            
            f.write("STATYSTYKI OGÓLNE:\n")
            f.write(f"Kategorie: {metadata.get('total_categories', 0)}\n")
            f.write(f"Usługi: {metadata.get('total_services', 0)}\n")
            f.write(f"Zasoby: {metadata.get('total_resources', 0)}\n\n")
            
            f.write("MAPOWANIE IKON:\n")
            f.write(f"Zmapowane usługi: {mapping_stats.get('mapped_services', 0)}\n")
            f.write(f"Nie zmapowane: {mapping_stats.get('unmapped_services', 0)}\n")
            f.write(f"Wysokie zaufanie: {mapping_stats.get('high_confidence', 0)}\n")
            f.write(f"Średnie zaufanie: {mapping_stats.get('medium_confidence', 0)}\n")
            f.write(f"Niskie zaufanie: {mapping_stats.get('low_confidence', 0)}\n\n")
            
            f.write("KATEGORIE:\n")
            categories = navigation.get('categories', {})
            for category_name, category_data in categories.items():
                f.write(f"{category_name}: {category_data.get('services_count', 0)} usług, "
                       f"{category_data.get('total_resources', 0)} zasobów\n")
            
            f.write(f"\nUSŁUGI BEZ IKON:\n")
            unmapped_count = 0
            for category_name, category_data in categories.items():
                for service in category_data.get('services', []):
                    if not service.get('icon'):
                        f.write(f"- {service['name']} ({category_name})\n")
                        unmapped_count += 1
                        if unmapped_count >= 30:  # Ogranicz do pierwszych 30
                            f.write("... (i więcej)\n")
                            break
                if unmapped_count >= 30:
                    break
        
        logger.info(f"Wygenerowano raport: {report_path}")
        return report_path
    
    def run(self) -> Optional[str]:
        """Główna funkcja generowania nawigacji"""
        logger.info("=== ROZPOCZYNANIE GENEROWANIA NAWIGACJI ===")
        
        # Skanuj ikony
        self.icons_cache = self.scan_icons()
        
        # Ładuj usługi z CSV
        services = self.load_services_from_csv()
        if not services:
            logger.error("Nie udało się załadować usług!")
            return None
        
        # Twórz strukturę nawigacji
        navigation = self.create_navigation_structure(services)
        
        # Zapisz nawigację
        output_file = self.save_navigation(navigation)
        if not output_file:
            logger.error("Nie udało się zapisać nawigacji!")
            return None
        
        # Wygeneruj raport
        self.generate_navigation_report(navigation)
        
        logger.info("=== GENEROWANIE NAWIGACJI ZAKOŃCZONE ===")
        return output_file

def main():
    """Główna funkcja"""
    generator = AzureNavigationGenerator()
    
    # Sprawdź czy pliki istnieją
    if not generator.csv_path.exists():
        logger.error(f"Nie znaleziono pliku: {generator.csv_path}")
        print(f"BŁĄD: Upewnij się, że plik {generator.csv_path} istnieje")
        return
    
    if not generator.icons_path.exists():
        logger.warning(f"Nie znaleziono folderu ikon: {generator.icons_path}")
        print(f"OSTRZEŻENIE: Folder {generator.icons_path} nie istnieje - nawigacja będzie bez ikon")
    
    # Uruchom generator
    result = generator.run()
    
    if result:
        print(f"\n✅ Nawigacja wygenerowana pomyślnie!")
        print(f"📄 Plik wyjściowy: {result}")
        print(f"📊 Raport: navigation_report.txt")
        
        # Pokaż próbkę struktury
        try:
            with open(result, 'r', encoding='utf-8') as f:
                nav_data = json.load(f)
            
            print(f"\n📋 PODSUMOWANIE:")
            metadata = nav_data.get('metadata', {})
            mapping_stats = nav_data.get('mapping_stats', {})
            
            print(f"• Kategorie: {metadata.get('total_categories', 0)}")
            print(f"• Usługi: {metadata.get('total_services', 0)}")
            print(f"• Zasoby: {metadata.get('total_resources', 0)}")
            print(f"• Zmapowane ikony: {mapping_stats.get('mapped_services', 0)}/{mapping_stats.get('total_services', 0)} ({mapping_stats.get('mapped_services', 0)/max(mapping_stats.get('total_services', 1), 1)*100:.1f}%)")
            
        except Exception as e:
            logger.error(f"Błąd przy odczycie wyniku: {e}")
    else:
        print("❌ Generowanie nawigacji nie powiodło się")

if __name__ == "__main__":
    main()