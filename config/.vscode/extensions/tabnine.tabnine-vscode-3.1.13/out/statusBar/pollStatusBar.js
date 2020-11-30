"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.disposeStatus = void 0;
const statusBar_1 = require("../binary/requests/statusBar");
const consts_1 = require("../consts");
const statusBar_2 = require("./statusBar");
const stusBarActionHandler_1 = require("./stusBarActionHandler");
let statusPollingInterval = null;
function pollStatuses(context) {
    statusPollingInterval = setInterval(() => void doPollStatus(context), consts_1.BINARY_STATUS_BAR_FIRST_MESSAGE_POLLING_INTERVAL);
}
exports.default = pollStatuses;
function cancelStatusPolling() {
    if (statusPollingInterval) {
        clearInterval(statusPollingInterval);
    }
}
async function doPollStatus(context) {
    const status = await statusBar_1.getStatus();
    if (!status) {
        return;
    }
    void stusBarActionHandler_1.default(context, status);
}
function disposeStatus() {
    stusBarActionHandler_1.disposeStatusBarCommand();
    cancelStatusPolling();
    statusBar_2.resetToDefaultStatus();
}
exports.disposeStatus = disposeStatus;
//# sourceMappingURL=pollStatusBar.js.map