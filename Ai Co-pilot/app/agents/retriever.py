"""Retriever Agent.

Enhanced semantic search with domain and temporal filtering. Returns top-K 
candidate chunks for the Context Optimizer to refine.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import List, Optional, Dict

from .. import config, vectorstore


def retrieve(
    query: str, 
    domain_filter: Optional[str] = None, 
    temporal_filter: Optional[Dict] = None,
    top_k: Optional[int] = None
) -> List[dict]:
    """
    Retrieve documents with optional domain and temporal filters.
    
    Args:
        query: The search query
        domain_filter: Filter by domain (Research, Personal, Work, etc.)
        temporal_filter: Dict with temporal constraints
            Examples:
            {"type": "last_week", "days_ago": 7}
            {"type": "specific_month", "year": 2026, "month": 1}
        top_k: Number of results to return
    """
    top_k = top_k or config.RETRIEVE_TOP_K
    
    # Build where clause
    where = {}
    where_conditions = []
    
    # Domain filter
    if domain_filter:
        where["domain"] = domain_filter
    
    # Temporal filter
    if temporal_filter:
        filter_type = temporal_filter.get("type")
        
        if filter_type in ["last_week", "last_month", "last_year"]:
            days_ago = temporal_filter.get("days_ago", 30)
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_ago)
            # Note: ChromaDB where clause for dates requires careful handling
            # We'll filter after retrieval for more reliable results
            
        elif filter_type == "specific_month":
            year = temporal_filter.get("year")
            month = temporal_filter.get("month")
            if year and month:
                where["year"] = year
                where["month"] = month
    
    # Query with filters
    where_clause = where if where else None
    hits = vectorstore.query_documents(query, top_k=top_k * 2, where=where_clause)
    
    # Post-filter by date if needed (more reliable than ChromaDB where clause for date ranges)
    if temporal_filter and temporal_filter.get("days_ago"):
        days_ago = temporal_filter["days_ago"]
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_ago)
        filtered_hits = []
        for hit in hits:
            modified_str = hit.get("metadata", {}).get("modified_date")
            if modified_str:
                try:
                    modified_date = datetime.fromisoformat(modified_str)
                    if modified_date >= cutoff_date:
                        filtered_hits.append(hit)
                except Exception:
                    # If date parsing fails, include the document
                    filtered_hits.append(hit)
            else:
                # If no date, include it
                filtered_hits.append(hit)
        hits = filtered_hits[:top_k]
    else:
        hits = hits[:top_k]
    
    # If filters returned nothing, retry without filters
    if not hits and (where_clause or temporal_filter):
        hits = vectorstore.query_documents(query, top_k=top_k)
    
    return hits
