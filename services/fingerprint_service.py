import httpx
from typing import Dict, Any, List
from utils.constants import HTTP_HEADERS, DEFAULT_TIMEOUT
from bs4 import BeautifulSoup

async def detect_technologies(url: str) -> Dict[str, Any]:
    """
    Fingerprint the web application by analyzing headers and HTML content.
    """
    try:
        async with httpx.AsyncClient(verify=False, timeout=DEFAULT_TIMEOUT) as client:
            response = await client.get(url, headers=HTTP_HEADERS, follow_redirects=True)
            
        technologies = set()
        headers = {k.lower(): v for k, v in response.headers.items()}
        
        server = headers.get("server")
        x_powered_by = headers.get("x-powered-by")
        
        if x_powered_by:
            technologies.add(f"Powered-By: {x_powered_by}")
            
        if "cf-ray" in headers:
            technologies.add("Cloudflare")
            
        if "x-amz-cf-id" in headers:
            technologies.add("Amazon CloudFront")
            
        if "x-vercel-id" in headers:
            technologies.add("Vercel")
            
        if "x-nf-request-id" in headers:
            technologies.add("Netlify")

        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        
        generator_meta = soup.find('meta', attrs={'name': 'generator'})
        if generator_meta and generator_meta.get('content'):
            technologies.add(f"Generator: {generator_meta.get('content')}")
            
        scripts = soup.find_all('script')
        for script in scripts:
            src = script.get('src', '').lower()
            if 'jquery' in src:
                technologies.add("jQuery")
            elif 'react' in src:
                technologies.add("React")
            elif 'vue' in src:
                technologies.add("Vue.js")
            elif 'wp-includes' in src or 'wp-content' in src:
                technologies.add("WordPress")
            elif 'next/static' in src or '_next' in src:
                technologies.add("Next.js")
            elif 'nuxt' in src:
                technologies.add("Nuxt.js")
                
        if 'cdn.shopify.com' in html_content:
            technologies.add("Shopify")
            
        return {
            "server": server,
            "technologies": list(technologies),
            "x_powered_by": x_powered_by
        }
        
    except Exception as e:
        raise Exception(f"Failed to fingerprint technologies: {str(e)}")
