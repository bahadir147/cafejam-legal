# Café Jam legal site

Static site for **Café Jam** (Synverse, `com.synverse.cafejam`). Three documents, each in 7 languages (en default, tr, es, pt-BR, fr, de, id):

- the privacy policy (the Turkish page doubles as the KVKK aydınlatma metni),
- the terms of use,
- the data deletion page (the game has no account and no cloud save, so it explains on-device deletion).

No scripts, cookies or trackers. Light/dark aware, mobile friendly. All internal links are relative, so it works under the `/cafejam-legal/` subpath.

## Layout

| Path | Content |
|---|---|
| `index.html`, `<lang>.html` | Landing page (game name + links) |
| `privacy/index.html`, `privacy/<lang>.html` | Privacy Policy |
| `terms/index.html`, `terms/<lang>.html` | Terms of Use |
| `delete-data/index.html`, `delete-data/<lang>.html` | Data deletion |
| `_src/build.py` | Generator. Constants: contact email, store title, links, languages |
| `_src/lang_<code>.py` | Texts per language |
| `DATA_SAFETY.md` | Pointer to the store privacy answers in `docs/store/` |

`index.html` in every folder is English.

## Before publishing (user)

1. Set `CONTACT_EMAIL` in `_src/build.py` (currently the placeholder `<contact_email>`; the build prints a warning while it is set). Optionally set `STORE_TITLE` to the final title from `docs/aso.md`.
2. Rebuild: `python3 legal-site/_src/build.py` (rewrites all 28 pages).
3. If the game's data flows change (new SDK, analytics, crash reporting, cloud save, accounts), update `_src/lang_*.py` **and** `docs/store/DATA_SAFETY.md` / `APP_PRIVACY.md`, then rebuild. Update `"date"` in all seven files when a policy changes.

## Publish on GitHub Pages (repo `cafejam-legal`, user does this)

```sh
# 1) GitHub: create an empty public repo bahadir147/cafejam-legal (no README).
# 2) From the game repo root, after the site is committed:
git subtree push --prefix legal-site https://github.com/bahadir147/cafejam-legal.git main
# 3) GitHub › cafejam-legal › Settings › Pages › Deploy from a branch › main, / (root) › Save.
```

Repeat step 2 after each change. Jekyll skips `_src/`, `README.md` and `DATA_SAFETY.md` (`_config.yml`).

## URLs for the stores

Base: `https://bahadir147.github.io/cafejam-legal/`

| Where | Field | URL |
|---|---|---|
| Play Console › App content › Privacy policy | Privacy policy URL | `https://bahadir147.github.io/cafejam-legal/privacy/` |
| Play Console › Data safety › Data deletion | Delete data URL (optional: no account) | `https://bahadir147.github.io/cafejam-legal/delete-data/` |
| Play Console › Store settings › Store listing contact details | Website | `https://bahadir147.github.io/` (root, so AdMob finds `app-ads.txt`) |
| App Store Connect › App Privacy | Privacy Policy URL | `https://bahadir147.github.io/cafejam-legal/privacy/` |
| App Store Connect › version › Support URL / Marketing URL | Support URL | `https://bahadir147.github.io/cafejam-legal/` (written by `tools/fastlane_sync.py`) |
| AdMob › Privacy & messaging › GDPR | Privacy policy URL | `https://bahadir147.github.io/cafejam-legal/privacy/` |
| In the game | `MonetizationConfig.privacyPolicyUrl` | `https://bahadir147.github.io/cafejam-legal/privacy/` (currently a placeholder in the asset) |

## app-ads.txt

`https://bahadir147.github.io/app-ads.txt` already exists for Watt Street's AdMob publisher (`pub-3012106898444732`). If Café Jam's AdMob apps are created in the **same** AdMob account, that single line already covers Café Jam and nothing needs to change. If a different AdMob account is used, add its line to that file. The developer website in both stores must be the root `https://bahadir147.github.io/` for AdMob's crawler.
