# Olymp Live Signal

Transparent GitHub Pages site that publishes buy/sell signals for Olymp Trade
forex pairs. Every data update is committed to the Git log for full traceability.

## 📦 Local Setup

```bash
git clone https://github.com/<your‑user>/olymplivesignal.git
cd olymplivesignal
python -m http.server 8000
# visit http://localhost:8000
```

## 🚀 One‑Click Deploy

1. Create **public** repo `olymplivesignal` on GitHub.
2. Push this code to `main`.
3. In **Settings → Pages**, choose **Deploy from a branch**, root folder.
4. Wait ~60 seconds; your site appears at  
   `https://<your‑user>.github.io/olymplivesignal/`.

## 🌐 Custom Domain

1. Register a free domain (e.g. `olymplivesignal.tk` on Freenom).
2. Add a CNAME record pointing to `<your‑user>.github.io`.
3. Add a plain‑text file named **CNAME** in the repo with the domain inside.
4. Commit & push. GitHub Pages will request an SSL certificate automatically.

## 🛠 Updating Signals

*Manual*: edit `signals.json`, commit, push.  
*Automated*: run your signal‑generation script and `git commit -am "new signal"`.

MIT License © 2025
