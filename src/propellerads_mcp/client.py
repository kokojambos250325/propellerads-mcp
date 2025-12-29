"""PropellerAds API Client."""

import os
from datetime import datetime, timedelta
from typing import Any

import httpx
from pydantic import BaseModel


class PropellerAdsError(Exception):
    """PropellerAds API error."""
    pass


class CampaignFilter(BaseModel):
    """Filter for listing campaigns."""
    status: list[int] | None = None
    ad_format: str | None = None
    name: str | None = None


class StatisticsParams(BaseModel):
    """Parameters for statistics queries."""
    date_from: str | None = None
    date_to: str | None = None
    group_by: list[str] | None = None
    campaign_id: int | None = None
    zone_id: int | None = None


# Campaign status codes
STATUS_MAP = {
    1: "Draft",
    2: "Moderation",
    3: "Rejected",
    4: "Ready",
    6: "Working",  # Active/Running
    7: "Paused",
    8: "Stopped",  # Archived
    9: "Completed"
}


class PropellerAdsClient:
    """Client for PropellerAds SSP API v5."""

    BASE_URL = "https://ssp-api.propellerads.com/v5"

    def __init__(self, api_token: str | None = None):
        self.api_token = api_token or os.getenv("PROPELLERADS_API_TOKEN")
        if not self.api_token:
            raise PropellerAdsError(
                "API token required. Set PROPELLERADS_API_TOKEN environment variable "
                "or pass api_token parameter."
            )
        self.client = httpx.Client(
            base_url=self.BASE_URL,
            headers={
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            timeout=30.0,
        )

    def _request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make API request."""
        try:
            response = self.client.request(
                method=method,
                url=endpoint,
                params=params,
                json=json_data,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            error_detail = ""
            try:
                error_detail = e.response.json()
            except Exception:
                error_detail = e.response.text
            raise PropellerAdsError(
                f"API error {e.response.status_code}: {error_detail}"
            ) from e
        except httpx.RequestError as e:
            raise PropellerAdsError(f"Request failed: {str(e)}") from e

    def _extract_data(self, result: Any) -> Any:
        """Extract data from API response.
        
        PropellerAds API returns data in different formats:
        - {"result": [...]} for list endpoints
        - {"result": {...}} for single item endpoints
        - Direct value for simple endpoints (like balance)
        """
        if isinstance(result, dict):
            # Try "result" key first (PropellerAds standard)
            if "result" in result:
                return result["result"]
            # Fallback to "data" key (some endpoints might use it)
            if "data" in result:
                return result["data"]
        # Return as-is if not wrapped
        return result

    # ========== Campaign Methods ==========

    def list_campaigns(
        self,
        status: list[int] | None = None,
        is_archived: int | None = 0,
        limit: int = 20,
        formats: list[str] | None = None,
        page: int = 1,
        page_size: int = 100,
    ) -> list[dict[str, Any]]:
        """List campaigns with optional filters.
        
        Args:
            status: List of status codes (1=Draft, 2=Moderation, 3=Rejected, 
                    4=Ready, 6=Working, 7=Paused, 8=Stopped, 9=Completed)
            is_archived: 0=not archived, 1=archived, None=all
            limit: Maximum number of campaigns to return (applied after sorting)
            formats: List of ad formats to filter
            page: Page number for API pagination
            page_size: Page size for API pagination (max 100)
        """
        params = {
            "page": page,
            "page_size": min(page_size, 100)  # API max is 100
        }
        
        if status:
            for i, s in enumerate(status):
                params[f"status[{i}]"] = s
        
        if is_archived is not None:
            params["is_archived"] = is_archived
            
        if formats:
            for i, f in enumerate(formats):
                params[f"formats[{i}]"] = f

        result = self._request("GET", "/adv/campaigns", params=params)
        campaigns = self._extract_data(result)
        
        if not isinstance(campaigns, list):
            return []
        
        # Sort by ID descending (newest first)
        campaigns.sort(key=lambda x: x.get('id', 0), reverse=True)
        
        # Apply limit
        return campaigns[:limit]

    def get_campaign(self, campaign_id: int) -> dict[str, Any]:
        """Get campaign details by ID."""
        result = self._request("GET", f"/adv/campaigns/{campaign_id}")
        return self._extract_data(result)

    def create_campaign(self, campaign_data: dict[str, Any]) -> dict[str, Any]:
        """Create a new campaign."""
        result = self._request("POST", "/adv/campaigns", json_data=campaign_data)
        return self._extract_data(result)

    def update_campaign(
        self, campaign_id: int, updates: dict[str, Any]
    ) -> dict[str, Any]:
        """Update campaign settings."""
        result = self._request(
            "PUT", f"/adv/campaigns/{campaign_id}", json_data=updates
        )
        return self._extract_data(result)

    def start_campaigns(self, campaign_ids: list[int]) -> dict[str, Any]:
        """Start (activate) campaigns."""
        result = self._request(
            "POST", "/adv/campaigns/start", json_data={"ids": campaign_ids}
        )
        return result

    def stop_campaigns(self, campaign_ids: list[int]) -> dict[str, Any]:
        """Stop (pause) campaigns."""
        result = self._request(
            "POST", "/adv/campaigns/stop", json_data={"ids": campaign_ids}
        )
        return result

    def clone_campaign(
        self, campaign_id: int, new_name: str | None = None
    ) -> dict[str, Any]:
        """Clone an existing campaign."""
        data = {}
        if new_name:
            data["name"] = new_name
        result = self._request(
            "POST", f"/adv/campaigns/{campaign_id}/clone", json_data=data or None
        )
        return self._extract_data(result)

    # ========== Statistics Methods ==========

    def get_statistics(
        self,
        day_from: str | None = None,
        day_to: str | None = None,
        group_by: list[str] | None = None,
        campaign_id: int | None = None,
        zone_id: int | None = None,
        tz: str | None = None,
    ) -> list[dict[str, Any]]:
        """Get performance statistics.
        
        Args:
            day_from: Start date in YYYY-MM-DD format (EST timezone)
            day_to: End date in YYYY-MM-DD format (EST timezone)
            group_by: Fields to group by (campaign_id, zone_id, date_time, etc.)
            campaign_id: Filter by campaign ID
            zone_id: Filter by zone ID  
            tz: UTC offset (e.g., '+0300', '-0500') - optional
        """
        # Default to last 7 days
        if not day_from:
            day_from = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        if not day_to:
            day_to = datetime.now().strftime("%Y-%m-%d")

        params: dict[str, Any] = {
            "day_from": day_from,
            "day_to": day_to,
        }

        if group_by:
            for i, gb in enumerate(group_by):
                params[f"group_by[{i}]"] = gb

        if campaign_id:
            params[f"campaign_id[0]"] = campaign_id
        if zone_id:
            params[f"zone_id[0]"] = zone_id
        if tz:
            params["tz"] = tz

        result = self._request("GET", "/adv/statistics", params=params)
        data = self._extract_data(result)
        return data if isinstance(data, list) else []

    def get_campaign_statistics(
        self,
        campaign_id: int,
        day_from: str | None = None,
        day_to: str | None = None,
    ) -> dict[str, Any]:
        """Get statistics for a specific campaign."""
        stats = self.get_statistics(
            day_from=day_from,
            day_to=day_to,
            campaign_id=campaign_id,
        )
        return stats[0] if stats else {}

    def get_zone_statistics(
        self,
        campaign_id: int | None = None,
        day_from: str | None = None,
        day_to: str | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """Get statistics grouped by zone."""
        stats = self.get_statistics(
            day_from=day_from,
            day_to=day_to,
            group_by=["zone_id"],
            campaign_id=campaign_id,
        )
        return stats[:limit] if isinstance(stats, list) else []

    def get_creative_statistics(
        self,
        campaign_id: int | None = None,
        day_from: str | None = None,
        day_to: str | None = None,
    ) -> list[dict[str, Any]]:
        """Get statistics grouped by creative."""
        return self.get_statistics(
            day_from=day_from,
            day_to=day_to,
            group_by=["creative_id"],
            campaign_id=campaign_id,
        )

    # ========== Creative Methods ==========

    def list_creatives(
        self, campaign_id: int | None = None
    ) -> list[dict[str, Any]]:
        """List creatives, optionally filtered by campaign."""
        params = {}
        if campaign_id:
            params["campaign_id"] = campaign_id

        result = self._request("GET", "/adv/creatives", params=params or None)
        data = self._extract_data(result)
        return data if isinstance(data, list) else []

    def get_creative(self, creative_id: int) -> dict[str, Any]:
        """Get creative details."""
        result = self._request("GET", f"/adv/creatives/{creative_id}")
        return self._extract_data(result)

    def create_creative(self, creative_data: dict[str, Any]) -> dict[str, Any]:
        """Create a new creative."""
        result = self._request("POST", "/adv/creatives", json_data=creative_data)
        return self._extract_data(result)

    def update_creative(
        self, creative_id: int, updates: dict[str, Any]
    ) -> dict[str, Any]:
        """Update creative."""
        result = self._request(
            "PUT", f"/adv/creatives/{creative_id}", json_data=updates
        )
        return self._extract_data(result)

    # ========== Targeting Methods ==========

    def get_zones(self, campaign_id: int | None = None) -> list[dict[str, Any]]:
        """Get zones, optionally for a specific campaign."""
        params = {}
        if campaign_id:
            params["campaign_id"] = campaign_id

        result = self._request("GET", "/adv/zones", params=params or None)
        data = self._extract_data(result)
        return data if isinstance(data, list) else []

    def add_zones_to_whitelist(
        self, campaign_id: int, zone_ids: list[int]
    ) -> dict[str, Any]:
        """Add zones to campaign whitelist."""
        return self._request(
            "POST",
            f"/adv/campaigns/{campaign_id}/targeting/zones/whitelist",
            json_data={"zone_ids": zone_ids},
        )

    def add_zones_to_blacklist(
        self, campaign_id: int, zone_ids: list[int]
    ) -> dict[str, Any]:
        """Add zones to campaign blacklist."""
        return self._request(
            "POST",
            f"/adv/campaigns/{campaign_id}/targeting/zones/blacklist",
            json_data={"zone_ids": zone_ids},
        )

    def remove_zones_from_whitelist(
        self, campaign_id: int, zone_ids: list[int]
    ) -> dict[str, Any]:
        """Remove zones from campaign whitelist."""
        return self._request(
            "DELETE",
            f"/adv/campaigns/{campaign_id}/targeting/zones/whitelist",
            json_data={"zone_ids": zone_ids},
        )

    def remove_zones_from_blacklist(
        self, campaign_id: int, zone_ids: list[int]
    ) -> dict[str, Any]:
        """Remove zones from campaign blacklist."""
        return self._request(
            "DELETE",
            f"/adv/campaigns/{campaign_id}/targeting/zones/blacklist",
            json_data={"zone_ids": zone_ids},
        )

    # ========== Account Methods ==========

    def get_balance(self) -> dict[str, Any]:
        """Get account balance."""
        result = self._request("GET", "/adv/balance")
        # Balance returns just a string value
        return result

    def get_countries(self) -> list[dict[str, Any]]:
        """Get available countries for targeting."""
        result = self._request("GET", "/adv/countries")
        data = self._extract_data(result)
        return data if isinstance(data, list) else []

    def get_ad_formats(self) -> list[dict[str, Any]]:
        """Get available ad formats."""
        result = self._request("GET", "/adv/ad-formats")
        data = self._extract_data(result)
        return data if isinstance(data, list) else []

    def close(self):
        """Close the HTTP client."""
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
