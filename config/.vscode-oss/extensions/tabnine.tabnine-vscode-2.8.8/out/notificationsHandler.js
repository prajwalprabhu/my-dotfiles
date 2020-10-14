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
var __spreadArrays = (this && this.__spreadArrays) || function () {
    for (var s = 0, i = 0, il = arguments.length; i < il; i++) s += arguments[i].length;
    for (var r = Array(s), k = 0, i = 0; i < il; i++)
        for (var a = arguments[i], j = 0, jl = a.length; j < jl; j++, k++)
            r[k] = a[j];
    return r;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.onEnableCloudAction = exports.handleStartUpNotification = exports.handleUserMessage = exports.handleWarningMessage = exports.handleErrorMessage = exports.handleInfoMessage = void 0;
var TabNine_1 = require("./TabNine");
var vscode_1 = require("vscode");
var os_1 = require("os");
var commandsHandler_1 = require("./commandsHandler");
var memoize = require('lodash.memoize');
var CONNECTION_ISSUE = "TabNine deep cloud requires an active internet connection. Please check your connection. You can still work locally with TabNine deep local";
var CONNECTION_ISSUE_WARNING = "TabNine deep cloud requires an active internet connection, please check your internet connection and reconnect again";
var CLOUD_CAPABLE_NOT_ENABLED = "You had registered to TabNine Professional but didn't enable the Deep Cloud";
var ENABLED_CLOUD_ACTION = "Enable Deep Cloud";
var FIRST_NOTIFICATION_DELAY = 10000;
exports.handleInfoMessage = memoize(function (tabNine, message, onClick) {
    var _a;
    if (onClick === void 0) { onClick = function (action) { }; }
    var args = [];
    for (var _i = 3; _i < arguments.length; _i++) {
        args[_i - 3] = arguments[_i];
    }
    tabNine.setState((_a = {}, _a[TabNine_1.StatePayload.message] = { message_type: TabNine_1.StateType.info, message: message }, _a));
    return vscode_1.window.showInformationMessage.apply(vscode_1.window, __spreadArrays([message], args)).then(onClick);
}, function (tabNine, message) { return message.toLocaleLowerCase(); });
exports.handleErrorMessage = memoize(function (tabNine, message, onClick) {
    var _a;
    if (onClick === void 0) { onClick = function (action) { }; }
    var args = [];
    for (var _i = 3; _i < arguments.length; _i++) {
        args[_i - 3] = arguments[_i];
    }
    tabNine.setState((_a = {}, _a[TabNine_1.StatePayload.message] = { message_type: TabNine_1.StateType.error, message: message }, _a));
    return vscode_1.window.showErrorMessage.apply(vscode_1.window, __spreadArrays([message], args)).then(onClick);
}, function (tabNine, message) { return message.toLocaleLowerCase(); });
exports.handleWarningMessage = memoize(function (tabNine, message, onClick) {
    var _a;
    if (onClick === void 0) { onClick = function (action) { }; }
    var args = [];
    for (var _i = 3; _i < arguments.length; _i++) {
        args[_i - 3] = arguments[_i];
    }
    tabNine.setState((_a = {}, _a[TabNine_1.StatePayload.message] = { message_type: TabNine_1.StateType.error, message: message }, _a));
    return vscode_1.window.showWarningMessage.apply(vscode_1.window, __spreadArrays([message], args)).then(onClick);
}, function (tabNine, message) { return message.toLocaleLowerCase(); });
function handleUserMessage(tabNine, _a) {
    var user_message = _a.user_message;
    exports.handleInfoMessage(tabNine, user_message.join(os_1.EOL));
}
exports.handleUserMessage = handleUserMessage;
function handleStartUpNotification(tabNine) {
    return __awaiter(this, void 0, void 0, function () {
        var _a, cloud_enabled, local_enabled, is_cloud_capable, is_authenticated;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0: return [4 /*yield*/, tabNine.request(TabNine_1.API_VERSION, { State: {} })];
                case 1:
                    _a = _b.sent(), cloud_enabled = _a.cloud_enabled, local_enabled = _a.local_enabled, is_cloud_capable = _a.is_cloud_capable, is_authenticated = _a.is_authenticated;
                    handleConnectivity(cloud_enabled, local_enabled, is_authenticated, tabNine);
                    handleCloudEnabling(is_cloud_capable, cloud_enabled, tabNine);
                    return [2 /*return*/];
            }
        });
    });
}
exports.handleStartUpNotification = handleStartUpNotification;
function handleCloudEnabling(is_cloud_capable, cloud_enabled, tabNine) {
    if (is_cloud_capable && !cloud_enabled) {
        exports.handleInfoMessage(tabNine, CLOUD_CAPABLE_NOT_ENABLED, onEnableCloudAction, ENABLED_CLOUD_ACTION);
    }
}
;
function handleConnectivity(cloud_enabled, local_enabled, is_authenticated, tabNine) {
    var _this = this;
    if (!is_authenticated) {
        setTimeout(function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, cloud_enabled, local_enabled, is_authenticated;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0: return [4 /*yield*/, tabNine.request(TabNine_1.API_VERSION, { State: {} })];
                    case 1:
                        _a = _b.sent(), cloud_enabled = _a.cloud_enabled, local_enabled = _a.local_enabled, is_authenticated = _a.is_authenticated;
                        if (cloud_enabled && !is_authenticated) {
                            if (!local_enabled) {
                                exports.handleErrorMessage(tabNine, CONNECTION_ISSUE, onEnableCloudAction, ENABLED_CLOUD_ACTION);
                            }
                            else {
                                exports.handleWarningMessage(tabNine, CONNECTION_ISSUE_WARNING);
                            }
                        }
                        return [2 /*return*/];
                }
            });
        }); }, FIRST_NOTIFICATION_DELAY);
    }
}
function onEnableCloudAction(action) {
    if (action === ENABLED_CLOUD_ACTION) {
        vscode_1.commands.executeCommand(commandsHandler_1.CONFIG_COMMAND, TabNine_1.StateType.notification, ENABLED_CLOUD_ACTION);
    }
}
exports.onEnableCloudAction = onEnableCloudAction;
//# sourceMappingURL=notificationsHandler.js.map