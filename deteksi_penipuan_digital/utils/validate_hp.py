import re
import pandas as pd
from typing import Dict, List, Tuple

class PhoneNumberValidator:
    def __init__(self):
        self.suspicious_patterns = [
            r'^(\+62|62|0)8[1-9][0-9]{6,9}$',  # Indonesian mobile numbers
            r'^(\+62|62|0)2[1-9][0-9]{6,8}$',  # Indonesian landline
        ]
        
        # Known scam numbers (example data)
        self.known_scam_numbers = [
            '+6281234567890',
            '+6289876543210',
            '081234567890',
            '089876543210'
        ]
        
        # Suspicious patterns in number
        self.suspicious_sequences = [
            '1234567890',
            '0987654321',
            '1111111111',
            '0000000000',
            '9999999999'
        ]
    
    def validate_phone_number(self, phone_number: str) -> Dict:
        """
        Validasi nomor telepon dan deteksi kemungkinan penipuan
        """
        result = {
            'is_valid': False,
            'is_suspicious': False,
            'risk_score': 0,
            'issues': [],
            'formatted_number': '',
            'country_code': '',
            'number_type': ''
        }
        
        # Clean the phone number
        cleaned_number = self._clean_phone_number(phone_number)
        result['formatted_number'] = cleaned_number
        
        # Basic validation
        if not self._is_valid_format(cleaned_number):
            result['issues'].append('Format nomor tidak valid')
            return result
        
        result['is_valid'] = True
        
        # Check for suspicious patterns
        risk_score = 0
        
        # Check if it's a known scam number
        if cleaned_number in self.known_scam_numbers:
            result['is_suspicious'] = True
            result['risk_score'] = 100
            result['issues'].append('Nomor terdaftar sebagai nomor penipuan')
            return result
        
        # Check for suspicious sequences
        if self._has_suspicious_sequence(cleaned_number):
            risk_score += 30
            result['issues'].append('Mengandung pola mencurigakan')
        
        # Check for repeated digits
        if self._has_repeated_digits(cleaned_number):
            risk_score += 20
            result['issues'].append('Mengandung digit berulang')
        
        # Check for sequential digits
        if self._has_sequential_digits(cleaned_number):
            risk_score += 25
            result['issues'].append('Mengandung digit berurutan')
        
        # Check number length
        if len(cleaned_number) < 10 or len(cleaned_number) > 15:
            risk_score += 15
            result['issues'].append('Panjang nomor tidak standar')
        
        # Determine country code and number type
        result['country_code'] = self._get_country_code(cleaned_number)
        result['number_type'] = self._get_number_type(cleaned_number)
        
        # Set risk level
        result['risk_score'] = min(risk_score, 100)
        result['is_suspicious'] = risk_score >= 50
        
        return result
    
    def _clean_phone_number(self, phone_number: str) -> str:
        """Clean phone number from special characters"""
        return re.sub(r'[^\d+]', '', phone_number)
    
    def _is_valid_format(self, phone_number: str) -> bool:
        """Check if phone number has valid format"""
        # Remove country code for basic validation
        number = phone_number.replace('+62', '').replace('62', '')
        if number.startswith('0'):
            number = number[1:]
        
        # Check if it's a valid Indonesian mobile number
        if len(number) >= 9 and len(number) <= 12:
            if number.startswith('8') and number[1] in '123456789':
                return True
        
        return False
    
    def _has_suspicious_sequence(self, phone_number: str) -> bool:
        """Check for suspicious digit sequences"""
        number = phone_number.replace('+', '').replace('62', '').replace('0', '', 1)
        
        for sequence in self.suspicious_sequences:
            if sequence in number:
                return True
        return False
    
    def _has_repeated_digits(self, phone_number: str) -> bool:
        """Check for repeated digits"""
        number = phone_number.replace('+', '').replace('62', '').replace('0', '', 1)
        
        # Check for 4 or more repeated digits
        for i in range(len(number) - 3):
            if number[i] == number[i+1] == number[i+2] == number[i+3]:
                return True
        return False
    
    def _has_sequential_digits(self, phone_number: str) -> bool:
        """Check for sequential digits"""
        number = phone_number.replace('+', '').replace('62', '').replace('0', '', 1)
        
        # Check for 4 or more sequential digits
        for i in range(len(number) - 3):
            try:
                if (int(number[i+1]) == int(number[i]) + 1 and
                    int(number[i+2]) == int(number[i]) + 2 and
                    int(number[i+3]) == int(number[i]) + 3):
                    return True
                if (int(number[i+1]) == int(number[i]) - 1 and
                    int(number[i+2]) == int(number[i]) - 2 and
                    int(number[i+3]) == int(number[i]) - 3):
                    return True
            except ValueError:
                continue
        return False
    
    def _get_country_code(self, phone_number: str) -> str:
        """Extract country code from phone number"""
        if phone_number.startswith('+62'):
            return '+62'
        elif phone_number.startswith('62'):
            return '62'
        elif phone_number.startswith('0'):
            return '+62'
        else:
            return 'Unknown'
    
    def _get_number_type(self, phone_number: str) -> str:
        """Determine the type of phone number"""
        number = phone_number.replace('+', '').replace('62', '').replace('0', '', 1)
        
        if number.startswith('8'):
            return 'Mobile'
        elif number.startswith('2'):
            return 'Landline'
        else:
            return 'Unknown'
    
    def add_scam_number(self, phone_number: str):
        """Add a new scam number to the database"""
        cleaned_number = self._clean_phone_number(phone_number)
        if cleaned_number not in self.known_scam_numbers:
            self.known_scam_numbers.append(cleaned_number)
    
    def get_risk_level(self, risk_score: int) -> str:
        """Get risk level description based on score"""
        if risk_score >= 80:
            return 'Sangat Tinggi'
        elif risk_score >= 60:
            return 'Tinggi'
        elif risk_score >= 40:
            return 'Sedang'
        elif risk_score >= 20:
            return 'Rendah'
        else:
            return 'Aman' 