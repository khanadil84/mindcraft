# MindCraft

## The Autonomous AI Game Designer & Infinite Micro-World Forge

> **MindCraft does not generate code and walk away.**
> It generates a playable 3D game, tests it in a real browser, diagnoses failures, heals itself, and delivers verified output — all in one autonomous loop.

[![Rote Play](https://img.shields.io/badge/Rote%20Play-mindcraft--3d--game--forge%400.0.1-blue)](https://play.modiqo.ai/mindcraft/mindcraft-3d-game-forge@0.0.1)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-1.62+-2EAD33)](https://playwright.dev/)
[![License](https://img.shields.io/badge/License-ISC-green)](LICENSE)

---

## The 30-Second Pitch

| What MindCraft Does | Why It Matters |
|---------------------|----------------|
| Generates playable 3D games from design specs | Not just code — complete, runnable micro-worlds |
| Tests every game in a real browser automatically | No guessing — every output is verified |
| Classifies failures into 7 distinct categories | Not all bugs are equal — repair strategies differ |
| Self-heals 5 supported failure classes | Pattern-based repair, not random patching |
| Enforces a standardized contract on every game | Programmatic verification, not visual inspection |
| Publishes verified games as Rote Plays | One command to install, run, and verify |

**The closed loop is the innovation.** Generation alone is not enough. Testing alone is not enough. The autonomous cycle of generate → test → diagnose → repair → verify is what makes MindCraft different.

---

## Rote Play Submission

**Published Play:** [`mindcraft/mindcraft-3d-game-forge@0.0.1`](https://play.modiqo.ai/mindcraft/mindcraft-3d-game-forge@0.0.1)

```bash
npx mindcraft-3d-game-forge@0.0.1
```

The Rote Play packages the complete MindCraft forge loop — design generation, 3D game forging, Playwright browser testing, and self-healing — into a single installable artifact. Run it once, and the entire autonomous cycle executes: design → generate → playtest → self-heal → verified output.

---

## The Problem AI Code Generation Doesn't Solve

Ask any AI to generate a game. You get a file. Then what?

- **No verification** that it actually runs
- **No testing** in a real browser environment
- **No failure detection** when something breaks
- **No self-repair** — you're the debugger
- **No contract** guaranteeing the output is usable

Traditional AI code generation is a **one-shot gamble**. You hope it works. MindCraft **proves** it works.

---

## The Autonomous Forge Loop

```
                        ┌─────────────────────┐
                        │   GAME DESIGN INPUT  │
                        │   (Markdown + Schema)│
                        └──────────┬──────────┘
                                   │
                                   ▼
                  ┌────────────────────────────────┐
                  │         FORGE ENGINE           │
                  │  Python → 3D HTML5 Canvas Game │
                  └───────────────┬────────────────┘
                                  │
                                  ▼
                  ┌────────────────────────────────┐
                  │      PLAYTEST SUITE            │
                  │  Playwright + Headless Chromium │
                  └───────────────┬────────────────┘
                                  │
                                  ▼
                  ┌────────────────────────────────┐
                  │      8-POINT VERIFICATION      │
                  │  Contract · Movement · Win/Loss │
                  └───────────────┬────────────────┘
                                  │
                         ┌────────┴────────┐
                         │                 │
                        PASS              FAIL
                         │                 │
                         ▼                 ▼
              ┌──────────────┐    ┌─────────────────┐
              │   OUTPUT     │    │   SELF-HEAL     │
              │  Verified ✓  │    │  Diagnose → Fix │
              └──────────────┘    └────────┬────────┘
                                           │
                                           ▼
                                  ┌────────────────┐
                                  │   RE-TEST      │
                                  │  PASS → OUTPUT │
                                  │  FAIL → Report │
                                  └────────────────┘
```

---

## What MindCraft Actually Builds

Four implemented game concepts, each a complete, playable 3D micro-world:

| Game | Mechanic | Win | Loss |
|------|----------|-----|------|
| **Gravity Flip** | Space flips gravity between floor/ceiling | Reach finish zone | Obstacle collision |
| **Orb Runner** | Collect orbs, evade hunters | Collect 10 orbs | Lose 3 lives |
| **Laser Dodge** | Dodge rotating laser beams | Survive 30 seconds | Touch a laser |
| **Color Gate** | Match colors (R/G/B/Y) at gates | Pass 6 gates correctly | Wrong color |

Every game is a **single self-contained HTML file**:
- Zero external runtime dependencies
- HTML5 Canvas 3D rendering
- Vanilla JavaScript
- `MINDCRAFT_GAME` contract exposed for automated testing

---

## Architecture

```
mindcraft/
├── engine/
│   ├── forge_game.py          # Main forge: design → 3D HTML game
│   ├── generate_design.py     # Design generator (4 game concepts)
│   └── self_heal.py           # Diagnose failures, apply repairs
├── designs/
│   ├── game-design.schema.md  # Contract: what every design must contain
│   └── game-design.md         # Current generated design
├── games/
│   ├── mindcraft-game.html    # Primary forge output
│   ├── rote-forge-game.html   # Alternate forge output
│   └── neon-escape-3d.html    # Earlier 3D prototype
├── tests/
│   ├── playtest-3d.js         # Playwright automated browser test
│   ├── playtest-report.txt    # Latest playtest result
│   └── repair-plan.txt        # Self-heal repair plan
└── backups/
    └── mindcraft-game.known-good.html  # Known-good backup
```

| Component | Purpose |
|-----------|---------|
| `engine/forge_game.py` | Reads design, generates complete 3D HTML game |
| `engine/generate_design.py` | Randomly selects from 4 game concepts |
| `engine/self_heal.py` | Diagnoses 7 failure classes, applies pattern repairs |
| `tests/playtest-3d.js` | Headless Chromium testing via Playwright |
| `designs/game-design.schema.md` | Contract defining required design fields |

---

## Contract-Driven Games

Every generated game exposes a standardized contract on `window.MINDCRAFT_GAME`:

```javascript
window.MINDCRAFT_GAME = {
  version: "1.0",
  engine: "3d",
  title: "Color Gate",
  gameType: "color-gate",

  getStatus: () => string,  // Current status text
  isEnded: () => boolean,   // Whether game has ended
  getState: () => object,   // Game state (position, progress)
  restart: () => void       // Reset to initial state
}
```

The test suite does not guess whether the game works. It **programmatically verifies** every required behavior through this interface.

---

## Automated Playtesting

Eight verification passes in every test run:

| # | Test | What It Checks |
|---|------|----------------|
| 1 | **Title** | Game title ends with `" — MindCraft"` |
| 2 | **Canvas** | Exactly one `<canvas>` element exists |
| 3 | **Errors** | Zero uncaught JavaScript errors |
| 4 | **Contract** | `MINDCRAFT_GAME` exists with all methods |
| 5 | **Movement** | Player position changes after input |
| 6 | **Win** | Win condition reachable through gameplay |
| 7 | **Loss** | Wrong input triggers game-over |
| 8 | **Restart** | `restart()` resets without corruption |

### Real Playtest Evidence

```
Title: Color Gate — MindCraft
Canvas count: 1
JavaScript errors: 0
Contract: {"exists":true,"version":"1.0","engine":"3d","gameType":"color-gate",...}
Movement test: {"x":1.5,"y":5.5} -> {"x":2.78,"y":5.5}
Win test state: {"ended":true,"progress":100,"status":"YOU WIN!"}
Loss test state: {"ended":true,"status":"GAME OVER — Wrong color!"}
Restart test: generic restart verified
PLAYTEST PASS: Generic 3D game "Color Gate" loads, contract works, movement works, restart works, and no JavaScript errors occur.
```

This output is from `tests/playtest-report.txt` — real verification, not a demo.

---

## Self-Healing

When playtesting fails, MindCraft classifies the failure and attempts automatic repair.

### Supported Failure Classes

| Class | Diagnosis | Auto-Repair |
|-------|-----------|-------------|
| `JAVASCRIPT_ERROR` | Runtime errors in game code | Restore from known-good backup |
| `CONTRACT_FAILURE` | Missing/broken `MINDCRAFT_GAME` | Restore `gameType` to valid value |
| `RESTART_FAILURE` | Restart key binding broken | Restore R-key restart behavior |
| `COLLISION_FAILURE` | Obstacle collision returns false | Restore collision detection logic |
| `WIN_FAILURE` | Win condition unreachable | Restore finish-zone logic |
| `INPUT_FAILURE` | Player movement broken | Diagnostic only — no auto-repair |
| `PLAYTEST_ENVIRONMENT_FAILURE` | Browser launch failed | Diagnostic only — environment issue |

### Self-Heal Flow

```
Playtest Fails → Diagnose → Classify → Repair → Re-test → Verified
                                                       or → Report
```

### What Self-Heal Does NOT Do

MindCraft's self-healing is **pattern-based and bounded**:
- Repairs known failure patterns in generated game code
- Does NOT repair arbitrary JavaScript bugs
- Does NOT fix browser compatibility issues
- Does NOT repair the Python engine itself
- Does NOT guarantee repair for every failure

If no repair pattern matches, MindCraft generates a diagnostic report and stops.

---

## Verification Philosophy

> **Generated output is not done until it is verified.**

```
Generate → Test → Diagnose → Repair → Re-test → Verified
```

Every game that passes the loop has:
- Loaded in a real browser (headless Chromium)
- Exposed the required contract
- Responded to player input
- Reached its win condition through valid gameplay
- Detected its loss condition correctly
- Restarted without state corruption
- Zero uncaught JavaScript errors

**Strongest evidence:** `tests/playtest-report.txt` shows a complete PASS with all 8 checks verified.

---

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- npm

### Install & Run

```bash
# Install dependencies
npm install

# Generate a random game design
python engine/generate_design.py

# Forge the design into a playable 3D game
python engine/forge_game.py

# Run the full autonomous loop (playtest + self-heal)
python engine/self_heal.py
```

### Run Tests Only

```bash
npm install playwright
npx playwright install chromium
node tests/playtest-3d.js
```

---

## Why This Is Different

| | Traditional Game Dev | AI Code Generation | **MindCraft** |
|---|---|---|---|
| **Output** | Playable game | Code file | Verified playable game |
| **Testing** | Manual QA | None | Automated browser testing |
| **Failure Detection** | Bug reports | None | 7-class failure taxonomy |
| **Self-Repair** | Developer fixes | None | Pattern-based auto-repair |
| **Verification** | Human judgment | None | Contract + behavioral checks |
| **Feedback Loop** | Days/weeks | None | Automated, sub-minute |

**The difference is the closed loop.** MindCraft does not stop at generation. It generates, tests, diagnoses, repairs, and verifies — autonomously, in a single execution.

---

## Why It Matters

MindCraft demonstrates that AI-generated software does not have to be a black box:

1. **Generated code can verify itself** — through contracts and automated browser testing
2. **Failures can be classified** — not all errors are equal, repair strategies differ
3. **Self-healing is practical** — for bounded failure classes with known patterns
4. **The feedback loop is the product** — not the generation, not the test, but the closed cycle

This is a working prototype of a future where software generates, tests, diagnoses, repairs, and delivers verified output.

---

## Future Vision

> **Note:** The following are future possibilities, not implemented functionality.

| Capability | Status | Description |
|------------|--------|-------------|
| LLM-Powered Design | Future | AI-driven game design generation |
| Dynamic Game Types | Future | Arbitrary game concepts beyond 4 implemented |
| Multi-Engine Forge | Future | WebGL, Three.js, Godot output |
| Cloud Deployment | Future | Auto-deploy verified games |
| Learning Repair | Future | Expand self-heal from failure history |
| Visual Regression | Future | Screenshot comparison testing |

---

## Rote Play

**Package:** `mindcraft/mindcraft-3d-game-forge@0.0.1`

**URI:** [https://play.modiqo.ai/mindcraft/mindcraft-3d-game-forge@0.0.1](https://play.modiqo.ai/mindcraft/mindcraft-3d-game-forge@0.0.1)

```bash
npx mindcraft-3d-game-forge@0.0.1
```

What the Rote Play does:
1. Generates a random game design from 4 implemented concepts
2. Forges the design into a playable 3D HTML5 Canvas game
3. Runs automated browser testing via Playwright
4. Diagnoses and repairs supported failure classes
5. Delivers a verified, playable game output

---

## Author

**khanadil84** — [GitHub](https://github.com/khanadil84)

Built with @Modiqo & #rote.

---

## License

ISC

---

<div align="center">

**MindCraft** — Generated. Tested. Verified. Playable.

</div>
