#!/usr/bin/env python3
"""Visitor logger for the homepage.

Runs two HTTP servers in one process:

  collector  127.0.0.1:8787  /collect  <- the public tunnel points here
  viewer     127.0.0.1:8788  /         <- dashboard, localhost only

Keeping them on separate ports means the tunnel exposes only the write
endpoint; the log itself is never reachable from the internet.

Usage:  python visitlog.py
"""

import html
import http.server
import json
import os
import socketserver
import sqlite3
import sys
import threading
import urllib.parse
from datetime import datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, "visits.db")

COLLECT_PORT = 8787
VIEW_PORT = 8788

# Your own IPs land here so they do not pollute the stats.
IGNORE_IPS = set()

# 1x1 transparent GIF returned to the browser beacon.
PIXEL = (
    b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00!\xf9\x04\x01"
    b"\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
)

BOT_MARKERS = (
    "bot", "crawler", "spider", "slurp", "curl", "wget", "python-requests",
    "headlesschrome", "preview", "monitor", "scan", "fetch", "http-client",
)

_lock = threading.Lock()


def connect():
    conn = sqlite3.connect(DB, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS visits (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                ts      TEXT NOT NULL,
                ip      TEXT,
                country TEXT,
                page    TEXT,
                referer TEXT,
                ua      TEXT,
                is_bot  INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_visits_ts ON visits(ts)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_visits_ip ON visits(ip)")


def client_ip(headers, fallback):
    """Real visitor IP. Behind a tunnel the socket peer is always localhost."""
    cf = headers.get("CF-Connecting-IP")
    if cf:
        return cf.strip()
    xff = headers.get("X-Forwarded-For")
    if xff:
        return xff.split(",")[0].strip()
    real = headers.get("X-Real-IP")
    if real:
        return real.strip()
    return fallback


def looks_like_bot(ua):
    low = (ua or "").lower()
    if not low:
        return True
    return any(m in low for m in BOT_MARKERS)


def record(headers, peer, query):
    ip = client_ip(headers, peer)
    if ip in IGNORE_IPS:
        return
    ua = headers.get("User-Agent", "")
    row = (
        datetime.now(timezone.utc).isoformat(timespec="seconds"),
        ip,
        (headers.get("CF-IPCountry") or "").strip(),
        (query.get("p", [""])[0])[:300],
        (query.get("r", [""])[0] or headers.get("Referer", ""))[:500],
        ua[:400],
        1 if looks_like_bot(ua) else 0,
    )
    with _lock, connect() as conn:
        conn.execute(
            "INSERT INTO visits (ts, ip, country, page, referer, ua, is_bot)"
            " VALUES (?, ?, ?, ?, ?, ?, ?)",
            row,
        )


class Quiet(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        pass

    def send_bytes(self, body, ctype, status=200, extra=None):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store, max-age=0")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)


class Collector(Quiet):
    """Public write endpoint. Answers /collect and nothing else."""

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path != "/collect":
            self.send_bytes(b"", "text/plain", status=404)
            return
        try:
            record(
                self.headers,
                self.client_address[0],
                urllib.parse.parse_qs(parsed.query),
            )
        except Exception as exc:  # never let a bad hit kill the endpoint
            print("collect error:", exc, file=sys.stderr)
        self.send_bytes(
            PIXEL, "image/gif", extra={"Access-Control-Allow-Origin": "*"}
        )

    def do_HEAD(self):
        self.send_bytes(b"", "image/gif")


def fetch_stats(days=30, limit=300, include_bots=False):
    where = "" if include_bots else " WHERE is_bot = 0"
    with connect() as conn:
        recent = conn.execute(
            "SELECT ts, ip, country, page, referer, ua, is_bot FROM visits"
            + where
            + " ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
        totals = conn.execute(
            "SELECT COUNT(*) AS hits, COUNT(DISTINCT ip) AS uniq FROM visits" + where
        ).fetchone()
        since = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        joiner = " AND" if where else " WHERE"
        top_ips = conn.execute(
            "SELECT ip, country, COUNT(*) AS n, MAX(ts) AS last FROM visits"
            + where
            + joiner
            + " ts >= ? GROUP BY ip ORDER BY n DESC LIMIT 15",
            (since,),
        ).fetchall()
        by_day = conn.execute(
            "SELECT substr(ts, 1, 10) AS day, COUNT(*) AS n FROM visits"
            + where
            + joiner
            + " ts >= ? GROUP BY day ORDER BY day DESC LIMIT 14",
            (since,),
        ).fetchall()
    return recent, totals, top_ips, by_day


def local_time(iso):
    try:
        return (
            datetime.fromisoformat(iso)
            .astimezone()
            .strftime("%Y-%m-%d %H:%M:%S")
        )
    except Exception:
        return iso


def render(include_bots):
    recent, totals, top_ips, by_day = fetch_stats(include_bots=include_bots)
    e = html.escape

    rows = "\n".join(
        "<tr><td class=t>{ts}</td><td class=ip>{ip}</td><td>{cc}</td>"
        "<td>{page}</td><td>{ref}</td><td class=ua title=\"{uafull}\">{ua}</td></tr>".format(
            ts=e(local_time(r["ts"])),
            ip=e(r["ip"] or ""),
            cc=e(r["country"] or ""),
            page=e(r["page"] or "/"),
            ref=e((r["referer"] or "")[:60]),
            ua=e((r["ua"] or "")[:45]),
            uafull=e(r["ua"] or ""),
        )
        for r in recent
    ) or "<tr><td colspan=6 class=empty>No visits recorded yet.</td></tr>"

    ip_rows = "\n".join(
        "<tr><td class=ip>{ip}</td><td>{cc}</td><td class=n>{n}</td>"
        "<td class=t>{last}</td></tr>".format(
            ip=e(r["ip"] or ""),
            cc=e(r["country"] or ""),
            n=r["n"],
            last=e(local_time(r["last"])),
        )
        for r in top_ips
    ) or "<tr><td colspan=4 class=empty>-</td></tr>"

    peak = max([r["n"] for r in by_day], default=1) or 1
    day_rows = "\n".join(
        "<tr><td class=t>{d}</td><td class=n>{n}</td>"
        "<td><span class=bar style='width:{w}px'></span></td></tr>".format(
            d=e(r["day"]), n=r["n"], w=int(r["n"] / peak * 240)
        )
        for r in by_day
    ) or "<tr><td colspan=3 class=empty>-</td></tr>"

    toggle = (
        "<a href='/?bots=0'>hide bots</a>"
        if include_bots
        else "<a href='/?bots=1'>show bots</a>"
    )

    return """<!doctype html><html><head><meta charset="utf-8">
<title>Visitor log</title>
<meta http-equiv="refresh" content="60">
<style>
 body{{font:13px/1.5 -apple-system,Segoe UI,Helvetica,Arial,sans-serif;
      margin:24px auto;max-width:1100px;color:#222;padding:0 16px}}
 h1{{font-size:19px;margin:0 0 4px}}
 h2{{font-size:14px;margin:26px 0 8px;color:#444}}
 .sub{{color:#777;margin-bottom:18px}}
 .cards{{display:flex;gap:12px;margin-bottom:8px}}
 .card{{border:1px solid #ddd;border-radius:6px;padding:10px 16px;background:#fafafa}}
 .card b{{display:block;font-size:22px;font-weight:600}}
 .card span{{color:#777;font-size:12px}}
 table{{border-collapse:collapse;width:100%;margin-bottom:6px}}
 th,td{{border-bottom:1px solid #eee;padding:5px 8px;text-align:left;
        vertical-align:top}}
 th{{background:#f5f5f5;font-weight:600;color:#555;white-space:nowrap}}
 td.t,td.ip{{white-space:nowrap;font-family:Consolas,Menlo,monospace;font-size:12px}}
 td.n{{text-align:right;width:60px}}
 td.ua{{color:#888;font-size:11px}}
 td.empty{{color:#999;text-align:center;padding:14px}}
 .bar{{display:inline-block;height:10px;background:#527bbd;border-radius:2px}}
 .two{{display:flex;gap:28px}} .two>div{{flex:1;min-width:0}}
 a{{color:#527bbd}}
</style></head><body>
<h1>Visitor log</h1>
<div class=sub>auto-refreshes every 60s &middot; {toggle}</div>
<div class=cards>
  <div class=card><b>{hits}</b><span>total hits</span></div>
  <div class=card><b>{uniq}</b><span>unique IPs</span></div>
</div>
<div class=two>
 <div><h2>Per day (last 14)</h2><table>{days}</table></div>
 <div><h2>Top IPs (last 30 days)</h2>
  <table><tr><th>IP</th><th>CC</th><th>hits</th><th>last seen</th></tr>
  {ips}</table></div>
</div>
<h2>Recent visits</h2>
<table><tr><th>time</th><th>IP</th><th>CC</th><th>page</th>
<th>referer</th><th>user agent</th></tr>
{rows}</table>
</body></html>""".format(
        toggle=toggle,
        hits=totals["hits"],
        uniq=totals["uniq"],
        days=day_rows,
        ips=ip_rows,
        rows=rows,
    )


class Viewer(Quiet):
    """Local dashboard. Bound to 127.0.0.1 so only you can read it."""

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed.query)
        if parsed.path == "/export.json":
            recent, _, _, _ = fetch_stats(limit=10000, include_bots=True)
            body = json.dumps([dict(r) for r in recent], indent=2).encode()
            self.send_bytes(body, "application/json")
            return
        if parsed.path != "/":
            self.send_bytes(b"Not found", "text/plain", status=404)
            return
        body = render(query.get("bots", ["0"])[0] == "1").encode("utf-8")
        self.send_bytes(body, "text/html; charset=utf-8")


class Server(socketserver.ThreadingTCPServer):
    daemon_threads = True
    allow_reuse_address = True


def main():
    init_db()
    collector = Server(("127.0.0.1", COLLECT_PORT), Collector)
    viewer = Server(("127.0.0.1", VIEW_PORT), Viewer)

    threading.Thread(target=collector.serve_forever, daemon=True).start()

    print("collector  http://127.0.0.1:%d/collect   (point the tunnel here)" % COLLECT_PORT)
    print("dashboard  http://127.0.0.1:%d/          (local only)" % VIEW_PORT)
    print("database   %s" % DB)
    print("\nCtrl+C to stop.")
    try:
        viewer.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")


if __name__ == "__main__":
    main()
