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
        title: window.MINDCRAFT_GAME?.title,
        hasState: typeof window.MINDCRAFT_GAME?.getState === "function",
        hasStatus: typeof window.MINDCRAFT_GAME?.getStatus === "function",
        hasRestart: typeof window.MINDCRAFT_GAME?.restart === "function"
    }));

    console.log(`Contract: ${JSON.stringify(contract)}`);

    if (!contract.exists) {
        throw new Error("FAIL: MINDCRAFT_GAME contract missing");
    }

    if (contract.engine !== "3d") {
        throw new Error("FAIL: Game engine is not 3d");
    }

    if (!contract.gameType || typeof contract.gameType !== "string") {
        throw new Error("FAIL: Game type missing");
    }

    if (!contract.title || typeof contract.title !== "string") {
        throw new Error("FAIL: Game title missing from contract");
    }

    if (!contract.hasState) {
        throw new Error("FAIL: getState() missing");
    }

    if (!contract.hasStatus) {
        throw new Error("FAIL: getStatus() missing");
    }

    if (!contract.hasRestart) {
        throw new Error("FAIL: restart() missing");
    }

    console.log(
        `Contract test: Generic 3D contract verified for "${contract.gameType}".`
    );

    // Generic movement test.
    const beforeMove = await page.evaluate(() => {
        const state = window.MINDCRAFT_GAME.getState();
        return {
            x: typeof state.x === "number" ? state.x : null,
            y: typeof state.y === "number" ? state.y : null
        };
    });

    await page.keyboard.down("d");
    await page.waitForTimeout(250);
    await page.keyboard.up("d");

    const afterMove = await page.evaluate(() => {
        const state = window.MINDCRAFT_GAME.getState();
        return {
            x: typeof state.x === "number" ? state.x : null,
            y: typeof state.y === "number" ? state.y : null
        };
    });

    console.log(
        `Movement test: ${JSON.stringify(beforeMove)} -> ${JSON.stringify(afterMove)}`
    );

    const moved =
        (beforeMove.x !== null &&
         afterMove.x !== null &&
         afterMove.x !== beforeMove.x) ||
        (beforeMove.y !== null &&
         afterMove.y !== null &&
         afterMove.y !== beforeMove.y);

    if (!moved) {
        throw new Error("FAIL: Player did not move.");
    }

    console.log("Movement test: generic player movement verified.");

    await page.close();

    // Generic restart test.
    const restartPage = await browser.newPage();

    await restartPage.goto(`file://${gamePath}`);

    const initialState = await restartPage.evaluate(() =>
        window.MINDCRAFT_GAME.getState()
    );

    await restartPage.keyboard.down("d");
    await restartPage.waitForTimeout(250);
    await restartPage.keyboard.up("d");

    const movedState = await restartPage.evaluate(() =>
        window.MINDCRAFT_GAME.getState()
    );

    if (JSON.stringify(initialState) === JSON.stringify(movedState)) {
        throw new Error("FAIL: Restart setup could not change game state.");
    }

    await restartPage.evaluate(() => {
        const game = window.MINDCRAFT_GAME;
        game.restart();
    });

    await restartPage.waitForTimeout(150);

    const restartedState = await restartPage.evaluate(() => ({
        state: window.MINDCRAFT_GAME.getState(),
        ended: window.MINDCRAFT_GAME.isEnded(),
        status: window.MINDCRAFT_GAME.getStatus()
    }));

    console.log(
        `Restart test state: ${JSON.stringify(restartedState)}`
    );

    if (restartedState.ended) {
        throw new Error("FAIL: Restart left game ended.");
    }

    console.log("Restart test: generic restart verified.");

    await restartPage.close();

    // Final health check.
    const finalPage = await browser.newPage();
    const finalErrors = [];

    finalPage.on("pageerror", error => {
        finalErrors.push(error.message);
    });

    await finalPage.goto(`file://${gamePath}`);
    await finalPage.waitForTimeout(100);

    if (finalErrors.length > 0) {
        throw new Error(
            `FAIL: JavaScript errors after restart: ${finalErrors.join("; ")}`
        );
    }

    const finalContract = await finalPage.evaluate(() => ({
        title: window.MINDCRAFT_GAME.title,
        gameType: window.MINDCRAFT_GAME.gameType,
        engine: window.MINDCRAFT_GAME.engine,
        status: window.MINDCRAFT_GAME.getStatus()
    }));

    console.log(
        `Final health check: ${JSON.stringify(finalContract)}`
    );

    await finalPage.close();
    await browser.close();

    console.log(
        `PLAYTEST PASS: Generic 3D game "${finalContract.title}" ` +
        `(${finalContract.gameType}) loads, contract works, ` +
        `movement works, restart works, and no JavaScript errors occur.`
    );
})();
