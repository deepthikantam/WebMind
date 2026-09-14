import os
import logging
from typing import Any, Dict, List, Optional
from anakin import (
    Anakin,
    AnakinError,
    AuthenticationError,
    InsufficientCreditsError,
    InvalidRequestError,
    JobFailedError,
    JobTimeoutError,
    RateLimitError,
    SearchResult,
    AgenticSearchResult,
    Document
)
from config import get_anakin_key

logger = logging.getLogger("WebMind.AnakinService")

class AnakinService:
    """
    Wrapper around the official Anakin Python SDK (anakin-sdk).
    Provides access to Search, Agentic Search, URL Scraper, and Wire.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or get_anakin_key()
        self.client: Optional[Anakin] = None
        if self.api_key:
            try:
                self.client = Anakin(api_key=self.api_key, timeout=90.0, max_retries=3)
            except Exception as e:
                logger.error(f"Failed to initialize Anakin client: {e}")
                self.client = None

    def is_available(self) -> bool:
        """Returns True if the Anakin client is configured with an API key."""
        return self.client is not None and bool(self.api_key)

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Execute live web search using Anakin Search API.
        Returns a list of items with url, title, snippet, and last updated.
        """
        if not self.client:
            raise AuthenticationError("Anakin API key is missing. Please configure ANAKIN_API_KEY in .env or sidebar.")

        try:
            logger.info(f"Executing Anakin Search for query: {query}")
            search_result: SearchResult = self.client.search(prompt=query, limit=limit)
            
            items = []
            for r in getattr(search_result, "results", []):
                items.append({
                    "url": getattr(r, "url", ""),
                    "title": getattr(r, "title", ""),
                    "snippet": getattr(r, "snippet", ""),
                    "date": getattr(r, "date", ""),
                    "last_updated": getattr(r, "last_updated", "")
                })
            return items
        except AuthenticationError:
            raise AuthenticationError("Invalid Anakin API key. Please check your credentials.")
        except InsufficientCreditsError as e:
            raise InsufficientCreditsError(f"Insufficient Anakin credits: {e}")
        except RateLimitError as e:
            raise RateLimitError(f"Anakin rate limit reached: {e}")
        except Exception as e:
            logger.error(f"Error during Anakin search: {e}")
            raise AnakinError(f"Anakin search failed: {str(e)}")

    def agentic_search(self, prompt: str, schema: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute multi-stage research pipeline using Anakin Agentic Search.
        Refines query, scrapes target sources, and synthesizes structured findings.
        """
        if not self.client:
            raise AuthenticationError("Anakin API key is missing. Please configure ANAKIN_API_KEY.")

        try:
            logger.info(f"Executing Anakin Agentic Search for prompt: {prompt}")
            res: AgenticSearchResult = self.client.agentic_search(
                prompt=prompt,
                schema=schema,
                poll_timeout=120.0
            )

            gen_json = getattr(res, "generated_json", None)
            summary = ""
            structured_data = None
            if gen_json:
                summary = getattr(gen_json, "summary", "") or ""
                structured_data = getattr(gen_json, "structured_data", None)

            return {
                "id": getattr(res, "id", ""),
                "status": str(getattr(res, "status", "")),
                "summary": summary,
                "structured_data": structured_data,
                "duration_ms": getattr(res, "duration_ms", 0),
                "error": getattr(res, "error", None)
            }
        except Exception as e:
            logger.error(f"Error during Anakin Agentic Search: {e}")
            raise AnakinError(f"Anakin agentic search failed: {str(e)}")

    def scrape(self, url: str) -> Dict[str, Any]:
        """
        Scrape a single target webpage and return clean markdown content.
        Uses Anakin URL Scraper.
        """
        if not self.client:
            raise AuthenticationError("Anakin API key is missing. Please configure ANAKIN_API_KEY.")

        try:
            logger.info(f"Scraping URL via Anakin URL Scraper: {url}")
            doc: Document = self.client.scrape(
                url=url,
                formats=["markdown"],
                use_browser=False
            )
            return {
                "id": getattr(doc, "id", ""),
                "url": getattr(doc, "url", url),
                "markdown": getattr(doc, "markdown", "") or "",
                "summary": getattr(doc, "summary", ""),
                "status": str(getattr(doc, "status", "")),
                "links": getattr(doc, "links", []) or [],
                "error": getattr(doc, "error", None)
            }
        except Exception as e:
            logger.error(f"Error during Anakin scrape of {url}: {e}")
            raise AnakinError(f"Anakin scrape failed for {url}: {str(e)}")
