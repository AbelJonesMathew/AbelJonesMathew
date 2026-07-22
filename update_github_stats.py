import os
import json
import re
import urllib.request
import urllib.error
import subprocess

def fetch_json(url):
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    )
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Error fetching JSON from {url}: {e}")
        return None

def fetch_html(url):
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    )
    try:
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching HTML from {url}: {e}")
        return None

def get_contributions(username):
    # Try the unofficial API first
    print("Fetching total contributions from unofficial API...")
    url = f"https://github-contributions-api.deno.dev/{username}.json"
    data = fetch_json(url)
    if data and "totalContributions" in data:
        return data["totalContributions"]
    
    # Fallback to scraping the public profile contributions page
    print("Fallback: Scraping contributions from GitHub profile graph page...")
    url = f"https://github.com/users/{username}/contributions"
    html = fetch_html(url)
    if html:
        # Match text like "354 contributions in the last year"
        match = re.search(r'(\d+[\d,]*)\s+contributions?\s+in\s+the\s+last\s+year', html, re.IGNORECASE)
        if match:
            contributions_str = match.group(1).replace(',', '')
            return int(contributions_str)
            
    print("Could not retrieve contributions count automatically. Using fallback.")
    return None

def get_repos_and_languages(username):
    print("Fetching repositories list...")
    url = f"https://api.github.com/users/{username}/repos?per_page=100"
    repos = fetch_json(url)
    if not repos:
        return None, None
    
    # Save repos cache
    try:
        with open("repos_cache.json", "w", encoding="utf-8") as f:
            json.dump(repos, f, indent=4)
        print("Updated repos_cache.json.")
    except Exception as e:
        print(f"Warning: Could not update repos_cache.json: {e}")
        
    # Aggregate languages
    language_counts = {}
    total_languages_size = 0
    
    print("Analyzing repository languages...")
    for repo in repos:
        if repo.get("fork"):
            continue  # skip forks
        
        # Use primary language field first to avoid rate limiting
        lang = repo.get("language")
        if lang:
            language_counts[lang] = language_counts.get(lang, 0) + 1
            total_languages_size += 1
            
    # Convert to percentages
    languages_percentage = {}
    if total_languages_size > 0:
        for lang, count in language_counts.items():
            languages_percentage[lang] = round((count / total_languages_size) * 100, 1)
            
    # Sort by percentage descending
    sorted_langs = dict(sorted(languages_percentage.items(), key=lambda item: item[1], reverse=True))
    return len(repos), sorted_langs

def main():
    username = "AbelJonesMathew"
    print(f"Updating GitHub statistics for user: {username}")
    
    # 1. Fetch user general info
    url = f"https://api.github.com/users/{username}"
    user_info = fetch_json(url)
    
    if not user_info:
        print("Error: Could not fetch user info from GitHub API. Please check your internet connection or rate limits.")
        return
        
    public_repos_count = user_info.get("public_repos", 0)
    followers = user_info.get("followers", 0)
    
    # 2. Get contributions
    contributions = get_contributions(username)
    if contributions is None:
        # Keep existing contribution count if fetch fails
        if os.path.exists("real_stats.json"):
            try:
                with open("real_stats.json", "r") as f:
                    old_data = json.load(f)
                    contributions = old_data.get("contributions", 26)
            except Exception:
                contributions = 26
        else:
            contributions = 26
            
    # 3. Get repository languages
    total_repos, languages = get_repos_and_languages(username)
    if total_repos is None:
        # Fallback to general API repo count
        total_repos = public_repos_count
        languages = {
            "Python": 32.0,
            "HTML": 20.0,
            "CSS": 20.0,
            "C": 12.0,
            "TypeScript": 4.0
        }
        
    # Write to real_stats.json
    stats_data = {
        "public_repos": total_repos,
        "followers": followers,
        "contributions": contributions,
        "languages": languages
    }
    
    with open("real_stats.json", "w", encoding="utf-8") as f:
        json.dump(stats_data, f, indent=4)
        
    print("\n--- Updated Stats Summary ---")
    print(f"Public Repos: {total_repos}")
    print(f"Followers: {followers}")
    print(f"Contributions: {contributions}")
    print("Languages:", json.dumps(languages, indent=2))
    print("-----------------------------\n")
    print("Successfully updated real_stats.json.")
    
    # Run assemble_assets.py
    if os.path.exists("assemble_assets.py"):
        print("Running assemble_assets.py to rebuild SVGs...")
        try:
            # We run python in the same environment
            result = subprocess.run(["python", "assemble_assets.py"], capture_output=True, text=True, check=True)
            print(result.stdout)
            print("Successfully updated all README SVG assets!")
        except subprocess.CalledProcessError as e:
            print(f"Error rebuilding SVG assets: {e}")
            print(e.stderr)
    else:
        print("Warning: assemble_assets.py not found in the current folder.")

if __name__ == "__main__":
    main()
