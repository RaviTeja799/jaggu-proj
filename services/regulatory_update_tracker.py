"""
Real-time Regulatory Update Tracking Service.
Monitors regulatory sources, detects changes, and provides alerts.
"""
import logging
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional
import uuid
from collections import defaultdict

from models.regulatory_update import (
    RegulatoryUpdate, RegulatorySource, UpdateType, UpdateSeverity, UpdateStatus, UpdateAlert
)
from services.serper_api_client import SerperAPIClient, OFFICIAL_SOURCES, DEFAULT_KEYWORDS
from services.groq_api_client import GroqAPIClient
from services.knowledge_base_loader import KnowledgeBaseLoader


logger = logging.getLogger(__name__)


class RegulatoryUpdateTracker:
    """Main service for tracking and analyzing regulatory updates."""
    
    def __init__(
        self,
        serper_api_key: Optional[str] = None,
        groq_api_key: Optional[str] = None,
        storage_dir: Optional[Path] = None
    ):
        """
        Initialize regulatory update tracker.
        
        Args:
            serper_api_key: Serper API key
            groq_api_key: Groq API key
            storage_dir: Directory for storing update history
        """
        self.serper = SerperAPIClient(api_key=serper_api_key)
        self.groq = GroqAPIClient(api_key=groq_api_key)
        self.knowledge_base = KnowledgeBaseLoader()
        
        self.storage_dir = storage_dir or Path(__file__).parent.parent / "data" / "regulatory_updates"
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        self.updates_file = self.storage_dir / "updates.jsonl"
        self.sources_file = self.storage_dir / "sources.json"
        self.alerts_file = self.storage_dir / "alerts.json"
        
        # In-memory caches
        self.sources: Dict[str, RegulatorySource] = {}
        self.alerts: List[UpdateAlert] = []
        self.recent_updates: List[RegulatoryUpdate] = []
        
        # Statistics
        self.stats = defaultdict(int)
        
        logger.info("Initializing RegulatoryUpdateTracker...")
        self._load_sources()
        self._load_alerts()
        self._load_recent_updates()
        
        logger.info(f"Loaded {len(self.sources)} sources and {len(self.alerts)} alerts")
    
    def _load_sources(self):
        """Load configured sources from file."""
        if self.sources_file.exists():
            try:
                with open(self.sources_file, 'r') as f:
                    sources_data = json.load(f)
                    for source_dict in sources_data:
                        source = RegulatorySource(**source_dict)
                        self.sources[source.source_id] = source
                logger.info(f"Loaded {len(self.sources)} sources from file")
            except Exception as e:
                logger.error(f"Failed to load sources: {e}")
        else:
            # Initialize default sources
            self._initialize_default_sources()
    
    def _initialize_default_sources(self):
        """Create default regulatory sources."""
        logger.info("Initializing default regulatory sources...")
        
        for framework, domains in OFFICIAL_SOURCES.items():
            for domain in domains:
                source_id = f"{framework.lower()}_{domain.replace('.', '_')}"
                source = RegulatorySource(
                    source_id=source_id,
                    name=f"{framework} - {domain}",
                    url=f"https://{domain}",
                    framework=framework,
                    source_type="Official",
                    check_frequency_hours=24,
                    keywords=DEFAULT_KEYWORDS.get(framework, [])
                )
                self.sources[source_id] = source
        
        self._save_sources()
        logger.info(f"Initialized {len(self.sources)} default sources")
    
    def _save_sources(self):
        """Save sources to file."""
        try:
            sources_data = [source.to_dict() for source in self.sources.values()]
            with open(self.sources_file, 'w') as f:
                json.dump(sources_data, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save sources: {e}")
    
    def _load_alerts(self):
        """Load alert configurations from file."""
        if self.alerts_file.exists():
            try:
                with open(self.alerts_file, 'r') as f:
                    alerts_data = json.load(f)
                    for alert_dict in alerts_data:
                        alert = UpdateAlert(**alert_dict)
                        self.alerts.append(alert)
                logger.info(f"Loaded {len(self.alerts)} alerts from file")
            except Exception as e:
                logger.error(f"Failed to load alerts: {e}")
    
    def _save_alerts(self):
        """Save alert configurations to file."""
        try:
            alerts_data = [
                {
                    'alert_id': alert.alert_id,
                    'framework': alert.framework,
                    'keywords': alert.keywords,
                    'min_severity': alert.min_severity.value,
                    'notification_channels': alert.notification_channels,
                    'is_active': alert.is_active
                }
                for alert in self.alerts
            ]
            with open(self.alerts_file, 'w') as f:
                json.dump(alerts_data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save alerts: {e}")
    
    def _load_recent_updates(self, days: int = 30):
        """Load recent updates from JSONL file."""
        if not self.updates_file.exists():
            return
        
        cutoff_date = datetime.now() - timedelta(days=days)
        count = 0
        
        try:
            with open(self.updates_file, 'r') as f:
                for line in f:
                    try:
                        data = json.loads(line.strip())
                        update = RegulatoryUpdate.from_dict(data)
                        
                        if update.detected_date >= cutoff_date:
                            self.recent_updates.append(update)
                            count += 1
                    except Exception as e:
                        logger.warning(f"Failed to parse update: {e}")
                        continue
            
            logger.info(f"Loaded {count} recent updates from last {days} days")
        except Exception as e:
            logger.error(f"Failed to load recent updates: {e}")
    
    def save_update(self, update: RegulatoryUpdate):
        """Save an update to JSONL file."""
        try:
            with open(self.updates_file, 'a') as f:
                f.write(update.to_jsonl() + '\n')
            
            self.recent_updates.append(update)
            self.stats['updates_saved'] += 1
            
            logger.info(f"Saved update: {update.update_id}")
        except Exception as e:
            logger.error(f"Failed to save update: {e}")
    
    def check_for_updates(
        self,
        framework: str,
        time_range: str = 'w',
        force_check: bool = False
    ) -> List[RegulatoryUpdate]:
        """
        Check for new regulatory updates for a framework.
        
        Args:
            framework: Framework to check (GDPR, HIPAA, CCPA, SOX)
            time_range: Time range to search ('d', 'w', 'm', 'y')
            force_check: Force check even if recently checked
        
        Returns:
            List of detected updates
        """
        logger.info(f"Checking for {framework} updates (time_range={time_range})")
        
        updates = []
        
        # Get sources for this framework
        framework_sources = [s for s in self.sources.values() if s.framework == framework and s.is_active]
        
        for source in framework_sources:
            # Check if we need to check this source
            if not force_check and source.last_checked:
                hours_since_check = (datetime.now() - source.last_checked).total_seconds() / 3600
                if hours_since_check < source.check_frequency_hours:
                    logger.debug(f"Skipping {source.name} - checked {hours_since_check:.1f}h ago")
                    continue
            
            # Search for updates
            try:
                search_results = self.serper.search_regulatory_updates(
                    framework=framework,
                    keywords=source.keywords,
                    num_results=10,
                    time_range=time_range
                )
                
                logger.info(f"Found {len(search_results)} results from {source.name}")
                
                # Process each result
                for result in search_results:
                    update = self._process_search_result(result, source, framework)
                    if update and not self._is_duplicate(update):
                        updates.append(update)
                
                # Update last checked time
                source.last_checked = datetime.now()
                
            except Exception as e:
                logger.error(f"Error checking source {source.name}: {e}")
                continue
        
        # Save updated sources
        self._save_sources()
        
        # Analyze updates with Groq
        for update in updates:
            try:
                analysis = self.groq.analyze_regulatory_text(
                    text=update.full_text,
                    framework=framework,
                    context=f"Source: {update.source.name}"
                )
                
                if 'error' not in analysis:
                    update.ai_analysis = json.dumps(analysis)
                    update.severity = UpdateSeverity(analysis.get('severity', 'Medium'))
                    update.impact_score = analysis.get('impact_score', 0.5)
                    update.required_actions = analysis.get('required_actions', [])
                
            except Exception as e:
                logger.error(f"Failed to analyze update with Groq: {e}")
        
        logger.info(f"Detected {len(updates)} new {framework} updates")
        
        # Save all new updates
        for update in updates:
            self.save_update(update)
        
        # Check alerts
        self._check_alerts(updates)
        
        self.stats['checks_performed'] += 1
        self.stats[f'{framework}_updates_found'] += len(updates)
        
        return updates
    
    def _process_search_result(
        self,
        result: Dict[str, Any],
        source: RegulatorySource,
        framework: str
    ) -> Optional[RegulatoryUpdate]:
        """Process a search result into a RegulatoryUpdate."""
        try:
            update_id = str(uuid.uuid4())
            
            title = result.get('title', 'Untitled')
            snippet = result.get('snippet', '')
            link = result.get('link', '')
            
            # Determine update type based on title/snippet
            update_type = self._classify_update_type(title + ' ' + snippet)
            
            # Initial severity (will be refined by AI)
            severity = UpdateSeverity.MEDIUM
            
            update = RegulatoryUpdate(
                update_id=update_id,
                framework=framework,
                title=title,
                summary=snippet,
                full_text=snippet,  # Will be expanded if we fetch full content
                source=source,
                update_type=update_type,
                severity=severity,
                status=UpdateStatus.DETECTED,
                detected_date=datetime.now(),
                source_url=link,
                keywords=source.keywords
            )
            
            return update
            
        except Exception as e:
            logger.error(f"Failed to process search result: {e}")
            return None
    
    def _classify_update_type(self, text: str) -> UpdateType:
        """Classify update type based on text."""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['new regulation', 'new rule', 'enacted']):
            return UpdateType.NEW_REGULATION
        elif any(word in text_lower for word in ['amendment', 'amended', 'modified', 'revised']):
            return UpdateType.AMENDMENT
        elif any(word in text_lower for word in ['clarification', 'guidance', 'interpretation']):
            return UpdateType.CLARIFICATION
        elif any(word in text_lower for word in ['enforcement', 'fine', 'penalty', 'violation']):
            return UpdateType.ENFORCEMENT
        elif any(word in text_lower for word in ['guidance', 'guide', 'best practice']):
            return UpdateType.GUIDANCE
        elif any(word in text_lower for word in ['case', 'court', 'ruling', 'decision']):
            return UpdateType.CASE_LAW
        elif any(word in text_lower for word in ['proposed', 'proposal', 'draft']):
            return UpdateType.PROPOSAL
        else:
            return UpdateType.CLARIFICATION
    
    def _is_duplicate(self, update: RegulatoryUpdate) -> bool:
        """Check if update is a duplicate of existing update."""
        for existing in self.recent_updates:
            # Check if titles are very similar
            if existing.title == update.title and existing.framework == update.framework:
                return True
            
            # Check if source URLs match
            if update.source_url and existing.source_url == update.source_url:
                return True
        
        return False
    
    def _check_alerts(self, updates: List[RegulatoryUpdate]):
        """Check if any alerts should be triggered for updates."""
        for update in updates:
            for alert in self.alerts:
                if alert.matches_update(update):
                    logger.info(f"Alert triggered: {alert.alert_id} for update {update.update_id}")
                    # In a full implementation, send notifications here
                    update.status = UpdateStatus.NOTIFIED
    
    def check_all_frameworks(self, frameworks: Optional[List[str]] = None, time_range: str = 'w') -> Dict[str, List[RegulatoryUpdate]]:
        """
        Check all enabled frameworks for updates.
        
        Args:
            frameworks: List of frameworks to check (default: all frameworks)
            time_range: Time range to check
        
        Returns:
            Dictionary mapping framework to list of updates
        """
        results = {}
        
        # Use provided frameworks or default to all
        frameworks_to_check = frameworks or ['GDPR', 'HIPAA', 'CCPA', 'SOX']
        
        for framework in frameworks_to_check:
            logger.info(f"Checking {framework}...")
            updates = self.check_for_updates(framework, time_range=time_range)
            results[framework] = updates
        
        return results
    
    def get_updates(
        self,
        framework: Optional[str] = None,
        severity: Optional[UpdateSeverity] = None,
        status: Optional[UpdateStatus] = None,
        days: int = 30,
        limit: Optional[int] = None
    ) -> List[RegulatoryUpdate]:
        """
        Get filtered list of updates.
        
        Args:
            framework: Filter by framework
            severity: Filter by minimum severity
            status: Filter by status
            days: Get updates from last N days
            limit: Maximum number of results
        
        Returns:
            Filtered list of updates
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        
        filtered = []
        for update in self.recent_updates:
            if update.detected_date < cutoff_date:
                continue
            
            if framework and update.framework != framework:
                continue
            
            if severity:
                severity_order = {
                    UpdateSeverity.LOW: 0,
                    UpdateSeverity.MEDIUM: 1,
                    UpdateSeverity.HIGH: 2,
                    UpdateSeverity.CRITICAL: 3
                }
                if severity_order[update.severity] < severity_order[severity]:
                    continue
            
            if status and update.status != status:
                continue
            
            filtered.append(update)
        
        # Sort by detected date (newest first)
        filtered.sort(key=lambda x: x.detected_date, reverse=True)
        
        if limit:
            filtered = filtered[:limit]
        
        return filtered
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get tracking statistics."""
        framework_counts = defaultdict(int)
        severity_counts = defaultdict(int)
        status_counts = defaultdict(int)
        
        for update in self.recent_updates:
            framework_counts[update.framework] += 1
            severity_counts[update.severity.value] += 1
            status_counts[update.status.value] += 1
        
        return {
            'total_sources': len(self.sources),
            'active_sources': sum(1 for s in self.sources.values() if s.is_active),
            'total_alerts': len(self.alerts),
            'active_alerts': sum(1 for a in self.alerts if a.is_active),
            'recent_updates': len(self.recent_updates),
            'by_framework': dict(framework_counts),
            'by_severity': dict(severity_counts),
            'by_status': dict(status_counts),
            'checks_performed': self.stats.get('checks_performed', 0),
            'updates_saved': self.stats.get('updates_saved', 0)
        }
