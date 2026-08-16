import json
from datetime import datetime

class CSAKeySprawlPlaybook:
    """Key Sprawl Management Playbook - ตาม CSA Paper"""
    
    def __init__(self):
        self.playbook = {
            "name": "Key Sprawl Management Playbook",
            "version": "1.0",
            "author": "Kriangkai Khatsom - CSA Reviewer",
            "framework": "CSA CCM v4.1 + NIST SP 800-57",
            "created": datetime.now().isoformat(),
            "phases": []
        }
    
    def build_playbook(self):
        # Phase 1: Discovery
        self.playbook["phases"].append({
            "phase": 1,
            "name": "Discovery & Inventory",
            "objective": "ค้นหา keys ทั้งหมดที่กระจัดกระจาย",
            "steps": [
                "สแกน cloud accounts (AWS/Azure/GCP)",
                "สแกน code repositories (GitHub/GitLab)",
                "สแกน CI/CD pipelines",
                "สแกน SaaS platforms",
                "สแกน environment variables",
                "สแกน shell history",
                "สร้าง inventory รวม"
            ],
            "tools": ["Gitleaks", "TruffleHog", "GitGuardian", "OMEGA Scanner"],
            "output": "csa_key_inventory.json",
            "time": "< 1 ชั่วโมง"
        })
        
        # Phase 2: Consolidation
        self.playbook["phases"].append({
            "phase": 2,
            "name": "Consolidation & Centralization",
            "objective": "รวม keys ทั้งหมดไว้ที่เดียว",
            "steps": [
                "ย้าย keys ทั้งหมดไปไว้ใน vault",
                "ใช้ KMS สำหรับ cloud keys",
                "กำหนด owner ทุก key",
                "ติด tag: environment, classification, expiration",
                "ลบ keys ที่ไม่ใช้แล้ว"
            ],
            "tools": ["HashiCorp Vault", "AWS KMS", "Azure Key Vault"],
            "output": "centralized_vault",
            "time": "< 1 วัน"
        })
        
        # Phase 3: Lifecycle Management
        self.playbook["phases"].append({
            "phase": 3,
            "name": "Lifecycle & Rotation",
            "objective": "จัดการวงจรชีวิต keys อัตโนมัติ",
            "steps": [
                "ตั้ง rotation policy (30/60/90 วัน)",
                "ใช้ short-lived credentials",
                "ปิดใช้งาน keys ที่ไม่ได้ใช้",
                "ทำลาย keys ที่หมดอายุ",
                "บันทึกทุกการเปลี่ยนแปลง"
            ],
            "tools": ["Vault Auto-Rotation", "Cloud KMS"],
            "output": "rotation_schedule",
            "time": "ต่อเนื่อง"
        })
        
        # Phase 4: Monitoring
        self.playbook["phases"].append({
            "phase": 4,
            "name": "Monitoring & Detection",
            "objective": "เฝ้าระวัง key misuse",
            "steps": [
                "ติดตาม key usage logs",
                "ตรวจจับ access จาก IP แปลก",
                "ตรวจจับ key ที่ไม่เคย rotate",
                "ตรวจจับ key ใน GitHub repos",
                "แจ้งเตือนอัตโนมัติ"
            ],
            "tools": ["SIEM", "OMEGA AI", "CloudTrail"],
            "output": "alerts",
            "time": "real-time"
        })
        
        # Phase 5: Incident Response
        self.playbook["phases"].append({
            "phase": 5,
            "name": "Incident Response",
            "objective": "ตอบสนองเมื่อ key รั่วไหล",
            "steps": [
                "1. Detect: พบ key ที่ leaked",
                "2. Confirm: ตรวจสอบว่า key ยัง active",
                "3. Contain: revoke ทันที",
                "4. Assess: ตรวจ blast radius",
                "5. Hunt: หา persistence",
                "6. Remediate: แก้ไขระบบ",
                "7. Report: บันทึก timeline"
            ],
            "tools": ["OMEGA AI", "Playbook Scripts"],
            "output": "incident_report",
            "time": "< 15 นาที"
        })
        
        # Phase 6: Governance
        self.playbook["phases"].append({
            "phase": 6,
            "name": "Governance & Compliance",
            "objective": "รักษามาตรฐานระยะยาว",
            "steps": [
                "Quarterly key reviews",
                "ตรวจ rotation compliance",
                "ตรวจ orphaned keys",
                "อัปเดต policy",
                "รายงานผู้บริหาร"
            ],
            "tools": ["ServiceNow GRC", "Jira"],
            "output": "compliance_report",
            "time": "ทุกไตรมาส"
        })
        
        return self.playbook
    
    def save(self):
        with open("csa_key_sprawl_playbook.json", "w") as f:
            json.dump(self.playbook, f, indent=2, ensure_ascii=False)
        print("✅ Playbook saved: csa_key_sprawl_playbook.json")
    
    def display(self):
        print("═" * 60)
        print("  🔑 CSA KEY SPRAWL MANAGEMENT PLAYBOOK")
        print("═" * 60)
        
        for phase in self.playbook["phases"]:
            print(f"\n📋 Phase {phase['phase']}: {phase['name']}")
            print(f"   วัตถุประสงค์: {phase['objective']}")
            print(f"   เวลา: {phase['time']}")
            print(f"   ขั้นตอน:")
            for step in phase["steps"]:
                print(f"     - {step}")
            print(f"   เครื่องมือ: {', '.join(phase['tools'])}")
        
        print("═" * 60)

if __name__ == "__main__":
    playbook = CSAKeySprawlPlaybook()
    playbook.build_playbook()
    playbook.display()
    playbook.save()
