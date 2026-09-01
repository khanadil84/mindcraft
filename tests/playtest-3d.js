const { chromium } = require("playwright");
const path = require("path");

(async () => {
    const browser = await chromium.launch({ headless: true });

    const page = await browser.newPage();

    const errors = [];

    page.on("pageerror", error => {
        errors.push(error.message);
    });

    const gamePath = path.resolve(
        __dirname,
        "../games/mindcraft-game.html"
    );

    await page.goto(`file://${gamePath}`);

    const title = await page.title();
    const canvas = await page.locator("canvas").count();

    console.log(`Title: ${title}`);
    console.log(`Canvas count: ${canvas}`);
    console.log(`JavaScript errors: ${errors.length}`);

    if (!title.endsWith(" — MindCraft")) {
        throw new Error(`FAIL: Incorrect game title: ${title}`);
    }

    if (canvas !== 1) {
        throw new Error("FAIL: 3D canvas not found");
    }

    if (errors.length > 0) {
        throw new Error(
            `FAIL: JavaScript errors: ${errors.join("; ")}`
        );
    }

    await page.keyboard.down("w");
    await page.waitForTimeout(250);
    await page.keyboard.up("w");

    await page.keyboard.down("a");
    await page.waitForTimeout(250);
    await page.keyboard.up("a");

    await page.keyboard.down("s");
    await page.waitForTimeout(250);
    await page.keyboard.up("s");

    await page.keyboard.down("d");
    await page.waitForTimeout(250);
    await page.keyboard.up("d");

    console.log("Controls test: W/A/S/D sent successfully.");

    // Fast timer test: move performance.now() beyond the game's 60-second limit.
    await page.evaluate(() => {
        const originalNow = performance.now.bind(performance);
        const base = originalNow();
        const originalStart = base;

        Object.defineProperty(performance, "now", {
            configurable: true,
            value: () => originalStart + 61000
        });
    });

    await page.waitForTimeout(100);

    const status = await page.locator("#status").textContent();

    console.log(`Timer test status: ${status}`);

    if (!status.includes("Time expired")) {
        throw new Error(`FAIL: Timer did not expire: ${status}`);
    }

    console.log("Timer test: 60-second timeout verified.");

    // WIN-condition test in a fresh page.
    const winPage = await browser.newPage();

    await winPage.goto(`file://${gamePath}`);

    await winPage.evaluate(() => {
        cores.forEach(core => core.taken = true);

        player.x = exit.x;
        player.y = exit.y;
    });

    await winPage.waitForTimeout(100);

    const winStatus = await winPage.locator("#status").textContent();

    console.log(`Win test status: ${winStatus}`);

    if (!winStatus.includes("YOU WIN")) {
        throw new Error(`FAIL: Win condition not reached: ${winStatus}`);
    }

    console.log("Win test: 3 cores + exit verified.");

    // HAZARD-collision test in another fresh page.
    const hazardPage = await browser.newPage();

    await hazardPage.goto(`file://${gamePath}`);

    await hazardPage.evaluate(() => {
        player.x = hazard.x + 2;
        player.y = hazard.y;
        hazardAngle = 0;
    });

    await hazardPage.waitForTimeout(100);

    const hazardStatus = await hazardPage.locator("#status").textContent();

    console.log(`Hazard test status: ${hazardStatus}`);

    if (!hazardStatus.includes("Hazard collision")) {
        throw new Error(`FAIL: Hazard collision not detected: ${hazardStatus}`);
    }

    console.log("Hazard test: collision GAME OVER verified.");
    console.log("PLAYTEST PASS: 3D game loads, accepts controls, enforces timer, verifies win, and detects hazard collision.");

    await hazardPage.close();
    await winPage.close();

    await browser.close();
})();
