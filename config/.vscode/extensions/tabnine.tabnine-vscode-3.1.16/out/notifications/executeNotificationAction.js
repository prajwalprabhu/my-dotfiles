"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const notifications_1 = require("../binary/requests/notifications");
async function executeNotificationAction(notification, selected) {
    const selectedAction = notification.options.find(({ key }) => key === selected);
    switch (selectedAction === null || selectedAction === void 0 ? void 0 : selectedAction.action) {
        case notifications_1.NotificationActions.NONE:
        default:
            // Nothing to do. It is either unrecognized or undefined, and for both we do nothing.
            return Promise.resolve();
    }
}
exports.default = executeNotificationAction;
//# sourceMappingURL=executeNotificationAction.js.map