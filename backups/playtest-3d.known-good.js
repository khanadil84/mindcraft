const { chromium } = require("playwright");
const path = require("path");

(async () => {
    const browser = await chromium.launch({ headless: true });

    const gamePath = path.resolve(
        __dirname,
        "../games/mindcraft-game.html"
    );

    const page = await browser.newPage();
    const errors = [];

    page.on("pageerror", error => {
        errors.push(error.message);
    });

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

    const contract = await page.evaluate(() => ({
        exists: !!window.MINDCRAFT_GAME,
        version: window.MINDCRAFT_GAME?.version,
        engine: window.MINDCRAFT_GAME?.engine,
        gameType: window.MINDCRAFT_GAME?.gameType,
        title: window.MINDCRAFT_GAME?.title
    }));

    console.log(`Contract: ${JSON.stringify(contract)}`);

    if (!contract.exists) {
        throw new Error("FAIL: MINDCRAFT_GAME contract missing");
    }

    if (contract.engine !== "3d") {
        throw new Error("FAIL: Game engine is not 3d");
    }

    if (contract.gameType !== "gravity-flip") {
        throw new Error(
            `FAIL: Wrong game type: ${contract.gameType}`
        );
    }

    console.log("Contract test: 3D Gravity Flip contract verified.");

    // Movement test.
    const beforeMove = await page.evaluate(
        () => window.MINDCRAFT_GAME.getState().x
    );

    await page.keyboard.down("d");
    await page.waitForTimeout(250);
    await page.keyboard.up("d");

    const afterMove = await page.evaluate(
        () => window.MINDCRAFT_GAME.getState().x
    );

    console.log(
        `Movement test: ${beforeMove.toFixed(2)} -> ${afterMove.toFixed(2)}`
    );

    if (afterMove <= beforeMove) {
        throw new Error("FAIL: Player did not move.");
    }

    console.log("Movement test: player movement verified.");

    // Gravity flip test.
    const beforeGravity = await page.evaluate(
        () => window.MINDCRAFT_GAME.getState().gravity
    );

    await page.keyboard.press("Space");
    await page.waitForTimeout(100);

    const afterGravity = await page.evaluate(
        () => window.MINDCRAFT_GAME.getState().gravity
    );

    console.log(
        `Gravity test: ${beforeGravity} -> ${afterGravity}`
    );

    if (beforeGravity === afterGravity) {
        throw new Error("FAIL: Space did not flip gravity.");
    }

    console.log("Gravity test: SPACE flip verified.");

    await page.close();

    // Fresh page for obstacle collision.
    const collisionPage = await browser.newPage();

    await collisionPage.goto(`file://${gamePath}`);

    await collisionPage.evaluate(() => {
        player.x = 4.0;
        player.y = 4.2;
    });

    await collisionPage.waitForTimeout(100);

    const collisionStatus =
        await collisionPage.locator("#status").textContent();

    console.log(`Obstacle test status: ${collisionStatus}`);

    if (!collisionStatus.includes("Obstacle collision")) {
        throw new Error(
            `FAIL: Obstacle collision not detected: ${collisionStatus}`
        );
    }

    console.log("Obstacle test: GAME OVER verified.");

    await collisionPage.close();

    // Fresh page for win condition.
    const winPage = await browser.newPage();

    await winPage.goto(`file://${gamePath}`);

    await winPage.evaluate(() => {
        player.x = finish.x;
    });

    await winPage.waitForTimeout(100);

    const winStatus =
        await winPage.locator("#status").textContent();

    console.log(`Win test status: ${winStatus}`);

    if (!winStatus.includes("YOU WIN")) {
        throw new Error(
            `FAIL: Win condition not reached: ${winStatus}`
        );
    }

    console.log("Win test: finish zone verified.");

    await winPage.close();

    // Restart test.
    const restartPage = await browser.newPage();

    await restartPage.goto(`file://${gamePath}`);

    await restartPage.evaluate(() => {
        player.x = 10;
        player.gravity = "ceiling";
    });

    await restartPage.waitForTimeout(50);

    await restartPage.keyboard.press("Space");
    await restartPage.waitForTimeout(50);

    await restartPage.evaluate(() => {
        ended = true;
        statusEl.textContent = "GAME OVER — Test state";
    });

    await restartPage.keyboard.press("r");
    await restartPage.waitForTimeout(150);

    const restartState = await restartPage.evaluate(() => ({
        ended: window.MINDCRAFT_GAME.isEnded(),
        gravity: window.MINDCRAFT_GAME.getState().gravity,
        x: window.MINDCRAFT_GAME.getState().x,
        status: window.MINDCRAFT_GAME.getStatus()
    }));

    console.log(
        `Restart test state: ${JSON.stringify(restartState)}`
    );

    if (
        restartState.ended ||
        restartState.x !== 1.5 ||
        restartState.gravity !== "floor"
    ) {
        throw new Error("FAIL: Restart did not reset the game.");
    }

    console.log("Restart test: R key reset verified.");

    await restartPage.close();

    console.log(
        "PLAYTEST PASS: 3D game loads, contract works, movement works, gravity flips, obstacles cause GAME OVER, finish causes YOU WIN, and restart works."
    );

    await browser.close();
})();
