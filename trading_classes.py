import yfinance as yf
import pandas as pd
import numpy as np
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TradingOpportunities:
    def __init__(self):
        self.stocks = []
        self.crypto = []
        
    def get_trading_opportunities(self):
        """Fetch top losing stocks and popular cryptocurrencies from Yahoo Finance"""
        try:
            # Get top losing stocks
            losers_url = "https://finance.yahoo.com/losers"
            # In a real implementation, we would use web scraping here
            # For now, we'll use a sample list of stocks
            self.stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']
            
            # Get popular cryptocurrencies
            crypto_url = "https://finance.yahoo.com/cryptocurrencies"
            # Similarly, we would scrape this in production
            self.crypto = ['BTC-USD', 'ETH-USD', 'SOL-USD', 'DOGE-USD']
            
            return self.stocks + self.crypto
            
        except Exception as e:
            logger.error(f"Error fetching trading opportunities: {str(e)}")
            return []
    
    def get_asset_info(self, symbol):
        """Get technical indicators for an asset"""
        try:
            # Get historical data
            asset = yf.Ticker(symbol)
            hist = asset.history(period="200d")
            
            if hist.empty:
                return None
            
            # Calculate Bollinger Bands
            hist['SMA20'] = hist['Close'].rolling(window=20).mean()
            hist['STD20'] = hist['Close'].rolling(window=20).std()
            hist['UpperBand'] = hist['SMA20'] + (hist['STD20'] * 2)
            hist['LowerBand'] = hist['SMA20'] - (hist['STD20'] * 2)
            
            # Calculate RSI
            delta = hist['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            hist['RSI'] = 100 - (100 / (1 + rs))
            
            # Get latest values
            latest = hist.iloc[-1]
            
            return {
                'symbol': symbol,
                'price': latest['Close'],
                'bb_lower': latest['LowerBand'],
                'bb_upper': latest['UpperBand'],
                'rsi': latest['RSI']
            }
            
        except Exception as e:
            logger.error(f"Error getting asset info for {symbol}: {str(e)}")
            return None

class AlpacaTrader:
    def __init__(self, api_key, secret_key, paper=True):
        self.client = TradingClient(api_key, secret_key, paper=paper)
        
    def get_portfolio(self):
        """Get current portfolio information"""
        try:
            account = self.client.get_account()
            positions = self.client.get_all_positions()
            
            return {
                'cash': float(account.cash),
                'portfolio_value': float(account.portfolio_value),
                'positions': positions
            }
        except Exception as e:
            logger.error(f"Error getting portfolio: {str(e)}")
            return None
    
    def sell_orders(self, positions):
        """Execute sell orders based on overbought conditions"""
        try:
            portfolio = self.get_portfolio()
            if not portfolio:
                return
            
            # Check if cash is less than 10% of portfolio
            if portfolio['cash'] < (portfolio['portfolio_value'] * 0.1):
                # Sell top 25% performing assets
                positions.sort(key=lambda x: float(x.unrealized_plpc), reverse=True)
                positions_to_sell = positions[:len(positions)//4]
                
                for position in positions_to_sell:
                    order = MarketOrderRequest(
                        symbol=position.symbol,
                        qty=float(position.qty),
                        side=OrderSide.SELL,
                        time_in_force=TimeInForce.DAY
                    )
                    self.client.submit_order(order)
                    logger.info(f"Sold {position.qty} shares of {position.symbol}")
                    
        except Exception as e:
            logger.error(f"Error executing sell orders: {str(e)}")
    
    def buy_orders(self, opportunities):
        """Execute buy orders for oversold assets"""
        try:
            portfolio = self.get_portfolio()
            if not portfolio:
                return
            
            buying_power = portfolio['cash']
            
            for opp in opportunities:
                if opp['rsi'] <= 30:  # Oversold condition
                    # Calculate position size (example: 5% of buying power)
                    position_size = buying_power * 0.05
                    qty = position_size / opp['price']
                    
                    if qty > 0:
                        order = MarketOrderRequest(
                            symbol=opp['symbol'],
                            qty=qty,
                            side=OrderSide.BUY,
                            time_in_force=TimeInForce.DAY
                        )
                        self.client.submit_order(order)
                        logger.info(f"Bought {qty} shares of {opp['symbol']}")
                        
        except Exception as e:
            logger.error(f"Error executing buy orders: {str(e)}") 