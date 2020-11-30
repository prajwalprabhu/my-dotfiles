"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.sendNotificationAction = exports.getNotifications = exports.NotificationActions = void 0;
const requests_1 = require("./requests");
var NotificationActions;
(function (NotificationActions) {
    NotificationActions[NotificationActions["NONE"] = 0] = "NONE";
})(NotificationActions = exports.NotificationActions || (exports.NotificationActions = {}));
function getNotifications() {
    return requests_1.tabNineProcess.request({ Notifications: {} });
}
exports.getNotifications = getNotifications;
async function sendNotificationAction(id, selected) {
    return requests_1.tabNineProcess.request({
        NotificationAction: { id, selected },
    });
}
exports.sendNotificationAction = sendNotificationAction;
//# sourceMappingURL=notifications.js.map