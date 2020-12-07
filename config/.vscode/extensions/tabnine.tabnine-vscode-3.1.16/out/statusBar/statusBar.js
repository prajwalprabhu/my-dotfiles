"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.clearPromotion = exports.setPromotionStatus = exports.setLoadingStatus = exports.resetDefaultStatuses = exports.setDefaultStatus = exports.onStartServiceLevel = exports.pollServiceLevel = exports.registerStatusBar = void 0;
const vscode_1 = require("vscode");
const requests_1 = require("../binary/requests/requests");
const commandsHandler_1 = require("../commandsHandler");
const consts_1 = require("../consts");
const StatusBarData_1 = require("./StatusBarData");
const SPINNER = "$(sync~spin)";
let statusBarData;
let promotion;
function registerStatusBar(context) {
    if (statusBarData) {
        return;
    }
    const statusBar = vscode_1.window.createStatusBarItem(vscode_1.StatusBarAlignment.Left, -1);
    promotion = vscode_1.window.createStatusBarItem(vscode_1.StatusBarAlignment.Left, -1);
    statusBarData = new StatusBarData_1.default(statusBar);
    statusBar.command = commandsHandler_1.STATUS_BAR_COMMAND;
    statusBar.tooltip = `${consts_1.FULL_BRAND_REPRESENTATION} (Click to open settings)`;
    statusBar.show();
    setLoadingStatus("Starting...");
    context.subscriptions.push(statusBar);
    context.subscriptions.push(promotion);
}
exports.registerStatusBar = registerStatusBar;
async function pollServiceLevel() {
    if (!statusBarData) {
        return;
    }
    const state = await requests_1.getState();
    statusBarData.serviceLevel = state === null || state === void 0 ? void 0 : state.service_level;
}
exports.pollServiceLevel = pollServiceLevel;
async function onStartServiceLevel() {
    if (!statusBarData) {
        return;
    }
    const state = await requests_1.getState();
    statusBarData.serviceLevel =
        (state === null || state === void 0 ? void 0 : state.service_level) === "Free"
            ? serviceLevelBaseOnAPIKey(state)
            : state === null || state === void 0 ? void 0 : state.service_level;
}
exports.onStartServiceLevel = onStartServiceLevel;
function serviceLevelBaseOnAPIKey(state) {
    return (state === null || state === void 0 ? void 0 : state.api_key) ? "Pro" : "Free";
}
function setDefaultStatus() {
    if (!statusBarData) {
        return;
    }
    statusBarData.icon = null;
    statusBarData.text = null;
}
exports.setDefaultStatus = setDefaultStatus;
function resetDefaultStatuses() {
    setDefaultStatus();
    clearPromotion();
}
exports.resetDefaultStatuses = resetDefaultStatuses;
function setLoadingStatus(issue) {
    if (!statusBarData) {
        return;
    }
    statusBarData.text = issue;
    statusBarData.icon = SPINNER;
}
exports.setLoadingStatus = setLoadingStatus;
function setPromotionStatus(message, command) {
    if (!statusBarData) {
        return;
    }
    promotion.text = `${message}`;
    promotion.command = command;
    promotion.tooltip = `${consts_1.FULL_BRAND_REPRESENTATION} - ${message}`;
    promotion.color = "yellow";
    statusBarData.text = " ";
    promotion.show();
}
exports.setPromotionStatus = setPromotionStatus;
function clearPromotion() {
    promotion.text = "";
    promotion.tooltip = "";
    promotion.hide();
}
exports.clearPromotion = clearPromotion;
//# sourceMappingURL=statusBar.js.map