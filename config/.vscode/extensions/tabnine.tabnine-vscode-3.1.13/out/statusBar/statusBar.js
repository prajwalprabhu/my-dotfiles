"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.clearPromotion = exports.setPromotionStatus = exports.setErrorStatus = exports.setLoadingStatus = exports.resetToDefaultStatus = exports.setDefaultStatus = exports.registerStatusBar = void 0;
const vscode_1 = require("vscode");
const commandsHandler_1 = require("../commandsHandler");
const consts_1 = require("../consts");
const SPINNER = "$(sync~spin)";
const WARNING = "$(warning)";
let statusBar;
let promotion;
function registerStatusBar(context) {
    if (statusBar) {
        return;
    }
    statusBar = vscode_1.window.createStatusBarItem(vscode_1.StatusBarAlignment.Left, -1);
    promotion = vscode_1.window.createStatusBarItem(vscode_1.StatusBarAlignment.Left, -1);
    setDefaults();
    setLoadingStatus("Starting...");
    statusBar.show();
    context.subscriptions.push(statusBar);
    context.subscriptions.push(promotion);
}
exports.registerStatusBar = registerStatusBar;
function setDefaults() {
    statusBar.command = commandsHandler_1.STATUS_BAR_COMMAND;
    statusBar.tooltip = `${consts_1.BRAND_NAME} (Click to open settings)`;
}
function setDefaultStatus() {
    setStatusBar();
}
exports.setDefaultStatus = setDefaultStatus;
function resetToDefaultStatus() {
    setDefaults();
    setStatusBar();
    clearPromotion();
}
exports.resetToDefaultStatus = resetToDefaultStatus;
function setLoadingStatus(issue) {
    setStatusBar(SPINNER, issue);
}
exports.setLoadingStatus = setLoadingStatus;
function setErrorStatus(issue) {
    setStatusBar(WARNING, issue);
    statusBar.color = new vscode_1.ThemeColor("errorForeground");
}
exports.setErrorStatus = setErrorStatus;
function setPromotionStatus(message, command) {
    promotion.text = `${message}`;
    promotion.command = command;
    promotion.tooltip = `${consts_1.BRAND_NAME} - ${message}`;
    promotion.color = "yellow";
    statusBar.text = `${consts_1.ATTRIBUTION_BRAND}${consts_1.BRAND_NAME}:`;
    promotion.show();
}
exports.setPromotionStatus = setPromotionStatus;
function clearPromotion() {
    promotion.text = "";
    promotion.tooltip = "";
    promotion.hide();
    setStatusBar();
}
exports.clearPromotion = clearPromotion;
function setStatusBar(icon, issue) {
    const iconText = icon ? ` ${icon}` : "";
    const issueText = issue ? `: ${issue}` : "";
    statusBar.text = `${consts_1.ATTRIBUTION_BRAND}${consts_1.BRAND_NAME}${iconText}${issueText}`;
}
//# sourceMappingURL=statusBar.js.map