import json
from collections import Counter
from urllib.parse import urlparse
import matplotlib.pyplot as plt

def analyze_crawler_data(json_file_path):
    """Perform basic analysis on web crawler data"""
    # Load the data
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Analyzing {len(data)} crawled pages...")
    
    # Basic statistics
    total_pages = len(data)
    total_links = sum(len(item.get('links', [])) for item in data)
    total_images = sum(len(item.get('images', [])) for item in data)
    
    print("\n=== BASIC STATISTICS ===")
    print(f"Total pages crawled: {total_pages}")
    print(f"Total links found: {total_links}")
    print(f"Total images found: {total_images}")
    print(f"Average links per page: {total_links/total_pages:.2f}")
    print(f"Average images per page: {total_images/total_pages:.2f}")
    
    # Analyze domains
    all_links = []
    for item in data:
        all_links.extend(item.get('links', []))
    
    domains = [urlparse(link).netloc for link in all_links if link]
    domain_counts = Counter(domains)
    
    print("\n=== TOP DOMAINS ===")
    for domain, count in domain_counts.most_common(10):
        print(f"{domain}: {count} links")
    
    # Simple text analysis
    all_text = ' '.join([item.get('text', '') for item in data])
    words = all_text.lower().split()
    # Remove very short words
    words = [word for word in words if len(word) > 3]
    word_counts = Counter(words)
    
    print("\n=== COMMON WORDS ===")
    for word, count in word_counts.most_common(20):
        print(f"{word}: {count}")
    
    # Create simple visualizations
    plt.figure(figsize=(10, 6))
    top_domains = dict(domain_counts.most_common(10))
    plt.bar(top_domains.keys(), top_domains.values())
    plt.xticks(rotation=45, ha='right')
    plt.title('Top 10 Domains')
    plt.tight_layout()
    plt.savefig('top_domains.png')
    plt.close()
    
    plt.figure(figsize=(10, 6))
    top_words = dict(word_counts.most_common(10))
    plt.bar(top_words.keys(), top_words.values())
    plt.xticks(rotation=45, ha='right')
    plt.title('Top 10 Words')
    plt.tight_layout()
    plt.savefig('top_words.png')
    
    print("\nAnalysis complete! Visualizations saved as 'top_domains.png' and 'top_words.png'")

if __name__ == "__main__":
    analyze_crawler_data('../output.json')