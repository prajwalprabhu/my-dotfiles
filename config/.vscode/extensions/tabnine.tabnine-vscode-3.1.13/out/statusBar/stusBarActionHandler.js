"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.disposeStatusBarCommand = void 0;
const vscode = require("vscode");
const setState_1 = require("../binary/requests/setState");
const statusBar_1 = require("../binary/requests/statusBar");
const consts_1 = require("../consts");
const statusBar_2 = require("./statusBar");
const utils_1 = require("../utils");
let statusBarCommandDisposable;
async function handleStatus(context, status) {
    registerStatusHandlingCommand(status, context);
    void setState_1.default({
        [consts_1.StatePayload.STATUS_SHOWN]: { text: status.message },
    });
    statusBar_2.setPromotionStatus(status.message, consts_1.OPEN_LP_FROM_STATUS_BAR);
    await utils_1.sleep(consts_1.STATUS_BAR_NOTIFICATION_PERIOD);
    statusBar_2.resetToDefaultStatus();
}
exports.default = handleStatus;
function registerStatusHandlingCommand(message, context) {
    statusBarCommandDisposable === null || statusBarCommandDisposable === void 0 ? void 0 : statusBarCommandDisposable.dispose();
    statusBarCommandDisposable = vscode.commands.registerCommand(consts_1.OPEN_LP_FROM_STATUS_BAR, () => {
        void statusBar_1.sendStatusBarAction(message.id, message.message);
    });
    context.subscriptions.push(statusBarCommandDisposable);
}
function disposeStatusBarCommand() {
    if (statusBarCommandDisposable) {
        statusBarCommandDisposable.dispose();
    }
}
exports.disposeStatusBarCommand = disposeStatusBarCommand;
//# sourceMappingURL=stusBarActionHandler.js.map