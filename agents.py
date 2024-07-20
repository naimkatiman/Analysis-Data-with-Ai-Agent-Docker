# agents.py

import os
import csv
import anthropic
from prompts import *
from datetime import datetime, timedelta
import random
import sys

# Set up the Anthropic API key
if not os.getenv("ANTHROPIC_API_KEY"):
    os.environ["ANTHROPIC_API_KEY"] = input("Please enter your Anthropic API key: ")

# Create the Anthropic client
client = anthropic.Anthropic()
sonnet = "claude-3-sonnet-20240720"

def read_csv(file_path):
    data = []
    with open(file_path, "r", newline="") as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            data.append(row)
    return data

def save_to_csv(data, output_file, headers=None):
    mode = 'w' if headers else 'a'
    with open(output_file, mode, newline="") as f:
        writer = csv.writer(f)
        if headers:
            writer.writerow(headers)
        for row in csv.reader(data.splitlines()):
            writer.writerow(row)

def analyzer_agent(sample_data):
    message = client.messages.create(
        model=sonnet,
        max_tokens=800,
        temperature=0.2,
        system=ANALYZER_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": ANALYZER_USER_PROMPT.format(sample_data=sample_data)
            }
        ]
    )
    return message.content[0].text

def generator_agent(analysis_result, sample_data, num_rows=30):
    message = client.messages.create(
        model=sonnet,
        max_tokens=2000,
        temperature=0.7,
        system=GENERATOR_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": GENERATOR_USER_PROMPT.format(
                    num_rows=num_rows,
                    analysis_result=analysis_result,
                    sample_data=sample_data
                )
            }
        ]
    )
    return message.content[0].text

def trend_analyzer_agent(generated_data):
    message = client.messages.create(
        model=sonnet,
        max_tokens=1000,
        temperature=0.3,
        system=TREND_ANALYZER_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": TREND_ANALYZER_USER_PROMPT.format(generated_data=generated_data)
            }
        ]
    )
    return message.content[0].text

def generate_time_series(start_date, num_days):
    return [start_date + timedelta(days=i) for i in range(num_days)]


def main():
    file_path = input("\nEnter the name of your CSV file: ")
    file_path = os.path.join('/app/data', file_path)
    
    try:
        desired_rows = int(input("Enter the number of rows you want in the new dataset: "))
        if desired_rows <= 0:
            raise ValueError("Number of rows must be positive")
    except ValueError as e:
        print(f"Invalid input: {e}")
        sys.exit(1)

    try:
        sample_data = read_csv(file_path)
        sample_data_str = "\n".join([",".join(row) for row in sample_data])
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        sys.exit(1)

    print("\nLaunching Cryptocurrency Analysis AI Agent...")
    try:
        analysis_result = analyzer_agent(sample_data_str)
        print("\n#### Analyzer Agent output: ####\n")
        print(analysis_result)
    except Exception as e:
        print(f"Error during analysis: {e}")
        sys.exit(1)

    print("\n------------------------------------------\n\nGenerating new data...")

    output_file = "/app/data/crypto_analysis_dataset.csv"
    headers = sample_data[0] + ["Date", "Trading Volume", "Market Cap"]
    save_to_csv("", output_file, headers)

    batch_size = 30
    generated_rows = 0
    all_generated_data = []

    start_date = datetime.now().date()
    time_series = generate_time_series(start_date, desired_rows)

    while generated_rows < desired_rows:
        rows_to_generate = min(batch_size, desired_rows - generated_rows)
        try:
            generated_data = generator_agent(analysis_result, sample_data_str, rows_to_generate)
            
            # Add time series data and additional metrics
            enhanced_data = []
            for row, date in zip(csv.reader(generated_data.splitlines()), time_series[generated_rows:]):
                try:
                    current_price = float(row[2])  # Assuming the price is always in the third column
                    trading_volume = round(random.uniform(1000000, 1000000000), 2)
                    market_cap = round(current_price * trading_volume * random.uniform(0.5, 2), 2)
                    enhanced_row = row + [date.strftime("%Y-%m-%d"), f"{trading_volume:.2f}", f"{market_cap:.2f}"]
                    enhanced_data.append(",".join(map(str, enhanced_row)))
                except (ValueError, IndexError) as e:
                    print(f"Error processing row: {row}. Error: {e}")
                    continue
            
            enhanced_data_str = "\n".join(enhanced_data)
            save_to_csv(enhanced_data_str, output_file)
            all_generated_data.extend(enhanced_data)
            
            generated_rows += len(enhanced_data)
            print(f"Generated {generated_rows} rows out of {desired_rows}")
        except Exception as e:
            print(f"Error generating data: {e}")
            continue

    print(f"\nGenerated data has been saved to {output_file}")

    print("\nAnalyzing trends in the generated data...")
    try:
        trend_analysis = trend_analyzer_agent("\n".join(all_generated_data))
        print("\n#### Trend Analysis: ####\n")
        print(trend_analysis)

        with open("/app/data/trend_analysis_report.txt", "w") as report_file:
            report_file.write(trend_analysis)
        print("\nTrend analysis report has been saved to /app/data/trend_analysis_report.txt")
    except Exception as e:
        print(f"Error during trend analysis: {e}")

if __name__ == "__main__":
    main()