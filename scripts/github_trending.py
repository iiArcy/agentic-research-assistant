#!/usr/bin/env python3
"""
GitHub Trending Tracker for AI/ML repos
Monitors trending repositories relevant to LLM fine-tuning, MLOps, Voice AI, etc.
"""

import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List
import urllib.request
import urllib.error
import ssl
import urllib.parse

# Configuration
STATE_FILE = Path.home() / ".openclaw" / "workspace" / "github-trending-state.json"
OUTPUT_DIR = Path.home() / "agentic-research-assistant" / "github-trending"

# Keywords to match (lower = checked case-insensitively)
KEYWORDS = [
    "fine-tun", "finetun", "lora", "qlora", "peft", "adapter",
    "mlops", "inference", "optimization", "quantization",
    "voice", "speech", "tts", "stt", "asr", "audio",
    "langchain", "langgraph", "llamaindex", "agentic",
    "transformer", "llm", "lm", "gpt", "claude",
    "vllm", "ollama", "llama.cpp", "tensorrt",
    "unsloth", "axolotl", "diffusion", "stable-diffusion"
]

class GitHubTrendingTracker:
    def __init__(self):
        self.state = self._load_state()
        self.new_repos: List[Dict] = []
        self.all_repos: List[Dict] = []
        
    def _load_state(self) -> Dict:
        if STATE_FILE.exists():
            try:
                with open(STATE_FILE, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {"seen_repos": {}, "last_run": None}
    
    def _save_state(self):
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        self.state["last_run"] = datetime.now().isoformat()
        with open(STATE_FILE, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def _api_request(self, url: str) -> Dict:
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Trending-Tracker"
        }
        token = os.getenv("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"token {token}"
        
        req = urllib.request.Request(url, headers=headers)
        ssl_context = ssl.create_default_context()
        
        try:
            with urllib.request.urlopen(req, context=ssl_context, timeout=30) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            print(f"  HTTP {e.code}: {e.reason}")
            return {}
        except Exception as e:
            print(f"  Error: {e}")
            return {}
    
    def _is_relevant(self, repo: Dict) -> bool:
        text = f"{repo.get('name', '')} {repo.get('description', '')}".lower()
        return any(kw.lower() in text for kw in KEYWORDS)
    
    def _get_tags(self, repo: Dict) -> List[str]:
        text = f"{repo.get('name', '')} {repo.get('description', '')}".lower()
        tags = []
        for kw in KEYWORDS:
            if kw.lower() in text and kw not in tags:
                tags.append(kw)
        return tags[:5]
    
    def fetch_trending(self) -> List[Dict]:
        """Fetch repos from GitHub search with multiple queries"""
        repos = []
        seen_names = set()
        
        # Calculate date for recent repos
        since_date = (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d")
        
        # Multiple simple queries
        search_terms = ["llm", "fine-tune", "lora", "voice ai", "langgraph", "mlops", "inference"]
        
        for term in search_terms:
            url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(term)}+created%3A>{since_date}&sort=stars&order=desc&per_page=15"
            print(f"  🔍 {term}...")
            
            data = self._api_request(url)
            if data and "items" in data:
                for item in data["items"]:
                    name = item.get("full_name")
                    if name and name not in seen_names:
                        repo = {
                            "name": name,
                            "description": item.get("description") or "",
                            "url": item.get("html_url"),
                            "stars": item.get("stargazers_count", 0),
                            "language": item.get("language") or "Unknown",
                            "topics": item.get("topics", []),
                            "created_at": item.get("created_at"),
                        }
                        # Filter: relevant + at least 50 stars
                        if repo["stars"] >= 50 and self._is_relevant(repo):
                            repos.append(repo)
                            seen_names.add(name)
                
            time.sleep(0.5)  # Rate limiting
        
        # Sort by stars
        repos.sort(key=lambda x: x["stars"], reverse=True)
        return repos[:40]  # Top 40
    
    def process_repos(self, repos: List[Dict]):
        seen = self.state.get("seen_repos", {})
        
        for repo in repos:
            repo_id = repo["name"]
            self.all_repos.append(repo)
            
            if repo_id not in seen:
                repo["tags"] = self._get_tags(repo)
                repo["discovered_at"] = datetime.now().isoformat()
                self.new_repos.append(repo)
                seen[repo_id] = {
                    "first_seen": datetime.now().isoformat(),
                    "stars_at_discovery": repo["stars"]
                }
        
        self.state["seen_repos"] = seen
    
    def generate_digest(self) -> str:
        date_str = datetime.now().strftime("%Y-%m-%d")
        
        lines = [
            f"# 🔥 GitHub Trending Digest - {date_str}",
            "",
            f"**New repos discovered:** {len(self.new_repos)}",
            f"**Total repos tracked:** {len(self.state.get('seen_repos', {}))}",
            "",
            "---",
            ""
        ]
        
        if not self.new_repos:
            lines.extend([
                "## No New Repos This Week",
                "",
                "No new trending repos matching your interests. Check back next week!",
                ""
            ])
        else:
            lines.append(f"## 🆕 {len(self.new_repos)} New Trending Repositories")
            lines.append("")
            
            for repo in sorted(self.new_repos, key=lambda x: x["stars"], reverse=True):
                tags_str = ", ".join([f"`{t}`" for t in repo.get("tags", [])])
                desc = repo.get("description", "No description") or "No description"
                
                lines.extend([
                    f"### [{repo['name']}]({repo['url']})",
                    "",
                    f"> {desc[:200]}{'...' if len(desc) > 200 else ''}",
                    "",
                    f"⭐ **{repo['stars']:,}** stars | 📝 {repo['language']} | 🏷️ {tags_str}",
                    "",
                    "---",
                    ""
                ])
        
        # Top repos section
        lines.extend(["", "## 📊 Top Repositories This Week", ""])
        for i, repo in enumerate(sorted(self.all_repos, key=lambda x: x["stars"], reverse=True)[:10], 1):
            desc = (repo.get("description") or "")[:50]
            lines.append(f"{i}. **[{repo['name']}]({repo['url']})** - ⭐ {repo['stars']:,} - {desc}...")
        
        lines.extend([
            "",
            "---",
            "",
            f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}*"
        ])
        
        return "\n".join(lines)
    
    def save_digest(self, content: str) -> Path:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        date_str = datetime.now().strftime("%Y-%m-%d")
        filepath = OUTPUT_DIR / f"{date_str}.md"
        with open(filepath, 'w') as f:
            f.write(content)
        return filepath
    
    def run(self) -> str:
        print("🚀 GitHub Trending Tracker starting...")
        print("Fetching trending repos from last 14 days...")
        
        repos = self.fetch_trending()
        print(f"📦 Found {len(repos)} relevant trending repositories")
        
        self.process_repos(repos)
        print(f"✨ {len(self.new_repos)} are new!")
        
        digest = self.generate_digest()
        filepath = self.save_digest(digest)
        print(f"📝 Saved to: {filepath}")
        
        self._save_state()
        return digest


def main():
    tracker = GitHubTrendingTracker()
    digest = tracker.run()
    
    # Print summary
    print("\n" + "="*50)
    print("📊 SUMMARY")
    print("="*50)
    print(f"New repos: {len(tracker.new_repos)}")
    print(f"Total tracked: {len(tracker.state.get('seen_repos', {}))}")
    
    if tracker.new_repos:
        print("\n🔥 Top new discoveries:")
        for repo in sorted(tracker.new_repos, key=lambda x: x["stars"], reverse=True)[:5]:
            print(f"  • {repo['name']} - ⭐ {repo['stars']:,}")
    
    return digest


if __name__ == "__main__":
    main()
