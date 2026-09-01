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

    if title == "Orb Runner":
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
<div id="status">Orbs: 0 / 10 | Lives: 3</div>
<div class="footer">Powered by @Modiqo & #rote</div>

<script>
"use strict";

const canvas=document.getElementById("game");
const ctx=canvas.getContext("2d");
const statusEl=document.getElementById("status");

const player={{x:1.5,y:5.5,radius:.25,speed:.075}};
const orbs=[
 {{x:3,y:2}},{{x:5,y:8}},{{x:7,y:3}},{{x:9,y:8}},{{x:11,y:2}},
 {{x:13,y:7}},{{x:15,y:3}},{{x:17,y:8}},{{x:19,y:3}},{{x:21,y:7}}
];
const hunters=[
 {{x:6,y:5,dx:.035,dy:.025}},
 {{x:14,y:5,dx:-.03,dy:.03}}
];

const keys=new Set();
let collected=0;
let lives=3;
let ended=false;

window.MINDCRAFT_GAME={{
 version:"1.0",
 engine:"3d",
 title:{title!r},
 gameType:"orb-runner",
 getStatus:()=>statusEl.textContent,
 isEnded:()=>ended,
 getState:()=>({{
   x:player.x,
   y:player.y,
   collected,
   lives,
   ended
 }}),
 restart:()=>location.reload()
}};

document.addEventListener("keydown",e=>{{
 const k=e.key.toLowerCase();
 if(k==="r" && ended){{location.reload();return}}
 keys.add(k);
 if(["arrowup","arrowdown","arrowleft","arrowright","w","a","s","d"].includes(k))
   e.preventDefault();
}});

document.addEventListener("keyup",e=>keys.delete(e.key.toLowerCase()));

function update(){{
 if(ended)return;

 if(keys.has("arrowright")||keys.has("d"))player.x+=player.speed;
 if(keys.has("arrowleft")||keys.has("a"))player.x-=player.speed;
 if(keys.has("arrowup")||keys.has("w"))player.y-=player.speed;
 if(keys.has("arrowdown")||keys.has("s"))player.y+=player.speed;

 player.x=Math.max(.5,Math.min(22,player.x));
 player.y=Math.max(1,Math.min(9,player.y));

 for(const o of orbs){{
   if(!o.taken && Math.hypot(player.x-o.x,player.y-o.y)<.45){{
     o.taken=true;
     collected++;
   }}
 }}

 for(const h of hunters){{
   h.x+=h.dx;
   h.y+=h.dy;
   if(h.x<2||h.x>21)h.dx*=-1;
   if(h.y<1.5||h.y>8.5)h.dy*=-1;

   if(Math.hypot(player.x-h.x,player.y-h.y)<.5){{
     lives--;
     player.x=1.5;
     player.y=5.5;

     if(lives<=0){{
       ended=true;
       statusEl.textContent="GAME OVER — All lives lost!";
       return;
     }}
   }}
 }}

 if(collected>=10){{
   ended=true;
   statusEl.textContent="YOU WIN! Orb Runner completed!";
   return;
 }}

 statusEl.textContent=`Orbs: ${{collected}} / 10 | Lives: ${{lives}}`;
}}

function draw3D(){{
 const w=canvas.width,h=canvas.height;

 ctx.fillStyle="#101827";
 ctx.fillRect(0,0,w,h/2);

 ctx.fillStyle="#020617";
 ctx.fillRect(0,h/2,w,h/2);

 for(let x=0;x<w;x+=3){{
   const wave=Math.sin(x*.025)*18;
   const wallHeight=120+wave;

   ctx.fillStyle=`rgb(${{20+Math.floor(Math.abs(wave))}},${{40+Math.floor(Math.abs(wave))}},90)`;
   ctx.fillRect(x,(h-wallHeight)/2,3,wallHeight);
 }}
}}

