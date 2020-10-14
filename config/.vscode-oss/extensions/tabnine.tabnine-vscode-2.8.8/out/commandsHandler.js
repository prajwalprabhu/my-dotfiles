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
exports.registerConfigurationCommand = exports.registerCommands = exports.STATUS_BAR_COMMAND = exports.CONFIG_COMMAND = void 0;
var TabNine_1 = require("./TabNine");
var progressBar_1 = require("./progressBar");
var notificationsHandler_1 = require("./notificationsHandler");
var vscode_1 = require("vscode");
var configHandler_1 = require("./configHandler");
exports.CONFIG_COMMAND = 'TabNine::config';
exports.STATUS_BAR_COMMAND = 'TabNine.statusBar';
function registerCommands(tabNine, context) {
    var _this = this;
    var getHandler = function (type) { return function (args) { return __awaiter(_this, void 0, void 0, function () {
        var config;
        var _a;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0: return [4 /*yield*/, tabNine.request(TabNine_1.API_VERSION, {
                        "Configuration": { quiet: true }
                    })];
                case 1:
                    config = _b.sent();
                    configHandler_1.registerConfig(context, tabNine, config);
                    progressBar_1.setProgressBar(tabNine);
                    notificationsHandler_1.handleStartUpNotification(tabNine);
                    tabNine.setState((_a = {}, _a[TabNine_1.StatePayload.state] = { state_type: (args === null || args === void 0 ? void 0 : args.join("-")) || type }, _a));
                    return [2 /*return*/];
            }
        });
    }); }; };
    context.subscriptions.push(vscode_1.commands.registerCommand(exports.CONFIG_COMMAND, getHandler(TabNine_1.StateType.pallette)));
    context.subscriptions.push(vscode_1.commands.registerCommand(exports.STATUS_BAR_COMMAND, getHandler(TabNine_1.StateType.status)));
}
exports.registerCommands = registerCommands;
function registerConfigurationCommand(tabNine, context) {
    var _this = this;
    var handler = function () { return __awaiter(_this, void 0, void 0, function () {
        var config;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, tabNine.request(TabNine_1.API_VERSION, {
                        "Configuration": {}
                    })];
                case 1:
                    config = _a.sent();
                    return [2 /*return*/];
            }
        });
    }); };
    context.subscriptions.push(vscode_1.commands.registerCommand(exports.CONFIG_COMMAND, handler));
}
exports.registerConfigurationCommand = registerConfigurationCommand;
//# sourceMappingURL=commandsHandler.js.map