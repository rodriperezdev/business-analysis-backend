"""
Service for currency conversion and exchange rate management.
"""

import httpx
from typing import Dict, Optional
from datetime import datetime, timedelta
from app.utils.logging import get_logger

logger = get_logger(__name__)


# Market to Currency mapping
MARKET_CURRENCIES: Dict[str, str] = {
    "usa": "USD",
    "argentina": "ARS",
    "brazil": "BRL",
    "mexico": "MXN",
    "colombia": "COP",
    "chile": "CLP",
    "other": "USD",  # Default to USD for other markets
}

# Fallback exchange rates (updated periodically, but API is preferred)
FALLBACK_RATES: Dict[str, float] = {
    "USD": 1.0,
    "ARS": 1050.0,  # Highly volatile - use API!
    "BRL": 5.8,
    "MXN": 17.0,
    "COP": 4100.0,
    "CLP": 980.0,
}


class CurrencyService:
    """Service for currency conversion using live exchange rates."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize currency service.
        
        Args:
            api_key: Exchange rate API key (optional, uses free tier if not provided)
        """
        self.api_key = api_key
        self.base_url = "https://api.exchangerate-api.com/v4/latest"
        self.cache: Dict[str, Dict] = {}
        self.cache_duration = timedelta(hours=1)  # Cache rates for 1 hour
    
    def get_currency_from_market(self, market: str) -> str:
        """
        Get currency code from market.
        
        Args:
            market: Market identifier (usa, argentina, brazil, etc.)
            
        Returns:
            Currency code (USD, ARS, BRL, etc.)
        """
        return MARKET_CURRENCIES.get(market.lower(), "USD")
    
    async def get_exchange_rate(
        self,
        from_currency: str,
        to_currency: str = "USD"
    ) -> float:
        """
        Get exchange rate from one currency to another.
        
        Args:
            from_currency: Source currency code
            to_currency: Target currency code (default: USD)
            
        Returns:
            Exchange rate (amount in to_currency per 1 from_currency)
        """
        if from_currency == to_currency:
            return 1.0
        
        # Check cache first
        cache_key = f"{from_currency}_{to_currency}"
        if cache_key in self.cache:
            cached_data = self.cache[cache_key]
            if datetime.now() - cached_data["timestamp"] < self.cache_duration:
                logger.debug(f"Using cached rate for {cache_key}: {cached_data['rate']}")
                return cached_data["rate"]
        
        try:
            # Use exchangerate-api.com (free tier, no API key needed)
            async with httpx.AsyncClient(timeout=5.0) as client:
                url = f"{self.base_url}/{from_currency}"
                response = await client.get(url)
                response.raise_for_status()
                data = response.json()
                
                rate = data["rates"].get(to_currency)
                if rate is None:
                    logger.warning(f"Rate not found for {to_currency}, using fallback")
                    return self._get_fallback_rate(from_currency, to_currency)
                
                # Cache the rate
                self.cache[cache_key] = {
                    "rate": rate,
                    "timestamp": datetime.now()
                }
                
                logger.info(f"Fetched exchange rate {from_currency}->{to_currency}: {rate}")
                return rate
                
        except Exception as e:
            logger.warning(f"Failed to fetch exchange rate: {e}. Using fallback rate.")
            return self._get_fallback_rate(from_currency, to_currency)
    
    def _get_fallback_rate(self, from_currency: str, to_currency: str) -> float:
        """Get fallback exchange rate."""
        if from_currency == to_currency:
            return 1.0
        
        from_rate = FALLBACK_RATES.get(from_currency, 1.0)
        to_rate = FALLBACK_RATES.get(to_currency, 1.0)
        
        # Convert via USD
        if from_currency != "USD":
            usd_amount = 1.0 / from_rate
        else:
            usd_amount = 1.0
        
        if to_currency != "USD":
            return usd_amount * to_rate
        else:
            return usd_amount
    
    def convert_to_usd(self, amount: float, from_currency: str) -> float:
        """
        Convert amount to USD synchronously (uses fallback rate).
        
        For async conversion with live rates, use convert_to_usd_async.
        
        Args:
            amount: Amount in source currency
            from_currency: Source currency code
            
        Returns:
            Amount in USD
        """
        if from_currency == "USD":
            return amount
        
        rate = FALLBACK_RATES.get(from_currency, 1.0)
        return amount / rate
    
    async def convert_to_usd_async(self, amount: float, from_currency: str) -> float:
        """
        Convert amount to USD using live exchange rates.
        
        Args:
            amount: Amount in source currency
            from_currency: Source currency code
            
        Returns:
            Amount in USD
        """
        if from_currency == "USD":
            return amount
        
        rate = await self.get_exchange_rate(from_currency, "USD")
        # Rate is "USD per 1 from_currency", so multiply to convert
        return amount * rate
    
    def convert_from_usd(self, amount: float, to_currency: str) -> float:
        """
        Convert amount from USD to target currency synchronously.
        
        Args:
            amount: Amount in USD
            to_currency: Target currency code
            
        Returns:
            Amount in target currency
        """
        if to_currency == "USD":
            return amount
        
        rate = FALLBACK_RATES.get(to_currency, 1.0)
        return amount * rate
    
    async def convert_from_usd_async(self, amount: float, to_currency: str) -> float:
        """
        Convert amount from USD to target currency using live rates.
        
        Args:
            amount: Amount in USD
            to_currency: Target currency code
            
        Returns:
            Amount in target currency
        """
        if to_currency == "USD":
            return amount
        
        rate = await self.get_exchange_rate("USD", to_currency)
        return amount * rate


# Global currency service instance
currency_service = CurrencyService()

