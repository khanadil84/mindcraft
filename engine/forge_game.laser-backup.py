from pathlib import Path
import re
import html
from datetime import datetime

ROOT = Path(__file__).parent.parent
DESIGN = ROOT / "designs" / "game-design.md"
OUTPUT = ROOT / "games" / "rote-forge-game.html"


def get_section(text, heading):
    pattern = rf"### {re.escape(heading)}\s*\n(.*?)(?=\n### |\n## |\Z)"
    match = re.search(pattern, text, re.S)
    return match.group(1).strip() if match else ""


def escape(value):
    return html.escape(value)


def build_laser_dodge(title, description, objective, controls, mechanic, win, lose):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(title)} — MindCraft</title>
<style>
* {{ box-sizing: border-box; }}

body {{
    margin: 0;
    min-height: 100vh;
    background: #111827;
    color: white;
    font-family: Arial, sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
}}

#app {{
    width: min(900px, 95vw);
    text-align: center;
}}

canvas {{
    display: block;
    width: 100%;
    max-width: 800px;
    margin: 18px auto;
    background: #020617;
    border: 2px solid #64748b;
    border-radius: 12px;
}}

.info {{
    color: #cbd5e1;
    margin: 5px auto;
}}

#status {{
    font-size: 20px;
    font-weight: bold;
    min-height: 28px;
}}

.footer {{
    margin-top: 12px;
    color: #94a3b8;
    font-size: 14px;
}}
</style>
</head>

<body>
<div id="app">

<h1>{escape(title)}</h1>
<div class="info">{escape(description)}</div>
<div class="info"><strong>Objective:</strong> {escape(objective)}</div>
<div class="info"><strong>Controls:</strong> {escape(controls)}</div>

<canvas id="game" width="800" height="450"></canvas>

<div id="status">Survive: 30.0 seconds</div>

<div class="info"><strong>Mechanic:</strong> {escape(mechanic)}</div>
<div class="info"><strong>Win:</strong> {escape(win)}</div>
<div class="info"><strong>Lose:</strong> {escape(lose)}</div>

<div class="footer">Powered by @Modiqo & #rote</div>

<script>
"use strict";

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");
const statusEl = document.getElementById("status");

const keys = new Set();

const player = {{
    x: 120,
    y: 225,
    radius: 12,
    speed: 4
}};

const center = {{
    x: 400,
    y: 225
}};

let angle = 0;
let startTime = performance.now();
let gameOver = false;

const survivalTime = 30000;
const laserLength = 330;
const laserWidth = 10;
const rotationSpeed = 0.0018;

document.addEventListener("keydown", event => {{
    keys.add(event.key.toLowerCase());
}});

document.addEventListener("keyup", event => {{
    keys.delete(event.key.toLowerCase());
}});

function clamp(value, min, max) {{
    return Math.max(min, Math.min(max, value));
}}

function movePlayer() {{
    if (keys.has("arrowup") || keys.has("w")) player.y -= player.speed;
    if (keys.has("arrowdown") || keys.has("s")) player.y += player.speed;
    if (keys.has("arrowleft") || keys.has("a")) player.x -= player.speed;
    if (keys.has("arrowright") || keys.has("d")) player.x += player.speed;

    player.x = clamp(player.x, player.radius, canvas.width - player.radius);
    player.y = clamp(player.y, player.radius, canvas.height - player.radius);
}}

function distanceToLaser(px, py) {{
    const dx = Math.cos(angle);
    const dy = Math.sin(angle);

    const vx = px - center.x;
    const vy = py - center.y;

    const projection = vx * dx + vy * dy;

    if (projection < 0 || projection > laserLength) return Infinity;

    const closestX = center.x + projection * dx;
    const closestY = center.y + projection * dy;

    return Math.hypot(px - closestX, py - closestY);
}}

function checkLaserCollision() {{
    return distanceToLaser(player.x, player.y)
        <= player.radius + laserWidth / 2;
}}

function drawLaser() {{
    const dx = Math.cos(angle);
    const dy = Math.sin(angle);

    const endX = center.x + dx * laserLength;
    const endY = center.y + dy * laserLength;

    ctx.save();
    ctx.beginPath();
    ctx.moveTo(center.x, center.y);
    ctx.lineTo(endX, endY);
    ctx.lineWidth = laserWidth;
    ctx.strokeStyle = "#ef4444";
    ctx.shadowBlur = 18;
    ctx.shadowColor = "#ef4444";
    ctx.stroke();
    ctx.restore();
}}