function project(x,y,color,size){{
 const dx=x-player.x;
 const dy=y-player.y;
 const distance=Math.hypot(dx,dy);

 if(distance<.1)return;

 const screenX=canvas.width/2+(dx/distance)*(canvas.width*.35);
 const projected=Math.min(80,canvas.height/(distance*.45))*size;

 ctx.beginPath();
 ctx.arc(screenX,canvas.height/2,projected,0,Math.PI*2);
 ctx.fillStyle=color;
 ctx.shadowBlur=20;
 ctx.shadowColor=color;
 ctx.fill();
 ctx.shadowBlur=0;
}}

function draw(){{
 draw3D();

 for(const o of orbs){{
   if(!o.taken)project(o.x,o.y,"#22d3ee",.18);
 }}

 for(const h of hunters){{
   project(h.x,h.y,"#ef4444",.28);
 }}

 ctx.fillStyle="white";
 ctx.font="16px Arial";
 ctx.fillText("3D ORB RUNNER",20,28);

 ctx.strokeStyle="rgba(255,255,255,.5)";
 ctx.beginPath();
 ctx.moveTo(canvas.width/2-8,canvas.height/2);
 ctx.lineTo(canvas.width/2+8,canvas.height/2);
 ctx.moveTo(canvas.width/2,canvas.height/2-8);
 ctx.lineTo(canvas.width/2,canvas.height/2+8);
 ctx.stroke();
}}

function loop(){{
 update();
 draw();
 requestAnimationFrame(loop);
}}

