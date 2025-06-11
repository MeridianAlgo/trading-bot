# Automated Trading Bot

This trading bot automatically identifies and executes trades based on technical indicators, using Alpaca for trading execution and Slack for notifications. The bot is designed for educational purposes and includes risk management features.

## Features

- Identifies trading opportunities using technical indicators (RSI, Bollinger Bands)
- Executes trades through Alpaca's API
- Sends real-time notifications to Slack
- Automated scheduling with CircleCI
- Risk management features (position sizing, cash management)

## Prerequisites

- Python 3.9 or higher
- Alpaca trading account (paper trading recommended)
- Slack workspace with bot token
- CircleCI account (for automated scheduling)

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd trading-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure credentials:
   - Copy `creds.cfg` and fill in your API keys:
     - Alpaca API key and secret
     - Slack bot token
     - Slack channel name

4. Set up CircleCI:
   - Connect your GitHub repository to CircleCI
   - The bot will run automatically every 4 hours

## Usage

Run the bot manually:
```bash
python main.py
```

The bot will:
1. Identify trading opportunities
2. Execute sell orders if needed
3. Execute buy orders for oversold assets
4. Send trade summaries to Slack

## Risk Management

- The bot uses paper trading by default
- Position sizing is limited to 5% of available cash per trade
- Maintains at least 10% cash in the portfolio
- Sells top 25% performing assets if cash falls below 10%

## Disclaimer

This trading bot is for educational purposes only. Trading involves significant risks, and past performance is not indicative of future results. Always consult with a licensed financial advisor before making investment decisions.

## License

MIT License 