import configparser
import logging
from trading_classes import TradingOpportunities, AlpacaTrader
from slack_app_notification import DiscordNotifier

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_config():
    """Load configuration from creds.cfg"""
    try:
        config = configparser.ConfigParser()
        config.read('creds.cfg')
        
        return {
            'alpaca_api_key': config['ALPACA']['API_KEY'],
            'alpaca_secret_key': config['ALPACA']['SECRET_KEY'],
            'discord_webhook_url': config['DISCORD']['WEBHOOK_URL']
        }
    except Exception as e:
        logger.error(f"Error loading configuration: {str(e)}")
        return None

def main():
    """Main function to run the trading bot"""
    try:
        # Load configuration
        config = load_config()
        if not config:
            raise Exception("Failed to load configuration")
        
        # Initialize components
        trading_opps = TradingOpportunities()
        trader = AlpacaTrader(
            api_key=config['alpaca_api_key'],
            secret_key=config['alpaca_secret_key'],
            paper=True  # Use paper trading for safety
        )
        notifier = DiscordNotifier(
            webhook_url=config['discord_webhook_url']
        )
        
        # Get trading opportunities
        symbols = trading_opps.get_trading_opportunities()
        opportunities = []
        
        for symbol in symbols:
            asset_info = trading_opps.get_asset_info(symbol)
            if asset_info:
                opportunities.append(asset_info)
        
        # Get current positions
        portfolio = trader.get_portfolio()
        if not portfolio:
            raise Exception("Failed to get portfolio information")
        
        # Execute sell orders if needed
        trader.sell_orders(portfolio['positions'])
        
        # Execute buy orders for oversold assets
        trader.buy_orders(opportunities)
        
        # Send trade summary to Discord
        trades = []  # In a real implementation, you would track actual trades
        notifier.send_trade_summary(trades)
        
        logger.info("Trading bot execution completed successfully")
        
    except Exception as e:
        error_message = f"Error in trading bot execution: {str(e)}"
        logger.error(error_message)
        if 'notifier' in locals():
            notifier.send_error_notification(error_message)

if __name__ == "__main__":
    main() 