loop();
</script>
</body>
</html>
"""

    if title == "Laser Dodge":
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{title}} — MindCraft</title>
<style>
body{{margin:0;background:#050816;color:white;font-family:Arial,sans-serif;text-align:center}}
#game{{display:block;width:min(900px,96vw);height:auto;margin:18px auto 8px;background:#000;border:2px solid #334155}}
#status{{font-size:20px;font-weight:bold}}
.info{{color:#cbd5e1;margin:5px}}
.footer{{color:#94a3b8;margin:12px}}
</style>
</head>
<body>
<h1>{{title}}</h1>
<div class="info">{{description}}</div>
<div class="info">{{controls}}</div>
<canvas id="game" width="900" height="500"></canvas>
<div id="status">Time: 0 | Lives: 3</div>
<div class="footer">Powered by @Modiqo & #rote</div>

<script>
"use strict";

const canvas=document.getElementById("game");
const ctx=canvas.getContext("2d");
const statusEl=document.getElementById("status");

const player={{x:2,y:5,radius:.28,speed:.08}};
const lasers=[
 {{x:6,y:2.5,dx:.045}},
 {{x:11,y:7.5,dx:-.055}},
 {{x:16,y:3.5,dx:.065}}
];

const keys=new Set();
let lives=3;
let ended=false;
let start=performance.now();

window.MINDCRAFT_GAME={{
 version:"1.0",
 engine:"3d",
 title:{{title!r}},
 gameType:"laser-dodge",
 getStatus:()=>statusEl.textContent,
 isEnded:()=>ended,
 getState:()=>({{
   x:player.x,
   y:player.y,
   lives,
   ended
 }}),
 restart:()=>location.reload()
}};

document.addEventListener("keydown",e=>{{
 const k=e.key.toLowerCase();

 if(k==="r" && ended){{
   location.reload();
   return;
 }}

 keys.add(k);

 if(["arrowup","arrowdown","arrowleft","arrowright","w","a","s","d"].includes(k))
   e.preventDefault();
}});

document.addEventListener("keyup",e=>keys.delete(e.key.toLowerCase()));

function update(){{
 if(ended)return;

 if(keys.has("arrowright")||keys.has("d"))player.x+=player.speed;
 if(keys.has("arrowleft")||keys.has("a"))player.x-=player.speed;
 if(keys.has("arrowup")||keys.has("w"))player.y-=player.speed;
 if(keys.has("arrowdown")||keys.has("s"))player.y+=player.speed;

 player.x=Math.max(1,Math.min(21,player.x));
 player.y=Math.max(1,Math.min(9,player.y));

 for(const l of lasers){{
   l.x+=l.dx;

   if(l.x<2||l.x>21)l.dx*=-1;

   if(Math.abs(player.x-l.x)<.45 &&
      Math.abs(player.y-l.y)<.55){{
     lives--;
     player.x=2;
     player.y=5;

     if(lives<=0){{
       ended=true;
       statusEl.textContent="GAME OVER — All lives lost!";
       return;
     }}
   }}
 }}

 const elapsed=Math.floor((performance.now()-start)/1000);

 if(elapsed>=30){{
   ended=true;
   statusEl.textContent="YOU WIN! Laser Dodge survived 30 seconds!";
   return;
 }}

 statusEl.textContent=`Time: ${{elapsed}} | Lives: ${{lives}}`;
}}

function draw3D(){{
 const w=canvas.width,h=canvas.height;

 ctx.fillStyle="#111827";
 ctx.fillRect(0,0,w,h/2);

 ctx.fillStyle="#020617";
 ctx.fillRect(0,h/2,w,h/2);

 for(let x=0;x<w;x+=4){{
   const wave=Math.sin(x*.025)*20;
   const wallHeight=110+wave;

   ctx.fillStyle=`rgb(30,45,${{90+Math.floor(Math.abs(wave))}})`;
   ctx.fillRect(x,(h-wallHeight)/2,4,wallHeight);
 }}
}}

function project(x,y,color,size){{
 const dx=x-player.x;
 const dy=y-player.y;
 const distance=Math.hypot(dx,dy);

 if(distance<.1)return;

 const screenX=canvas.width/2+(dx/distance)*(canvas.width*.36);
 const projected=Math.min(100,canvas.height/(distance*.4))*size;

 ctx.beginPath();
 ctx.arc(screenX,canvas.height/2,projected,0,Math.PI*2);
 ctx.fillStyle=color;
 ctx.shadowBlur=24;
 ctx.shadowColor=color;
 ctx.fill();
 ctx.shadowBlur=0;
}}

function draw(){{
 draw3D();

 for(const l of lasers)
   project(l.x,l.y,"#ef4444",.3);

 project(player.x+1,player.y,"#22d3ee",.22);

 ctx.fillStyle="white";
 ctx.font="16px Arial";
 ctx.fillText("3D LASER DODGE",20,28);

 ctx.strokeStyle="rgba(255,255,255,.5)";
 ctx.beginPath();
 ctx.moveTo(canvas.width/2-8,canvas.height/2);
 ctx.lineTo(canvas.width/2+8,canvas.height/2);
 ctx.moveTo(canvas.width/2,canvas.height/2-8);
 ctx.lineTo(canvas.width/2,canvas.height/2+8);
 ctx.stroke();
}}

function loop(){{
 update();
 draw();
 requestAnimationFrame(loop);
}}

loop();
</script>
</body>
</html>
"""

    if title == "Color Gate":
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
<div id="status">Gate: BLUE | Progress: 0%</div>
<div class="footer">Powered by @Modiqo & #rote</div>

<script>
"use strict";

const canvas=document.getElementById("game");
const ctx=canvas.getContext("2d");
const statusEl=document.getElementById("status");

const player={{x:1.5,y:5.5,speed:.08,radius:.25}};
const gates=[
 {{x:5,y:3,color:"red"}},
 {{x:8,y:7,color:"blue"}},
 {{x:11,y:3,color:"green"}},
 {{x:14,y:7,color:"yellow"}},
 {{x:17,y:3,color:"red"}},
 {{x:20,y:7,color:"blue"}}
];

const colors=["red","blue","green","yellow"];
const keys=new Set();

let selected="blue";
let progress=0;
let ended=false;

window.MINDCRAFT_GAME={{
 version:"1.0",
 engine:"3d",
 title:{title!r},
 gameType:"color-gate",
 getStatus:()=>statusEl.textContent,
 isEnded:()=>ended,
 getState:()=>({{
   x:player.x,
   y:player.y,
   color:selected,
   progress,
   ended
 }}),
 restart:()=>location.reload()
}};

