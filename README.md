# Twittus_Extractorium - Twitter/X Web Scraper 
<mark>Center for Aritficial Intelligence Research (CAIR) Nepal</mark>

A robust, ethical web scraping tool for collecting public Twitter/X data for academic research and data analysis purposes. Built with Playwright for reliable browser automation and designed with responsible scraping practices.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Basic Usage](#basic-usage)
  - [Profile Scraping](#profile-scraping)
  - [Search Query Scraping](#search-query-scraping)
  - [Batch Scraping](#batch-scraping)
- [Configuration](#configuration)
- [Data Schema](#data-schema)
- [Ethical Guidelines](#ethical-guidelines)
- [Troubleshooting](#troubleshooting)
- [Limitations](#limitations)
- [Contributing](#contributing)
- [License](#license)
- [Disclaimer](#disclaimer)

## Overview

This Twitter/X web scraper enables researchers and data analysts to collect publicly available tweets without relying on official APIs. The tool employs browser automation via Playwright, implementing human-like behavior patterns to ensure responsible data collection.

### Key Capabilities

- Scrape tweets from public user profiles
- Collect tweets based on search queries
- Extract comprehensive tweet metadata (engagement metrics, timestamps, author information)
- Automatic deduplication and SQLite database storage
- Rate limiting and human-like delays to respect platform resources
- Single-login session for efficient batch operations

## Features

### Core Functionality

- **Multi-Source Scraping**: Collect data from user profiles and search results
- **Intelligent Scrolling**: Dynamic page scrolling with content detection
- **Comprehensive Data Extraction**:
  - Tweet text content
  - Author username and display name
  - Engagement metrics (likes, retweets, replies)
  - Timestamps and tweet URLs
  - Source tracking (profile/search)
  
### Technical Features

- **Automated Deduplication**: Prevents duplicate entries in database
- **Robust Error Handling**: Comprehensive logging and exception management
- **Human-Like Behavior**: Randomized delays and gradual scrolling
- **Session Persistence**: Single login for multiple scraping tasks
- **SQLite Integration**: Efficient local data storage with indexing

## Requirements

### System Requirements

- Python 3.8 or higher
- 4GB RAM minimum (8GB recommended)
- Stable internet connection
- Operating System: Windows, macOS, or Linux

### Python Dependencies

```
playwright>=1.40.0
sqlite3 (included in Python standard library)
```

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/twitter-scraper.git
cd twitter-scraper
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install playwright
```

### Step 4: Install Playwright Browsers

```bash
playwright install chromium
```

## Usage

### Basic Usage

```python
from twitter_scraper_fixed import TwitterScraper

# Initialize scraper
scraper = TwitterScraper(
    db_path="twitter_data.db",
    headless=False  # Set to False for manual login
)

# Define scraping tasks
tasks = [
    {
        'type': 'search',
        'target': 'artificial intelligence',
        'max_scrolls': 10
    }
]

# Execute scraping
scraper.scrape_with_single_login(tasks)
```

### Profile Scraping

Collect tweets from a specific user's profile:

```python
tasks = [
    {
        'type': 'profile',
        'target': 'username',  # Without @ symbol
        'max_scrolls': 15
    }
]

scraper.scrape_with_single_login(tasks)
```

**Parameters:**
- `type`: Must be `'profile'`
- `target`: Twitter username (without @ symbol)
- `max_scrolls`: Number of scroll iterations (each loads ~10-20 tweets)

### Search Query Scraping

Collect tweets matching specific search criteria:

```python
tasks = [
    {
        'type': 'search',
        'target': 'climate change',
        'max_scrolls': 20
    }
]

scraper.scrape_with_single_login(tasks)
```

**Advanced Search Operators:**

```python
# Language-specific search
{'type': 'search', 'target': 'python lang:en', 'max_scrolls': 10}

# Hashtag search
{'type': 'search', 'target': '#MachineLearning', 'max_scrolls': 10}

# From specific user
{'type': 'search', 'target': 'from:username keyword', 'max_scrolls': 10}

# Date range (requires X Premium)
{'type': 'search', 'target': 'AI since:2024-01-01 until:2024-12-31', 'max_scrolls': 10}
```

### Batch Scraping

Execute multiple scraping tasks with a single login session:

```python
tasks = [
    {'type': 'profile', 'target': 'OpenAI', 'max_scrolls': 10},
    {'type': 'search', 'target': 'deep learning', 'max_scrolls': 15},
    {'type': 'search', 'target': '#NLP', 'max_scrolls': 10},
    {'type': 'profile', 'target': 'AndrewYNg', 'max_scrolls': 8}
]

scraper.scrape_with_single_login(tasks)
```

**Benefits:**
- Login only once for all tasks
- Efficient resource usage
- Reduced detection risk
- Automatic delays between tasks

## Configuration

### Scraper Initialization Options

```python
scraper = TwitterScraper(
    db_path="custom_database.db",  # Database file path
    headless=False                  # Browser visibility (False = visible)
)
```

### Customizing Delays

Modify delay parameters in the code to adjust scraping speed:

```python
# In human_delay() method
self.human_delay(min_seconds=2.0, max_seconds=5.0)

# Between scrolls
self.human_delay(3, 6)

# Between tasks
self.human_delay(5, 10)
```

### Logging Configuration

Adjust logging level in the code:

```python
logging.basicConfig(
    level=logging.INFO,  # Options: DEBUG, INFO, WARNING, ERROR
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

## Data Schema

### Database Structure

The scraper stores data in SQLite with the following schema:

```sql
CREATE TABLE tweets (
    tweet_id TEXT PRIMARY KEY,
    author_username TEXT,
    author_display_name TEXT,
    tweet_text TEXT,
    tweet_url TEXT,
    like_count INTEGER,
    reply_count INTEGER,
    retweet_count INTEGER,
    timestamp TEXT,
    scraped_at TEXT,
    source_type TEXT,
    source_query TEXT
)
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `tweet_id` | TEXT | Unique tweet identifier |
| `author_username` | TEXT | Twitter handle (without @) |
| `author_display_name` | TEXT | User's display name |
| `tweet_text` | TEXT | Full tweet content |
| `tweet_url` | TEXT | Direct URL to tweet |
| `like_count` | INTEGER | Number of likes |
| `reply_count` | INTEGER | Number of replies |
| `retweet_count` | INTEGER | Number of retweets |
| `timestamp` | TEXT | ISO format timestamp |
| `scraped_at` | TEXT | Collection timestamp |
| `source_type` | TEXT | 'profile' or 'search' |
| `source_query` | TEXT | Username or search term |

### Querying the Database

```python
import sqlite3

# Connect to database
conn = sqlite3.connect('twitter_data.db')
cursor = conn.cursor()

# Example queries
# 1. Get all tweets from specific user
cursor.execute("SELECT * FROM tweets WHERE author_username = ?", ('OpenAI',))

# 2. Get most liked tweets
cursor.execute("SELECT * FROM tweets ORDER BY like_count DESC LIMIT 10")

# 3. Count tweets by source
cursor.execute("SELECT source_type, COUNT(*) FROM tweets GROUP BY source_type")

# 4. Search tweet content
cursor.execute("SELECT * FROM tweets WHERE tweet_text LIKE ?", ('%machine learning%',))

# 5. Get recent tweets
cursor.execute("SELECT * FROM tweets ORDER BY timestamp DESC LIMIT 100")

conn.close()
```

### Exporting Data

```python
import pandas as pd
import sqlite3

# Export to CSV
conn = sqlite3.connect('twitter_data.db')
df = pd.read_sql_query("SELECT * FROM tweets", conn)
df.to_csv('tweets_export.csv', index=False)
conn.close()

# Export to JSON
df.to_json('tweets_export.json', orient='records', indent=2)

# Export to Excel
df.to_excel('tweets_export.xlsx', index=False)
```

## Ethical Guidelines

### Responsible Use Policy

This tool is designed for **ethical research and analysis only**. Users must:

#### DO:
- Only collect publicly accessible data
- Respect rate limits and delays
- Use data for legitimate research purposes
- Comply with Twitter's Terms of Service
- Cite data sources appropriately
- Protect user privacy in publications

#### DON'T:
- Scrape private or protected accounts
- Use data for harassment or spam
- Bypass authentication or security measures
- Violate platform Terms of Service
- Share or sell collected data inappropriately
- Use data for discriminatory purposes

### Legal Considerations

- **Terms of Service**: Review Twitter/X Terms of Service before use
- **Data Protection**: Comply with GDPR, CCPA, and other privacy regulations
- **Copyright**: Respect intellectual property rights
- **Research Ethics**: Obtain IRB approval if required by your institution

### Best Practices

1. **Minimize Impact**: Use conservative scroll counts and delays
2. **Transparency**: Document your data collection methodology
3. **Data Retention**: Only keep data necessary for your research
4. **Anonymization**: Consider anonymizing usernames in publications
5. **Attribution**: Properly credit data sources

## Troubleshooting

### Common Issues and Solutions

#### Login Issues

**Problem**: Login verification fails
```
Solution:
1. Ensure you complete the full login process
2. Wait for the home feed to load completely
3. Press ENTER only after seeing your timeline
4. If issues persist, manually confirm login when prompted
```

#### No Tweets Found

**Problem**: Scraper reports "No tweets found"
```
Solutions:
1. Check if the profile/search query is valid
2. Verify account is not private or suspended
3. Ensure you're logged in properly
4. Try increasing initial wait time (human_delay)
5. Check if Twitter has changed HTML structure
```

#### Duplicate Tweets

**Problem**: Same tweets appear multiple times
```
Solution:
- This is normal during scraping but should be prevented in database
- Check logs for "skipped duplicates" messages
- Verify PRIMARY KEY constraint on tweet_id
- Query: SELECT tweet_id, COUNT(*) FROM tweets GROUP BY tweet_id HAVING COUNT(*) > 1
```

#### Timeout Errors

**Problem**: PlaywrightTimeout exceptions
```
Solutions:
1. Increase timeout values in goto() calls
2. Check internet connection stability
3. Reduce max_scrolls if scraping too aggressively
4. Change wait_until from 'networkidle' to 'domcontentloaded'
```

#### Rate Limiting

**Problem**: Twitter blocks or limits requests
```
Solutions:
1. Increase delays between scrolls and tasks
2. Reduce max_scrolls per task
3. Spread scraping over multiple sessions
4. Use authenticated account with good standing
5. Avoid scraping during peak hours
```

### Debug Mode

Enable detailed logging:

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,  # Enable debug messages
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

### Getting Help

1. Check the [BUG_REPORT.md](BUG_REPORT.md) for known issues
2. Review closed issues on GitHub
3. Enable debug logging and examine output
4. Create a new issue with:
   - Python version
   - Playwright version
   - Error messages
   - Steps to reproduce

## Limitations

### Technical Limitations

- **Login Required**: Manual login necessary (by design for security)
- **Public Content Only**: Cannot access private/protected accounts
- **Rate Limiting**: Subject to Twitter's rate limits
- **Dynamic Content**: May not capture all tweets if scrolling too fast
- **Structure Changes**: Twitter can modify HTML structure anytime

### Data Collection Constraints

- **Historical Data**: Limited to recent tweets (Twitter's search limitations)
- **Deleted Tweets**: Cannot recover deleted content
- **Real-time**: Not suitable for real-time streaming
- **API Alternatives**: Official API provides more comprehensive data

### Performance Considerations

- **Speed**: Slower than official API due to human-like delays
- **Scalability**: Not designed for massive data collection
- **Resources**: Browser automation requires more memory than API calls

## Contributing

We welcome contributions from the community! Here's how you can help:

### Ways to Contribute

1. **Report Bugs**: Open issues for any bugs you encounter
2. **Suggest Features**: Propose new functionality or improvements
3. **Improve Documentation**: Help clarify or expand documentation
4. **Submit Pull Requests**: Contribute code improvements

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/yourusername/twitter-scraper.git
cd twitter-scraper

# Create a branch for your feature
git checkout -b feature/your-feature-name

# Make changes and test thoroughly

# Commit with clear messages
git commit -m "Add feature: description"

# Push and create pull request
git push origin feature/your-feature-name
```

### Code Standards

- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Include type hints where appropriate
- Write meaningful commit messages
- Test changes before submitting
- Update documentation as needed

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License Summary

```
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software.
```

## Disclaimer

### Important Notice

This tool is provided for **educational and research purposes only**. Users are solely responsible for ensuring their use complies with:

- Twitter/X Terms of Service
- Applicable laws and regulations
- Institutional research ethics policies
- Data protection and privacy laws

### No Warranty

This software is provided "as is", without warranty of any kind, express or implied. The authors and contributors:

- Make no guarantees about functionality or reliability
- Are not responsible for any misuse or violations
- Do not endorse any particular use case
- Assume no liability for data collection activities

### Responsible Use

By using this tool, you agree to:

1. Use it only for legitimate research purposes
2. Respect the privacy and rights of Twitter users
3. Comply with all applicable laws and terms of service
4. Not use collected data to harm, harass, or discriminate
5. Take responsibility for your own data collection practices

---

## Acknowledgments

- Built with [Playwright](https://playwright.dev/) for browser automation
- Inspired by the need for accessible academic research tools
- Thanks to the open-source community for continuous improvements

## Contact

For questions, suggestions, or collaboration opportunities:

- **Email**: samriddha.pathak@cair-nepal.org or samriddhapathak123333@gmail.com

---

**Last Updated**: February 2026

**Version**: 1.0.0

**Maintained By**: Samriddha Pathak
