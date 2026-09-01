from pathlib import Path
import re
import html

ROOT = Path(__file__).parent.parent
DESIGN = ROOT / "designs" / "game-design.md"
OUTPUT = ROOT / "games" / "rote-forge-game.html"


def get_section(text, heading):
    pattern = rf"### {re.escape(heading)}\s*\n(.*?)(?=\n### |\n## |\Z)"
    match = re.search(pattern, text, re.S)
    return match.group(1).strip() if match else ""


def forge():
    if not DESIGN.exists():
        raise SystemExit("ERROR: game-design.md does not exist. Generate a design first.")

    text = DESIGN.read_text(encoding="utf-8")

    title = text.splitlines()[0].replace("# ", "").strip()
    description = get_section(text, "Short Description")
    objective = get_section(text, "Core Objective")
    controls = get_section(text, "Player Controls")
    mechanic = get_section(text, "Main Mechanic")
    win = get_section(text, "Win Condition")
    lose = get_section(text, "Lose Condition")

    safe_title = html.escape(title)
    safe_description = html.escape(description)
    safe_objective = html.escape(objective)
    safe_controls = html.escape(controls)
    safe_mechanic = html.escape(mechanic)
    safe_win = html.escape(win)
    safe_lose = html.escape(lose)

    game = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{safe_title} — MindCraft</title>

<style>
* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    min-height: 100vh;
    font-family: Arial, sans-serif;
    background: #111827;
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
}}

#app {{
    width: min(900px, 95vw);
    text-align: center;
}}

h1 {{
    margin-bottom: 6px;
}}

.info {{
    margin: 6px auto;
    max-width: 700px;
    color: #cbd5e1;
}}

canvas {{
    display: block;
    width: 100%;
    max-width: 800px;
    height: auto;
    margin: 20px auto;
    background: #020617;
    border: 2px solid #64748b;
    border-radius: 12px;
}}

#status {{
    font-size: 20px;
    font-weight: bold;
    min-height: 28px;
}}

.footer {{
    margin-top: 15px;
    color: #94a3b8;
    font-size: 14px;
}}
</style>
</head>

<body>
<div id="app">

<h1>{safe_title}</h1>

<div class="info">{safe_description}</div>
<div class="info"><strong>Objective:</strong> {safe_objective}</div>
<div class="info"><strong>Controls:</strong> {safe_controls}</div>

<canvas id="game" width="800" height="450"></canvas>

<div id="status">Collect 10 orbs to win!</div>

<div class="info">
<strong>Mechanic:</strong> {safe_mechanic}
</div>

<div class="info">
<strong>Win:</strong> {safe_win}
</div>

<div class="info">
<strong>Lose:</strong> {safe_lose}
</div>

<div class="footer">
Powered by @Modiqo & #rote
</div>

</div>

<script>
"use strict";

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");
const statusEl = document.getElementById("status");

const keys = new Set();

const player = {{
    x: 100,
    y: 225,
    size: 22,
    speed: 4
}};

let score = 0;
let lives = 3;
let gameOver = false;

const orb = {{
    x: 600,
    y: 200,
    size: 14
}};

const enemies = [
    {{ x: 350, y: 120, size: 24, vx: 2 }},
    {{ x: 500, y: 330, size: 24, vx: -2 }}
];

document.addEventListener("keydown", event => {{
    keys.add(event.key.toLowerCase());
}});

document.addEventListener("keyup", event => {{
    keys.delete(event.key.toLowerCase());
}});

function clamp(value, min, max) {{
    return Math.max(min, Math.min(max, value));
}}

function distance(a, b) {{
    return Math.hypot(a.x - b.x, a.y - b.y);
}}

function movePlayer() {{
    if (keys.has("arrowup") || keys.has("w")) player.y -= player.speed;
    if (keys.has("arrowdown") || keys.has("s")) player.y += player.speed;
    if (keys.has("arrowleft") || keys.has("a")) player.x -= player.speed;
    if (keys.has("arrowright") || keys.has("d")) player.x += player.speed;

    player.x = clamp(player.x, player.size, canvas.width - player.size);
    player.y = clamp(player.y, player.size, canvas.height - player.size);
}}

function moveEnemies() {{
    for (const enemy of enemies) {{
        enemy.x += enemy.vx;

        if (enemy.x < enemy.size || enemy.x > canvas.width - enemy.size) {{
            enemy.vx *= -1;
        }}
    }}
}}

function checkCollisions() {{
    if (distance(player, orb) < player.size + orb.size) {{
        score += 1;

        orb.x = 50 + Math.random() * (canvas.width - 100);
        orb.y = 50 + Math.random() * (canvas.height - 100);

        if (score >= 10) {{
            gameOver = true;
            statusEl.textContent = "YOU WIN! 🎉";
        }}
    }}

    for (const enemy of enemies) {{
        if (distance(player, enemy) < player.size + enemy.size) {{
            lives -= 1;

            player.x = 100;
            player.y = 225;

            if (lives <= 0) {{
                gameOver = true;
                statusEl.textContent = "GAME OVER";
            }}
        }}
    }}
}}

function draw() {{
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Player
    ctx.fillStyle = "#38bdf8";
    ctx.fillRect(
        player.x - player.size,
        player.y - player.size,
        player.size * 2,
        player.size * 2
    );

    // Orb
    ctx.beginPath();
    ctx.arc(orb.x, orb.y, orb.size, 0, Math.PI * 2);
    ctx.fillStyle = "#facc15";
    ctx.fill();

    // Enemies
    for (const enemy of enemies) {{
        ctx.fillStyle = "#f43f5e";
        ctx.fillRect(
            enemy.x - enemy.size,
            enemy.y - enemy.size,
            enemy.size * 2,
            enemy.size * 2
        );
    }}

    ctx.fillStyle = "white";
    ctx.font = "18px Arial";
    ctx.fillText(`Orbs: ${{score}} / 10`, 20, 30);
    ctx.fillText(`Lives: ${{lives}}`, 680, 30);
}}

function loop() {{
    if (!gameOver) {{
        movePlayer();
        moveEnemies();
        checkCollisions();

        statusEl.textContent =
            `Orbs: ${{score}} / 10 | Lives: ${{lives}}`;
    }}

    draw();
    requestAnimationFrame(loop);
}}

loop();
</script>

</body>
</html>
"""

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(game, encoding="utf-8")

    print(f"Forged: {OUTPUT}")
    print(f"Game: {title}")


if __name__ == "__main__":
    forge()
