import requests
import os
import time
import json

# ၁။ စက်ရဲ့ သီးသန့် ID ကို ယူတဲ့အပိုင်း
def get_stable_id():
    # symbols: __pyx_v_device_id, __pyx_v_serial
    try:
        # Android device serial ကို ဖတ်တာဖြစ်ဖို့ များပါတယ်
        device_id = os.popen("getprop ro.serialno").read().strip()
        if not device_id:
            device_id = "0000-0000-0000"
        return device_id
    except Exception:
        return "UNKNOWN_ID"

# ၂။ အင်တာနက် အခြေအနေ စစ်ဆေးခြင်း
def check_real_internet():
    # symbols: __pyx_v_test_url, portal_host
    test_url = "http://connectivitycheck.gstatic.com/generate_204"
    try:
        response = requests.get(test_url, timeout=5)
        # HTTP 204 ဆိုရင် အင်တာနက် အစစ်အမှန် ရနေတာပါ
        return response.status_code == 204
    except:
        return False

# ၃။ Activation Key ကို စစ်ဆေးခြင်း
def verify_activation(input_key):
    # symbols: __pyx_v_auth_link, voucher_api, saved_key
    # ဒီနေရာမှာ Ghidra ထဲက ရှာမတွေ့သေးတဲ့ server link လာပါမယ်
    auth_link = "http://YOUR_ADMIN_SERVER_URL/verify" 
    device_id = get_stable_id()
    
    payload = {
        "key": input_key,
        "device_id": device_id
    }
    
    try:
        # Admin Server ဆီကို key ပို့ပြီး စစ်ခိုင်းတာပါ
        r = requests.post(auth_link, data=payload, timeout=10)
        if r.status_code == 200 and r.json().get("status") == "success":
            return True
    except:
        pass
    return False

# ၄။ Bypass လုပ်ငန်းစဉ် စတင်ခြင်း
def start_process():
    # symbols: __pyx_v_portal_url, gw_addr, gw_port
    print("[*] Checking Internet Connection...")
    if check_real_internet():
        print("[+] Internet is already working.")
    else:
        print("[-] Captive Portal Detected. Starting Bypass...")
        
        # ဒီနေရာမှာ portal login ကိုကျော်မယ့် logic လာပါမယ်
        # ပုံမှန်အားဖြင့် requests.post() နဲ့ portal data တွေ ပို့တာမျိုးပါ
        pass

# Main Logic
if __name__ == "__main__":
    print("=== STARLINK BYPASS TOOL ===")
    
    # symbols: __pyx_v_input_key
    user_key = input("Enter your Activation Key: ")
    
    if verify_activation(user_key):
        print("[+] Activation Successful!")
        start_process()
    else:
        print("[!] Invalid Key. Please contact admin.")
