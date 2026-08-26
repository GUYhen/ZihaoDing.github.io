# Visitor log

Records the IP of every visit to the homepage, stores it locally, and shows it
on a dashboard only you can reach.

## How it works

GitHub Pages serves the site, so GitHub — not you — receives the visitor's
request, and it gives you no access logs. The only way to see an IP is to make
the page call an endpoint you control:

```
visitor's browser
      |  loads guyhen.github.io/ZihaoDing.github.io/
      |  the page fires a 1x1 image beacon
      v
Cloudflare Tunnel (public URL)
      v
127.0.0.1:8787/collect   <- this program, on your PC
      v
visits.db  (SQLite, stays on your disk)
      v
127.0.0.1:8788           <- dashboard, localhost only
```

Two ports on purpose: the tunnel exposes only `/collect`, which accepts writes
and returns a transparent pixel. Every other path on that port answers 404, so
the database and the dashboard are never reachable from the internet.

## 1. Run it

```
python visitlog.py
```

```
collector  http://127.0.0.1:8787/collect   (point the tunnel here)
dashboard  http://127.0.0.1:8788/          (local only)
```

No dependencies — standard library only. Leave it running.

## 2. Expose the collector

Install [cloudflared](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/),
then:

```
cloudflared tunnel --url http://127.0.0.1:8787
```

It prints a public URL such as `https://random-words-1234.trycloudflare.com`.

**This URL changes every time you restart cloudflared.** Since the beacon lives
in the published site, a new URL means editing and redeploying the page. Two
ways to get a stable address:

- **Named tunnel** — needs a domain on Cloudflare. Gives a fixed hostname such
  as `log.yourdomain.com`. See the cloudflared docs for `tunnel create` /
  `tunnel route dns`.
- **ngrok** — the free plan includes one permanent static domain:
  `ngrok http 8787 --domain=your-name.ngrok-free.app`

Nothing is lost while the tunnel is down, but visits during that time are not
recorded at all.

## 3. Add the beacon to the site

Put this in `docs/mysite.conf` inside the `[bodystart]` block, just before
`</head>`, so every page reports (index, publications, awards, blog):

```html
<script>
(function () {
  var endpoint = "https://YOUR-TUNNEL-URL/collect";
  new Image().src = endpoint
    + "?p=" + encodeURIComponent(location.pathname)
    + "&r=" + encodeURIComponent(document.referrer)
    + "&t=" + Date.now();
})();
</script>
```

Replace `YOUR-TUNNEL-URL`, then rebuild and push:

```
cd docs
.\build.ps1
git add -A && git commit -m "add visitor beacon" && git push
```

An image beacon is used rather than `fetch` so no CORS handshake is needed, and
a failed request never shows an error in the visitor's console.

## 4. Read the log

Open <http://127.0.0.1:8788/>. It auto-refreshes every 60s and shows:

- total hits and unique IPs
- hits per day for the last 14 days
- the 15 busiest IPs over the last 30 days
- the 300 most recent visits: time, IP, country, page, referer, user agent

Obvious crawlers (Googlebot, curl, headless browsers, …) are flagged on the way
in and hidden by default; `?bots=1` shows them.

`http://127.0.0.1:8788/export.json` dumps everything, bots included, as JSON.

## Filtering your own visits

Add your own address to `IGNORE_IPS` near the top of `visitlog.py`:

```python
IGNORE_IPS = {"1.2.3.4"}
```

Find it by loading the site yourself and reading the newest row.

## Notes

- The PC must be on and both the program and the tunnel running; anything else
  is missed. There is no backfill.
- `visits.db` is in `.gitignore` and must stay there — the repository is
  public, and the file contains visitor IP addresses.
- An IP is personal data under GDPR and PIPL. A short privacy note in the page
  footer is the usual practice for a site with international visitors.
