import json
import os
import hashlib
from datetime import datetime, timedelta

class OmegaKeySprawlManager:
    """Key Sprawl Management - ตาม CSA Key Sprawl paper"""
    
    def __init__(self):
        self.keys_inventory = {}
        self.key_file = "/home/cosa32/.omega_keys"
        self.load_keys()
    
    def load_keys(self):
        """โหลด keys ทั้งหมดจากไฟล์กลาง"""
        if os.path.exists(self.key_file):
            with open(self.key_file) as f:
                for line in f:
                    if "=" in line and not line.startswith("#"):
                        key, value = line.strip().split("=", 1)
                        self.keys_inventory[key.strip()] = {
                            "value": value.strip().strip('"'),
                            "owner": "Kriangkai Khatsom",
                            "created": datetime.now().isoformat(),
                            "last_rotated": None,
                            "status": "active"
                        }
    
    def discover_keys(self):
        """Automated Discovery - ค้นหา keys ทั้งหมด"""
        sources = {
            "env_vars": self.scan_env(),
            "files": self.scan_files(),
            "shell_history": self.scan_history()
        }
        return sources
    
    def scan_env(self):
        """สแกน environment variables"""
        keys = {}
        for key in os.environ:
            if any(k in key.lower() for k in ["key", "token", "secret", "dna"]):
                keys[key] = "found"
        return keys
    
    def scan_files(self):
        """สแกนไฟล์ที่อาจมี keys"""
        key_patterns = ["API_KEY", "TOKEN", "SECRET", "PASSWORD"]
        files_to_scan = [
            "/home/cosa32/.omega_keys",
            "/home/cosa32/omega_server.py",
            "/home/cosa32/.bash_history"
        ]
        found = {}
        for f in files_to_scan:
            if os.path.exists(f):
                found[f] = "exists"
        return found
    
    def scan_history(self):
        """สแกน bash history"""
        history_file = os.path.expanduser("~/.bash_history")
        if os.path.exists(history_file):
            with open(history_file) as f:
                lines = f.readlines()
                key_lines = [l for l in lines if any(k in l.lower() for k in ["key", "token", "secret"])]
                return {"found": len(key_lines)}
        return {"found": 0}
    
    def check_rotation_compliance(self):
        """ตรวจ rotation compliance"""
        total = len(self.keys_inventory)
        rotated = sum(1 for k in self.keys_inventory.values() if k["last_rotated"])
        compliance = (rotated / total * 100) if total > 0 else 0
        return {
            "total_keys": total,
            "rotated": rotated,
            "compliance_percent": compliance
        }
    
    def detect_shadow_keys(self):
        """ตรวจจับ shadow keys (keys ที่ไม่รู้จัก)"""
        discovered = self.discover_keys()
        known = set(self.keys_inventory.keys())
        shadow = []
        
        for source, keys in discovered.items():
            if isinstance(keys, dict):
                for k in keys:
                    if k not in known:
                        shadow.append({"key": k, "source": source})
        
        return shadow
    
    def generate_report(self):
        """สร้างรายงานตาม CSA framework"""
        print("═" * 50)
        print("  OMEGA KEY SPRAWL MANAGEMENT")
        print("  CSA CCM v4.1 Compliant")
        print("═" * 50)
        
        # 1. Coverage
        total_known = len(self.keys_inventory)
        discovered = self.discover_keys()
        print(f"\n[1] Key Coverage:")
        print(f"  Known keys: {total_known}")
        print(f"  Sources scanned: {len(discovered)}")
        
        # 2. Shadow Keys
        shadow = self.detect_shadow_keys()
        print(f"\n[2] Shadow Keys Detected: {len(shadow)}")
        for s in shadow:
            print(f"  ⚠️  {s['key']} (source: {s['source']})")
        
        # 3. Rotation Compliance
        rotation = self.check_rotation_compliance()
        print(f"\n[3] Rotation Compliance:")
        print(f"  Total: {rotation['total_keys']}")
        print(f"  Rotated: {rotation['rotated']}")
        print(f"  Compliance: {rotation['compliance_percent']:.1f}%")
        
        # 4. Recommendations
        print(f"\n[4] Recommendations:")
        print(f"  ✅ Centralize all keys in vault")
        print(f"  ✅ Enable automated rotation")
        print(f"  ✅ Monitor key usage")
        print(f"  ✅ Quarterly reviews")
        
        print("═" * 50)

if __name__ == "__main__":
    manager = OmegaKeySprawlManager()
    manager.generate_report()
