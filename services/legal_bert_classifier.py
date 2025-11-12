"""
LegalBERT-based clause classification service.
"""
import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModel
from typing import Tuple, List
import numpy as np
from utils.logger import get_logger

logger = get_logger(__name__)


class LegalBERTClassifier:
    """LegalBERT-based clause classification."""
    
    def __init__(self, model_name: str = "nlpaueb/legal-bert-base-uncased"):
        """
        Initialize LegalBERT classifier.
        
        Args:
            model_name: Hugging Face model identifier
        """
        self.model_name = model_name
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {self.device}")
        
        # Load model and tokenizer with caching
        self.model = self._load_model()
        self.tokenizer = self._load_tokenizer()
        
        # Define clause type mappings for classification
        self.clause_types = [
            "Data Processing",
            "Sub-processor Authorization",
            "Data Subject Rights",
            "Breach Notification",
            "Data Transfer",
            "Security Safeguards",
            "Permitted Uses and Disclosures",
            "Other"
        ]
        
        # Keywords for rule-based classification assistance
        self.clause_keywords = {
            "Data Processing": [
                "process", "processing", "processor", "controller", "instructions",
                "documented instructions", "personal data processing", "data controller",
                "data processor", "processing activities", "lawful basis"
            ],
            "Sub-processor Authorization": [
                "sub-processor", "subprocessor", "sub processor", "authorization", "prior written",
                "notification", "object", "third party processor", "engage third party",
                "downstream processor", "subcontractor"
            ],
            "Data Subject Rights": [
                "data subject", "rights", "access", "rectification", "erasure",
                "portability", "restriction", "objection", "right to", "individual rights",
                "access request", "deletion request", "right to be forgotten"
            ],
            "Breach Notification": [
                "breach", "notification", "notify", "security breach", "incident",
                "data breach", "unauthorized access", "breach response", "incident response",
                "72 hours", "without undue delay", "security incident"
            ],
            "Data Transfer": [
                "transfer", "cross-border", "third country", "international",
                "standard contractual clauses", "adequacy decision", "SCC", "SCCs",
                "international transfer", "outside", "data export", "transfer mechanism"
            ],
            "Security Safeguards": [
                "security", "safeguards", "measures", "technical", "organizational",
                "encryption", "pseudonymization", "confidentiality", "integrity",
                "availability", "security measures", "technical and organizational measures",
                "access controls", "authentication", "backup"
            ],
            "Permitted Uses and Disclosures": [
                "permitted", "allowed", "disclosure", "use", "purpose",
                "authorized use", "permitted disclosure", "lawful purpose",
                "legitimate interest", "specific purpose", "purpose limitation"
            ]
        }
        
        # Phrase weights - longer/more specific phrases get higher weight
        self.phrase_weights = {
            "technical and organizational measures": 3.0,
            "documented instructions": 2.5,
            "standard contractual clauses": 2.5,
            "data subject rights": 2.5,
            "sub-processor": 2.0,
            "security breach": 2.0,
            "cross-border": 2.0,
            "personal data": 1.5,
            "processing": 1.0
        }
    
    @st.cache_resource
    def _load_model(_self):
        """
        Load LegalBERT model with Streamlit caching.
        
        Returns:
            Loaded model
        """
        try:
            logger.info(f"Loading LegalBERT model: {_self.model_name}")
            model = AutoModel.from_pretrained(_self.model_name)
            model.to(_self.device)
            model.eval()
            logger.info("LegalBERT model loaded successfully")
            return model
        except Exception as e:
            logger.error(f"Error loading LegalBERT model: {e}")
            raise
    
    @st.cache_resource
    def _load_tokenizer(_self):
        """
        Load tokenizer with Streamlit caching.
        
        Returns:
            Loaded tokenizer
        """
        try:
            logger.info(f"Loading tokenizer: {_self.model_name}")
            tokenizer = AutoTokenizer.from_pretrained(_self.model_name)
            logger.info("Tokenizer loaded successfully")
            return tokenizer
        except Exception as e:
            logger.error(f"Error loading tokenizer: {e}")
            raise
    
    def _keyword_based_classification(self, text: str) -> List[Tuple[str, float]]:
        """
        Perform enhanced keyword-based classification.
        Uses weighted phrase matching for better accuracy.
        
        Args:
            text: Clause text to classify
            
        Returns:
            List of (clause_type, score) tuples sorted by score
        """
        text_lower = text.lower()
        scores = {}
        
        for clause_type, keywords in self.clause_keywords.items():
            total_score = 0.0
            
            # Check each keyword/phrase
            for keyword in keywords:
                if keyword in text_lower:
                    # Apply weight if phrase is in weight dict
                    weight = self.phrase_weights.get(keyword, 1.0)
                    
                    # Bonus for exact phrase match (not just substring)
                    if f" {keyword} " in f" {text_lower} ":
                        weight *= 1.5
                    
                    total_score += weight
            
            # Normalize by total possible score for this category
            max_possible_score = sum(self.phrase_weights.get(kw, 1.0) for kw in keywords)
            normalized_score = total_score / max_possible_score if max_possible_score > 0 else 0.0
            
            scores[clause_type] = normalized_score
        
        # Sort by score descending
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_scores
    
    def predict(self, text: str, top_k: int = 3) -> Tuple[str, float, List[Tuple[str, float]]]:
        """
        Predict clause type with confidence score.
        
        Args:
            text: Clause text to classify
            top_k: Number of alternative predictions to return
            
        Returns:
            Tuple of (predicted_type, confidence, alternatives)
            where alternatives is a list of (type, score) tuples
        """
        try:
            # Use keyword-based classification
            # In a production system, this would use the actual LegalBERT model
            # for sequence classification. For now, we use keyword matching
            # as a practical implementation.
            
            keyword_scores = self._keyword_based_classification(text)
            
            if not keyword_scores or keyword_scores[0][1] == 0.0:
                # No matches found, classify as "Other"
                predicted_type = "Other"
                confidence = 0.5
                alternatives = [("Other", 0.5)]
            else:
                predicted_type = keyword_scores[0][0]
                # Scale confidence based on keyword match ratio
                raw_score = keyword_scores[0][1]
                confidence = min(0.95, 0.5 + (raw_score * 0.45))  # Scale to 0.5-0.95 range
                
                # Get top_k alternatives
                alternatives = [(t, min(0.95, 0.5 + (s * 0.45))) 
                               for t, s in keyword_scores[:top_k]]
            
            logger.info(f"Classified clause as '{predicted_type}' with confidence {confidence:.2f}")
            return predicted_type, confidence, alternatives
            
        except Exception as e:
            logger.error(f"Error in clause classification: {e}")
            # Return safe default
            return "Other", 0.5, [("Other", 0.5)]
    
    def get_embeddings(self, text: str) -> np.ndarray:
        """
        Generate embeddings for text using LegalBERT.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector as numpy array
        """
        try:
            # Tokenize
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                max_length=512,
                padding=True
            )
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Get embeddings
            with torch.no_grad():
                outputs = self.model(**inputs)
                # Use [CLS] token embedding (first token)
                embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()
            
            logger.debug(f"Generated embeddings with shape: {embeddings.shape}")
            return embeddings[0]
            
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            # Return zero vector as fallback
            return np.zeros(768)  # BERT base dimension
