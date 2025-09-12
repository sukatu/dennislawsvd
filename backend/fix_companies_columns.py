#!/usr/bin/env python3
"""
Script to fix companies table column sizes and add more companies
"""

from sqlalchemy import create_engine, text
from config import settings
from datetime import datetime, date
import json

def fix_companies_columns():
    """Fix companies table column sizes for large numbers"""
    engine = create_engine(settings.database_url)
    
    with engine.connect() as conn:
        # Fix authorized_shares column to handle large numbers
        print("Fixing authorized_shares column...")
        conn.execute(text("ALTER TABLE companies MODIFY COLUMN authorized_shares BIGINT"))
        
        # Fix stated_capital column to handle large numbers
        print("Fixing stated_capital column...")
        conn.execute(text("ALTER TABLE companies MODIFY COLUMN stated_capital DECIMAL(20,2)"))
        
        conn.commit()
        print("Column fixes applied successfully!")

def add_more_companies():
    """Add more companies with comprehensive data"""
    engine = create_engine(settings.database_url)
    
    companies_data = [
        {
            'name': 'Ecobank Ghana Limited',
            'type_of_company': 'Public Limited Company',
            'address': '2 Independence Avenue, Accra Central, Ghana',
            'district': 'Accra Metropolitan',
            'region': 'Greater Accra',
            'date_of_incorporation': '1989-03-15',
            'date_of_commencement': '1989-04-01',
            'nature_of_business': 'Banking and Financial Services',
            'registration_number': 'RC456789',
            'tax_identification_number': 'C0004567890',
            'phone_number': '+233-302-234567',
            'email': 'info@ecobank.com.gh',
            'directors': [
                {
                    'name': 'Mr. Daniel Sackey',
                    'address': '123 Airport Residential Area, Accra',
                    'nationality': 'Ghanaian',
                    'occupation': 'Banker',
                    'email': 'daniel.sackey@ecobank.com.gh',
                    'contact': '+233-244-567890',
                    'tax_identification_number': 'P0005678901',
                    'other_directorship': ['Ghana Association of Bankers', 'Ecobank Transnational Incorporated']
                },
                {
                    'name': 'Mrs. Akosua Serwaa',
                    'address': '456 Labone, Accra',
                    'nationality': 'Ghanaian',
                    'occupation': 'Accountant',
                    'email': 'akosua.serwaa@ecobank.com.gh',
                    'contact': '+233-244-678901',
                    'tax_identification_number': 'P0006789012',
                    'other_directorship': ['Institute of Chartered Accountants Ghana']
                }
            ],
            'secretary': {
                'name': 'Mr. Kwame Asante',
                'address': '789 Ring Road, Accra',
                'nationality': 'Ghanaian',
                'occupation': 'Company Secretary',
                'email': 'kwame.asante@ecobank.com.gh',
                'contact': '+233-244-789012',
                'tax_identification_number': 'P0007890123'
            },
            'auditor': {
                'name': 'Deloitte Ghana',
                'address': '15 Independence Avenue, Accra',
                'nationality': 'Ghanaian',
                'occupation': 'Auditing Firm',
                'email': 'ghana@deloitte.com',
                'contact': '+233-302-345678',
                'tax_identification_number': 'C0003456789'
            },
            'authorized_shares': 2000000000,
            'stated_capital': 1000000000.00,
            'shareholders': [
                {
                    'name': 'Ecobank Transnational Incorporated',
                    'address': '2365, Boulevard du Mono, Lomé, Togo',
                    'nationality': 'Togolese',
                    'occupation': 'Holding Company',
                    'email': 'info@ecobank.net',
                    'contact': '+228-2221-2000',
                    'tax_identification_number': 'T0001234567',
                    'shares_alloted': 1200000000,
                    'consideration_payable': 'Cash'
                },
                {
                    'name': 'Dr. Kofi Mensah',
                    'address': '321 East Legon, Accra',
                    'nationality': 'Ghanaian',
                    'occupation': 'Businessman',
                    'email': 'kofi.mensah@email.com',
                    'contact': '+233-244-890123',
                    'tax_identification_number': 'P0008901234',
                    'shares_alloted': 50000000,
                    'consideration_payable': 'Cash'
                }
            ],
            'other_linked_companies': [
                'Ecobank Investment Corporation',
                'Ecobank Capital Limited',
                'Ecobank Insurance Brokers Limited'
            ]
        },
        {
            'name': 'Vodafone Ghana Limited',
            'type_of_company': 'Public Limited Company',
            'address': '1 Vodafone Close, Airport City, Accra',
            'district': 'Accra Metropolitan',
            'region': 'Greater Accra',
            'date_of_incorporation': '2008-07-01',
            'date_of_commencement': '2008-08-01',
            'nature_of_business': 'Telecommunications and Digital Services',
            'registration_number': 'RC789012',
            'tax_identification_number': 'C0007890123',
            'phone_number': '+233-302-345678',
            'email': 'info@vodafone.com.gh',
            'directors': [
                {
                    'name': 'Mr. Patricia Obo-Nai',
                    'address': '123 Cantonments, Accra',
                    'nationality': 'Ghanaian',
                    'occupation': 'Telecommunications Executive',
                    'email': 'patricia.obonai@vodafone.com.gh',
                    'contact': '+233-244-901234',
                    'tax_identification_number': 'P0009012345',
                    'other_directorship': ['Ghana Chamber of Telecommunications']
                }
            ],
            'secretary': {
                'name': 'Ms. Adwoa Asante',
                'address': '789 Ridge, Accra',
                'nationality': 'Ghanaian',
                'occupation': 'Company Secretary',
                'email': 'adwoa.asante@vodafone.com.gh',
                'contact': '+233-244-123456',
                'tax_identification_number': 'P0001234567'
            },
            'auditor': {
                'name': 'PricewaterhouseCoopers Ghana',
                'address': '20 Independence Avenue, Accra',
                'nationality': 'Ghanaian',
                'occupation': 'Auditing Firm',
                'email': 'ghana@pwc.com',
                'contact': '+233-302-456789',
                'tax_identification_number': 'C0004567890'
            },
            'authorized_shares': 5000000000,
            'stated_capital': 2500000000.00,
            'shareholders': [
                {
                    'name': 'Vodafone Group Plc',
                    'address': 'Vodafone House, The Connection, Newbury, Berkshire, UK',
                    'nationality': 'British',
                    'occupation': 'Telecommunications Company',
                    'email': 'investor.relations@vodafone.com',
                    'contact': '+44-1635-33251',
                    'tax_identification_number': 'GB0001234567',
                    'shares_alloted': 3000000000,
                    'consideration_payable': 'Cash'
                }
            ],
            'other_linked_companies': [
                'Vodafone Ghana Foundation',
                'Vodafone Business Ghana',
                'Vodafone Cash Limited'
            ]
        },
        {
            'name': 'Gold Fields Ghana Limited',
            'type_of_company': 'Public Limited Company',
            'address': 'Tarkwa Mine, Tarkwa, Western Region',
            'district': 'Tarkwa Nsuaem',
            'region': 'Western',
            'date_of_incorporation': '1993-05-10',
            'date_of_commencement': '1993-06-01',
            'nature_of_business': 'Mining and Mineral Processing',
            'registration_number': 'RC234567',
            'tax_identification_number': 'C0002345678',
            'phone_number': '+233-312-345678',
            'email': 'info@goldfields.com.gh',
            'directors': [
                {
                    'name': 'Mr. Alfred Baku',
                    'address': '123 East Legon, Accra',
                    'nationality': 'Ghanaian',
                    'occupation': 'Mining Engineer',
                    'email': 'alfred.baku@goldfields.com.gh',
                    'contact': '+233-244-234567',
                    'tax_identification_number': 'P0002345678',
                    'other_directorship': ['Ghana Chamber of Mines']
                }
            ],
            'secretary': {
                'name': 'Mr. Samuel Asante',
                'address': '789 Labone, Accra',
                'nationality': 'Ghanaian',
                'occupation': 'Company Secretary',
                'email': 'samuel.asante@goldfields.com.gh',
                'contact': '+233-244-456789',
                'tax_identification_number': 'P0004567890'
            },
            'auditor': {
                'name': 'Ernst & Young Ghana',
                'address': '25 Independence Avenue, Accra',
                'nationality': 'Ghanaian',
                'occupation': 'Auditing Firm',
                'email': 'ghana@ey.com',
                'contact': '+233-302-567890',
                'tax_identification_number': 'C0005678901'
            },
            'authorized_shares': 10000000000,
            'stated_capital': 5000000000.00,
            'shareholders': [
                {
                    'name': 'Gold Fields Limited',
                    'address': '150 Helen Road, Sandown, Sandton, South Africa',
                    'nationality': 'South African',
                    'occupation': 'Mining Company',
                    'email': 'info@goldfields.com',
                    'contact': '+27-11-562-9700',
                    'tax_identification_number': 'ZA0001234567',
                    'shares_alloted': 6000000000,
                    'consideration_payable': 'Cash'
                }
            ],
            'other_linked_companies': [
                'Gold Fields Ghana Foundation',
                'Gold Fields Tarkwa Mine',
                'Gold Fields Damang Mine'
            ]
        },
        {
            'name': 'Newmont Ghana Gold Limited',
            'type_of_company': 'Public Limited Company',
            'address': 'Ahafo Mine, Kenyasi, Brong-Ahafo Region',
            'district': 'Asutifi North',
            'region': 'Brong-Ahafo',
            'date_of_incorporation': '2004-08-15',
            'date_of_commencement': '2004-09-01',
            'nature_of_business': 'Gold Mining and Processing',
            'registration_number': 'RC345678',
            'tax_identification_number': 'C0003456789',
            'phone_number': '+233-352-456789',
            'email': 'info@newmont.com.gh',
            'directors': [
                {
                    'name': 'Mr. Francois Hardy',
                    'address': '123 Airport Residential, Accra',
                    'nationality': 'South African',
                    'occupation': 'Mining Executive',
                    'email': 'francois.hardy@newmont.com.gh',
                    'contact': '+233-244-567890',
                    'tax_identification_number': 'P0005678901',
                    'other_directorship': ['Newmont Corporation']
                }
            ],
            'secretary': {
                'name': 'Mr. Kwame Nkrumah',
                'address': '789 Ridge, Accra',
                'nationality': 'Ghanaian',
                'occupation': 'Company Secretary',
                'email': 'kwame.nkrumah@newmont.com.gh',
                'contact': '+233-244-789012',
                'tax_identification_number': 'P0007890123'
            },
            'auditor': {
                'name': 'KPMG Ghana',
                'address': '10 Independence Avenue, Accra',
                'nationality': 'Ghanaian',
                'occupation': 'Auditing Firm',
                'email': 'ghana@kpmg.com',
                'contact': '+233-302-678901',
                'tax_identification_number': 'C0006789012'
            },
            'authorized_shares': 8000000000,
            'stated_capital': 4000000000.00,
            'shareholders': [
                {
                    'name': 'Newmont Corporation',
                    'address': '6900 E Layton Avenue, Denver, Colorado, USA',
                    'nationality': 'American',
                    'occupation': 'Mining Company',
                    'email': 'investor.relations@newmont.com',
                    'contact': '+1-303-863-7414',
                    'tax_identification_number': 'US0001234567',
                    'shares_alloted': 4800000000,
                    'consideration_payable': 'Cash'
                }
            ],
            'other_linked_companies': [
                'Newmont Ahafo Development Foundation',
                'Newmont Akyem Mine',
                'Newmont Ghana Foundation'
            ]
        },
        {
            'name': 'AngloGold Ashanti Ghana Limited',
            'type_of_company': 'Public Limited Company',
            'address': 'Obuasi Mine, Obuasi, Ashanti Region',
            'district': 'Obuasi Municipal',
            'region': 'Ashanti',
            'date_of_incorporation': '2004-11-20',
            'date_of_commencement': '2004-12-01',
            'nature_of_business': 'Gold Mining and Refining',
            'registration_number': 'RC456789',
            'tax_identification_number': 'C0004567890',
            'phone_number': '+233-322-567890',
            'email': 'info@anglogoldashanti.com.gh',
            'directors': [
                {
                    'name': 'Mr. Eric Asubonteng',
                    'address': '123 Airport City, Accra',
                    'nationality': 'Ghanaian',
                    'occupation': 'Mining Engineer',
                    'email': 'eric.asubonteng@anglogoldashanti.com.gh',
                    'contact': '+233-244-789012',
                    'tax_identification_number': 'P0007890123',
                    'other_directorship': ['Ghana Chamber of Mines']
                }
            ],
            'secretary': {
                'name': 'Mr. Samuel Osei',
                'address': '789 Labone, Accra',
                'nationality': 'Ghanaian',
                'occupation': 'Company Secretary',
                'email': 'samuel.osei@anglogoldashanti.com.gh',
                'contact': '+233-244-901234',
                'tax_identification_number': 'P0009012345'
            },
            'auditor': {
                'name': 'Deloitte Ghana',
                'address': '15 Independence Avenue, Accra',
                'nationality': 'Ghanaian',
                'occupation': 'Auditing Firm',
                'email': 'ghana@deloitte.com',
                'contact': '+233-302-789012',
                'tax_identification_number': 'C0007890123'
            },
            'authorized_shares': 12000000000,
            'stated_capital': 6000000000.00,
            'shareholders': [
                {
                    'name': 'AngloGold Ashanti Limited',
                    'address': '76 Jeppe Street, Newtown, Johannesburg, South Africa',
                    'nationality': 'South African',
                    'occupation': 'Mining Company',
                    'email': 'info@anglogoldashanti.com',
                    'contact': '+27-11-637-6000',
                    'tax_identification_number': 'ZA0002345678',
                    'shares_alloted': 7200000000,
                    'consideration_payable': 'Cash'
                }
            ],
            'other_linked_companies': [
                'AngloGold Ashanti Obuasi Mine',
                'AngloGold Ashanti Iduapriem Mine',
                'AngloGold Ashanti Ghana Foundation'
            ]
        }
    ]
    
    with engine.connect() as conn:
        for company in companies_data:
            # Convert JSON data to strings
            company['directors'] = json.dumps(company['directors'])
            company['secretary'] = json.dumps(company['secretary'])
            company['auditor'] = json.dumps(company['auditor'])
            company['shareholders'] = json.dumps(company['shareholders'])
            company['other_linked_companies'] = json.dumps(company['other_linked_companies'])
            
            # Insert company
            insert_sql = """
            INSERT INTO companies (
                name, type_of_company, address, district, region, 
                date_of_incorporation, date_of_commencement, nature_of_business,
                registration_number, tax_identification_number, phone_number, email,
                directors, secretary, auditor, authorized_shares, stated_capital,
                shareholders, other_linked_companies, is_active, is_verified,
                search_count, created_at, updated_at, status
            ) VALUES (
                :name, :type_of_company, :address, :district, :region,
                :date_of_incorporation, :date_of_commencement, :nature_of_business,
                :registration_number, :tax_identification_number, :phone_number, :email,
                :directors, :secretary, :auditor, :authorized_shares, :stated_capital,
                :shareholders, :other_linked_companies, :is_active, :is_verified,
                :search_count, :created_at, :updated_at, :status
            )
            """
            
            company_data = {
                **company,
                'is_active': True,
                'is_verified': True,
                'search_count': 0,
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
                'status': 'ACTIVE'
            }
            
            conn.execute(text(insert_sql), company_data)
            print(f"✓ Added company: {company['name']}")
        
        conn.commit()
        print(f"\nSuccessfully added {len(companies_data)} companies to the database!")

if __name__ == "__main__":
    print("Fixing companies table columns...")
    fix_companies_columns()
    
    print("\nAdding more companies...")
    add_more_companies()
    
    print("\nDone!")
