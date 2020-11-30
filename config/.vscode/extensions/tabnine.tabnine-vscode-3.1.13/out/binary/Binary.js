"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const await_semaphore_1 = require("await-semaphore");
const consts_1 = require("../consts");
const runBinary_1 = require("./runBinary");
class Binary {
    constructor() {
        this.consecutiveRestarts = 0;
        this.requestFailures = 0;
        this.isRestarting = false;
        this.mutex = new await_semaphore_1.Mutex();
    }
    init() {
        this.startChild();
    }
    async request(request, timeout = 1000) {
        var _a;
        const release = await this.mutex.acquire();
        try {
            if (this.isRestarting) {
                return null;
            }
            if (this.isBinaryDead()) {
                console.warn("Binary died. It is being restarted.");
                this.restartChild();
                return null;
            }
            (_a = this.proc) === null || _a === void 0 ? void 0 : _a.stdin.write(`${JSON.stringify({
                version: consts_1.API_VERSION,
                request,
            })}\n`, "utf8");
            const result = await this.readLineWithLimit(timeout);
            this.consecutiveRestarts = 0;
            this.requestFailures = 0;
            return JSON.parse(result.toString());
        }
        catch (err) {
            this.requestFailures += 1;
            if (this.requestFailures > consts_1.REQUEST_FAILURES_THRESHOLD) {
                console.warn("Binary not returning results, it is being restarted.");
                this.restartChild();
            }
        }
        finally {
            release();
        }
        return null;
    }
    readLineWithLimit(timeout) {
        return new Promise((resolve, reject) => {
            var _a;
            setTimeout(() => {
                reject(new Error("Binary request timed out."));
            }, timeout);
            (_a = this.rl) === null || _a === void 0 ? void 0 : _a.once("line", resolve);
        });
    }
    isBinaryDead() {
        var _a, _b;
        return (_b = (_a = this.proc) === null || _a === void 0 ? void 0 : _a.killed) !== null && _b !== void 0 ? _b : false;
    }
    restartChild() {
        var _a, _b;
        (_a = this.proc) === null || _a === void 0 ? void 0 : _a.removeAllListeners();
        (_b = this.proc) === null || _b === void 0 ? void 0 : _b.kill();
        this.isRestarting = true;
        this.consecutiveRestarts += 1;
        if (this.consecutiveRestarts >= consts_1.CONSECUTIVE_RESTART_THRESHOLD) {
            return; // We gave up. Keep it dead.
        }
        setTimeout(() => {
            this.startChild();
        }, consts_1.restartBackoff(this.consecutiveRestarts));
    }
    startChild() {
        const { proc, readLine } = runBinary_1.default([
            `ide-restart-counter=${this.consecutiveRestarts}`,
        ]);
        this.proc = proc;
        this.rl = readLine;
        this.isRestarting = false;
        this.proc.unref(); // AIUI, this lets Node exit without waiting for the child
        this.proc.on("exit", (code, signal) => {
            console.warn(`Binary child process exited with code ${code !== null && code !== void 0 ? code : "unknown"} signal ${signal !== null && signal !== void 0 ? signal : "unknown"}`);
            this.restartChild();
        });
        this.proc.on("error", (error) => {
            console.warn(`Binary child process error: ${error.message}`);
            this.restartChild();
        });
        this.proc.stdin.on("error", (error) => {
            console.warn(`Binary child process stdin error: ${error.message}`);
            this.restartChild();
        });
        this.proc.stdout.on("error", (error) => {
            console.warn(`Binary child process stdout error: ${error.message}`);
            this.restartChild();
        });
    }
}
exports.default = Binary;
//# sourceMappingURL=Binary.js.map