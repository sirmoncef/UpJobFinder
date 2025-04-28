import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict
import random
import asyncio

async def scrape_upwork(search_query: str = "python") -> List[Dict]:
    """Scrape Python jobs from Upwork with detailed info"""
    url = f"https://www.upwork.com/nx/search/jobs/?contractor_tier=1,2&nbs=1&q={search_query}&sort=recency"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Referer': 'https://www.upwork.com/',
    'Upgrade-Insecure-Requests': '1',
}

    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    raise Exception(f"Upwork returned {response.status}")
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                jobs = []
                
                titles = soup.select('a[data-test="job-tile-title-link"]')
                posted_times = soup.select('span[data-v-6e74a038]')
                locations = soup.select('div.air3-badge-tagline')
                budgets = soup.select('li[data-test="is-fixed-price"] strong:nth-of-type(2)')
                durations = soup.select('li[data-test="duration-label"] strong:nth-of-type(2)')

                total_jobs = len(titles)
                
                for idx in range(total_jobs):
                    try:
                        title_tag = titles[idx]
                        title = title_tag.text.strip()
                        link = "https://www.upwork.com" + title_tag['href']

                        # Filter unwanted titles (like "senior")
                        if 'senior' in title.lower():
                            continue

                        posted = posted_times[idx].text.strip() if idx < len(posted_times) else "/"
                        location = locations[idx].text.strip() if idx < len(locations) else "/"
                        budget = budgets[idx].text.strip() if idx < len(budgets) else "/"
                        duration = durations[idx].text.strip() if idx < len(durations) else "/"

                        jobs.append({
                            'title': title,
                            'link': link,
                            'posted': posted,
                            'location': location.replace('\n', ' ').strip(),
                            'budget': budget,
                            'duration': duration,
                            'source': 'Upwork'
                        })
                    except Exception as e:
                        # Skip problematic jobs
                        print(f"⚠️ Skipping a job due to error: {e}")
                        continue
                
                return jobs
                
    except Exception as e:
        print(f"⚠️ Upwork scrape error: {e}")
        return []

async def get_latest_jobs(search_query: str = "python") -> List[Dict]:
    """Main function to get jobs with custom search"""
    return await scrape_upwork(search_query)
