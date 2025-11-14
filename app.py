from flask import Flask, request, jsonify
import requests, os
from google.oauth2 import service_account
from googleapiclient.discovery import build

app = Flask(__name__)

# تحميل إعدادات من البيئة
BITLY_TOKEN = os.getenv('BITLY_TOKEN', '')
SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_SERVICE_ACCOUNT', 'service_account.json')
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# إعداد Google creds
creds = None
if os.path.exists(SERVICE_ACCOUNT_FILE):
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

@app.route('/')
def index():
    return jsonify({'ok': True, 'service': 'Dropshipping Agent API'})

@app.route('/create_sheet', methods=['POST'])
def create_sheet():
    if creds is None:
        return jsonify({'error': 'service_account.json not found'}), 500
    data = request.json or {}
    title = data.get('title', 'Dropshipping Data')
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets().create(body={'properties': {'title': title}}).execute()
    return jsonify({'spreadsheetId': sheet['spreadsheetId'], 'url': f"https://docs.google.com/spreadsheets/d/{sheet['spreadsheetId']}"})

@app.route('/bitly_shorten', methods=['POST'])
def bitly_shorten():
    if not BITLY_TOKEN:
        return jsonify({'error': 'BITLY_TOKEN not set'}), 500
    data = request.json or {}
    long_url = data.get('url')
    if not long_url:
        return jsonify({'error': 'missing url'}), 400
    resp = requests.post(
        'https://api-ssl.bitly.com/v4/shorten',
        headers={'Authorization': f'Bearer {BITLY_TOKEN}', 'Content-Type': 'application/json'},
        json={'long_url': long_url}
    )
    return jsonify(resp.json()), resp.status_code

@app.route('/fetch_product', methods=['GET'])
def fetch_product():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'no url'}), 400
    try:
        res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=20)
        # مخرجات مبسطة — يمكن تحسينها بـ BeautifulSoup
        return jsonify({'status': res.status_code, 'size': len(res.text), 'sample': res.text[:500]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/notify', methods=['POST'])
def notify():
    data = request.json or {}
    # هنا يمكنك ربط بوت Telegram أو بريد لإرسال الإشعار الفعلي
    print('Approval request received:', data)
    return jsonify({'received': True, 'message': 'approval logged'})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)