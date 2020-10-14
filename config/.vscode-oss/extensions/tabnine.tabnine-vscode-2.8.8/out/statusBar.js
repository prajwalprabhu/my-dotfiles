"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.updateStatusBar = exports.stopSpinner = exports.startSpinner = exports.registerStatusBar = void 0;
var vscode_1 = require("vscode");
var TabNine_1 = require("./TabNine");
var commandsHandler_1 = require("./commandsHandler");
var SPINNER = '$(sync~spin)';
var GEAR = "$(gear)";
var WARNING = "$(warning)";
var FIRST_EXECUTION_DELAY = 4000;
var STATUS_BAR_TITLE = "click to open TabNine settings page";
var statusBar;
var currentFilename = null;
function registerStatusBar(context, tabNine) {
    statusBar = vscode_1.window.createStatusBarItem(vscode_1.StatusBarAlignment.Left, -1);
    statusBar.command = commandsHandler_1.STATUS_BAR_COMMAND;
    context.subscriptions.push(statusBar);
    statusBar.tooltip = STATUS_BAR_TITLE;
    statusBar.text = "[ TabNine " + GEAR + " ]";
    statusBar.show();
    vscode_1.workspace.onDidOpenTextDocument(function (_a) {
        var fileName = _a.fileName;
        var firstExecutionDelay = currentFilename ? 0 : FIRST_EXECUTION_DELAY;
        setTimeout(function () {
            currentFilename = fileName.replace(/[.git]+$/, "");
            updateStatusBar(tabNine, currentFilename);
        }, firstExecutionDelay);
    });
}
exports.registerStatusBar = registerStatusBar;
function startSpinner() {
    statusBar.text = statusBar.text.replace("[ ", "[ " + SPINNER + " ");
}
exports.startSpinner = startSpinner;
function stopSpinner() {
    statusBar.text = statusBar.text.replace(" " + SPINNER, "");
}
exports.stopSpinner = stopSpinner;
function updateStatusBar(tabNine, filename) {
    return __awaiter(this, void 0, void 0, function () {
        var _a, local_enabled, cloud_enabled, is_cpu_supported, is_authenticated;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0: return [4 /*yield*/, tabNine.request(TabNine_1.API_VERSION, { State: { filename: filename } })];
                case 1:
                    _a = _b.sent(), local_enabled = _a.local_enabled, cloud_enabled = _a.cloud_enabled, is_cpu_supported = _a.is_cpu_supported, is_authenticated = _a.is_authenticated;
                    if (isInErrorState(local_enabled, is_cpu_supported, cloud_enabled, is_authenticated)) {
                        statusBar.text = statusBar.text.replace("" + GEAR, "" + WARNING);
                        statusBar.color = "pink";
                        statusBar.tooltip = cloud_enabled ? "network issue" : "hardware issue";
                    }
                    return [2 /*return*/];
            }
        });
    });
}
exports.updateStatusBar = updateStatusBar;
function isInErrorState(local_enabled, is_cpu_supported, cloud_enabled, is_authenticated) {
    return local_enabled && !is_cpu_supported || cloud_enabled && !is_authenticated;
}
//# sourceMappingURL=statusBar.js.map