function drawPlayer() {{
    ctx.beginPath();
    ctx.arc(player.x, player.y, player.radius, 0, Math.PI * 2);
    ctx.fillStyle = "#38bdf8";
    ctx.fill();
    ctx.strokeStyle = "white";
    ctx.lineWidth = 2;
    ctx.stroke();
}}

function drawCenter() {{
    ctx.beginPath();
    ctx.arc(center.x, center.y, 8, 0, Math.PI * 2);
    ctx.fillStyle = "#facc15";
    ctx.fill();
}}

function update(now) {{
    if (gameOver) return;

    movePlayer();
    angle += rotationSpeed * 16;

    if (checkLaserCollision()) {{
        gameOver = true;
        statusEl.textContent = "GAME OVER — You touched the laser!";
        return;
    }}

    const elapsed = now - startTime;
    const remaining = Math.max(0, (survivalTime - elapsed) / 1000);

    statusEl.textContent =
        `Survive: ${{remaining.toFixed(1)}} seconds`;

    if (elapsed >= survivalTime) {{
        gameOver = true;
        statusEl.textContent = "YOU WIN! Extraction reached!";
    }}
}}

function draw() {{
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawLaser();
    drawCenter();
    drawPlayer();

    ctx.fillStyle = "white";
    ctx.font = "18px Arial";
    ctx.fillText("LASER DODGE", 20, 30);
}}

function loop(now) {{
    update(now);
    draw();
    requestAnimationFrame(loop);
}}

requestAnimationFrame(loop);
</script>

</body>
</html>
"""


def build_generic(title, description, objective, controls, mechanic, win, lose):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(title)} — MindCraft</title>
</head>
<body>

<h1>{escape(title)}</h1>
<p>{escape(description)}</p>
<p><strong>Objective:</strong> {escape(objective)}</p>
<p><strong>Controls:</strong> {escape(controls)}</p>

<canvas id="game" width="800" height="450"></canvas>

<p><strong>Mechanic:</strong> {escape(mechanic)}</p>
<p><strong>Win:</strong> {escape(win)}</p>
<p><strong>Lose:</strong> {escape(lose)}</p>

<p>Powered by @Modiqo & #rote</p>

<script>
"use strict";
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

ctx.fillStyle = "#38bdf8";
ctx.fillRect(370, 205, 60, 60);

ctx.fillStyle = "black";
ctx.font = "24px Arial";
ctx.fillText("MindCraft generated game", 250, 330);
</script>

</body>
</html>
"""


def forge():
    if not DESIGN.exists():
        raise SystemExit("ERROR: designs/game-design.md does not exist.")

    text = DESIGN.read_text(encoding="utf-8")

    lines = text.splitlines()
    title = lines[0].replace("# ", "").strip()

    description = get_section(text, "Short Description")
    objective = get_section(text, "Core Objective")
    controls = get_section(text, "Player Controls")
    mechanic = get_section(text, "Main Mechanic")
    win = get_section(text, "Win Condition")
    lose = get_section(text, "Lose Condition")

    title_lower = title.lower()
    mechanic_lower = mechanic.lower()

    if (
        "laser" in title_lower
        or "laser" in mechanic_lower
        or "dodge" in title_lower
    ):
        game = build_laser_dodge(
            title,
            description,
            objective,
            controls,
            mechanic,
            win,
            lose
        )
        engine = "laser-dodge"
    else:
        game = build_generic(
            title,
            description,
            objective,
            controls,
            mechanic,
            win,
            lose
        )
        engine = "generic"

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(game, encoding="utf-8")

    print(f"Forged: {OUTPUT}")
    print(f"Game: {title}")
    print(f"Engine: {engine}")
    print(f"Generated: {datetime.now().isoformat(timespec='seconds')}")
    # Automatically open the generated game on Windows.
    import subprocess
    try:
        windows_path = subprocess.check_output(
            ["wslpath", "-w", str(OUTPUT.resolve())],
            text=True
        ).strip()
        subprocess.Popen(["explorer.exe", windows_path])
        print("Opened: game in Windows")
    except Exception as exc:
        print(f"Auto-open skipped: {exc}")



if __name__ == "__main__":
    forge()
