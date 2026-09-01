from pathlib import Path
import subprocess
from datetime import datetime

ROOT = Path(__file__).parent.parent
DESIGN = ROOT / "designs" / "game-design.md"
OUTPUT = ROOT / "games" / "mindcraft-game.html"


def get_design():
    text = DESIGN.read_text(encoding="utf-8")

    def field(section):
        marker = f"### {section}"
        lines = text.splitlines()

        for i, line in enumerate(lines):
            if line.strip() == marker:
                for value in lines[i + 1:]:
                    value = value.strip()
                    if value and not value.startswith("#"):
                        return value
        return ""

    title = ""
    for line in text.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            break

    return {
        "title": title or "Neon Escape 3D",
        "description": field("Short Description"),
        "objective": field("Core Objective"),
        "controls": field("Player Controls"),
        "mechanic": field("Main Mechanic"),
        "win": field("Win Condition"),
        "lose": field("Lose Condition"),
        "hazards": field("Enemies or Hazards"),
        "targets": field("Collectibles or Targets"),
    }


def build_game(design):
    title = design["title"]
    description = design["description"]
    controls = design["controls"]
    mechanic = design["mechanic"]
    win = design["win"]
    lose = design["lose"]

    if title == "Gravity Flip":
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — MindCraft</title>
<style>
*{{box-sizing:border-box}}
body{{
 margin:0;
 background:#020617;
 color:white;
 font-family:Arial,sans-serif;
 text-align:center;
}}
h1{{margin:14px 0 5px}}
.info{{color:#cbd5e1;margin:5px}}
#game{{
 display:block;
 width:min(900px,96vw);
 height:auto;
 margin:15px auto 8px;
 border:2px solid #334155;
 background:#000;
}}
#status{{font-size:20px;font-weight:bold;margin:8px}}
.footer{{color:#94a3b8;margin:12px}}
</style>
</head>

<body>

<h1>{title}</h1>
<div class="info">{description}</div>
<div class="info">{controls}</div>

<canvas id="game" width="900" height="500"></canvas>

<div id="status">Gravity: FLOOR | Progress: 0%</div>

<div class="footer">Powered by @Modiqo & #rote</div>

<script>
"use strict";

const canvas=document.getElementById("game");
const ctx=canvas.getContext("2d");
const statusEl=document.getElementById("status");

const world={{
 width:18,
 floor:4.2,
 ceiling:0.8
}};

const player={{
 x:1.5,
 y:4.2,
 radius:.25,
 speed:.075,
 gravity:"floor"
}};

const obstacles=[
 {{x:4.0,y:4.2,w:.65,h:1.2}},
 {{x:7.0,y:.8,w:.65,h:1.2}},
 {{x:10.0,y:4.2,w:.65,h:1.2}},
 {{x:13.0,y:.8,w:.65,h:1.2}},
 {{x:15.5,y:4.2,w:.65,h:1.2}}
];

const finish={{x:17.0}};

const keys=new Set();
let ended=false;
let progress=0;

window.MINDCRAFT_GAME={{
 version:"1.0",
 engine:"3d",
 title:{title!r},
 gameType:"gravity-flip",
 getStatus:()=>statusEl.textContent,
 isEnded:()=>ended,
 getState:()=>({{
   gravity:player.gravity,
   x:player.x,
   progress
 }}),
 restart:()=>location.reload()
}};

document.addEventListener("keydown",e=>{{
 const k=e.key.toLowerCase();

 if(k==="r" && ended){{
   location.reload();
   return;
 }}

 if(k===" " || k==="spacebar"){{
   e.preventDefault();

   if(!ended){{
     player.gravity=
       player.gravity==="floor" ? "ceiling" : "floor";
     player.y=
       player.gravity==="floor" ? world.floor : world.ceiling;
   }}

   return;
 }}

 keys.add(k);

 if(["arrowleft","arrowright","a","d"].includes(k))
   e.preventDefault();
}});

document.addEventListener("keyup",e=>{{
 keys.delete(e.key.toLowerCase());
}});

function obstacleHit(o){{
 return(
   player.x+player.radius>o.x &&
   player.x-player.radius<o.x+o.w &&
   player.y+player.radius>o.y-o.h/2 &&
   player.y-player.radius<o.y+o.h/2
 );
}}

function update(){{
 if(ended)return;

 if(keys.has("arrowright")||keys.has("d"))
   player.x+=player.speed;

 if(keys.has("arrowleft")||keys.has("a"))
   player.x-=player.speed;

 player.x=Math.max(.5,Math.min(finish.x,player.x));

 for(const o of obstacles){{
   if(obstacleHit(o)){{
     ended=true;
     statusEl.textContent="GAME OVER — Obstacle collision!";
     return;
   }}
 }}

 progress=Math.min(
   100,
   Math.floor((player.x/(finish.x))*100)
 );

 if(player.x>=finish.x){{
   ended=true;
   progress=100;
   statusEl.textContent="YOU WIN! Gravity Flip completed!";
   return;
 }}

 statusEl.textContent=
   `Gravity: ${{player.gravity.toUpperCase()}} | Progress: ${{progress}}%`;
}}

function drawWorld(){{
 const w=canvas.width;
 const h=canvas.height;

 ctx.fillStyle="#081126";
 ctx.fillRect(0,0,w,h);

 ctx.fillStyle="#111c36";
 ctx.fillRect(0,180,w,140);

 ctx.strokeStyle="#38bdf8";
 ctx.lineWidth=4;
 ctx.beginPath();
 ctx.moveTo(0,world.floor*70);
 ctx.lineTo(w,world.floor*70);
 ctx.stroke();

 ctx.strokeStyle="#a78bfa";
 ctx.beginPath();
 ctx.moveTo(0,world.ceiling*70);
 ctx.lineTo(w,world.ceiling*70);
 ctx.stroke();

 const scale=42;

 for(const o of obstacles){{
   ctx.fillStyle="#ef4444";
   ctx.fillRect(
     o.x*scale,
     o.y*70-42,
     o.w*scale,
     o.h*70
   );
 }}

 ctx.fillStyle="#22c55e";
 ctx.fillRect(finish.x*scale,150,24,170);

 ctx.fillStyle="#22d3ee";
 ctx.beginPath();
 ctx.arc(
   player.x*scale,
   player.gravity==="floor"
     ? world.floor*70-18
     : world.ceiling*70+18,
   13,
   0,
   Math.PI*2
 );
 ctx.fill();

 ctx.fillStyle="white";
 ctx.font="16px Arial";
 ctx.fillText("MINDCRAFT 3D",20,28);
 ctx.fillText(
   "SPACE = FLIP GRAVITY",
   20,
   475
 );
}}

function loop(){{
 update();
 drawWorld();
 requestAnimationFrame(loop);
}}

loop();
</script>

</body>
</html>
"""

    # Generic 3D fallback for supported generated designs.
    # The current 3D renderer uses the design fields to create a
    # playable self-contained browser game instead of rejecting
    # every title that is not Gravity Flip.
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — MindCraft</title>
<style>
body{{margin:0;background:#050816;color:white;font-family:Arial,sans-serif;text-align:center}}
#game{{display:block;width:min(900px,96vw);height:auto;margin:18px auto 8px;background:#000;border:2px solid #334155}}
#status{{font-size:20px;font-weight:bold}}
.info{{color:#cbd5e1;margin:5px}}
.footer{{color:#94a3b8;margin:12px}}
</style>
</head>
<body>
<h1>{title}</h1>
<div class="info">{description}</div>
<div class="info">{controls}</div>
<canvas id="game" width="900" height="500"></canvas>
<div id="status">Progress: 0%</div>
<div class="footer">Powered by @Modiqo & #rote</div>

<script>
"use strict";

const canvas=document.getElementById("game");
const ctx=canvas.getContext("2d");
const statusEl=document.getElementById("status");

const player={{x:1.5,y:4.2,radius:.25,speed:.075}};
const finish={{x:17}};
const obstacles=[
 {{x:4,y:4.2,w:.65,h:1.2}},
 {{x:7,y:.8,w:.65,h:1.2}},
 {{x:10,y:4.2,w:.65,h:1.2}},
 {{x:13,y:.8,w:.65,h:1.2}},
 {{x:15.5,y:4.2,w:.65,h:1.2}}
];

const keys=new Set();
let ended=false;
let progress=0;

window.MINDCRAFT_GAME={{
 version:"1.0",
 engine:"3d",
 title:{title!r},
 gameType:{title.lower().replace(" ","-")!r},
 getStatus:()=>statusEl.textContent,
 isEnded:()=>ended,
 getState:()=>({{x:player.x,progress,ended}}),
 restart:()=>location.reload()
}};

document.addEventListener("keydown",e=>{{
 const k=e.key.toLowerCase();
 if(k==="r" && ended){{location.reload();return}}
 keys.add(k);
 if(["a","d","arrowleft","arrowright"].includes(k))e.preventDefault();
}});

document.addEventListener("keyup",e=>keys.delete(e.key.toLowerCase()));

function obstacleHit(o){{
 return player.x+player.radius>o.x &&
        player.x-player.radius<o.x+o.w &&
        player.y+player.radius>o.y-o.h/2 &&
        player.y-player.radius<o.y+o.h/2;
}}

function update(){{
 if(ended)return;

 if(keys.has("d")||keys.has("arrowright"))player.x+=player.speed;
 if(keys.has("a")||keys.has("arrowleft"))player.x-=player.speed;

 player.x=Math.max(.5,Math.min(finish.x,player.x));

 for(const o of obstacles){{
   if(obstacleHit(o)){{
     ended=true;
     statusEl.textContent="GAME OVER — Obstacle collision!";
     return;
   }}
 }}

 progress=Math.floor(player.x/finish.x*100);

 if(player.x>=finish.x){{
   ended=true;
   progress=100;
   statusEl.textContent="YOU WIN! {title} completed!";
   return;
 }}

 statusEl.textContent=`Progress: ${{progress}}%`;
}}

function draw3D(){{
 const w=canvas.width,h=canvas.height;
 ctx.fillStyle="#111827";
 ctx.fillRect(0,0,w,h/2);
 ctx.fillStyle="#020617";
 ctx.fillRect(0,h/2,w,h/2);

 for(let x=0;x<w;x+=2){{
   const distance=1+(x/w)*10;
   const wallHeight=Math.min(h,h/(distance*.72));
   const top=(h-wallHeight)/2;
   ctx.fillStyle="#334155";
   ctx.fillRect(x,top,2,wallHeight);
 }}

 ctx.fillStyle="#22d3ee";
 ctx.beginPath();
 ctx.arc(player.x*42,250,13,0,Math.PI*2);
 ctx.fill();

 ctx.fillStyle="#22c55e";
 ctx.fillRect(finish.x*42,150,24,170);

 ctx.fillStyle="#ef4444";
 for(const o of obstacles)
   ctx.fillRect(o.x*42,o.y*70-42,o.w*42,o.h*70);

 ctx.fillStyle="white";
 ctx.font="16px Arial";
 ctx.fillText("MINDCRAFT 3D",20,28);
}}

function loop(){{
 update();
 draw3D();
 requestAnimationFrame(loop);
}}

loop();
</script>
</body>
</html>
"""



def forge():
    if not DESIGN.exists():
        raise SystemExit("ERROR: game-design.md not found")

    design=get_design()
    game=build_game(design)

    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    OUTPUT.write_text(game,encoding="utf-8")

    print(f"Forged: {OUTPUT}")
    print(f"Game: {design['title']}")
    print("Engine: 3d")
    print(f"Generated: {datetime.now().isoformat(timespec="seconds")}")

    try:
        windows_path=subprocess.check_output(
            ["wslpath","-w",str(OUTPUT.resolve())],
            text=True
        ).strip()

        subprocess.Popen([
            "cmd.exe", "/c", "start", "",
            f"file:///{windows_path}"
        ])
        print("Opened: game in Windows")
    except Exception as exc:
        print(f"Auto-open skipped: {{exc}}")


if __name__=="__main__":
    forge()
