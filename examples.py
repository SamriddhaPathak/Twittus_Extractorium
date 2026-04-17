# Twitter/X Scraper - Example Configuration
# Copy this file to 'my_scraping_tasks.py' and customize for your needs

from twitter_scraper_fixed import TwitterScraper

def run_research_project():
    """
    Example: Academic research on AI discussions
    """
    scraper = TwitterScraper(
        db_path="ai_research.db",
        headless=False
    )
    
    tasks = [
        # Collect from AI research accounts
        {'type': 'profile', 'target': 'OpenAI', 'max_scrolls': 15},
        {'type': 'profile', 'target': 'AndrewYNg', 'max_scrolls': 15},
        {'type': 'profile', 'target': 'ylecun', 'max_scrolls': 15},
        
        # Collect from search queries
        {'type': 'search', 'target': 'machine learning', 'max_scrolls': 20},
        {'type': 'search', 'target': '#AI ethics', 'max_scrolls': 20},
        {'type': 'search', 'target': 'deep learning research', 'max_scrolls': 20},
    ]
    
    scraper.scrape_with_single_login(tasks)


def run_brand_monitoring():
    """
    Example: Brand mention monitoring
    """
    scraper = TwitterScraper(
        db_path="brand_mentions.db",
        headless=False
    )
    
    brand_name = "YourBrandName"
    
    tasks = [
        # Monitor brand mentions
        {'type': 'search', 'target': f'{brand_name}', 'max_scrolls': 25},
        {'type': 'search', 'target': f'#{brand_name}', 'max_scrolls': 25},
        
        # Monitor competitors
        {'type': 'search', 'target': 'competitor_brand', 'max_scrolls': 15},
        
        # Monitor industry keywords
        {'type': 'search', 'target': 'industry_keyword', 'max_scrolls': 15},
    ]
    
    scraper.scrape_with_single_login(tasks)


def run_event_tracking():
    """
    Example: Track tweets about specific events
    """
    scraper = TwitterScraper(
        db_path="event_tracking.db",
        headless=False
    )
    
    tasks = [
        # Track conference hashtag
        {'type': 'search', 'target': '#ConferenceName2024', 'max_scrolls': 30},
        
        # Track event speakers
        {'type': 'profile', 'target': 'speaker1', 'max_scrolls': 10},
        {'type': 'profile', 'target': 'speaker2', 'max_scrolls': 10},
        
        # Track event discussions
        {'type': 'search', 'target': 'ConferenceName keynote', 'max_scrolls': 20},
    ]
    
    scraper.scrape_with_single_login(tasks)


def run_sentiment_analysis_collection():
    """
    Example: Collect data for sentiment analysis
    """
    scraper = TwitterScraper(
        db_path="sentiment_data.db",
        headless=False
    )
    
    topics = [
        'climate change',
        'electric vehicles',
        'renewable energy',
        'sustainability'
    ]
    
    tasks = []
    for topic in topics:
        tasks.append({
            'type': 'search',
            'target': f'{topic} lang:en',  # English only
            'max_scrolls': 20
        })
    
    scraper.scrape_with_single_login(tasks)


def run_influencer_analysis():
    """
    Example: Analyze influencer content
    """
    scraper = TwitterScraper(
        db_path="influencer_analysis.db",
        headless=False
    )
    
    influencers = [
        'influencer1',
        'influencer2',
        'influencer3',
        'influencer4',
        'influencer5'
    ]
    
    tasks = []
    for influencer in influencers:
        tasks.append({
            'type': 'profile',
            'target': influencer,
            'max_scrolls': 20
        })
    
    scraper.scrape_with_single_login(tasks)


def run_custom_search():
    """
    Example: Custom advanced search
    """
    scraper = TwitterScraper(
        db_path="custom_search.db",
        headless=False
    )
    
    tasks = [
        # Advanced search examples
        
        # Search with multiple keywords
        {'type': 'search', 'target': 'python OR javascript', 'max_scrolls': 15},
        
        # Exclude terms
        {'type': 'search', 'target': 'programming -tutorial', 'max_scrolls': 15},
        
        # From specific user
        {'type': 'search', 'target': 'from:username keyword', 'max_scrolls': 10},
        
        # To specific user
        {'type': 'search', 'target': 'to:username', 'max_scrolls': 10},
        
        # Language-specific
        {'type': 'search', 'target': 'technology lang:en', 'max_scrolls': 15},
        
        # Minimum engagement
        {'type': 'search', 'target': 'viral min_faves:1000', 'max_scrolls': 15},
        
        # Questions only
        {'type': 'search', 'target': 'python ?', 'max_scrolls': 15},
    ]
    
    scraper.scrape_with_single_login(tasks)


# ============================================================================
# Main execution
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("Twitter/X Scraper - Example Configurations")
    print("=" * 70)
    print("\nAvailable functions:")
    print("1. run_research_project() - Academic AI research")
    print("2. run_brand_monitoring() - Brand mention tracking")
    print("3. run_event_tracking() - Event coverage tracking")
    print("4. run_sentiment_analysis_collection() - Data for sentiment analysis")
    print("5. run_influencer_analysis() - Influencer content analysis")
    print("6. run_custom_search() - Advanced search examples")
    print("\nUncomment the function you want to run:")
    print("=" * 70)
    print()
    
    # Uncomment ONE of the following to run:
    
    # run_research_project()
    # run_brand_monitoring()
    # run_event_tracking()
    # run_sentiment_analysis_collection()
    # run_influencer_analysis()
    # run_custom_search()
    
    # Or create your own custom configuration:
    
    # scraper = TwitterScraper(db_path="my_data.db", headless=False)
    # tasks = [
    #     {'type': 'search', 'target': 'your query here', 'max_scrolls': 10}
    # ]
    # scraper.scrape_with_single_login(tasks)
    
    print("\nPlease uncomment a function in the code to run it.")
