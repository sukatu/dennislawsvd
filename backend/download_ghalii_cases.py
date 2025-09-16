#!/usr/bin/env python3
"""
Script to download and add Circuit Court and District Court cases from GhaLII
to the DennisLaw SVD database.
"""

import sys
import os
import requests
import json
import time
import re
from datetime import datetime
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import logging

# Add the backend directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from database import get_db
from models.reported_cases import ReportedCases
from config import settings

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GhaLIICaseDownloader:
    def __init__(self):
        self.base_url = "https://ghalii.org"
        self.district_court_url = "https://ghalii.org/judgments/GHADC/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.db = next(get_db())
        
    def get_case_links(self, court_type="district", max_pages=50):
        """Get all case links from GhaLII"""
        case_links = []
        
        if court_type == "district":
            base_url = self.district_court_url
        else:
            # Add Circuit Court URL when available
            base_url = f"{self.base_url}/judgments/GHACC/"
            
        logger.info(f"Fetching case links from {base_url}")
        
        for page in range(1, max_pages + 1):
            try:
                # GhaLII uses pagination
                url = f"{base_url}?page={page}" if page > 1 else base_url
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find case links in the table
                case_rows = soup.find_all('tr')
                page_cases = 0
                
                for row in case_rows:
                    link_elem = row.find('a', href=True)
                    if link_elem and '/akn/gh/judgment/' in link_elem['href']:
                        case_url = self.base_url + link_elem['href']
                        case_title = link_elem.get_text(strip=True)
                        case_links.append({
                            'url': case_url,
                            'title': case_title,
                            'court_type': court_type
                        })
                        page_cases += 1
                
                logger.info(f"Page {page}: Found {page_cases} cases")
                
                # If no cases found on this page, we've reached the end
                if page_cases == 0:
                    break
                    
                # Be respectful to the server
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error fetching page {page}: {e}")
                continue
                
        logger.info(f"Total case links found: {len(case_links)}")
        return case_links
    
    def extract_case_details(self, case_url, case_title, court_type):
        """Extract detailed case information from individual case page"""
        try:
            response = self.session.get(case_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract case details
            case_data = {
                'title': case_title,
                'court_type': court_type,
                'url': case_url,
                'content': '',
                'date': None,
                'citation': '',
                'judge': '',
                'region': '',
                'town': '',
                'year': None,
                'protagonist': '',
                'antagonist': '',
                'decision': '',
                'area_of_law': '',
                'keywords_phrases': '',
                'case_summary': ''
            }
            
            # Extract citation from URL or content
            if '/akn/gh/judgment/' in case_url:
                citation_match = re.search(r'\[(\d{4})\] GHADC (\d+)', case_title)
                if citation_match:
                    case_data['citation'] = f"[{citation_match.group(1)}] GHADC {citation_match.group(2)}"
                    case_data['year'] = int(citation_match.group(1))
            
            # Extract date from title or content
            date_match = re.search(r'(\d{1,2} \w+ \d{4})', case_title)
            if date_match:
                try:
                    case_data['date'] = datetime.strptime(date_match.group(1), '%d %B %Y').date()
                except:
                    try:
                        case_data['date'] = datetime.strptime(date_match.group(1), '%d %b %Y').date()
                    except:
                        pass
            
            # Extract main content
            content_div = soup.find('div', class_='judgment-content') or soup.find('div', class_='content')
            if content_div:
                case_data['content'] = content_div.get_text(strip=True)
            else:
                # Fallback: get all text content
                case_data['content'] = soup.get_text(strip=True)
            
            # Extract case parties from title
            if ' VRS ' in case_title.upper():
                parties = case_title.split(' VRS ')
                if len(parties) >= 2:
                    case_data['protagonist'] = parties[0].strip()
                    case_data['antagonist'] = parties[1].strip()
            elif ' V ' in case_title.upper():
                parties = case_title.split(' V ')
                if len(parties) >= 2:
                    case_data['protagonist'] = parties[0].strip()
                    case_data['antagonist'] = parties[1].strip()
            
            # Extract area of law from content
            law_areas = [
                'Criminal Law', 'Civil Law', 'Land Law', 'Contract Law', 'Family Law',
                'Commercial Law', 'Constitutional Law', 'Administrative Law',
                'Property Law', 'Tort Law', 'Employment Law', 'Tax Law'
            ]
            
            content_upper = case_data['content'].upper()
            for area in law_areas:
                if area.upper() in content_upper:
                    case_data['area_of_law'] = area
                    break
            
            # Generate case summary from content
            if case_data['content']:
                # Take first 500 characters as summary
                case_data['case_summary'] = case_data['content'][:500] + '...' if len(case_data['content']) > 500 else case_data['content']
            
            # Extract keywords
            keywords = []
            if case_data['area_of_law']:
                keywords.append(case_data['area_of_law'])
            if case_data['protagonist']:
                keywords.append(case_data['protagonist'])
            if case_data['antagonist']:
                keywords.append(case_data['antagonist'])
            
            case_data['keywords_phrases'] = ', '.join(keywords)
            
            return case_data
            
        except Exception as e:
            logger.error(f"Error extracting case details from {case_url}: {e}")
            return None
    
    def save_case_to_database(self, case_data):
        """Save case data to database"""
        try:
            # Check if case already exists
            existing_case = self.db.query(ReportedCases).filter(
                ReportedCases.title == case_data['title']
            ).first()
            
            if existing_case:
                logger.info(f"Case already exists: {case_data['title']}")
                return False
            
            # Create new case record
            new_case = ReportedCases(
                title=case_data['title'],
                citation=case_data['citation'],
                date=case_data['date'],
                court_type=case_data['court_type'],
                region=case_data['region'],
                town=case_data['town'],
                year=case_data['year'],
                protagonist=case_data['protagonist'],
                antagonist=case_data['antagonist'],
                decision=case_data['decision'],
                area_of_law=case_data['area_of_law'],
                keywords_phrases=case_data['keywords_phrases'],
                case_summary=case_data['case_summary'],
                detail_content=case_data['content'],
                file_url=case_data['url'],
                dl_citation_no=case_data['citation'],
                created_at=datetime.now(),
                updated_at=datetime.now(),
                published=True,
                status=1  # 1 for Active, 0 for Inactive
            )
            
            self.db.add(new_case)
            self.db.commit()
            
            logger.info(f"Saved case: {case_data['title']}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving case to database: {e}")
            self.db.rollback()
            return False
    
    def download_cases(self, court_type="district", max_cases=100):
        """Download and save cases from GhaLII"""
        logger.info(f"Starting download of {court_type} court cases...")
        
        # Get case links
        case_links = self.get_case_links(court_type, max_pages=50)
        
        if not case_links:
            logger.warning("No case links found")
            return
        
        # Limit to max_cases
        case_links = case_links[:max_cases]
        
        successful_downloads = 0
        failed_downloads = 0
        
        for i, case_link in enumerate(case_links, 1):
            logger.info(f"Processing case {i}/{len(case_links)}: {case_link['title']}")
            
            # Extract case details
            case_data = self.extract_case_details(
                case_link['url'], 
                case_link['title'], 
                case_link['court_type']
            )
            
            if case_data:
                # Save to database
                if self.save_case_to_database(case_data):
                    successful_downloads += 1
                else:
                    failed_downloads += 1
            else:
                failed_downloads += 1
            
            # Be respectful to the server
            time.sleep(2)
            
            # Progress update every 10 cases
            if i % 10 == 0:
                logger.info(f"Progress: {i}/{len(case_links)} cases processed")
        
        logger.info(f"Download completed!")
        logger.info(f"Successful downloads: {successful_downloads}")
        logger.info(f"Failed downloads: {failed_downloads}")
        
        return successful_downloads, failed_downloads

def main():
    """Main function to download cases"""
    downloader = GhaLIICaseDownloader()
    
    try:
        # Download District Court cases
        logger.info("Downloading District Court cases...")
        district_success, district_failed = downloader.download_cases("district", max_cases=100)
        
        # You can add Circuit Court cases here when available
        # logger.info("Downloading Circuit Court cases...")
        # circuit_success, circuit_failed = downloader.download_cases("circuit", max_cases=100)
        
        logger.info("All downloads completed!")
        
    except Exception as e:
        logger.error(f"Error in main process: {e}")
    finally:
        downloader.db.close()

if __name__ == "__main__":
    main()
