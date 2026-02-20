#!/usr/bin/env python3
import json
import os
import secrets
import string
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Lock
from urllib.parse import parse_qs, urlparse

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8787"))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.getenv("DATA_DIR", BASE_DIR)
CODES_FILE = os.path.join(DATA_DIR, "redeem_codes.json")
ASSESSMENTS_FILE = os.path.join(DATA_DIR, "assessment_sessions.json")
SEED_CODES_FILE = os.path.join(BASE_DIR, "redeem_codes.json")
SEED_ASSESSMENTS_FILE = os.path.join(BASE_DIR, "assessment_sessions.json")
SUPER_CODE = "INLIGHT"
LOCK = Lock()
SENSITIVE_EXACT_PATHS = {
    "/redeem_codes.json",
    "/assessment_sessions.json",
    "/render.yaml",
    "/vercel.json",
    "/server.py",
    "/redeem_codes.txt",
}
SENSITIVE_EXTENSIONS = (".json", ".py", ".yaml", ".yml", ".md", ".txt", ".log")


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def gen_code(length=8):
    alphabet = string.ascii_uppercase + string.digits
    while True:
        code = "".join(secrets.choice(alphabet) for _ in range(length))
        if any(ch.isalpha() for ch in code) and any(ch.isdigit() for ch in code):
            return code


def gen_id(prefix):
    return f"{prefix}_{secrets.token_urlsafe(10)}"


def normalize_code(raw):
    raw = (raw or "").strip().upper()
    return "".join(ch for ch in raw if ch.isalnum())


def type_from_scores(scores):
    if not isinstance(scores, dict):
        return ""
    pairs = [("E", "I"), ("S", "N"), ("T", "F"), ("J", "P")]
    result = []
    for left, right in pairs:
        lv = int(scores.get(left, 0) or 0)
        rv = int(scores.get(right, 0) or 0)
        result.append(left if lv >= rv else right)
    return "".join(result)


def init_files():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(CODES_FILE):
        if os.path.exists(SEED_CODES_FILE):
            save_json(CODES_FILE, load_json(SEED_CODES_FILE))
        else:
            data = {}
            while len(data) < 200:
                code = gen_code(8)
                data[code] = {
                    "self_used": 0,
                    "peer_used": 0,
                    "total_used": 0,
                    "assessment_id": None,
                    "updated_at": now_iso(),
                }
            save_json(CODES_FILE, data)

    if not os.path.exists(ASSESSMENTS_FILE):
        if os.path.exists(SEED_ASSESSMENTS_FILE):
            save_json(ASSESSMENTS_FILE, load_json(SEED_ASSESSMENTS_FILE))
        else:
            save_json(ASSESSMENTS_FILE, {})


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def make_resp(ok, msg="", extra=None):
    payload = {"ok": ok, "msg": msg}
    if extra:
        payload.update(extra)
    return payload


def sanitize_scores(raw_scores):
    if not isinstance(raw_scores, dict):
        return None
    dims = ["E", "I", "S", "N", "T", "F", "J", "P"]
    out = {}
    try:
        for dim in dims:
            out[dim] = int(raw_scores.get(dim, 0))
    except Exception:
        return None
    return out


def find_assessment_by_token(assessments, invite_token):
    for aid, item in assessments.items():
        if item.get("invite_token") == invite_token:
            return aid, item
    return None, None


def find_latest_open_super_assessment(assessments):
    # 超级码直连他评时，兜底选择最近一条“已完成自评且未完成他评”的会话
    candidates = []
    for aid, item in assessments.items():
        if item.get("code") != SUPER_CODE:
            continue
        if not item.get("self_submitted"):
            continue
        if item.get("peer_submitted"):
            continue
        candidates.append((item.get("updated_at", ""), aid, item))
    if not candidates:
        return None, None
    candidates.sort(key=lambda x: x[0], reverse=True)
    _, aid, item = candidates[0]
    return aid, item


def find_best_assessment_for_code(assessments, code):
    """
    当兑换码映射的 assessment_id 失效或滞后时，兜底回溯该兑换码关联会话。
    优先级：
    1) 已完成自评且未完成他评（可直接进入他评）
    2) 已完成自评（已完成他评也允许用于查看结果）
    """
    open_candidates = []
    submitted_candidates = []
    for aid, item in assessments.items():
        if item.get("code") != code:
            continue
        if not item.get("self_submitted"):
            continue
        updated = item.get("updated_at", "")
        submitted_candidates.append((updated, aid, item))
        if not item.get("peer_submitted"):
            open_candidates.append((updated, aid, item))

    if open_candidates:
        open_candidates.sort(key=lambda x: x[0], reverse=True)
        _, aid, item = open_candidates[0]
        return aid, item
    if submitted_candidates:
        submitted_candidates.sort(key=lambda x: x[0], reverse=True)
        _, aid, item = submitted_candidates[0]
        return aid, item
    return None, None


