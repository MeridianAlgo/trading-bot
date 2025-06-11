import requests
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DiscordNotifier:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url
        
    def send_trade_summary(self, trades):
        """Send a summary of trades to Discord"""
        try:
            if not trades:
                return
                
            # Create message content
            message = f"**Trading Summary - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**\n\n"
            
            # Add trade details
            for trade in trades:
                message += (
                    f"**Symbol:** {trade['symbol']}\n"
                    f"**Action:** {trade['side']}\n"
                    f"**Quantity:** {trade['qty']}\n"
                    f"**Price:** ${trade['price']:.2f}\n"
                    "-------------------\n"
                )
            
            # Send message
            payload = {"content": message}
            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()
            
            logger.info("Successfully sent trade summary to Discord")
            
        except Exception as e:
            logger.error(f"Error sending trade summary to Discord: {str(e)}")
    
    def send_error_notification(self, error_message):
        """Send error notifications to Discord"""
        try:
            message = (
                "🚨 **Trading Bot Error**\n\n"
                f"**Error Message:**\n{error_message}\n\n"
                f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            
            payload = {"content": message}
            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()
            
            logger.info("Successfully sent error notification to Discord")
            
        except Exception as e:
            logger.error(f"Error sending error notification to Discord: {str(e)}") 