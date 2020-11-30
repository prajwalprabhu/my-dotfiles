"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.sendStatusBarAction = exports.getStatus = exports.StatusBarActionActions = void 0;
const requests_1 = require("./requests");
var StatusBarActionActions;
(function (StatusBarActionActions) {
    StatusBarActionActions[StatusBarActionActions["NONE"] = 0] = "NONE";
})(StatusBarActionActions = exports.StatusBarActionActions || (exports.StatusBarActionActions = {}));
function getStatus() {
    return requests_1.tabNineProcess.request({ StatusBar: {} });
}
exports.getStatus = getStatus;
async function sendStatusBarAction(id, selected) {
    return requests_1.tabNineProcess.request({
        StatusBarAction: { id, selected },
    });
}
exports.sendStatusBarAction = sendStatusBarAction;
//# sourceMappingURL=statusBar.js.map