document.addEventListener("keydown",e=>{{
 const k=e.key.toLowerCase();

 if(k==="r" && ended){{
   location.reload();
   return;
 }}

 if(["1","2","3","4"].includes(k)){{
   selected=colors[Number(k)-1];
 }}

 keys.add(k);

 if(["arrowup","arrowdown","arrowleft","arrowright","w","a","s","d"].includes(k))
   e.preventDefault();
}});

document.addEventListener("keyup",e=>keys.delete(e.key.toLowerCase()));

function update(){{
 if(ended)return;

 if(keys.has("arrowright")||keys.has("d"))player.x+=player.speed;
 if(keys.has("arrowleft")||keys.has("a"))player.x-=player.speed;
 if(keys.has("arrowup")||keys.has("w"))player.y-=player.speed;
 if(keys.has("arrowdown")||keys.has("s"))player.y+=player.speed;

 player.x=Math.max(.5,Math.min(21.5,player.x));
 player.y=Math.max(1,Math.min(9,player.y));

 for(const g of gates){{
   if(!g.passed &&
      Math.abs(player.x-g.x)<.35){{

     if(selected!==g.color){{
       ended=true;
       statusEl.textContent=
         `GAME OVER — Wrong color! Gate was ${{g.color.toUpperCase()}}`;
       return;
     }}

     g.passed=true;
     progress=Math.floor(
       gates.filter(x=>x.passed).length/gates.length*100
     );
   }}
 }}

 if(progress>=100){{
   ended=true;
   statusEl.textContent="YOU WIN! Color Gate completed!";
   return;
 }}

 statusEl.textContent=
   `Gate: ${{selected.toUpperCase()}} | Progress: ${{progress}}%`;
}}

function draw3D(){{
 const w=canvas.width,h=canvas.height;

 ctx.fillStyle="#111827";
 ctx.fillRect(0,0,w,h/2);

 ctx.fillStyle="#020617";
 ctx.fillRect(0,h/2,w,h/2);

 for(let x=0;x<w;x+=4){{
   const wave=Math.sin(x*.025)*18;
   const wallHeight=115+wave;

   ctx.fillStyle=
     `rgb(25,45,${{90+Math.floor(Math.abs(wave))}})`;

   ctx.fillRect(x,(h-wallHeight)/2,4,wallHeight);
 }}
}}

function project(x,y,color,size){{
 const dx=x-player.x;
 const dy=y-player.y;
 const distance=Math.hypot(dx,dy);

 if(distance<.1)return;

 const screenX=
   canvas.width/2+
   (dx/distance)*(canvas.width*.36);

 const projected=
   Math.min(110,canvas.height/(distance*.4))*size;

 ctx.beginPath();
 ctx.arc(
   screenX,
   canvas.height/2,
   projected,
   0,
   Math.PI*2
 );

 ctx.fillStyle=color;
 ctx.shadowBlur=24;
 ctx.shadowColor=color;
 ctx.fill();
 ctx.shadowBlur=0;
}}

function draw(){{
 draw3D();

 for(const g of gates){{
   if(!g.passed)
     project(g.x,g.y,g.color,.32);
 }}

 project(
   player.x+1,
   player.y,
   selected,
   .22
 );

 ctx.fillStyle="white";
 ctx.font="16px Arial";
 ctx.fillText("3D COLOR GATE",20,28);
 ctx.fillText(
   "1=RED  2=BLUE  3=GREEN  4=YELLOW",
   20,
   475
 );

 ctx.strokeStyle="rgba(255,255,255,.5)";
 ctx.beginPath();
 ctx.moveTo(canvas.width/2-8,canvas.height/2);
 ctx.lineTo(canvas.width/2+8,canvas.height/2);
 ctx.moveTo(canvas.width/2,canvas.height/2-8);
 ctx.lineTo(canvas.width/2,canvas.height/2+8);
 ctx.stroke();
}}

function loop(){{
 update();
 draw();
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
