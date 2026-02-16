import re
import pandas as pd
from typing import Dict, List
from email_validator import validate_email, EmailNotValidError

class EmailProcessor:
    def __init__(self):
        # Spam keywords in Indonesian and English
        self.spam_keywords = [
            # Indonesian spam words
            'menang', 'hadiah', 'undian', 'lotre', 'jackpot', 'kaya', 'uang',
            'dollar', 'rupiah', 'transfer', 'bank', 'pinjaman', 'kredit',
            'gratis', 'free', 'discount', 'diskon', 'promo', 'promosi',
            'urgent', 'penting', 'segera', 'terbatas', 'limited', 'terakhir',
            'last', 'chance', 'kesempatan', 'beruntung', 'lucky', 'winner',
            'pemenang', 'million', 'juta', 'billion', 'miliar', 'cash',
            'tunai', 'prize', 'hadiah', 'reward', 'imbalan', 'bonus',
            
            # English spam words
            'winner', 'won', 'prize', 'money', 'cash', 'million', 'billion',
            'dollar', 'free', 'urgent', 'limited', 'offer', 'discount',
            'credit', 'loan', 'bank', 'transfer', 'account', 'password',
            'verify', 'confirm', 'update', 'security', 'suspended', 'blocked',
            'unlock', 'activate', 'claim', 'inheritance', 'lottery', 'jackpot',
            'investment', 'profit', 'earn', 'income', 'wealth', 'rich',
            'exclusive', 'vip', 'premium', 'special', 'unique', 'amazing',
            'incredible', 'unbelievable', 'shocking', 'secret', 'hidden'
        ]
        
        # Suspicious patterns
        self.suspicious_patterns = [
            r'\b\d{10,}\b',  # Long numbers
            r'\b[A-Z]{5,}\b',  # All caps words
            r'\$\d+',  # Dollar amounts
            r'\b\d{1,3}(,\d{3})*\b',  # Numbers with commas
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',  # URLs
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email addresses
        ]
        
        # Legitimate domains (example)
        self.legitimate_domains = [
            'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
            'google.com', 'microsoft.com', 'apple.com', 'amazon.com',
            'facebook.com', 'twitter.com', 'linkedin.com', 'instagram.com'
        ]
    
    def analyze_email(self, email_content: str, sender_email: str = "") -> Dict:
        """
        Analisis email untuk deteksi spam/palsu
        """
        result = {
            'is_spam': False,
            'spam_score': 0,
            'issues': [],
            'features': {},
            'recommendations': []
        }
        
        # Extract features
        features = self._extract_features(email_content, sender_email)
        result['features'] = features
        
        # Calculate spam score
        spam_score = 0
        
        # Check sender email
        if sender_email:
            sender_analysis = self._analyze_sender(sender_email)
            spam_score += sender_analysis['score']
            result['issues'].extend(sender_analysis['issues'])
        
        # Check content features
        if features['spam_keyword_count'] > 5:
            spam_score += 30
            result['issues'].append(f"Mengandung {features['spam_keyword_count']} kata spam")
        
        if features['suspicious_pattern_count'] > 3:
            spam_score += 25
            result['issues'].append(f"Mengandung {features['suspicious_pattern_count']} pola mencurigakan")
        
        if features['all_caps_ratio'] > 0.3:
            spam_score += 20
            result['issues'].append("Terlalu banyak huruf kapital")
        
        if features['exclamation_count'] > 5:
            spam_score += 15
            result['issues'].append("Terlalu banyak tanda seru")
        
        if features['url_count'] > 3:
            spam_score += 20
            result['issues'].append("Terlalu banyak link")
        
        if features['number_count'] > 10:
            spam_score += 15
            result['issues'].append("Terlalu banyak angka")
        
        if features['length'] < 50:
            spam_score += 10
            result['issues'].append("Email terlalu pendek")
        
        if features['length'] > 2000:
            spam_score += 10
            result['issues'].append("Email terlalu panjang")
        
        # Set result
        result['spam_score'] = min(spam_score, 100)
        result['is_spam'] = spam_score >= 50
        
        # Generate recommendations
        result['recommendations'] = self._generate_recommendations(result)
        
        return result
    
    def _extract_features(self, email_content: str, sender_email: str) -> Dict:
        """Extract features from email content"""
        features = {
            'length': len(email_content),
            'word_count': len(email_content.split()),
            'spam_keyword_count': 0,
            'suspicious_pattern_count': 0,
            'all_caps_ratio': 0,
            'exclamation_count': email_content.count('!'),
            'question_count': email_content.count('?'),
            'url_count': len(re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', email_content)),
            'number_count': len(re.findall(r'\d+', email_content)),
            'email_count': len(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email_content))
        }
        
        # Count spam keywords
        content_lower = email_content.lower()
        for keyword in self.spam_keywords:
            if keyword.lower() in content_lower:
                features['spam_keyword_count'] += 1
        
        # Count suspicious patterns
        for pattern in self.suspicious_patterns:
            matches = re.findall(pattern, email_content)
            features['suspicious_pattern_count'] += len(matches)
        
        # Calculate all caps ratio
        words = email_content.split()
        if words:
            all_caps_words = sum(1 for word in words if word.isupper() and len(word) > 2)
            features['all_caps_ratio'] = all_caps_words / len(words)
        
        return features
    
    def _analyze_sender(self, sender_email: str) -> Dict:
        """Analyze sender email address"""
        result = {
            'score': 0,
            'issues': []
        }
        
        try:
            # Validate email format
            valid = validate_email(sender_email)
            email = valid.email
            
            # Extract domain
            domain = email.split('@')[1]
            
            # Check if domain is legitimate
            if domain not in self.legitimate_domains:
                result['score'] += 15
                result['issues'].append(f"Domain pengirim tidak dikenal: {domain}")
            
            # Check for suspicious patterns in email
            if re.search(r'\d{4,}', email):
                result['score'] += 10
                result['issues'].append("Email mengandung banyak angka")
            
            if re.search(r'[A-Z]{3,}', email):
                result['score'] += 5
                result['issues'].append("Email mengandung huruf kapital berlebihan")
            
        except EmailNotValidError:
            result['score'] += 25
            result['issues'].append("Format email tidak valid")
        
        return result
    
    def _generate_recommendations(self, analysis_result: Dict) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        if analysis_result['is_spam']:
            recommendations.append("⚠️ Email ini kemungkinan besar adalah spam")
            recommendations.append("Jangan klik link atau lampiran dalam email ini")
            recommendations.append("Jangan berikan informasi pribadi")
            recommendations.append("Hapus email ini dan blokir pengirim")
        else:
            recommendations.append("✅ Email ini tampak aman")
            recommendations.append("Tetap waspada terhadap link mencurigakan")
            recommendations.append("Verifikasi pengirim jika ragu")
        
        if analysis_result['features']['url_count'] > 0:
            recommendations.append("🔗 Periksa semua link sebelum diklik")
        
        if analysis_result['features']['spam_keyword_count'] > 0:
            recommendations.append("📝 Email mengandung kata-kata yang sering digunakan dalam spam")
        
        return recommendations
    
    def get_spam_level(self, spam_score: int) -> str:
        """Get spam level description based on score"""
        if spam_score >= 80:
            return 'Sangat Tinggi'
        elif spam_score >= 60:
            return 'Tinggi'
        elif spam_score >= 40:
            return 'Sedang'
        elif spam_score >= 20:
            return 'Rendah'
        else:
            return 'Aman' 