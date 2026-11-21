# Nexora daily posts: how the "social media team" (Claude) works

Rana's decisions (20 Nov 2026):
- One NEW post every day, Nexora's services mixed (rotation in `services.json`), each day a different style.
- For Facebook (image/carousel), TikTok and YouTube (short vertical video). Download/website link written in the caption so it can be copied.
- Every post has the fixed header/footer (`nexora_post.py`): gold header with big logo + "NEXORA / DIGITAL SERVICES";
  footer Website https://nexoradsa.org | Email info@nexoradsa.org | WhatsApp 0345 0383301.
- Rana reviews every post on WhatsApp through the Nexora WhatsApp agent (Phase 11). He answers `ok <ref>` or
  `change <ref> <what>`. Changes are made and the post is sent again. Nothing is scheduled without his ok, and the ok
  must come at least 6 hours before the post time.
- Nexora Accounting posts wait until the new exe is on the download (`state.json` -> `accounting_exe_ready`).

## Repos
- Posts repo (public): `RanaTahir-source/nexora-social-posts`, branch `main`.
  ```
  kit/                      copy of this folder (nexora_post.py, services.json, README.md)
  state.json                {"next_rotation": 0, "accounting_exe_ready": false, "recent_styles": [], "processed": {}}
  queue/<ref>.json          the post (read by the agent; see format below)
  posts/<ref>/v<N>/         1.png 2.png ... short.mp4 (media for that version)
  decisions/<ref>-v<N>.json written by the agent: {"decision": "ok"|"change", "note": ..., "at": ...}
  ```
- Agent repo: `RanaTahir-source/nexoradsa` (Phase 11 code; this kit also lives in its `social-kit/`).

Media URLs: `https://raw.githubusercontent.com/RanaTahir-source/nexora-social-posts/main/posts/<ref>/v<N>/<file>`.
After pushing, check each URL returns HTTP 200 (curl) before setting `"status": "review"`.

## queue/<ref>.json
```json
{"ref": "p1122", "version": 1, "status": "review",
 "title": "School Software: fee receipt on WhatsApp", "service": "school_software", "style": "carousel",
 "publish_at": "2026-11-22T18:00:00+05:00", "publish_at_label": "Itwar 22 Nov, shaam 6 baje",
 "platforms": ["Facebook", "TikTok", "YouTube"],
 "caption": "<Urdu caption with the https link, WhatsApp and email>",
 "youtube_title": "<max 90 chars>",
 "images": ["https://raw.githubusercontent.com/.../posts/p1122/v1/1.png", "..."],
 "video": "https://raw.githubusercontent.com/.../posts/p1122/v1/short.mp4",
 "history": [], "metricool": null}
```
ref = `p` + MMDD of the publish day (+ a letter if two posts share a day, e.g. old posts redone: `p1123r`).
status: `review` (agent sends it) -> `approved` -> `scheduled` -> (`published`). Only `review` is sent by the agent.

## Run A: daily create (08:41 PKT)
1. Clone/pull the posts repo (attach it with push access). If it does not exist: stop and say so in the run summary.
   If `kit/` is missing, copy `social-kit/*` from the nexoradsa repo into `kit/` and create `state.json`.
2. Do Run B (decisions) first.
3. Pick the service: `services.json.rotation[state.next_rotation]`; skip `nexora_accounting` while
   `accounting_exe_ready` is false; advance `next_rotation`.
4. Pick a style from `services.json.styles` NOT in `state.recent_styles` (keep the last 4).
5. Write the post in Urdu script (same tone as the approved posts: short, clear, honest). Facts ONLY from
   `services.json` (and the Accounting brief for Accounting). Hook in the first line. One CTA.
6. Render with `kit/nexora_post.py`: 1-6 images 1080x1350 (`render`), then `video(images, short.mp4, seconds=4)`
   (1080x1920, under 16 MB). Look at every PNG before pushing (text cut, overlap with "اگلی سلائیڈ" or footer).
7. Caption: Urdu, 3-6 short lines + the CTA line + `🌐 https://nexoradsa.org` (or the service link) +
   `📲 واٹس ایپ: 0345 0383301` + `📧 info@nexoradsa.org` + 5-8 hashtags (#NexoraDigitalServices #Bhakkar #Kalurkot ...).
8. publish_at = today 18:00 PKT. Push media + `queue/<ref>.json` (status review, version 1) + state.json.
   The agent sends it to Rana within ~5 minutes.

## Run B: decisions (08:41, 10:41, 11:41, 15:41, 20:41 PKT)
For each `decisions/<ref>-v<N>.json` not yet in `state.processed`:
- `change`: apply the note (Rana's words; if unclear, do the most reasonable reading and say what you did in the
  caption of the review text), render again, push `posts/<ref>/v<N+1>/`, set queue version N+1, status review,
  append to `history`. The agent sends the new version.
- `ok`: if `now <= publish_at - 6h` schedule at publish_at; otherwise move publish_at to the next free slot at
  least 6 h after the ok (10:00 or 18:00 PKT, never 23:00-08:00) and schedule there. Then status `scheduled`,
  store the Metricool ids in `metricool`.
- Mark it in `state.processed` and push.
A post still in review when its publish time is less than 6 h away: move publish_at to the next day 18:00 and
push (the agent does not resend the same version; the new time shows when it is scheduled).

## Metricool (connector), brand 7425122, timezone Asia/Karachi, autoPublish true
- Facebook: `providers [{"network":"facebook"}]`, `facebookData {"type":"POST"}`, media = the PNG URL(s) (carousel ok).
- TikTok: separate post, media = short.mp4, `tiktokData {"privacyOption":"PUBLIC_TO_EVERYONE","title":"..."}`.
- YouTube: separate post, media = short.mp4, `youtubeData {"title": youtube_title, "type":"short", "privacy":"public","madeForKids": false}`.
- text = the caption (links included so people can copy them).
- After scheduling, read back with getScheduledPosts to confirm.

## Never
- Post or schedule without Rana's ok; change the header/footer; use prices, guarantees, percentages, fake reviews,
  income/job promises; copy other creators' footage; use the old proof points (3.4x, 150+ brands, +212%).
- Mix in school campus branding (Dar e Arqam / Rodi etc.) - those are separate brands.
