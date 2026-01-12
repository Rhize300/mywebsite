import re
import tldextract
import requests
from urllib.parse import urlparse
import whois
from datetime import datetime
from difflib import SequenceMatcher
import socket

POPULAR_DOMAINS = [
    'microsoft.com', 'google.com', 'facebook.com', 'apple.com', 'amazon.com',
    'paypal.com', 'ebay.com', 'yahoo.com', 'instagram.com', 'twitter.com',
    'linkedin.com', 'netflix.com', 'whatsapp.com', 'telegram.org', 'bankofamerica.com',
    'wellsfargo.com', 'chase.com', 'gmail.com', 'outlook.com', 'icloud.com'
]

def is_typo_domain(domain, threshold=0.8):
    """Cek apakah domain mirip dengan domain populer (typo-squatting)"""
    domain = domain.lower()
    for popular in POPULAR_DOMAINS:
        base = popular.split('.')[0]
        ratio = SequenceMatcher(None, domain, base).ratio()
        if ratio >= threshold and domain != base:
            return 1
    return 0

def extract_url_features(url):
    """
    Ekstraksi fitur-fitur dari URL untuk deteksi phishing
    """
    features = {}
    
    try:
        # Parse URL
        parsed_url = urlparse(url)
        extracted = tldextract.extract(url)
        
        # Basic URL features
        features['url_length'] = len(url)
        features['domain_length'] = len(extracted.domain)
        features['subdomain_count'] = len(extracted.subdomain.split('.')) if extracted.subdomain else 0
        features['path_length'] = len(parsed_url.path)
        features['query_length'] = len(parsed_url.query)
        
        # Special characters
        features['special_chars'] = len(re.findall(r'[^a-zA-Z0-9]', url))
        features['at_symbol'] = 1 if '@' in url else 0
        features['double_slash'] = 1 if '//' in url else 0
        features['dash_count'] = url.count('-')
        features['underscore_count'] = url.count('_')
        features['dot_count'] = url.count('.')
        features['equal_count'] = url.count('=')
        features['question_count'] = url.count('?')
        features['hash_count'] = url.count('#')
        features['percent_count'] = url.count('%')
        
        # Domain features
        features['domain_age'] = get_domain_age(extracted.domain + '.' + extracted.suffix)
        features['https_used'] = 1 if parsed_url.scheme == 'https' else 0
        features['port_present'] = 1 if parsed_url.port else 0
        
        # Suspicious patterns
        features['ip_in_domain'] = 1 if re.search(r'\d+\.\d+\.\d+\.\d+', extracted.domain) else 0
        features['suspicious_words'] = count_suspicious_words(url.lower())
        features['redirect_count'] = count_redirects(url)
        
        # URL structure
        features['url_depth'] = len([x for x in parsed_url.path.split('/') if x])
        features['favicon_domain_match'] = check_favicon_domain(url)
        features['is_typo_domain'] = is_typo_domain(extracted.domain)
        features['is_judol'] = 1 if 'judol' in url.lower() else 0
        
    except Exception as e:
        # Return default values if extraction fails
        features = {key: 0 for key in [
            'url_length', 'domain_length', 'subdomain_count', 'path_length',
            'query_length', 'special_chars', 'at_symbol', 'double_slash',
            'dash_count', 'underscore_count', 'dot_count', 'equal_count',
            'question_count', 'hash_count', 'percent_count', 'domain_age',
            'https_used', 'port_present', 'ip_in_domain', 'suspicious_words',
            'redirect_count', 'url_depth', 'favicon_domain_match', 'is_typo_domain',
            'is_judol'
        ]}
    
    return features

def get_domain_age(domain):
    """Get domain age in days"""
    try:
        # Set timeout untuk WHOIS query
        socket.setdefaulttimeout(5)  # 5 detik timeout
        
        w = whois.whois(domain)
        if w.creation_date:
            if isinstance(w.creation_date, list):
                creation_date = w.creation_date[0]
            else:
                creation_date = w.creation_date
            age = (datetime.now() - creation_date).days
            return age if age > 0 else 0
    except (socket.timeout, Exception) as e:
        # Log error jika diperlukan
        # print(f"WHOIS timeout for {domain}: {e}")
        pass
    finally:
        # Reset timeout ke default
        socket.setdefaulttimeout(None)
    return 0

def count_suspicious_words(url):
    """Count suspicious words in URL"""
    suspicious_words = [
        'login', 'signin', 'banking', 'secure', 'account', 'update',
        'verify', 'confirm', 'password', 'credit', 'card', 'paypal',
        'amazon', 'ebay', 'facebook', 'google', 'microsoft', 'apple'
    ]
    count = 0
    for word in suspicious_words:
        if word in url:
            count += 1
    return count

def count_redirects(url):
    """Count number of redirects"""
    try:
        response = requests.head(url, allow_redirects=False, timeout=5)
        if response.status_code in [301, 302, 303, 307, 308]:
            return 1
    except:
        pass
    return 0

def check_favicon_domain(url):
    """Check if favicon domain matches main domain"""
    try:
        favicon_url = f"{url}/favicon.ico"
        response = requests.head(favicon_url, timeout=5)
        return 1 if response.status_code == 200 else 0
    except:
        return 0 