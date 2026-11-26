#!/usr/bin/env python3
"""Turn stats/data.json into the row files the Caught Short Analytics dashboard reads."""
import json, sys, os, datetime as dt
src=sys.argv[1]; out=sys.argv[2]; os.makedirs(out,exist_ok=True)
d=json.load(open(src))
def w(name,rows,meta=None):
    json.dump({"rows":rows,"meta":meta or [{"label":"Source","value":"GoatCounter API via stats/data.json on loo.bcvr.io"},{"label":"Generated","value":d["generated"]}]},open(os.path.join(out,name),"w"))
days=d["total"]["days"]
w("daily.json",[{"day":x["day"],"views":int(x["views"])} for x in days])
today=days[-1] if days else {"day":str(dt.date.today()),"hourly":[0]*24}
w("hourly.json",[{"hour":f"{h:02d}:00","views":int(v)} for h,v in enumerate(today.get("hourly",[0]*24))])
w("events.json",[{"event":e["path"].replace("ev/",""),"title":e.get("title") or e["path"],"count":int(e["views"])} for e in sorted(d["events"],key=lambda e:-e["views"])])
w("pages.json",[{"path":p["path"],"views":int(p["views"]),"visitors":int(p.get("visitors",0))} for p in sorted(d["pages"],key=lambda p:-p["views"])])
for k,name,col in [("toprefs","refs.json","referrer"),("locations","countries.json","country"),("systems","devices.json","system"),("browsers","browsers.json","browser"),("campaigns","campaigns.json","campaign")]:
    w(name,[{col:(x["name"] or "Direct / QR"),"count":int(x["count"])} for x in d.get(k,[])])
f=d["funnel"]; f=dict(f); f["generated"]=d["generated"]; f["launch"]=d["launch"]; f["today_views"]=int(today.get("views",0)); f["days_live"]=len(days)
w("funnel.json",[f])
print("wrote",sorted(os.listdir(out)))
