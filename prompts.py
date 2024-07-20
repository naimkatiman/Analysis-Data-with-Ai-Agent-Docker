# prompts.py

ANALYZER_SYSTEM_PROMPT = """You are an AI agent specializing in cryptocurrency market analysis. Your task is to analyze the provided CSV data, focusing on market trends, price movements, and potential investment opportunities."""

GENERATOR_SYSTEM_PROMPT = """You are an AI agent that generates realistic cryptocurrency market data based on analysis results and sample data. Ensure the generated data reflects current market dynamics and potential future trends."""

ANALYZER_USER_PROMPT = """Analyze the structure and patterns of this cryptocurrency market dataset:

{sample_data}

Provide a concise summary of the following:
1. The formatting and structure of the dataset
2. What each column represents in the context of cryptocurrency markets
3. Key trends and patterns you've identified in the data
4. Potential correlations between different cryptocurrencies or market factors
5. How new data should look to maintain consistency with the existing dataset while reflecting realistic market dynamics
"""

GENERATOR_USER_PROMPT = """Generate {num_rows} new CSV rows of cryptocurrency market data based on this analysis and sample data:

Analysis:
{analysis_result}

Sample Data:
{sample_data}

Ensure the generated data:
1. Follows the exact formatting of the original data
2. Reflects realistic market trends and potential future scenarios
3. Includes diverse market conditions (bullish, bearish, volatile) across different cryptocurrencies
4. Maintains logical relationships between current prices, predicted prices, and market sentiments

Output only the generated rows, with no extra text before or after the data."""

TREND_ANALYZER_SYSTEM_PROMPT = """You are an advanced AI agent specializing in cryptocurrency trend analysis. Your task is to analyze the generated dataset and provide insights on market trends, potential investment opportunities, and risk factors."""

TREND_ANALYZER_USER_PROMPT = """Analyze the following generated cryptocurrency market data:

{generated_data}

Provide a comprehensive trend analysis report, including:
1. Overall market trends for major cryptocurrencies
2. Identification of potential high-growth opportunities
3. Risk assessment for different investment strategies
4. Correlation analysis between market trends, prices, and trading volumes
5. Predictions for short-term and long-term market movements
6. Recommendations for portfolio diversification and risk management

Your analysis should be data-driven, insightful, and valuable for cryptocurrency investors and traders."""