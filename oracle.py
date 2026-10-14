import json, math

def pos(x): return isinstance(x,(int,float)) and math.isfinite(x) and x>0
def round2(x): return math.floor(x*100+0.5)/100
def jround(x): return math.floor(x+0.5)

def jsnum(x):
    if isinstance(x,float) and x==int(x): return str(int(x))
    return str(x)

def band(cu):
    if cu<1000: return "a rinser"
    if cu<2000: return "light duty - cars and patio furniture"
    if cu<4000: return "medium duty - decks and fences"
    if cu<7000: return "heavy duty - driveways and siding"
    return "industrial territory"

def clean_plan(psi,gpm):
    if not pos(psi) or not pos(gpm): return {"error":"pressure and flow must both be above zero"}
    cu=psi*gpm
    return {"units":jround(cu),"band":band(cu),"hype":psi>=2000 and gpm<1.3}

def render_clean(r,psi,gpm):
    s="Your "+jsnum(psi)+" PSI at "+jsnum(gpm)+" GPM makes "+jsnum(r["units"])+" cleaning units - "+r["band"]
    if r["hype"]: s+=", and the box is selling pressure more than cleaning"
    return s+"."

def nozzle_plan(gpm,psi):
    if not pos(psi) or not pos(gpm): return {"error":"pressure and flow must both be above zero"}
    raw=gpm*math.sqrt(4000/psi)
    half=jround(raw*2)/2
    return {"orifice":half,"raw":round2(raw)}

def render_nozzle(r,gpm,psi):
    return ("Your "+jsnum(gpm)+" GPM at "+jsnum(psi)+" PSI calls for a #"+jsnum(r["orifice"])+" orifice ("
            +jsnum(r["raw"])+" rounded to the nearest half size) - the orifice sets the working pressure; the fan angle only spreads it.")

def time_plan(units,sqft):
    if not pos(units) or not pos(sqft): return {"error":"area and cleaning units must both be above zero"}
    cleaner=jround(sqft/(units/10)*60)
    wand=jround(sqft/(units/20)*60)
    return {"cleanerMin":cleaner,"wandMin":wand}

def render_time(r,units,sqft):
    return ("Your "+jsnum(sqft)+" sq ft at "+jsnum(units)+" cleaning units figures about "+jsnum(r["cleanerMin"])
            +" minutes with a surface cleaner and "+jsnum(r["wandMin"])+" with a wand - a labeled norm, not a promise.")

cases=[]
def add(tool,args):
    if tool=="clean": r=clean_plan(*args); fn=render_clean
    elif tool=="nozzle": r=nozzle_plan(*args); fn=render_nozzle
    else: r=time_plan(*args); fn=render_time
    case={"tool":tool,"args":args,"result":r}
    if "error" not in r: case["render"]=fn(r,*args)
    cases.append(case)

# clean plan: band boundaries judged unrounded
for a in [(2000,1.2),(1300,1.4),(3200,2.5),(4200,4.0),(900,1.1),(1500,0.8),
          (1600,1.25),(3000,2.0),(2500,0.8),(4000,1.75),(1000,1.0),(2500,2.8)]:
    add("clean",a)
# nozzle plan
for a in [(2.5,2500),(3.0,3000),(1.2,2000),(4.0,4000),(1.5,1300),(2.0,1600),(1.1,900),(3.5,2500)]:
    add("nozzle",a)
# time plan
for a in [(2400,400),(3000,600),(1100,200),(7000,1200),(1600,150),(4200,800),(950,90),(2800,350)]:
    add("time",a)
# error branches
add("clean",[0,1.5]); add("clean",[2000,0]); add("nozzle",[0,2000]); add("nozzle",[2.0,0]); add("time",[0,400]); add("time",[2400,0])

json.dump(cases,open("expected.json","w"),separators=(",",":"))
print(len(cases),"cases")
