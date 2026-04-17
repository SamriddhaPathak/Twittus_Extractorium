"""
Twitter/X Web Scraper
Research tool for scraping public tweets without using official APIs.

ETHICAL USE ONLY:
- Only scrapes publicly accessible content
- Respects rate limits with delays
- For academic research purposes
- Do not use for harassment, spam, or unauthorized data collection
"""

import sqlite3
import time
import random
import re
import os
from datetime import datetime
from typing import List, Dict, Optional
from playwright.sync_api import sync_playwright, Page, TimeoutError as PlaywrightTimeout
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TwitterScraper:
    """
    Ethical web scraper for Twitter/X public content.
    Uses Playwright for browser automation with human-like behavior.
    """
    
    def __init__(self, db_path: str = "twitter_data.db", headless: bool = False):
        """
        Initialize the scraper.
        
        Args:
            db_path: Path to SQLite database file
            headless: Run browser in headless mode (False = visible for human-like behavior)
        """
        self.db_path = db_path
        self.headless = headless
        self.setup_database()
    
    def wait_for_manual_login(self, page: Page):
        """
        Wait for user to manually login to Twitter/X.
        
        Args:
            page: Playwright page object
        """
        try:
            logger.info("=" * 60)
            logger.info("MANUAL LOGIN REQUIRED")
            logger.info("=" * 60)
            logger.info("Please login to your X (Twitter) account in the browser window.")
            logger.info("The scraper will wait until you are logged in.")
            logger.info("=" * 60)
            
            # Navigate to login page
            page.goto("https://x.com/i/flow/login", wait_until="networkidle", timeout=30000)
            
            print("\n" + "=" * 60)
            print("Please complete the login process in the browser window.")
            print("Press ENTER in this console AFTER you have successfully logged in.")
            print("=" * 60 + "\n")
            
            # Wait for user to press Enter
            input(">>> Press ENTER after logging in... ")
            
            # Verify login
            logger.info("Checking if login was successful...")
            time.sleep(2)
            
            # Check multiple indicators of successful login
            logged_in_checks = {
                'URL contains home': 'home' in page.url.lower(),
                'Primary column exists': page.locator('[data-testid="primaryColumn"]').count() > 0,
                'Account switcher exists': page.locator('[data-testid="SideNav_AccountSwitcher_Button"]').count() > 0,
                'Post button exists': page.locator('[data-testid="tweetButtonInline"]').count() > 0,
            }
            
            logger.info("Login verification:")
            for check_name, result in logged_in_checks.items():
                status = "[PASS]" if result else "[FAIL]"
                logger.info(f"  {status} {check_name}")
            
            if any(logged_in_checks.values()):
                logger.info("Login verified successfully!")
                logger.info(f"Current URL: {page.url}")
                return True
            else:
                logger.warning("Could not verify login automatically.")
                response = input("\nAre you logged in? (y/n): ").strip().lower()
                if response == 'y':
                    logger.info("User confirmed login - proceeding...")
                    return True
                else:
                    logger.error("Login not confirmed - aborting")
                    return False
                    
        except Exception as e:
            logger.error(f"Error during manual login: {e}")
            return False
        
    def setup_database(self):
        """Create database and tables if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tweets (
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
        """)
        
        # Create index for faster queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_author_username 
            ON tweets(author_username)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_scraped_at 
            ON tweets(scraped_at)
        """)
        
        conn.commit()
        conn.close()
        logger.info(f"Database initialized at {self.db_path}")
    
    def save_tweets(self, tweets: List[Dict]):
        """
        Save tweets to database with deduplication.
        
        Args:
            tweets: List of tweet dictionaries
        """
        if not tweets:
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        saved_count = 0
        duplicate_count = 0
        
        for tweet in tweets:
            try:
                cursor.execute("""
                    INSERT OR IGNORE INTO tweets 
                    (tweet_id, author_username, author_display_name, tweet_text, 
                     tweet_url, like_count, reply_count, retweet_count, 
                     timestamp, scraped_at, source_type, source_query)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    tweet['tweet_id'],
                    tweet['author_username'],
                    tweet['author_display_name'],
                    tweet['tweet_text'],
                    tweet['tweet_url'],
                    tweet['like_count'],
                    tweet['reply_count'],
                    tweet['retweet_count'],
                    tweet['timestamp'],
                    tweet['scraped_at'],
                    tweet['source_type'],
                    tweet['source_query']
                ))
                
                if cursor.rowcount > 0:
                    saved_count += 1
                else:
                    duplicate_count += 1
                    
            except sqlite3.Error as e:
                logger.error(f"Error saving tweet {tweet.get('tweet_id')}: {e}")
        
        conn.commit()
        conn.close()
        
        logger.info(f"Saved {saved_count} new tweets, skipped {duplicate_count} duplicates")
    
    def human_delay(self, min_seconds: float = 1.5, max_seconds: float = 4.0):
        """
        Add randomized delay to mimic human behavior.
        
        Args:
            min_seconds: Minimum delay
            max_seconds: Maximum delay
        """
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    
    def scroll_page(self, page: Page, scrolls: int = 3):
        """
        Scroll page gradually to load dynamic content.
        
        Args:
            page: Playwright page object
            scrolls: Number of scroll actions
        """
        for i in range(scrolls):
            # Get current scroll position
            prev_height = page.evaluate("document.body.scrollHeight")
            
            # Scroll by random amount
            scroll_amount = random.randint(500, 900)
            page.evaluate(f"window.scrollBy(0, {scroll_amount})")
            
            # Wait for content to load
            self.human_delay(1.5, 3.0)
            
            # Check if new content loaded
            new_height = page.evaluate("document.body.scrollHeight")
            logger.debug(f"Scroll {i+1}/{scrolls} - Height: {prev_height} -> {new_height}")
            
            # If we've reached the bottom, wait a bit longer for lazy loading
            if new_height == prev_height:
                logger.debug("Reached bottom, waiting for lazy load...")
                time.sleep(2)
    
    def extract_number(self, text: str) -> int:
        """
        Extract numeric value from text like '1.2K', '500', '1M'.
        
        Args:
            text: Text containing number
            
        Returns:
            Integer value
        """
        if not text:
            return 0
        
        # Remove commas and spaces
        text = text.replace(',', '').replace(' ', '').upper()
        
        # Handle K (thousands) and M (millions)
        multiplier = 1
        if 'K' in text:
            multiplier = 1000
            text = text.replace('K', '')
        elif 'M' in text:
            multiplier = 1000000
            text = text.replace('M', '')
        
        # Extract numeric part
        match = re.search(r'[\d.]+', text)
        if match:
            try:
                return int(float(match.group()) * multiplier)
            except ValueError:
                return 0
        return 0
    
    def extract_tweet_id(self, url: str) -> Optional[str]:
        """
        Extract tweet ID from URL.
        
        Args:
            url: Tweet URL
            
        Returns:
            Tweet ID or None
        """
        if not url:
            return None
        match = re.search(r'/status/(\d+)', url)
        return match.group(1) if match else None
    
    def parse_tweet(self, article_element, source_type: str, source_query: str) -> Optional[Dict]:
        """
        Parse tweet data from article element.
        
        Args:
            article_element: Playwright element containing tweet
            source_type: 'profile' or 'search'
            source_query: Username or search term
            
        Returns:
            Dictionary with tweet data or None
        """
        try:
            # Extract tweet URL (most reliable identifier)
            time_element = article_element.locator('time').first
            if not time_element.count():
                return None
            
            # Get parent link of time element (tweet URL)
            parent_link = time_element.locator('xpath=ancestor::a[contains(@href, "/status/")]').first
            if not parent_link.count():
                return None
                
            tweet_link = parent_link.get_attribute('href')
            if not tweet_link:
                return None
            
            # Make full URL - handle both x.com and twitter.com
            if tweet_link.startswith('/'):
                tweet_url = f"https://x.com{tweet_link}"
            else:
                tweet_url = tweet_link
            
            tweet_id = self.extract_tweet_id(tweet_url)
            if not tweet_id:
                return None
            
            # Extract author username from URL
            username_match = re.search(r'(?:x\.com|twitter\.com)/([^/]+)/', tweet_url)
            author_username = username_match.group(1) if username_match else "unknown"
            
            # Extract display name
            display_name = "Unknown"
            try:
                user_name_div = article_element.locator('[data-testid="User-Name"]').first
                if user_name_div.count():
                    # Get first span with text (display name)
                    name_spans = user_name_div.locator('span').all()
                    for span in name_spans:
                        text = span.inner_text().strip()
                        if text and not text.startswith('@'):
                            display_name = text
                            break
            except Exception as e:
                logger.debug(f"Could not extract display name: {e}")
            
            # Extract tweet text
            tweet_text = ""
            try:
                tweet_text_div = article_element.locator('[data-testid="tweetText"]').first
                if tweet_text_div.count():
                    tweet_text = tweet_text_div.inner_text().strip()
            except Exception as e:
                logger.debug(f"Could not extract tweet text: {e}")
            
            # Extract engagement metrics
            like_count = 0
            reply_count = 0
            retweet_count = 0
            
            try:
                # Like button
                like_button = article_element.locator('[data-testid="like"]').first
                if like_button.count():
                    like_text = like_button.get_attribute('aria-label') or ""
                    like_count = self.extract_number(like_text)
                
                # Reply button
                reply_button = article_element.locator('[data-testid="reply"]').first
                if reply_button.count():
                    reply_text = reply_button.get_attribute('aria-label') or ""
                    reply_count = self.extract_number(reply_text)
                
                # Retweet button
                retweet_button = article_element.locator('[data-testid="retweet"]').first
                if retweet_button.count():
                    retweet_text = retweet_button.get_attribute('aria-label') or ""
                    retweet_count = self.extract_number(retweet_text)
            except Exception as e:
                logger.debug(f"Could not extract engagement metrics: {e}")
            
            # Extract timestamp
            timestamp = ""
            try:
                time_element = article_element.locator('time').first
                if time_element.count():
                    timestamp = time_element.get_attribute('datetime') or ""
            except Exception as e:
                logger.debug(f"Could not extract timestamp: {e}")
            
            return {
                'tweet_id': tweet_id,
                'author_username': author_username,
                'author_display_name': display_name,
                'tweet_text': tweet_text,
                'tweet_url': tweet_url,
                'like_count': like_count,
                'reply_count': reply_count,
                'retweet_count': retweet_count,
                'timestamp': timestamp,
                'scraped_at': datetime.now().isoformat(),
                'source_type': source_type,
                'source_query': source_query
            }
            
        except Exception as e:
            logger.debug(f"Error parsing tweet: {e}")
            return None
    
    def scrape_profile(self, username: str, max_scrolls: int = 5, 
                       page: Page = None, context = None, browser = None) -> List[Dict]:
        """
        Scrape tweets from a public profile.
        
        Args:
            username: Twitter/X username to scrape (without @)
            max_scrolls: Number of times to scroll for more content
            page: Existing Playwright page (optional)
            context: Existing browser context (optional)
            browser: Existing browser instance (optional)
            
        Returns:
            List of tweet dictionaries
        """
        tweets = []
        seen_tweet_ids = set()
        url = f"https://x.com/{username}"
        
        logger.info(f"Scraping profile: @{username}")
        
        # Use existing page or create new one
        should_close = False
        if page is None:
            should_close = True
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=self.headless)
                context = browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    viewport={'width': 1280, 'height': 720}
                )
                page = context.new_page()
                
                # Wait for manual login
                if not self.wait_for_manual_login(page):
                    return tweets
        
        try:
            # Navigate to profile
            logger.info(f"Navigating to {url}")
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            self.human_delay(3, 5)
            
            # Wait for tweets to load
            try:
                page.wait_for_selector('article[data-testid="tweet"]', timeout=10000)
            except PlaywrightTimeout:
                logger.warning("No tweets found on profile page")
            
            # Check if profile is accessible (not private/suspended)
            if "This account doesn't exist" in page.content() or "Account suspended" in page.content():
                logger.warning(f"Profile @{username} is not accessible")
                return tweets
            
            # Scroll to load tweets
            for scroll_num in range(max_scrolls):
                logger.info(f"Scroll {scroll_num + 1}/{max_scrolls}")
                
                # Parse tweets before scrolling
                articles = page.locator('article[data-testid="tweet"]').all()
                logger.info(f"Found {len(articles)} tweet elements on page")
                
                for article in articles:
                    tweet_data = self.parse_tweet(article, 'profile', username)
                    if tweet_data and tweet_data['tweet_id'] not in seen_tweet_ids:
                        tweets.append(tweet_data)
                        seen_tweet_ids.add(tweet_data['tweet_id'])
                        logger.debug(f"Parsed tweet {tweet_data['tweet_id']}")
                
                # Scroll for more content
                self.scroll_page(page, scrolls=2)
                
                # Rate limiting between scrolls
                self.human_delay(2, 4)
            
            logger.info(f"Scraped {len(tweets)} unique tweets from @{username}")
            
        except PlaywrightTimeout:
            logger.error(f"Timeout loading profile @{username}")
        except Exception as e:
            logger.error(f"Error scraping profile @{username}: {e}")
            import traceback
            logger.error(traceback.format_exc())
        finally:
            if should_close and context and browser:
                context.close()
                browser.close()
        
        return tweets
    
    def scrape_search(self, query: str, max_scrolls: int = 5,
                      page: Page = None, context = None, browser = None) -> List[Dict]:
        """
        Scrape tweets from search results.
        
        Args:
            query: Search term
            max_scrolls: Number of times to scroll for more content
            page: Existing Playwright page (optional)
            context: Existing browser context (optional)
            browser: Existing browser instance (optional)
            
        Returns:
            List of tweet dictionaries
        """
        tweets = []
        seen_tweet_ids = set()
        # URL encode the query properly
        from urllib.parse import quote
        encoded_query = quote(query)
        url = f"https://x.com/search?q={encoded_query}&src=typed_query&f=live"
        
        logger.info(f"Scraping search results for: {query}")
        
        # Use existing page or create new one
        should_close = False
        if page is None:
            should_close = True
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=self.headless)
                context = browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    viewport={'width': 1280, 'height': 720}
                )
                page = context.new_page()
                
                # Wait for manual login
                if not self.wait_for_manual_login(page):
                    return tweets
        
        try:
            logger.info(f"Navigating to {url}")
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            self.human_delay(3, 5)
            
            # Wait for search results to load
            try:
                page.wait_for_selector('article[data-testid="tweet"]', timeout=10000)
            except PlaywrightTimeout:
                logger.warning("No tweets found in search results")
                return tweets
            
            # Scroll to load tweets
            for scroll_num in range(max_scrolls):
                logger.info(f"Scroll {scroll_num + 1}/{max_scrolls}")
                
                # Parse tweets before scrolling
                articles = page.locator('article[data-testid="tweet"]').all()
                logger.info(f"Found {len(articles)} tweet elements on page")
                
                for article in articles:
                    tweet_data = self.parse_tweet(article, 'search', query)
                    if tweet_data and tweet_data['tweet_id'] not in seen_tweet_ids:
                        tweets.append(tweet_data)
                        seen_tweet_ids.add(tweet_data['tweet_id'])
                        logger.debug(f"Parsed tweet {tweet_data['tweet_id']}")
                
                # Scroll for more content
                self.scroll_page(page, scrolls=2)
                
                # Rate limiting between scrolls
                self.human_delay(2, 4)
            
            logger.info(f"Scraped {len(tweets)} unique tweets from search '{query}'")
            
        except PlaywrightTimeout:
            logger.error(f"Timeout loading search results for '{query}'")
        except Exception as e:
            logger.error(f"Error scraping search '{query}': {e}")
            import traceback
            logger.error(traceback.format_exc())
        finally:
            if should_close and context and browser:
                context.close()
                browser.close()
        
        return tweets
    
    def scrape_with_single_login(self, tasks: List[Dict]):
        """
        Perform multiple scraping tasks with a single login session.
        
        Args:
            tasks: List of task dictionaries with 'type', 'target', and 'max_scrolls'
                   Example: [
                       {'type': 'profile', 'target': 'elonmusk', 'max_scrolls': 5},
                       {'type': 'search', 'target': 'AI research', 'max_scrolls': 10}
                   ]
        """
        logger.info(f"Starting batch scraping with {len(tasks)} tasks")
        
        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(headless=self.headless)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={'width': 1280, 'height': 720}
            )
            page = context.new_page()
            
            try:
                # Wait for manual login ONCE
                if not self.wait_for_manual_login(page):
                    logger.error("Login failed - aborting all tasks")
                    return
                
                logger.info("Login successful - starting scraping tasks...")
                self.human_delay(2, 3)
                
                # Execute all tasks with the same logged-in session
                for i, task in enumerate(tasks, 1):
                    logger.info(f"\n{'='*60}")
                    logger.info(f"Task {i}/{len(tasks)}: {task['type']} - {task['target']}")
                    logger.info(f"{'='*60}")
                    
                    if task['type'] == 'profile':
                        tweets = self.scrape_profile(
                            username=task['target'],
                            max_scrolls=task.get('max_scrolls', 5),
                            page=page,
                            context=context,
                            browser=browser
                        )
                    elif task['type'] == 'search':
                        tweets = self.scrape_search(
                            query=task['target'],
                            max_scrolls=task.get('max_scrolls', 5),
                            page=page,
                            context=context,
                            browser=browser
                        )
                    else:
                        logger.error(f"Unknown task type: {task['type']}")
                        continue
                    
                    # Save tweets
                    self.save_tweets(tweets)
                    
                    # Delay between tasks
                    if i < len(tasks):
                        logger.info("Waiting before next task...")
                        self.human_delay(5, 10)
                
                logger.info("\n" + "="*60)
                logger.info("ALL TASKS COMPLETED")
                logger.info("="*60)
                
            except Exception as e:
                logger.error(f"Error during batch scraping: {e}")
                import traceback
                logger.error(traceback.format_exc())
            finally:
                context.close()
                browser.close()