class Handler(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        self.send_error(403, "Directory listing is disabled")
        return None

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def _send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self):
        content_length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(content_length) if content_length > 0 else b"{}"
        try:
            return json.loads(raw.decode("utf-8"))
        except Exception:
            return None

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/api/health":
            self._send_json(200, make_resp(True, "ok", {"service": "mbti-api"}))
            return

        if parsed.path == "/api/assessment/status":
            query = parse_qs(parsed.query)
            assessment_id = (query.get("assessment_id") or [""])[0].strip()
            if not assessment_id:
                self._send_json(200, make_resp(False, "缺少 assessment_id"))
                return
            with LOCK:
                assessments = load_json(ASSESSMENTS_FILE)
                item = assessments.get(assessment_id)
            if not item:
                self._send_json(200, make_resp(False, "未找到测评会话"))
                return
            payload = {
                "assessment_id": assessment_id,
                "code": item.get("code", ""),
                "invite_code": item.get("code", ""),
                "invite_token": item.get("invite_token", ""),
                "self_submitted": bool(item.get("self_submitted")),
                "peer_submitted": bool(item.get("peer_submitted")),
                "self_scores": item.get("self_scores"),
                "peer_scores": item.get("peer_scores"),
                "self_type": item.get("self_type", ""),
                "peer_type": item.get("peer_type", ""),
                "updated_at": item.get("updated_at", ""),
            }
            self._send_json(200, make_resp(True, "ok", payload))
            return

        if parsed.path == "/":
            self._send_json(200, make_resp(True, "MBTI API is running"))
            return

        if self._is_blocked_static_path(parsed.path):
            self.send_error(403, "Forbidden")
            return

        return super().do_GET()

    def _is_blocked_static_path(self, path):
        clean = (path or "").split("?", 1)[0].strip()
        if not clean:
            return False
        lower = clean.lower()

        if lower in SENSITIVE_EXACT_PATHS:
            return True
        if "/.git" in lower or lower.startswith("/.git"):
            return True
        if lower.startswith("/.") or "/." in lower:
            return True
        for ext in SENSITIVE_EXTENSIONS:
            if lower.endswith(ext):
                return True
        return False

    def do_POST(self):
        parsed = urlparse(self.path)
        payload = self._read_json_body()
        if payload is None:
            self._send_json(400, make_resp(False, "请求格式错误"))
            return

        if parsed.path == "/api/redeem/verify-self":
            self.handle_verify_self(payload)
            return

        if parsed.path == "/api/assessment/self-submit":
            self.handle_self_submit(payload)
            return

        if parsed.path == "/api/redeem/verify-peer":
            self.handle_verify_peer(payload)
            return

        if parsed.path == "/api/assessment/peer-submit":
            self.handle_peer_submit(payload)
            return

        self._send_json(404, make_resp(False, "Not Found"))

    def handle_verify_self(self, payload):
        code = normalize_code(payload.get("code"))
        if not code:
            self._send_json(200, make_resp(False, "⚠️ 兑换码不能为空"))
            return

        with LOCK:
            codes = load_json(CODES_FILE)
            assessments = load_json(ASSESSMENTS_FILE)

            if code != SUPER_CODE and code not in codes:
                self._send_json(200, make_resp(False, "⚠️ 兑换码无效，请联系管理员获取正确兑换码"))
                return

            if code == SUPER_CODE:
                assessment_id = gen_id("ast")
                invite_token = gen_id("inv")
                assessments[assessment_id] = {
                    "code": code,
                    "super": True,
                    "invite_token": invite_token,
                    "self_submitted": False,
                    "peer_submitted": False,
                    "self_scores": None,
                    "peer_scores": None,
                    "self_type": "",
                    "peer_type": "",
                    "created_at": now_iso(),
                    "updated_at": now_iso(),
                }
                save_json(ASSESSMENTS_FILE, assessments)
                self._send_json(200, make_resp(True, "ok", {
                    "code": code,
                    "super": True,
                    "assessment_id": assessment_id,
                    "invite_code": code,
                    "invite_token": invite_token,
                    "self_submitted": False,
                    "peer_submitted": False,
                }))
                return

            rec = codes[code]
            assessment_id = rec.get("assessment_id")
            if assessment_id and assessment_id in assessments:
                item = assessments[assessment_id]
                self._send_json(200, make_resp(True, "ok", {
                    "code": code,
                    "assessment_id": assessment_id,
                    "invite_code": code,
                    "invite_token": item.get("invite_token", ""),
                    "self_submitted": bool(item.get("self_submitted")),
                    "peer_submitted": bool(item.get("peer_submitted")),
                }))
                return

            if rec.get("total_used", 0) >= 2:
                self._send_json(200, make_resp(False, "⚠️ 兑换码已用完，如仍有需要请联系「悦见InLight」"))
                return

            assessment_id = gen_id("ast")
            invite_token = gen_id("inv")
            assessments[assessment_id] = {
                "code": code,
                "super": False,
                "invite_token": invite_token,
                "self_submitted": False,
                "peer_submitted": False,
                "self_scores": None,
                "peer_scores": None,
                "self_type": "",
                "peer_type": "",
                "created_at": now_iso(),
                "updated_at": now_iso(),
            }
            rec["assessment_id"] = assessment_id
            rec["updated_at"] = now_iso()
            codes[code] = rec

            save_json(CODES_FILE, codes)
            save_json(ASSESSMENTS_FILE, assessments)

            self._send_json(200, make_resp(True, "ok", {
                "code": code,
                "assessment_id": assessment_id,
                "invite_code": code,
                "invite_token": invite_token,
                "self_submitted": False,
                "peer_submitted": False,
            }))

    def handle_self_submit(self, payload):
        assessment_id = (payload.get("assessment_id") or "").strip()
        scores = sanitize_scores(payload.get("scores"))
        if not assessment_id or scores is None:
            self._send_json(200, make_resp(False, "参数缺失或格式错误"))
            return

        with LOCK:
            codes = load_json(CODES_FILE)
            assessments = load_json(ASSESSMENTS_FILE)
            item = assessments.get(assessment_id)
            if not item:
                self._send_json(200, make_resp(False, "未找到测评会话"))
                return

            code = item.get("code", "")
            is_super = bool(item.get("super")) or code == SUPER_CODE
            if not is_super:
                rec = codes.get(code)
                if not rec:
                    self._send_json(200, make_resp(False, "兑换码状态异常，请联系管理员"))
                    return
                # 首次提交自评时消费1次
                if not item.get("self_submitted"):
                    if rec.get("self_used", 0) >= 1:
                        self._send_json(200, make_resp(False, "⚠️ 该兑换码已完成过自评，每个兑换码仅支持1次自评"))
                        return
                    if rec.get("total_used", 0) >= 2:
                        self._send_json(200, make_resp(False, "⚠️ 兑换码已用完，如仍有需要请联系「悦见InLight」"))
                        return
                    rec["self_used"] = rec.get("self_used", 0) + 1
                    rec["total_used"] = rec.get("total_used", 0) + 1
                rec["assessment_id"] = assessment_id
                rec["updated_at"] = now_iso()
                codes[code] = rec

            item["self_scores"] = scores
            item["self_type"] = type_from_scores(scores)
            item["self_submitted"] = True
            item["updated_at"] = now_iso()
            assessments[assessment_id] = item

            if not is_super:
                save_json(CODES_FILE, codes)
            save_json(ASSESSMENTS_FILE, assessments)

            self._send_json(200, make_resp(True, "ok", {
                "assessment_id": assessment_id,
                "invite_code": code,
                "invite_token": item.get("invite_token", ""),
                "self_type": item.get("self_type", ""),
                "peer_submitted": bool(item.get("peer_submitted")),
                "peer_scores": item.get("peer_scores"),
                "peer_type": item.get("peer_type", ""),
            }))

    def handle_verify_peer(self, payload):
        code = normalize_code(payload.get("code"))
        invite_token = (payload.get("invite_token") or "").strip()
        assessment_id_from_payload = (payload.get("assessment_id") or "").strip()

        with LOCK:
            codes = load_json(CODES_FILE)
            assessments = load_json(ASSESSMENTS_FILE)

            assessment_id = None
            item = None

            if assessment_id_from_payload:
                assessment_id = assessment_id_from_payload
                item = assessments.get(assessment_id)
                if item and invite_token and item.get("invite_token") != invite_token:
                    self._send_json(200, make_resp(False, "⚠️ 邀请链接无效，请让TA重新分享"))
                    return
                # assessment_id 失效时，不应直接失败，继续尝试 invite_token/code 兜底
                if not item:
                    assessment_id = None
            elif invite_token:
                assessment_id, item = find_assessment_by_token(assessments, invite_token)
            if (not item) and invite_token:
                assessment_id, item = find_assessment_by_token(assessments, invite_token)
            if (not item) and code:
                if code != SUPER_CODE and code not in codes:
                    self._send_json(200, make_resp(False, "⚠️ 邀请码无效，请联系TA重新分享"))
                    return
                if code == SUPER_CODE:
                    assessment_id, item = find_latest_open_super_assessment(assessments)
                    if not assessment_id or not item:
                        self._send_json(200, make_resp(False, "⚠️ 未找到可用的超级会话，请先在自评完成提交后再进入他评"))
                        return
                if code != SUPER_CODE:
                    rec = codes[code]
                    assessment_id = rec.get("assessment_id")
                    item = assessments.get(assessment_id) if assessment_id else None
                    # 兜底：若映射会话为空或尚未完成自评，回溯同兑换码最近有效会话
                    if (not item) or (not item.get("self_submitted")):
                        fallback_id, fallback_item = find_best_assessment_for_code(assessments, code)
                        if fallback_id and fallback_item:
                            assessment_id, item = fallback_id, fallback_item
                            rec["assessment_id"] = fallback_id
                            rec["updated_at"] = now_iso()
                            codes[code] = rec
                            save_json(CODES_FILE, codes)

            if not item or not assessment_id:
                self._send_json(200, make_resp(False, "⚠️ 未找到对应邀请，请确认邀请码或链接"))
                return

            if not item.get("self_submitted"):
                self._send_json(200, make_resp(False, "⚠️ TA 还未完成自评，暂时无法进行他评"))
                return

            if item.get("peer_submitted"):
                invite_code = item.get("code", "")
                self._send_json(200, make_resp(True, "ok", {
                    "assessment_id": assessment_id,
                    "invite_code": invite_code,
                    "invite_token": item.get("invite_token", ""),
                    "self_type": item.get("self_type", ""),
                    "peer_type": item.get("peer_type", ""),
                    "already_submitted": True,
                }))
                return

            invite_code = item.get("code", "")
            self._send_json(200, make_resp(True, "ok", {
                "assessment_id": assessment_id,
                "invite_code": invite_code,
                "invite_token": item.get("invite_token", ""),
                "self_type": item.get("self_type", ""),
            }))

    def handle_peer_submit(self, payload):
        assessment_id = (payload.get("assessment_id") or "").strip()
        scores = sanitize_scores(payload.get("scores"))
        if not assessment_id or scores is None:
            self._send_json(200, make_resp(False, "参数缺失或格式错误"))
            return

        with LOCK:
            codes = load_json(CODES_FILE)
            assessments = load_json(ASSESSMENTS_FILE)
            item = assessments.get(assessment_id)
            if not item:
                self._send_json(200, make_resp(False, "未找到测评会话"))
                return

            if not item.get("self_submitted"):
                self._send_json(200, make_resp(False, "⚠️ TA 还未完成自评，无法提交他评"))
                return

            code = item.get("code", "")
            is_super = bool(item.get("super")) or code == SUPER_CODE

            if not is_super:
                rec = codes.get(code)
                if not rec:
                    self._send_json(200, make_resp(False, "兑换码状态异常，请联系管理员"))
                    return
                if not item.get("peer_submitted"):
                    if rec.get("peer_used", 0) >= 1:
                        self._send_json(200, make_resp(False, "⚠️ 该兑换码已完成过1次他评，每位用户仅可邀请1人他评"))
                        return
                    if rec.get("total_used", 0) >= 2:
                        self._send_json(200, make_resp(False, "⚠️ 兑换码已用完，如仍有需要请联系「悦见InLight」"))
                        return
                    rec["peer_used"] = rec.get("peer_used", 0) + 1
                    rec["total_used"] = rec.get("total_used", 0) + 1
                rec["updated_at"] = now_iso()
                codes[code] = rec

            item["peer_scores"] = scores
            item["peer_type"] = type_from_scores(scores)
            item["peer_submitted"] = True
            item["updated_at"] = now_iso()
            assessments[assessment_id] = item

            if not is_super:
                save_json(CODES_FILE, codes)
            save_json(ASSESSMENTS_FILE, assessments)

            self._send_json(200, make_resp(True, "ok", {
                "assessment_id": assessment_id,
                "self_type": item.get("self_type", ""),
                "peer_type": item.get("peer_type", ""),
            }))


def main():
    os.chdir(BASE_DIR)
    init_files()
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"MBTI server running at http://{HOST}:{PORT}")
    print(f"Open: http://{HOST}:{PORT}/MBTI-test.html")
    server.serve_forever()


if __name__ == "__main__":
    main()
