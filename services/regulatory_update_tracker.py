"""
Regulatory Update Tracking System
Monitors regulatory changes from public APIs and databases
"""

import os
import logging
import requests
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import hashlib
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class RegulatoryUpdateTracker:
    """
    Service for tracking regulatory updates from various sources.
    Monitors SEC Edgar, EUR-Lex, and other regulatory APIs.
    """
    
    def __init__(self):
        """Initialize regulatory update tracker."""
        self.logger = logging.getLogger(__name__)
        self.cache_dir = Path(__file__).parent.parent / "data" / "regulatory_cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # API configurations
        self.sec_edgar_url = os.getenv('SEC_EDGAR_API_URL', 'https://www.sec.gov/cgi-bin/browse-edgar')
        self.user_agent = os.getenv('REGULATORY_USER_AGENT', 'ComplianceBot/1.0')
        self.polling_interval_hours = int(os.getenv('POLLING_INTERVAL_HOURS', '24'))
        
        # Track last update times
        self.last_check_file = self.cache_dir / "last_check.json"
        self.last_checks = self._load_last_checks()
    
    def _load_last_checks(self) -> Dict[str, str]:
        """Load last check timestamps."""
        if self.last_check_file.exists():
            try:
                with open(self.last_check_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Error loading last checks: {e}")
        return {}
    
    def _save_last_checks(self):
        """Save last check timestamps."""
        try:
            with open(self.last_check_file, 'w') as f:
                json.dump(self.last_checks, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving last checks: {e}")
    
    def should_check_source(self, source: str) -> bool:
        """
        Check if enough time has passed since last check for a source.
        
        Args:
            source: Source identifier
            
        Returns:
            True if should check now
        """
        if source not in self.last_checks:
            return True
        
        last_check = datetime.fromisoformat(self.last_checks[source])
        hours_since = (datetime.now() - last_check).total_seconds() / 3600
        
        return hours_since >= self.polling_interval_hours
    
    def _calculate_content_hash(self, content: str) -> str:
        """Calculate SHA-256 hash of content for change detection."""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def fetch_sec_edgar_updates(
        self,
        company: Optional[str] = None,
        form_type: str = '10-K',
        days_back: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Fetch updates from SEC Edgar.
        
        Args:
            company: Company ticker or CIK (optional)
            form_type: Type of SEC form to monitor
            days_back: Number of days to look back
            
        Returns:
            List of regulatory updates
        """
        if not self.should_check_source('sec_edgar'):
            self.logger.info("Skipping SEC Edgar check (too recent)")
            return []
        
        try:
            self.logger.info(f"Fetching SEC Edgar updates (form: {form_type}, days: {days_back})")
            
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            # Build request parameters
            params = {
                'action': 'getcompany',
                'type': form_type,
                'dateb': end_date.strftime('%Y%m%d'),
                'datea': start_date.strftime('%Y%m%d'),
                'output': 'atom',
                'count': 100
            }
            
            if company:
                params['CIK'] = company
            
            headers = {
                'User-Agent': self.user_agent,
                'Accept': 'application/atom+xml'
            }
            
            # Make request
            response = requests.get(
                self.sec_edgar_url,
                params=params,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                # Parse response (simplified - real implementation would parse XML)
                updates = self._parse_sec_edgar_response(response.text)
                
                # Update last check time
                self.last_checks['sec_edgar'] = datetime.now().isoformat()
                self._save_last_checks()
                
                self.logger.info(f"Found {len(updates)} SEC Edgar updates")
                return updates
            else:
                self.logger.error(f"SEC Edgar API error: {response.status_code}")
                return []
                
        except Exception as e:
            self.logger.error(f"Error fetching SEC Edgar updates: {e}")
            return []
    
    def _parse_sec_edgar_response(self, xml_content: str) -> List[Dict[str, Any]]:
        """
        Parse SEC Edgar XML response.
        
        Args:
            xml_content: XML content from SEC Edgar
            
        Returns:
            List of parsed updates
        """
        # Simplified parsing - real implementation would use XML parser
        updates = []
        
        try:
            # This is a placeholder - implement proper XML parsing
            updates.append({
                'source': 'SEC Edgar',
                'title': 'Sample SEC Filing Update',
                'description': 'New regulatory filing detected',
                'url': 'https://www.sec.gov/edgar',
                'published_date': datetime.now().isoformat(),
                'severity': 'medium',
                'jurisdiction': 'US',
                'applicable_domain': 'Finance'
            })
        except Exception as e:
            self.logger.error(f"Error parsing SEC Edgar response: {e}")
        
        return updates
    
    def fetch_gdpr_updates(self) -> List[Dict[str, Any]]:
        """
        Fetch GDPR-related updates from EUR-Lex.
        
        Returns:
            List of regulatory updates
        """
        if not self.should_check_source('eur_lex'):
            self.logger.info("Skipping EUR-Lex check (too recent)")
            return []
        
        try:
            self.logger.info("Fetching EUR-Lex GDPR updates")
            
            # EUR-Lex API endpoint (example)
            url = "https://eur-lex.europa.eu/search.html"
            params = {
                'qid': '1234567890',
                'DTS_DOM': 'ALL',
                'type': 'advanced',
                'lang': 'en',
                'SUBDOM_INIT': 'EU_LAW',
                'DTS_SUBDOM': 'EU_LAW'
            }
            
            headers = {
                'User-Agent': self.user_agent
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=30)
            
            if response.status_code == 200:
                updates = self._parse_eur_lex_response(response.text)
                
                # Update last check time
                self.last_checks['eur_lex'] = datetime.now().isoformat()
                self._save_last_checks()
                
                self.logger.info(f"Found {len(updates)} EUR-Lex updates")
                return updates
            else:
                self.logger.error(f"EUR-Lex API error: {response.status_code}")
                return []
                
        except Exception as e:
            self.logger.error(f"Error fetching EUR-Lex updates: {e}")
            return []
    
    def _parse_eur_lex_response(self, html_content: str) -> List[Dict[str, Any]]:
        """
        Parse EUR-Lex HTML response.
        
        Args:
            html_content: HTML content from EUR-Lex
            
        Returns:
            List of parsed updates
        """
        # Placeholder - implement proper HTML parsing
        updates = []
        
        updates.append({
            'source': 'EUR-Lex',
            'title': 'Sample GDPR Amendment',
            'description': 'Updated data processing requirements',
            'url': 'https://eur-lex.europa.eu',
            'published_date': datetime.now().isoformat(),
            'severity': 'high',
            'jurisdiction': 'EU',
            'applicable_domain': 'GDPR'
        })
        
        return updates
    
    def fetch_all_updates(self) -> List[Dict[str, Any]]:
        """
        Fetch updates from all configured sources.
        
        Returns:
            Combined list of regulatory updates
        """
        all_updates = []
        
        # Fetch from SEC Edgar
        sec_updates = self.fetch_sec_edgar_updates()
        all_updates.extend(sec_updates)
        
        # Fetch from EUR-Lex
        gdpr_updates = self.fetch_gdpr_updates()
        all_updates.extend(gdpr_updates)
        
        # Add more sources as needed
        # hipaa_updates = self.fetch_hipaa_updates()
        # all_updates.extend(hipaa_updates)
        
        return all_updates
    
    def extract_keywords_from_update(self, update: Dict[str, Any]) -> List[str]:
        """
        Extract relevant keywords from regulatory update using NLP.
        
        Args:
            update: Regulatory update dictionary
            
        Returns:
            List of extracted keywords
        """
        try:
            # Try to use spaCy if available
            import spacy
            
            # Load English model
            try:
                nlp = spacy.load("en_core_web_sm")
            except:
                self.logger.warning("spaCy model not found. Using simple keyword extraction.")
                return self._simple_keyword_extraction(update)
            
            # Combine title and description
            text = f"{update.get('title', '')} {update.get('description', '')}"
            
            # Process text
            doc = nlp(text)
            
            # Extract entities and key phrases
            keywords = []
            
            # Add named entities
            for ent in doc.ents:
                if ent.label_ in ['ORG', 'LAW', 'GPE', 'PRODUCT']:
                    keywords.append(ent.text.lower())
            
            # Add important nouns and noun phrases
            for chunk in doc.noun_chunks:
                if len(chunk.text.split()) <= 3:  # Limit phrase length
                    keywords.append(chunk.text.lower())
            
            # Remove duplicates and return
            return list(set(keywords))[:20]  # Limit to top 20
            
        except ImportError:
            self.logger.info("spaCy not available, using simple keyword extraction")
            return self._simple_keyword_extraction(update)
        except Exception as e:
            self.logger.error(f"Error extracting keywords: {e}")
            return self._simple_keyword_extraction(update)
    
    def _simple_keyword_extraction(self, update: Dict[str, Any]) -> List[str]:
        """
        Simple keyword extraction without NLP.
        
        Args:
            update: Regulatory update dictionary
            
        Returns:
            List of keywords
        """
        text = f"{update.get('title', '')} {update.get('description', '')}".lower()
        
        # Common legal/compliance keywords
        legal_terms = [
            'data', 'privacy', 'protection', 'security', 'consent', 'processing',
            'controller', 'processor', 'breach', 'notification', 'rights', 'subject',
            'transfer', 'compliance', 'audit', 'liability', 'penalty', 'regulation',
            'directive', 'law', 'requirement', 'obligation', 'contract', 'agreement'
        ]
        
        # Extract matching terms
        keywords = [term for term in legal_terms if term in text]
        
        return keywords[:10]
    
    def calculate_urgency_score(self, update: Dict[str, Any]) -> float:
        """
        Calculate modification urgency score for a regulatory update.
        
        Args:
            update: Regulatory update dictionary
            
        Returns:
            Urgency score (0-100)
        """
        score = 0.0
        
        # Base score on severity
        severity = update.get('severity', 'medium').lower()
        severity_scores = {
            'critical': 100,
            'high': 80,
            'medium': 50,
            'low': 20
        }
        score += severity_scores.get(severity, 50)
        
        # Adjust for recency
        try:
            published = datetime.fromisoformat(update.get('published_date', datetime.now().isoformat()))
            days_old = (datetime.now() - published).days
            
            if days_old <= 7:
                score += 10
            elif days_old <= 30:
                score += 5
        except:
            pass
        
        # Adjust for jurisdiction importance
        jurisdiction = update.get('jurisdiction', '').upper()
        if jurisdiction in ['EU', 'US']:
            score += 5
        
        # Cap at 100
        return min(score, 100.0)


# Example usage
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Initialize tracker
    tracker = RegulatoryUpdateTracker()
    
    # Fetch updates
    updates = tracker.fetch_all_updates()
    
    # Process each update
    for update in updates:
        print(f"\nRegulatory Update: {update['title']}")
        print(f"Source: {update['source']}")
        print(f"Severity: {update['severity']}")
        
        # Extract keywords
        keywords = tracker.extract_keywords_from_update(update)
        print(f"Keywords: {', '.join(keywords[:5])}")
        
        # Calculate urgency
        urgency = tracker.calculate_urgency_score(update)
        print(f"Urgency Score: {urgency:.1f}/100")
