from flask import Flask, jsonify, request
import requests
import random
import base64

app = Flask(__name__)

# إعدادات API الخارجي
api_url = "https://ippocloud.com/api/v1/voucher/google-play/check_code"
headers = {
    "Authorization": "Basic d27ecee55e78cb346aca783d918935c1",
    "Content-Type": "application/json"
}

# إعدادات المفتاح وكلمة المرور
API_KEY = 'byte'
PASSWORD = 'BYTE11'

# دالة لتوليد كود جوجل بلاي عشوائي بطول UCS7-GL3Q-IPEU-OGCM-OFWE
def generate_code():
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    code = '-'.join(''.join(random.choice(characters) for _ in range(4)) for _ in range(5))
    return code

# دالة للتحقق من الكود باستخدام API الخارجي
def check_code(code):
    data = {"code": code}
    response = requests.post(api_url, headers=headers, json=data)
    
    if response.status_code == 200:
        return {"code": code, "valid": True}
    elif response.status_code == 404:
        return {"code": code, "valid": False}
    else:
        return {"code": code, "valid": None, "error": response.status_code}

# نقطة نهاية لاستلام طلب GET والتحقق من الأكواد
@app.route('/check_codes', methods=['GET'])
def check_codes():
    # التحقق من صحة المفتاح وكلمة المرور
    key = request.args.get('key')
    password = request.args.get('password')
    if key != API_KEY or password != PASSWORD:
        return jsonify({"error": "Unauthorized access"}), 403

    # عدد الأكواد المطلوب
    count = min(max(int(request.args.get('count', 1)), 1), 20)

    # إنشاء أكواد وتحقق من صحتها
    codes_status = [check_code(generate_code()) for _ in range(count)]

    # سرعة الاستجابة العشوائية
    response_time = round(random.uniform(0.5, 2.0), 2)

    # إنشاء استجابة JSON
    response = {
        "by": "Byte team BOT",
        "message": "Games Modder 🇪🇬💗",
        "api_response_time": f"{response_time} seconds",
        "codes": codes_status
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)