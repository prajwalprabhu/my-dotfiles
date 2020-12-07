"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const consts_1 = require("../consts");
class StatusBarData {
    constructor(_statusBarItem) {
        this._statusBarItem = _statusBarItem;
    }
    set serviceLevel(serviceLevel) {
        this._serviceLevel = serviceLevel;
        this.updateStatusBar();
    }
    get serviceLevel() {
        return this._serviceLevel;
    }
    set icon(icon) {
        this._icon = icon || undefined;
        this.updateStatusBar();
    }
    get icon() {
        return this._icon;
    }
    set text(text) {
        this._text = text || undefined;
        this.updateStatusBar();
    }
    get text() {
        return this._text;
    }
    updateStatusBar() {
        const iconText = this._icon ? ` ${this._icon}` : "";
        const issueText = this._text ? `: ${this._text}` : "";
        const serviceLevel = this._serviceLevel === "Pro" || this._serviceLevel === "Trial"
            ? " pro"
            : "";
        this._statusBarItem.text = `${consts_1.FULL_BRAND_REPRESENTATION}${serviceLevel}${iconText}${issueText}`;
    }
}
exports.default = StatusBarData;
//# sourceMappingURL=StatusBarData.js.map