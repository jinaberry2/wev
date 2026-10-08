"""밀리초 클릭 타이머용 로컬 측정 프록시.

브라우저가 다른 사이트(예: weverse.io)에 직접 요청을 보내면 CORS 정책 때문에
응답을 읽을 수 없습니다. 이 프록시는 같은 컴퓨터에서 실행되어 대신 요청을
보내고(서버 간 요청은 CORS 제한이 없음) 결과를 돌려줍니다.

실행: python proxy_server.py  (또는 run_proxy.bat / run_proxy.sh 더블클릭)
"""
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = 8787


class Handler(BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")

    def _send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self._send_cors_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == "/health":
            self._send_json(200, {"ok": True})
            return

        if parsed.path != "/measure":
            self._send_json(404, {"ok": False, "error": "unknown path"})
            return

        qs = urllib.parse.parse_qs(parsed.query)
        target = qs.get("url", [None])[0]
        if not target:
            self._send_json(400, {"ok": False, "error": "url 파라미터가 필요합니다."})
            return
        if not (target.startswith("http://") or target.startswith("https://")):
            self._send_json(400, {"ok": False, "error": "http:// 또는 https:// 로 시작하는 주소를 입력하세요."})
            return

        req = urllib.request.Request(
            target,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            },
        )

        try:
            t1 = time.time() * 1000
            try:
                res = urllib.request.urlopen(req, timeout=8)
                headers = res.headers
                status = res.status
            except urllib.error.HTTPError as e:
                # 403/404 등도 응답 헤더(Date 포함)는 유효한 측정 데이터
                headers = e.headers
                status = e.code
            t2 = time.time() * 1000

            server_date = headers.get("Date") if headers else None
            self._send_json(200, {
                "ok": True,
                "t1": t1,
                "t2": t2,
                "serverDate": server_date,
                "status": status,
            })
        except Exception as e:
            self._send_json(200, {"ok": False, "error": str(e)})

    def log_message(self, format, *args):
        pass  # 콘솔에 요청 로그를 찍지 않음


if __name__ == "__main__":
    print(f"로컬 측정 프록시 실행 중: http://localhost:{PORT}")
    print("이 창을 열어둔 채로 index.html에서 측정하세요. (닫으면 프록시가 꺼집니다)")
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
