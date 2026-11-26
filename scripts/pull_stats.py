#!/usr/bin/env python3
"""Pull Caught Short analytics from GoatCounter into stats/data.json (no secrets in the output)."""
import json, os, sys, datetime as dt, urllib.request, urllib.parse
SITE=os.environ.get("GOATCOUNTER_SITE","https://caughtshort.goatcounter.com")
TOKEN=os.environ["GOATCOUNTER_TOKEN"]
LAUNCH="2026-11-26"
today=dt.date.today()
end=str(today+dt.timedelta(days=1))  # GoatCounter treats end as that day's midnight, so ask up to tomorrow
start=LAUNCH
def get(path,**q):
    url=f"{SITE}/api/v0/{path}"+("?"+urllib.parse.urlencode({k:v for k,v in q.items() if v is not None}) if q else "")
    req=urllib.request.Request(url,headers={"Authorization":"Bearer "+TOKEN,"Accept":"application/json"})
    with urllib.request.urlopen(req,timeout=30) as r: return json.load(r)
out={"generated":dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),"launch":LAUNCH,"range":{"start":start,"end":str(today)}}
total=get("stats/total",start=start,end=end)
out["total"]={"views":total.get("total",0),"events":total.get("total_events",0),"days":[{"day":d["day"],"views":d.get("daily",sum(d.get("hourly",[]))),"hourly":d.get("hourly",[])} for d in total.get("stats",[]) if d["day"]<=str(today)]}
# today's hourly (local-ish: GoatCounter returns in site timezone)
hits=get("stats/hits",start=start,end=end,limit=100,daily="true")
pages=[];events=[]
for h in hits.get("hits",[]):
    rec={"path":h.get("path"),"title":h.get("title"),"views":h.get("count",0),"visitors":h.get("count_unique",h.get("count",0)),"days":[{"day":s["day"],"views":s.get("daily",0)} for s in h.get("stats",[])]}
    (events if h.get("event") or str(h.get("path","")).startswith("ev/") else pages).append(rec)
out["pages"]=pages; out["events"]=events
for page in ["toprefs","locations","systems","browsers","sizes","campaigns"]:
    try:
        r=get(f"stats/{page}",start=start,end=end,limit=20)
        out[page]=[{"name":x.get("name") or x.get("id") or "(unknown)","id":x.get("id"),"count":x.get("count",0)} for x in r.get("stats",[])]
    except Exception as e:
        out[page]=[]; out.setdefault("errors",[]).append(f"{page}: {e}")
# funnel
ev={e["path"]:e for e in events}
def n(k): return ev.get(k,{}).get("views",0)
out["funnel"]={"views":out["total"]["views"],"start":n("ev/start")+n("ev/start-demo"),"first_target":n("ev/first-target"),"arrived":n("ev/arrived")+n("ev/arrived-manual"),"ar_webxr":n("ev/ar-webxr"),"ar_camera":n("ev/ar-camera"),"list_open":n("ev/list-open"),"map_open":n("ev/map-open"),"not_there":n("ev/not-there"),"data_unreachable":n("ev/data-unreachable")}
os.makedirs("stats",exist_ok=True)
json.dump(out,open("stats/data.json","w"),indent=1)
print("views",out["total"]["views"],"events",out["total"]["events"],"pages",len(pages),"events-kinds",len(events))
