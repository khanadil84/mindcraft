from pathlib import Path
import subprocess
import sys
from datetime import datetime

ROOT = Path(__file__).parent.parent
PLAYTEST = ROOT / "tests" / "playtest-3d.js"
REPORT = ROOT / "tests" / "playtest-report.txt"


def diagnose(output):
    text = output.lower()

    if "javascript errors:" in text and "javascript errors: 0" not in text:
        return "JAVASCRIPT_ERROR"

    if "restart did not reset the game" in text or "restart" in text and "fail:" in text:
        return "RESTART_FAILURE"

    if "win condition not reached" in text or "finish zone" in text and "fail:" in text:
        return "WIN_FAILURE"

    if "obstacle collision not detected" in text or "obstacle collision" in text and "fail:" in text:
        return "COLLISION_FAILURE"

    if "player did not move" in text or "movement" in text and "fail:" in text:
        return "INPUT_FAILURE"

    if "win condition" in text or "finish zone" in text and "fail:" in text:
        return "WIN_FAILURE"

    if "contract" in text and (
        "fail:" in text or "contract missing" in text
    ):
        return "CONTRACT_FAILURE"

    if "error:" in text or "fail:" in text:
        return "UNKNOWN_FAILURE"

    return "PASS"


def run_playtest():
    print("SELF-HEAL: Running automated playtest...")

    result = subprocess.run(
        ["node", str(PLAYTEST)],
        cwd=ROOT,
        capture_output=True,
        text=True
    )

    output = result.stdout + result.stderr
    diagnosis = diagnose(output)

    REPORT.write_text(
        f"MindCraft Playtest Report\n"
        f"Generated: {datetime.now().isoformat(timespec='seconds')}\n"
        f"Exit Code: {result.returncode}\n"
        f"Diagnosis: {diagnosis}\n\n"
        f"{output}",
        encoding="utf-8"
    )

    print(output)
    print(f"SELF-HEAL: Diagnosis = {diagnosis}")

    if result.returncode == 0:
        print("SELF-HEAL: PLAYTEST PASS")
        return True

    print("SELF-HEAL: PLAYTEST FAIL")
    print(f"SELF-HEAL: Failure classified as {diagnosis}")
    print(f"Report saved: {REPORT}")

    return False



def repair_game(diagnosis):
    game_file = ROOT / "games" / "mindcraft-game.html"

    if diagnosis == "JAVASCRIPT_ERROR":
        backup_file = Path("/tmp/mindcraft-game.js-backup.html")

        if backup_file.exists():
            game_file.write_text(
                backup_file.read_text(encoding="utf-8"),
                encoding="utf-8"
            )
            print("SELF-HEAL: Applied JAVASCRIPT_ERROR repair.")
            print("SELF-HEAL: Restored last known-good game backup.")
            return True

        print("SELF-HEAL: JavaScript backup not found.")
        return False

    if diagnosis == "CONTRACT_FAILURE":
        text = game_file.read_text(encoding="utf-8")

        if 'gameType:"broken-game"' in text:
            text = text.replace(
                'gameType:"broken-game"',
                'gameType:"gravity-flip"',
                1
            )
            game_file.write_text(text, encoding="utf-8")
            print("SELF-HEAL: Applied CONTRACT_FAILURE repair.")
            print("SELF-HEAL: Restored gameType to gravity-flip.")
            return True

        print("SELF-HEAL: Contract repair pattern not found.")
        return False

    if diagnosis == "RESTART_FAILURE":
        text = game_file.read_text(encoding="utf-8")

        if 'if(k==="x" && ended){' in text:
            text = text.replace(
                'if(k==="x" && ended){',
                'if(k==="r" && ended){',
                1
            )
            game_file.write_text(text, encoding="utf-8")
            print("SELF-HEAL: Applied RESTART_FAILURE repair.")
            print("SELF-HEAL: Restored R-key restart behavior.")
            return True

        print("SELF-HEAL: Restart repair pattern not found.")
        return False

    if diagnosis == "COLLISION_FAILURE":
        text = game_file.read_text(encoding="utf-8")

        old_collision = "function obstacleHit(o){\n return false;\n}"

        new_collision = """function obstacleHit(o){
 return(
   player.x+player.radius>o.x &&
   player.x-player.radius<o.x+o.w &&
   player.y+player.radius>o.y-o.h/2 &&
   player.y-player.radius<o.y+o.h/2
 );
}"""

        if old_collision in text:
            text = text.replace(old_collision, new_collision, 1)
            game_file.write_text(text, encoding="utf-8")
            print("SELF-HEAL: Applied COLLISION_FAILURE repair.")
            print("SELF-HEAL: Restored obstacle collision logic.")
            return True

        print("SELF-HEAL: Collision repair pattern not found.")
        return False

    if diagnosis == "WIN_FAILURE":
        text = game_file.read_text(encoding="utf-8")

        old_win = """if(false){
   ended=true;
   progress=100;
   statusEl.textContent="YOU WIN! Gravity Flip completed!";
   return;
 }"""

        new_win = """if(player.x>=finish.x){
   ended=true;
   progress=100;
   statusEl.textContent="YOU WIN! Gravity Flip completed!";
   return;
 }"""

        if old_win in text:
            text = text.replace(old_win, new_win, 1)
            game_file.write_text(text, encoding="utf-8")
            print("SELF-HEAL: Applied WIN_FAILURE repair.")
            print("SELF-HEAL: Restored win-condition logic.")
            return True

        print("SELF-HEAL: Win repair pattern not found.")
        return False

    print(f"SELF-HEAL: No automatic repair available for {diagnosis}.")
    return False


def create_repair_plan(diagnosis):
    repairs = {
        "JAVASCRIPT_ERROR":
            "Inspect JavaScript errors and repair the generated game code.",
        "CONTRACT_FAILURE":
            "Restore the required MINDCRAFT_GAME 3D contract.",
        "INPUT_FAILURE":
            "Repair player input handling and movement logic.",
        "COLLISION_FAILURE":
            "Repair obstacle or hazard collision logic.",
        "WIN_FAILURE":
            "Repair the game's win-condition and finish-zone logic.",
        "RESTART_FAILURE":
            "Repair the R-key restart/reset behavior.",
        "UNKNOWN_FAILURE":
            "Inspect the playtest report and determine the safest game-code repair.",
        "PASS":
            "No repair required."
    }

    plan = repairs.get(diagnosis, repairs["UNKNOWN_FAILURE"])

    repair_file = ROOT / "tests" / "repair-plan.txt"

    repair_file.write_text(
        f"MindCraft Self-Heal Repair Plan\n"
        f"Generated: {datetime.now().isoformat(timespec='seconds')}\n"
        f"Diagnosis: {diagnosis}\n"
        f"Action: {plan}\n",
        encoding="utf-8"
    )

    print(f"SELF-HEAL: Repair plan = {plan}")
    print(f"SELF-HEAL: Repair plan saved: {repair_file}")


if __name__ == "__main__":
    success = run_playtest()

    if not success:
        diagnosis = "UNKNOWN_FAILURE"

        if REPORT.exists():
            report = REPORT.read_text(encoding="utf-8")
            diagnosis_line = next(
                (
                    line
                    for line in report.splitlines()
                    if line.startswith("Diagnosis:")
                ),
                ""
            )

            diagnosis = diagnosis_line.replace(
                "Diagnosis:", ""
            ).strip() or diagnosis

        create_repair_plan(diagnosis)

        repaired = repair_game(diagnosis)

        if repaired:
            print("SELF-HEAL: Re-running playtest after repair...")
            success = run_playtest()

    sys.exit(0 if success else 1)
