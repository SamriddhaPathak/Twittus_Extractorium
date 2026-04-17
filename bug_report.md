# Twitter Scraper - Bug Report and Fixes

## Critical Issues Found and Fixed

### 1. **MAIN ISSUE: Scrolling and Data Collection Problems**

#### Problem:
The scraper was unable to properly scroll and collect data during search queries. Several factors contributed to this:

**a) Parse-Before-Scroll Issue:**
- Original code scrolled FIRST, then parsed tweets
- This caused newly loaded tweets to be missed on subsequent iterations
- After scrolling, the parser would find the same tweets again

**b) Missing Duplicate Tracking:**
- No mechanism to track already-seen tweet IDs during a single scraping session
- Used list comparison (`tweet_data not in tweets`) which is unreliable for dictionaries
- This caused the same tweets to be parsed multiple times

**c) Timing Issues:**
- `wait_until="networkidle"` was too strict and often timed out
- No explicit wait for tweet elements to load after navigation
- Insufficient delay after scrolling for lazy-loaded content

#### Fixes Applied:
```python
# Added tweet ID tracking
seen_tweet_ids = set()

# Changed navigation wait strategy
page.goto(url, wait_until="domcontentloaded", timeout=30000)  # Less strict
self.human_delay(3, 5)  # Give more time

# Added explicit wait for tweets
try:
    page.wait_for_selector('article[data-testid="tweet"]', timeout=10000)
except PlaywrightTimeout:
    logger.warning("No tweets found in search results")
    return tweets

# Fixed scroll order: Parse BEFORE scroll
for scroll_num in range(max_scrolls):
    # Parse tweets FIRST
    articles = page.locator('article[data-testid="tweet"]').all()
    
    for article in articles:
        tweet_data = self.parse_tweet(article, 'search', query)
        if tweet_data and tweet_data['tweet_id'] not in seen_tweet_ids:  # Proper deduplication
            tweets.append(tweet_data)
            seen_tweet_ids.add(tweet_data['tweet_id'])
    
    # Then scroll for more content
    self.scroll_page(page, scrolls=2)
```

---

### 2. **URL Encoding Issues**

#### Problem:
```python
# Original - incorrect encoding
encoded_query = query.replace(' ', '%20')
```
- Only replaced spaces, didn't handle special characters
- Queries with symbols like `#`, `&`, `=` would break the URL

#### Fix:
```python
from urllib.parse import quote
encoded_query = quote(query)
```

---

### 3. **Improved Scrolling Logic**

#### Problem:
- No detection of whether new content actually loaded
- No special handling for reaching bottom of page

#### Fix:
```python
def scroll_page(self, page: Page, scrolls: int = 3):
    for i in range(scrolls):
        # Track scroll height changes
        prev_height = page.evaluate("document.body.scrollHeight")
        
        scroll_amount = random.randint(500, 900)  # Increased from 300-700
        page.evaluate(f"window.scrollBy(0, {scroll_amount})")
        
        self.human_delay(1.5, 3.0)
        
        new_height = page.evaluate("document.body.scrollHeight")
        logger.debug(f"Scroll {i+1}/{scrolls} - Height: {prev_height} -> {new_height}")
        
        # If no new content, wait longer for lazy loading
        if new_height == prev_height:
            logger.debug("Reached bottom, waiting for lazy load...")
            time.sleep(2)
```

---

### 4. **Tweet Link Extraction Issues**

#### Problem:
```python
# Original - fragile selector
tweet_link = time_element.locator('..').get_attribute('href')
```
- Using `..` (parent) selector was unreliable
- Time element's parent wasn't always the link

#### Fix:
```python
# Use XPath to find ancestor link containing /status/
parent_link = time_element.locator('xpath=ancestor::a[contains(@href, "/status/")]').first
if not parent_link.count():
    return None
    
tweet_link = parent_link.get_attribute('href')
```

---

### 5. **Missing Error Handling**

#### Problem:
- `extract_tweet_id()` didn't handle None URLs
- Multiple functions lacked try-except blocks
- Generic exception catching hid specific errors

#### Fix:
```python
def extract_tweet_id(self, url: str) -> Optional[str]:
    if not url:  # Added None check
        return None
    match = re.search(r'/status/(\d+)', url)
    return match.group(1) if match else None

# Added specific exception logging
except Exception as e:
    logger.debug(f"Could not extract display name: {e}")
```

### 7. **Added Better Error Tracking**

#### Addition:
```python
except Exception as e:
    logger.error(f"Error scraping search '{query}': {e}")
    import traceback
    logger.error(traceback.format_exc())  # Full stack trace for debugging
```

---

### 8. **Improved Delays and Timing**

#### Changes:
```python
# After navigation, increased delay
self.human_delay(3, 5)  # Was 2, 4

# Between scrolls, adjusted
self.human_delay(2, 4)  # Was 3, 6 - too long, slowed scraping

# Within scroll function
self.human_delay(1.5, 3.0)  # Was 1.0, 2.5 - better balance
```

---

## Additional Improvements

### 9. **Better Logging**
- Changed log levels appropriately (warnings vs errors)
- Added more debug information about scroll behavior
- Clearer status messages

### 10. **Code Organization**
- Added docstring clarifications
- Better variable naming
- Consistent error handling patterns

---

## Testing Recommendations

1. **Test with Different Queries:**
   ```python
   tasks = [
       {'type': 'search', 'target': 'python programming', 'max_scrolls': 5},
       {'type': 'search', 'target': '#AI', 'max_scrolls': 5},
       {'type': 'search', 'target': 'climate change', 'max_scrolls': 10},
   ]
   ```

2. **Verify Duplicate Prevention:**
   - Check database for duplicate tweet_ids
   - Monitor logs for "skipped duplicates" messages

3. **Monitor Scroll Behavior:**
   - Watch for "Reached bottom" messages
   - Verify new content is loading between scrolls

4. **Check Data Quality:**
   ```sql
   SELECT COUNT(*), COUNT(DISTINCT tweet_id) FROM tweets;
   -- Should be equal (no duplicates)
   
   SELECT * FROM tweets WHERE tweet_text = '';
   -- Should be minimal
   ```

---

## Usage Example

```python
from twitter_scraper_fixed import TwitterScraper

scraper = TwitterScraper(db_path="twitter_data.db", headless=False)

tasks = [
    {
        'type': 'search',
        'target': 'artificial intelligence',
        'max_scrolls': 20
    },
    {
        'type': 'profile',
        'target': 'OpenAI',
        'max_scrolls': 10
    }
]

scraper.scrape_with_single_login(tasks)
```

---

## Known Limitations

1. **Rate Limiting:** Twitter/X may still rate limit aggressive scraping
2. **Dynamic Content:** Some tweets may not load if scrolling too fast
3. **Login Required:** Scraper requires manual login (by design for security)
4. **Structural Changes:** X/Twitter can change HTML structure anytime

---

## Maintenance Notes

- Monitor Twitter's HTML structure for changes to `data-testid` attributes
- Adjust delays if rate limiting occurs
- Update selectors if tweet parsing fails
- Consider implementing exponential backoff for retries

**Update**: February 2026