def main():
    """
    Example usage of the Twitter/X scraper with manual login.
    """
    print("=" * 60)
    print("Twitter/X Web Scraper - Academic Research Tool")
    print("=" * 60)
    print("\nETHICAL USE ONLY:")
    print("- Public content only")
    print("- Respects rate limits")
    print("- For research purposes")
    print("=" * 60)
    print()
    
    # Initialize scraper
    scraper = TwitterScraper(
        db_path="twitter_data.db",
        headless=False  # Must be False for manual login
    )
    
    # Define your scraping tasks
    tasks = [
        # Example 1: Scrape a profile
        # {
        #     'type': 'profile',
        #     'target': 'elonmusk',
        #     'max_scrolls': 5
        # },
        
        # Example 2: Scrape search results
        # {
        #     'type': 'search',
        #     'target': 'Healthcare Nepal',
        #     'max_scrolls': 50
        # },
    ]
    
    # Execute all tasks with single login
    scraper.scrape_with_single_login(tasks)
    
    # Summary
    print("\n" + "=" * 60)
    print("SCRAPING COMPLETE")
    print("=" * 60)
    
    # Query database for summary
    conn = sqlite3.connect("twitter_data.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM tweets")
    total_tweets = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT author_username) FROM tweets")
    unique_authors = cursor.fetchone()[0]
    
    cursor.execute("SELECT source_type, COUNT(*) FROM tweets GROUP BY source_type")
    by_source = cursor.fetchall()
    
    conn.close()
    
    print(f"\nTotal tweets in database: {total_tweets}")
    print(f"Unique authors: {unique_authors}")
    print("\nTweets by source:")
    for source_type, count in by_source:
        print(f"  {source_type}: {count}")
    
    print(f"\nData saved to: twitter_data.db")
    print("\nUse SQLite browser or Python to query the data.")


if __name__ == "__main__":
    main()