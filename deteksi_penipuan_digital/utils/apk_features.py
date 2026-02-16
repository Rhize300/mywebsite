import os
import zipfile
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional
import re

class APKAnalyzer:
    def __init__(self):
        # Suspicious permissions
        self.suspicious_permissions = [
            'android.permission.READ_PHONE_STATE',
            'android.permission.READ_CONTACTS',
            'android.permission.READ_SMS',
            'android.permission.SEND_SMS',
            'android.permission.RECORD_AUDIO',
            'android.permission.CAMERA',
            'android.permission.ACCESS_FINE_LOCATION',
            'android.permission.ACCESS_COARSE_LOCATION',
            'android.permission.READ_EXTERNAL_STORAGE',
            'android.permission.WRITE_EXTERNAL_STORAGE',
            'android.permission.SYSTEM_ALERT_WINDOW',
            'android.permission.REQUEST_INSTALL_PACKAGES',
            'android.permission.INSTALL_PACKAGES',
            'android.permission.DELETE_PACKAGES',
            'android.permission.ACCESS_SUPERUSER',
            'android.permission.WRITE_SECURE_SETTINGS',
            'android.permission.WRITE_SETTINGS',
            'android.permission.MODIFY_PHONE_STATE',
            'android.permission.INTERNET',
            'android.permission.ACCESS_NETWORK_STATE',
            'android.permission.ACCESS_WIFI_STATE',
            'android.permission.CHANGE_WIFI_STATE',
            'android.permission.ACCESS_BLUETOOTH',
            'android.permission.BLUETOOTH_ADMIN'
        ]
        
        # Dangerous permissions (high risk)
        self.dangerous_permissions = [
            'android.permission.READ_PHONE_STATE',
            'android.permission.READ_CONTACTS',
            'android.permission.READ_SMS',
            'android.permission.SEND_SMS',
            'android.permission.RECORD_AUDIO',
            'android.permission.CAMERA',
            'android.permission.ACCESS_FINE_LOCATION',
            'android.permission.ACCESS_COARSE_LOCATION',
            'android.permission.READ_EXTERNAL_STORAGE',
            'android.permission.WRITE_EXTERNAL_STORAGE'
        ]
        
        # Known malicious package names
        self.malicious_packages = [
            'com.fake.banking',
            'com.scam.wallet',
            'com.malware.trojan',
            'com.spyware.tracker'
        ]
    
    def analyze_apk(self, apk_path: str) -> Dict:
        """
        Analisis file APK untuk deteksi malware
        """
        result = {
            'is_malicious': False,
            'risk_score': 0,
            'issues': [],
            'features': {},
            'recommendations': []
        }
        
        try:
            # Extract APK features
            features = self._extract_apk_features(apk_path)
            result['features'] = features
            
            # Calculate risk score
            risk_score = 0
            
            # Check permissions
            if features['dangerous_permission_count'] > 5:
                risk_score += 30
                result['issues'].append(f"Menggunakan {features['dangerous_permission_count']} permission berbahaya")
            
            if features['suspicious_permission_count'] > 10:
                risk_score += 25
                result['issues'].append(f"Menggunakan {features['suspicious_permission_count']} permission mencurigakan")
            
            # Check package name
            if features['package_name'] in self.malicious_packages:
                risk_score += 50
                result['issues'].append("Package name terdaftar sebagai malware")
            
            # Check app size
            if features['app_size'] < 1000000:  # Less than 1MB
                risk_score += 10
                result['issues'].append("Ukuran aplikasi terlalu kecil (mencurigakan)")
            
            if features['app_size'] > 100000000:  # More than 100MB
                risk_score += 5
                result['issues'].append("Ukuran aplikasi sangat besar")
            
            # Check version
            if features['version_code'] < 1:
                risk_score += 15
                result['issues'].append("Version code tidak valid")
            
            # Check activities
            if features['activity_count'] == 0:
                risk_score += 20
                result['issues'].append("Tidak memiliki activity (mencurigakan)")
            
            # Check services
            if features['service_count'] > 5:
                risk_score += 15
                result['issues'].append("Terlalu banyak service")
            
            # Check receivers
            if features['receiver_count'] > 10:
                risk_score += 10
                result['issues'].append("Terlalu banyak receiver")
            
            # Check providers
            if features['provider_count'] > 3:
                risk_score += 10
                result['issues'].append("Terlalu banyak content provider")
            
            # Set result
            result['risk_score'] = min(risk_score, 100)
            result['is_malicious'] = risk_score >= 50
            
            # Generate recommendations
            result['recommendations'] = self._generate_recommendations(result)
            
        except Exception as e:
            result['issues'].append(f"Error analyzing APK: {str(e)}")
            result['risk_score'] = 100
            result['is_malicious'] = True
        
        return result
    
    def _extract_apk_features(self, apk_path: str) -> Dict:
        """Extract features from APK file"""
        features = {
            'app_name': '',
            'package_name': '',
            'version_name': '',
            'version_code': 0,
            'app_size': 0,
            'permission_count': 0,
            'dangerous_permission_count': 0,
            'suspicious_permission_count': 0,
            'activity_count': 0,
            'service_count': 0,
            'receiver_count': 0,
            'provider_count': 0,
            'permissions': [],
            'activities': [],
            'services': [],
            'receivers': [],
            'providers': []
        }
        
        # Get file size
        features['app_size'] = os.path.getsize(apk_path)
        
        # Extract APK contents
        with zipfile.ZipFile(apk_path, 'r') as apk_zip:
            # Find AndroidManifest.xml
            manifest_path = None
            for file_info in apk_zip.filelist:
                if file_info.filename.endswith('AndroidManifest.xml'):
                    manifest_path = file_info.filename
                    break
            
            if manifest_path:
                # Read and parse manifest
                manifest_data = apk_zip.read(manifest_path)
                self._parse_manifest(manifest_data, features)
        
        return features
    
    def _parse_manifest(self, manifest_data: bytes, features: Dict):
        """Parse AndroidManifest.xml"""
        try:
            # This is a simplified parser - in real implementation, you'd use proper APK parsing
            manifest_text = manifest_data.decode('utf-8', errors='ignore')
            
            # Extract package name
            package_match = re.search(r'package="([^"]+)"', manifest_text)
            if package_match:
                features['package_name'] = package_match.group(1)
            
            # Extract version
            version_match = re.search(r'android:versionName="([^"]+)"', manifest_text)
            if version_match:
                features['version_name'] = version_match.group(1)
            
            version_code_match = re.search(r'android:versionCode="(\d+)"', manifest_text)
            if version_code_match:
                features['version_code'] = int(version_code_match.group(1))
            
            # Extract app name
            app_name_match = re.search(r'android:label="([^"]+)"', manifest_text)
            if app_name_match:
                features['app_name'] = app_name_match.group(1)
            
            # Count permissions
            permissions = re.findall(r'android:name="([^"]+)"', manifest_text)
            features['permissions'] = permissions
            features['permission_count'] = len(permissions)
            
            # Count dangerous permissions
            dangerous_count = sum(1 for perm in permissions if perm in self.dangerous_permissions)
            features['dangerous_permission_count'] = dangerous_count
            
            # Count suspicious permissions
            suspicious_count = sum(1 for perm in permissions if perm in self.suspicious_permissions)
            features['suspicious_permission_count'] = suspicious_count
            
            # Count components
            features['activity_count'] = len(re.findall(r'<activity', manifest_text))
            features['service_count'] = len(re.findall(r'<service', manifest_text))
            features['receiver_count'] = len(re.findall(r'<receiver', manifest_text))
            features['provider_count'] = len(re.findall(r'<provider', manifest_text))
            
        except Exception as e:
            # If parsing fails, set default values
            features['package_name'] = 'unknown'
            features['version_name'] = 'unknown'
            features['version_code'] = 0
            features['app_name'] = 'unknown'
    
    def _generate_recommendations(self, analysis_result: Dict) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        if analysis_result['is_malicious']:
            recommendations.append("⚠️ APK ini kemungkinan besar berbahaya")
            recommendations.append("Jangan install aplikasi ini")
            recommendations.append("Hapus file APK dari perangkat")
            recommendations.append("Scan perangkat dengan antivirus")
        else:
            recommendations.append("✅ APK ini tampak aman")
            recommendations.append("Tetap waspada saat memberikan permission")
            recommendations.append("Install hanya dari sumber terpercaya")
        
        features = analysis_result['features']
        
        if features['dangerous_permission_count'] > 0:
            recommendations.append(f"🔒 Aplikasi meminta {features['dangerous_permission_count']} permission berbahaya")
        
        if features['suspicious_permission_count'] > 0:
            recommendations.append(f"⚠️ Aplikasi meminta {features['suspicious_permission_count']} permission mencurigakan")
        
        if features['activity_count'] == 0:
            recommendations.append("🚨 Aplikasi tidak memiliki activity (sangat mencurigakan)")
        
        return recommendations
    
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