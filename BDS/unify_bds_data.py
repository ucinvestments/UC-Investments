#!/usr/bin/env python3
"""
BDS Data Unification Script
Merges data from three sources:
1. boycott.thewitness - Consumer boycott brands
2. dontbuyintooccupation.org - Companies involved in occupation
3. investigate.afsc.org - Comprehensive company investigation data
"""

import json
import csv
import os
from datetime import datetime
from typing import Dict, List, Any, Set
from pathlib import Path

class BDSDataUnifier:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.unified_data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "sources": [],
                "total_entities": 0,
                "statistics": {}
            },
            "entities": []
        }
        self.entity_map = {}  # For deduplication by normalized name

    def normalize_company_name(self, name: str) -> str:
        """Normalize company name for matching"""
        if not name:
            return ""
        # Remove common suffixes and normalize
        normalized = name.lower().strip()
        # Remove common corporate suffixes
        suffixes = [
            " inc", " llc", " ltd", " limited", " corp", " corporation",
            " plc", " gmbh", " sa", " ag", " nv", " bv", " co", " company",
            " group", " holdings", " international", " global"
        ]
        for suffix in suffixes:
            if normalized.endswith(suffix):
                normalized = normalized[:-len(suffix)].strip()
        # Remove special characters
        normalized = ''.join(c for c in normalized if c.isalnum() or c.isspace())
        normalized = ' '.join(normalized.split())  # Normalize whitespace
        return normalized

    def load_boycott_brands(self) -> int:
        """Load data from boycott.thewitness"""
        file_path = self.base_path / "boycott.thewitness/output/boycott_brands_latest.json"
        if not file_path.exists():
            print(f"Warning: File not found - {file_path}")
            return 0

        with open(file_path, 'r') as f:
            data = json.load(f)

        count = 0
        for brand in data.get('brands', []):
            normalized_name = self.normalize_company_name(brand['name'])

            entity = {
                "name": brand['name'],
                "normalized_name": normalized_name,
                "type": "brand",
                "sources": ["boycott.thewitness"],
                "data": {
                    "boycott_thewitness": {
                        "image_url": brand.get('image_url'),
                        "target_link": brand.get('target_link'),
                        "page_number": brand.get('page_number'),
                        "scraped_at": brand.get('scraped_at')
                    }
                },
                "categories": ["consumer_boycott"],
                "involvement_types": set()
            }

            if normalized_name in self.entity_map:
                # Merge with existing entity
                existing = self.entity_map[normalized_name]
                existing['sources'].append("boycott.thewitness")
                existing['data']['boycott_thewitness'] = entity['data']['boycott_thewitness']
                if "consumer_boycott" not in existing['categories']:
                    existing['categories'].append("consumer_boycott")
            else:
                self.entity_map[normalized_name] = entity
                count += 1

        self.unified_data['metadata']['sources'].append({
            "name": "boycott.thewitness",
            "file": str(file_path),
            "entities_loaded": count,
            "total_brands": data.get('total_brands', 0)
        })

        print(f"Loaded {count} brands from boycott.thewitness")
        return count

    def load_who_profits(self) -> int:
        """Load data from dontbuyintooccupation.org (Who Profits)"""
        file_path = self.base_path / "dontbuyintooccupation.org/output/who_profits_results_latest.json"
        if not file_path.exists():
            print(f"Warning: File not found - {file_path}")
            return 0

        with open(file_path, 'r') as f:
            data = json.load(f)

        count = 0
        for key, result in data.get('results', {}).items():
            if result.get('found') and result.get('matches'):
                for match in result['matches']:
                    company_name = match.get('company_name', '').split('א')[0].strip()  # Remove Hebrew text
                    normalized_name = self.normalize_company_name(company_name)

                    involvement_types = set()
                    if match.get('involvement'):
                        involvement_types = set(i.strip() for i in match['involvement'].split('|') if i.strip())

                    entity = {
                        "name": company_name,
                        "normalized_name": normalized_name,
                        "type": "company",
                        "sources": ["who_profits"],
                        "data": {
                            "who_profits": {
                                "traded_in": match.get('traded_in'),
                                "headquarters": match.get('headquarters'),
                                "involvement": list(involvement_types),
                                "search_term": match.get('search_term')
                            }
                        },
                        "categories": ["occupation_involvement"],
                        "involvement_types": involvement_types
                    }

                    if normalized_name in self.entity_map:
                        # Merge with existing entity
                        existing = self.entity_map[normalized_name]
                        if "who_profits" not in existing['sources']:
                            existing['sources'].append("who_profits")
                        existing['data']['who_profits'] = entity['data']['who_profits']
                        if "occupation_involvement" not in existing['categories']:
                            existing['categories'].append("occupation_involvement")
                        existing['involvement_types'].update(involvement_types)
                    else:
                        self.entity_map[normalized_name] = entity
                        count += 1

        self.unified_data['metadata']['sources'].append({
            "name": "who_profits",
            "file": str(file_path),
            "entities_loaded": count,
            "companies_found": data['metadata'].get('companies_found', 0),
            "total_searched": data['metadata'].get('total_companies', 0)
        })

        print(f"Loaded {count} companies from Who Profits")
        return count

    def load_investigate_afsc(self) -> int:
        """Load data from investigate.afsc.org"""
        file_path = self.base_path / "investigate.afsc.org/investigate-dataset-july-2025.csv"
        if not file_path.exists():
            print(f"Warning: File not found - {file_path}")
            return 0

        count = 0
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                company_name = row.get('Company Standard Name', row.get('Company Short Name', '')).strip()
                if not company_name:
                    continue

                normalized_name = self.normalize_company_name(company_name)

                # Determine involvement categories
                involvement_categories = []
                involvement_details = {}

                if row.get('Prisons') == '1':
                    involvement_categories.append('prisons')
                    involvement_details['prisons'] = True

                if row.get('Occupations') == '1':
                    involvement_categories.append('occupations')
                    involvement_details['occupations'] = True

                if row.get('Borders') == '1':
                    involvement_categories.append('borders')
                    involvement_details['borders'] = True

                if row.get('Divestment Shortlist'):
                    involvement_categories.append('divestment_shortlist')
                    involvement_details['divestment_shortlist'] = True

                entity = {
                    "name": company_name,
                    "normalized_name": normalized_name,
                    "type": "company",
                    "sources": ["investigate_afsc"],
                    "data": {
                        "investigate_afsc": {
                            "short_name": row.get('Company Short Name'),
                            "country_hq": row.get('Country of HQ'),
                            "primary_symbol": row.get('Primary Symbol'),
                            "exchange": row.get('Primary Exchange Name'),
                            "industry": row.get('Industry'),
                            "isin": row.get('Primary ISIN'),
                            "summary": row.get('Summary'),
                            "involvement": involvement_details,
                            "link": row.get('Link')
                        }
                    },
                    "categories": involvement_categories if involvement_categories else ["tracked_company"],
                    "involvement_types": set()
                }

                if normalized_name in self.entity_map:
                    # Merge with existing entity
                    existing = self.entity_map[normalized_name]
                    if "investigate_afsc" not in existing['sources']:
                        existing['sources'].append("investigate_afsc")
                    existing['data']['investigate_afsc'] = entity['data']['investigate_afsc']
                    for cat in involvement_categories:
                        if cat not in existing['categories']:
                            existing['categories'].append(cat)
                else:
                    self.entity_map[normalized_name] = entity
                    count += 1

        self.unified_data['metadata']['sources'].append({
            "name": "investigate_afsc",
            "file": str(file_path),
            "entities_loaded": count
        })

        print(f"Loaded {count} companies from investigate.afsc.org")
        return count

    def generate_statistics(self):
        """Generate statistics about the unified data"""
        stats = {
            "total_entities": len(self.entity_map),
            "by_type": {},
            "by_category": {},
            "by_source": {},
            "multi_source_entities": 0,
            "involvement_types": {}
        }

        for entity in self.entity_map.values():
            # Count by type
            entity_type = entity.get('type', 'unknown')
            stats['by_type'][entity_type] = stats['by_type'].get(entity_type, 0) + 1

            # Count by category
            for category in entity.get('categories', []):
                stats['by_category'][category] = stats['by_category'].get(category, 0) + 1

            # Count by source
            for source in entity.get('sources', []):
                stats['by_source'][source] = stats['by_source'].get(source, 0) + 1

            # Count multi-source entities
            if len(entity.get('sources', [])) > 1:
                stats['multi_source_entities'] += 1

            # Count involvement types
            for inv_type in entity.get('involvement_types', set()):
                stats['involvement_types'][inv_type] = stats['involvement_types'].get(inv_type, 0) + 1

        self.unified_data['metadata']['statistics'] = stats

    def unify_data(self):
        """Main method to unify all data sources"""
        print("Starting BDS data unification...")
        print("=" * 60)

        # Load data from each source
        self.load_boycott_brands()
        self.load_who_profits()
        self.load_investigate_afsc()

        # Convert entity_map to list and clean up sets
        for entity in self.entity_map.values():
            # Convert sets to lists for JSON serialization
            if 'involvement_types' in entity:
                entity['involvement_types'] = list(entity['involvement_types'])
            self.unified_data['entities'].append(entity)

        # Sort entities by name
        self.unified_data['entities'].sort(key=lambda x: x['name'].lower())

        # Generate statistics
        self.generate_statistics()

        # Update total entities count
        self.unified_data['metadata']['total_entities'] = len(self.unified_data['entities'])

        print("\n" + "=" * 60)
        print("Unification complete!")
        print(f"Total unique entities: {len(self.unified_data['entities'])}")
        print("\nStatistics:")
        for key, value in self.unified_data['metadata']['statistics'].items():
            if isinstance(value, dict):
                print(f"  {key}:")
                for k, v in value.items():
                    print(f"    - {k}: {v}")
            else:
                print(f"  {key}: {value}")

    def save_unified_data(self, output_file: str = "unified_bds_data.json"):
        """Save the unified data to a JSON file"""
        output_path = self.base_path / output_file

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.unified_data, f, indent=2, ensure_ascii=False)

        print(f"\nUnified data saved to: {output_path}")

        # Also save a compact version without indentation
        compact_path = self.base_path / output_file.replace('.json', '_compact.json')
        with open(compact_path, 'w', encoding='utf-8') as f:
            json.dump(self.unified_data, f, ensure_ascii=False, separators=(',', ':'))

        print(f"Compact version saved to: {compact_path}")

        # Save a CSV summary
        csv_path = self.base_path / output_file.replace('.json', '_summary.csv')
        self.save_csv_summary(csv_path)

    def save_csv_summary(self, csv_path: Path):
        """Save a CSV summary of the unified data"""
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                'Name', 'Type', 'Sources', 'Categories',
                'Country_HQ', 'Industry', 'Stock_Symbol',
                'Prisons', 'Occupations', 'Borders', 'Divestment_Shortlist',
                'Involvement_Types'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for entity in self.unified_data['entities']:
                row = {
                    'Name': entity['name'],
                    'Type': entity.get('type', ''),
                    'Sources': '|'.join(entity.get('sources', [])),
                    'Categories': '|'.join(entity.get('categories', [])),
                    'Involvement_Types': '|'.join(entity.get('involvement_types', []))
                }

                # Add investigate_afsc specific data if available
                if 'investigate_afsc' in entity.get('data', {}):
                    afsc_data = entity['data']['investigate_afsc']
                    row['Country_HQ'] = afsc_data.get('country_hq', '')
                    row['Industry'] = afsc_data.get('industry', '')
                    row['Stock_Symbol'] = afsc_data.get('primary_symbol', '')

                    involvement = afsc_data.get('involvement', {})
                    row['Prisons'] = 'Yes' if involvement.get('prisons') else ''
                    row['Occupations'] = 'Yes' if involvement.get('occupations') else ''
                    row['Borders'] = 'Yes' if involvement.get('borders') else ''
                    row['Divestment_Shortlist'] = 'Yes' if involvement.get('divestment_shortlist') else ''

                writer.writerow(row)

        print(f"CSV summary saved to: {csv_path}")


def main():
    """Main function to run the unification"""
    import argparse

    parser = argparse.ArgumentParser(description='Unify BDS data from multiple sources')
    parser.add_argument('--path', default='.', help='Base path for BDS data directories')
    parser.add_argument('--output', default='unified_bds_data.json', help='Output filename')

    args = parser.parse_args()

    unifier = BDSDataUnifier(args.path)
    unifier.unify_data()
    unifier.save_unified_data(args.output)


if __name__ == "__main__":
    main()