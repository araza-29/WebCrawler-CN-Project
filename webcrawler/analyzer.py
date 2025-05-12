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
    
    # Check the structure of the data
    if isinstance(data, list):
        # If data is a list, check the first item to determine structure
        if len(data) > 0:
            first_item = data[0]
            if isinstance(first_item, dict):
                # Process as list of dictionaries
                return analyze_dict_data(data)
            elif isinstance(first_item, list):
                # Process as list of lists
                return analyze_list_data(data)
            else:
                print(f"Unexpected data type: {type(first_item)}")
                return
        else:
            print("Data is empty")
            return
    elif isinstance(data, dict):
        # Process as a single dictionary
        return analyze_dict_data([data])
    else:
        print(f"Unexpected data structure: {type(data)}")
        return

def analyze_dict_data(data):
    """Analyze data structured as a list of dictionaries"""
    # Basic statistics
    total_pages = len(data)
    
    # Safely extract links and images
    total_links = 0
    total_images = 0
    all_links = []
    all_text = []
    
    for item in data:
        # Handle links
        if 'links' in item:
            links = item['links']
            if isinstance(links, list):
                total_links += len(links)
                all_links.extend(links)
        
        # Handle images
        if 'images' in item:
            images = item['images']
            if isinstance(images, list):
                total_images += len(images)
        
        # Handle text
        if 'text' in item:
            text = item['text']
            if isinstance(text, str):
                all_text.append(text)
    
    print("\n=== BASIC STATISTICS ===")
    print(f"Total pages crawled: {total_pages}")
    print(f"Total links found: {total_links}")
    print(f"Total images found: {total_images}")
    
    if total_pages > 0:
        print(f"Average links per page: {total_links/total_pages:.2f}")
        print(f"Average images per page: {total_images/total_pages:.2f}")
    
    # Analyze domains
    domains = [urlparse(link).netloc for link in all_links if link and isinstance(link, str)]
    domain_counts = Counter(domains)
    
    print("\n=== TOP DOMAINS ===")
    for domain, count in domain_counts.most_common(10):
        print(f"{domain}: {count} links")
    
    # Simple text analysis
    all_text_str = ' '.join(all_text)
    words = all_text_str.lower().split()
    # Remove very short words
    words = [word for word in words if len(word) > 3]
    word_counts = Counter(words)
    
    print("\n=== COMMON WORDS ===")
    for word, count in word_counts.most_common(20):
        print(f"{word}: {count}")
    
    # Create visualizations
    create_visualizations(domain_counts, word_counts)
    
    return domain_counts, word_counts

def analyze_list_data(data):
    """Analyze data structured as a list of lists"""
    # Basic statistics
    total_pages = len(data)
    
    # Flatten the list of lists to get all items
    flattened_data = []
    for sublist in data:
        if isinstance(sublist, list):
            flattened_data.extend(sublist)
        else:
            flattened_data.append(sublist)
    
    # Count items
    total_items = len(flattened_data)
    
    print("\n=== BASIC STATISTICS ===")
    print(f"Total pages/sections: {total_pages}")
    print(f"Total items: {total_items}")
    
    # Try to extract text and links if possible
    all_text = []
    all_links = []
    
    for item in flattened_data:
        if isinstance(item, dict):
            # Extract text
            if 'text' in item and isinstance(item['text'], str):
                all_text.append(item['text'])
            
            # Extract links
            if 'links' in item and isinstance(item['links'], list):
                all_links.extend(item['links'])
            elif 'url' in item and isinstance(item['url'], str):
                all_links.append(item['url'])
        elif isinstance(item, str):
            # Assume it might be a URL or text
            if item.startswith('http'):
                all_links.append(item)
            else:
                all_text.append(item)
    
    # Analyze domains if we found links
    domains = [urlparse(link).netloc for link in all_links if link and isinstance(link, str)]
    domain_counts = Counter(domains)
    
    if domains:
        print("\n=== TOP DOMAINS ===")
        for domain, count in domain_counts.most_common(10):
            print(f"{domain}: {count} links")
    
    # Simple text analysis if we found text
    if all_text:
        all_text_str = ' '.join(all_text)
        words = all_text_str.lower().split()
        # Remove very short words
        words = [word for word in words if len(word) > 3]
        word_counts = Counter(words)
        
        print("\n=== COMMON WORDS ===")
        for word, count in word_counts.most_common(20):
            print(f"{word}: {count}")
    else:
        word_counts = Counter()
    
    # Create visualizations
    create_visualizations(domain_counts, word_counts)
    
    return domain_counts, word_counts

def create_visualizations(domain_counts, word_counts):
    """Create and save visualizations"""
    # Domain visualization
    if domain_counts:
        plt.figure(figsize=(10, 6))
        top_domains = dict(domain_counts.most_common(10))
        plt.bar(top_domains.keys(), top_domains.values())
        plt.xticks(rotation=45, ha='right')
        plt.title('Top 10 Domains')
        plt.tight_layout()
        plt.savefig('top_domains.png')
        plt.close()
    
    # Word visualization
    if word_counts:
        plt.figure(figsize=(10, 6))
        top_words = dict(word_counts.most_common(10))
        plt.bar(top_words.keys(), top_words.values())
        plt.xticks(rotation=45, ha='right')
        plt.title('Top 10 Words')
        plt.tight_layout()
        plt.savefig('top_words.png')
        plt.close()
    
    print("\nAnalysis complete! Visualizations saved as 'top_domains.png' and 'top_words.png'")

if __name__ == "__main__":
    analyze_crawler_data('output.json')