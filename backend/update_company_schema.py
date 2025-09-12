#!/usr/bin/env python3
"""
Script to update company schema with comprehensive profile fields
"""

from sqlalchemy import create_engine, text
from config import settings

def update_company_table():
    """Update the companies table with comprehensive profile fields"""
    engine = create_engine(settings.database_url)
    
    # Add new columns to companies table
    alter_queries = [
        # Basic Company Information
        "ALTER TABLE companies ADD COLUMN type_of_company VARCHAR(100)",
        "ALTER TABLE companies ADD COLUMN address TEXT",
        "ALTER TABLE companies ADD COLUMN district VARCHAR(100)",
        "ALTER TABLE companies ADD COLUMN region VARCHAR(50)",
        "ALTER TABLE companies ADD COLUMN date_of_incorporation DATE",
        "ALTER TABLE companies ADD COLUMN date_of_commencement DATE",
        "ALTER TABLE companies ADD COLUMN nature_of_business TEXT",
        "ALTER TABLE companies ADD COLUMN registration_number VARCHAR(100)",
        "ALTER TABLE companies ADD COLUMN tax_identification_number VARCHAR(50)",
        "ALTER TABLE companies ADD COLUMN phone_number VARCHAR(20)",
        "ALTER TABLE companies ADD COLUMN email VARCHAR(100)",
        
        # Directors (JSON array)
        "ALTER TABLE companies ADD COLUMN directors JSON",
        
        # Secretary (JSON object)
        "ALTER TABLE companies ADD COLUMN secretary JSON",
        
        # Auditor (JSON object)
        "ALTER TABLE companies ADD COLUMN auditor JSON",
        
        # Capital Details
        "ALTER TABLE companies ADD COLUMN authorized_shares INT",
        "ALTER TABLE companies ADD COLUMN stated_capital DECIMAL(15,2)",
        
        # Shareholders (JSON array)
        "ALTER TABLE companies ADD COLUMN shareholders JSON",
        
        # Other Linked Companies (JSON array)
        "ALTER TABLE companies ADD COLUMN other_linked_companies JSON"
    ]
    
    with engine.connect() as conn:
        for query in alter_queries:
            try:
                conn.execute(text(query))
                print(f"✓ Added column: {query.split('ADD COLUMN ')[1].split(' ')[0]}")
            except Exception as e:
                if "Duplicate column name" in str(e):
                    print(f"⚠ Column already exists: {query.split('ADD COLUMN ')[1].split(' ')[0]}")
                else:
                    print(f"✗ Error adding column: {e}")
        conn.commit()
        print("Company table schema updated successfully!")

def create_sample_company_data():
    """Create sample data for a comprehensive company profile"""
    engine = create_engine(settings.database_url)
    
    sample_company = {
        'name': 'Ghana Commercial Bank Limited',
        'type_of_company': 'Public Limited Company',
        'address': 'High Street, Accra Central, Ghana',
        'district': 'Accra Metropolitan',
        'region': 'Greater Accra',
        'date_of_incorporation': '1953-01-01',
        'date_of_commencement': '1953-02-01',
        'nature_of_business': 'Banking and Financial Services',
        'registration_number': 'RC123456',
        'tax_identification_number': 'C0001234567',
        'phone_number': '+233-302-123456',
        'email': 'info@gcbbank.com',
        'directors': [
            {
                'name': 'Dr. Ernest Addison',
                'address': '123 Independence Avenue, Accra',
                'nationality': 'Ghanaian',
                'occupation': 'Banker',
                'email': 'ernest.addison@gcbbank.com',
                'contact': '+233-244-123456',
                'tax_identification_number': 'P0001234567',
                'other_directorship': ['Bank of Ghana', 'Ghana Stock Exchange']
            },
            {
                'name': 'Mrs. Grace Amoah',
                'address': '456 Ring Road, Accra',
                'nationality': 'Ghanaian',
                'occupation': 'Accountant',
                'email': 'grace.amoah@gcbbank.com',
                'contact': '+233-244-234567',
                'tax_identification_number': 'P0002345678',
                'other_directorship': ['Ghana Revenue Authority']
            }
        ],
        'secretary': {
            'name': 'Mr. Kwame Asante',
            'address': '789 Oxford Street, Accra',
            'nationality': 'Ghanaian',
            'occupation': 'Company Secretary',
            'email': 'kwame.asante@gcbbank.com',
            'contact': '+233-244-345678',
            'tax_identification_number': 'P0003456789'
        },
        'auditor': {
            'name': 'KPMG Ghana',
            'address': '10 Independence Avenue, Accra',
            'nationality': 'Ghanaian',
            'occupation': 'Auditing Firm',
            'email': 'ghana@kpmg.com',
            'contact': '+233-302-456789',
            'tax_identification_number': 'C0004567890'
        },
        'authorized_shares': 1000000000,
        'stated_capital': 500000000.00,
        'shareholders': [
            {
                'name': 'Government of Ghana',
                'address': 'Flagstaff House, Accra',
                'nationality': 'Ghanaian',
                'occupation': 'Government',
                'email': 'info@ghana.gov.gh',
                'contact': '+233-302-789012',
                'tax_identification_number': 'G0007890123',
                'shares_alloted': 600000000,
                'consideration_payable': 'Cash'
            },
            {
                'name': 'Dr. John Mensah',
                'address': '321 Labone, Accra',
                'nationality': 'Ghanaian',
                'occupation': 'Businessman',
                'email': 'john.mensah@email.com',
                'contact': '+233-244-456789',
                'tax_identification_number': 'P0004567890',
                'shares_alloted': 10000000,
                'consideration_payable': 'Cash'
            }
        ],
        'other_linked_companies': [
            'GCB Capital Limited',
            'GCB Properties Limited',
            'GCB Insurance Brokers Limited'
        ]
    }
    
    # Update the first company with comprehensive data
    import json
    
    update_query = """
    UPDATE companies SET 
        type_of_company = :type_of_company,
        address = :address,
        district = :district,
        region = :region,
        date_of_incorporation = :date_of_incorporation,
        date_of_commencement = :date_of_commencement,
        nature_of_business = :nature_of_business,
        registration_number = :registration_number,
        tax_identification_number = :tax_identification_number,
        phone_number = :phone_number,
        email = :email,
        directors = :directors,
        secretary = :secretary,
        auditor = :auditor,
        authorized_shares = :authorized_shares,
        stated_capital = :stated_capital,
        shareholders = :shareholders,
        other_linked_companies = :other_linked_companies
    WHERE id = 1
    """
    
    # Convert JSON data to strings
    sample_company['directors'] = json.dumps(sample_company['directors'])
    sample_company['secretary'] = json.dumps(sample_company['secretary'])
    sample_company['auditor'] = json.dumps(sample_company['auditor'])
    sample_company['shareholders'] = json.dumps(sample_company['shareholders'])
    sample_company['other_linked_companies'] = json.dumps(sample_company['other_linked_companies'])
    
    with engine.connect() as conn:
        conn.execute(text(update_query), sample_company)
        conn.commit()
        print("Sample company data updated successfully!")

if __name__ == "__main__":
    print("Updating company schema...")
    update_company_table()
    
    print("\nAdding sample company data...")
    create_sample_company_data()
    
    print("Done!")
