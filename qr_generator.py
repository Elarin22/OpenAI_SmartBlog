import qrcode
import requests
import os
import sys
from datetime import datetime

# ngrok API에서 현재 터널 URL 가져오기
def get_ngrok_url():
    try:
        print("🔍 ngrok 터널 정보를 확인 중...")
        response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
        data = response.json()
        
        if data.get('tunnels'):
            for tunnel in data['tunnels']:
                # HTTPS 터널 찾기
                if tunnel['proto'] == 'https':
                    public_url = tunnel['public_url']
                    print(f"✅ ngrok 터널 발견: {public_url}")
                    return public_url
            
            # HTTPS가 없으면 첫 번째 터널 사용
            public_url = data['tunnels'][0]['public_url']
            print(f"✅ 터널 발견: {public_url}")
            return public_url
        else:
            print("❌ 활성화된 ngrok 터널이 없습니다.")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ ngrok이 실행되지 않았습니다. 먼저 'ngrok http 8000'을 실행하세요.")
        return None
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return None

# QR 코드 생성
def generate_qr_code(url):
    try:
        print("📱 QR 코드 생성 중...")
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        
        # 파일명에 타임스탬프 추가
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"smartblog_qr_{timestamp}.png"
        
        # 현재 디렉토리에 저장
        img.save(filename)
        
        print(f"✅ QR 코드 저장 완료: {filename}")
        print(f"📱 휴대폰 카메라로 스캔하세요!")
        
        return filename
        
    except Exception as e:
        print(f"❌ QR 코드 생성 실패: {e}")
        return None

def create_html_page(url, qr_filename):
    # HTML<브라우저> QR코드 페이지 생성
    html_content = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Blog QR 코드</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            text-align: center;
            background: linear-gradient(135deg, #f9a8d4, #ec4899);
            min-height: 100vh;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #ec4899;
            margin-bottom: 20px;
        }}
        .qr-code {{
            margin: 20px 0;
        }}
        .url {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            word-break: break-all;
            font-family: monospace;
        }}
        .instructions {{
            color: #666;
            margin-top: 20px;
        }}
        a {{
            color: #ec4899;
            text-decoration: none;
            font-weight: bold;
        }}
        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Smart Blog 접속</h1>
        
        <div class="qr-code">
            <img src="{qr_filename}" alt="QR Code" style="max-width: 300px;">
        </div>
        
        <div class="url">
            <strong>접속 주소:</strong><br>
            <a href="{url}" target="_blank">{url}</a>
        </div>
        
        <div class="instructions">
            <p>📱 <strong>휴대폰 접속 방법:</strong></p>
            <p>1. 휴대폰 카메라로 위 QR 코드 스캔</p>
            <p>2. 또는 위 URL을 복사해서 브라우저에 입력</p>
            <p>3. Smart Blog를 모바일에서 체험하세요!</p>
        </div>
        
        <p style="margin-top: 30px; color: #888; font-size: 12px;">
            생성 시간: {datetime.now().strftime("%Y년 %m월 %d일 %H:%M:%S")}
        </p>
    </div>
</body>
</html>
"""
    
    html_filename = f"smartblog_qr_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    
    try:
        with open(html_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ HTML 페이지 생성: {html_filename}")
        return html_filename
    except Exception as e:
        print(f"❌ HTML 페이지 생성 실패: {e}")
        return None

# 생성된 파일 자동으로 열기
def open_file(filename):
    try:
        if sys.platform.startswith('win'):
            os.startfile(filename)
        elif sys.platform.startswith('darwin'):  # macOS 환경
            os.system(f'open {filename}')
        else: # Linux 환경
            os.system(f'xdg-open {filename}')
    except Exception as e:
        print(f"⚠️ 파일 자동 열기 실패: {e}")

def main():
    print("=" * 50)
    print("🚀 Smart Blog QR 코드 생성기")
    print("=" * 50)
    
    # ngrok URL 가져오기
    url = get_ngrok_url()
    if not url:
        print("\n❌ 실행 순서:")
        print("1. 터미널에서: python manage.py runserver 8000")
        print("2. 새 터미널에서: ngrok http 8000")
        print("3. 다시 이 스크립트 실행: python qr_generator.py")
        return
    
    # QR 코드 생성
    qr_filename = generate_qr_code(url)
    if not qr_filename:
        return
    
    # HTML 페이지 생성
    html_filename = create_html_page(url, qr_filename)
    
    print("\n" + "=" * 50)
    print("✅ 완료!")
    print("=" * 50)
    print(f"🔗 Smart Blog 주소: {url}")
    print(f"📱 QR 코드 파일: {qr_filename}")
    if html_filename:
        print(f"🌐 HTML 페이지: {html_filename}")
    
    print("\n📱 모바일 접속 방법:")
    print("• QR 코드를 휴대폰 카메라로 스캔")
    print("• 또는 위 URL을 휴대폰 브라우저에 입력")
    
    # HTML 파일 자동으로 열기
    if html_filename:
        print(f"\n🌐 브라우저에서 {html_filename} 열기 중...")
        open_file(html_filename)

if __name__ == "__main__":
    main()