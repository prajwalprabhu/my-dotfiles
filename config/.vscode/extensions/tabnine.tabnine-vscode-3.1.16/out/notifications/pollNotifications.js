"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.cancelNotificationsPolling = void 0;
const vscode = require("vscode");
const notifications_1 = require("../binary/requests/notifications");
const executeNotificationAction_1 = require("./executeNotificationAction");
const consts_1 = require("../consts");
const utils_1 = require("../utils");
const setState_1 = require("../binary/requests/setState");
let pollingInterval = null;
function pollNotifications(context) {
    pollingInterval = setInterval(() => void doPollNotifications(context), consts_1.BINARY_NOTIFICATION_POLLING_INTERVAL);
}
exports.default = pollNotifications;
function cancelNotificationsPolling() {
    if (pollingInterval) {
        clearInterval(pollingInterval);
    }
}
exports.cancelNotificationsPolling = cancelNotificationsPolling;
async function doPollNotifications(context) {
    const notifications = await notifications_1.getNotifications();
    if (!notifications || !notifications.notifications) {
        return;
    }
    notifications.notifications.forEach((notification) => void handleNotification(notification, context));
}
async function handleNotification(notification, context) {
    try {
        await utils_1.assertFirstTimeReceived(notification.id, context);
        void setState_1.default({
            [consts_1.StatePayload.NOTIFICATION_SHOWN]: { text: notification.message },
        });
        return vscode.window
            .showInformationMessage(notification.message, ...notification.options.map((option) => option.key))
            .then((selected) => {
            void notifications_1.sendNotificationAction(notification.id, selected);
            void executeNotificationAction_1.default(notification, selected);
        });
    }
    catch (error) {
        // This is OK, as we prevented the same popup to appear twice.
        return Promise.resolve();
    }
}
//# sourceMappingURL=pollNotifications.js.map