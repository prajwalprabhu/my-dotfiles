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
exports.setProgressBar = void 0;
var vscode_1 = require("vscode");
var statusBar_1 = require("./statusBar");
var TabNine_1 = require("./TabNine");
var notificationsHandler_1 = require("./notificationsHandler");
var os_1 = require("os");
var FOUR_SECONDS = 4000;
var ONE_MINUTE = 60000;
var PROGRESS_BAR_TITLE = "TabNine local model is being downloaded";
var PROGRESS_BAR_MESSAGE = "Once it is downloaded you will be able to get the best of TabNine";
var DOWNLOAD_FAILED = "TabNine initialization is not completed, please check your internet connection and try to restart VS Code. If it doesn’t help, please contact support@tabnine.com";
var CONTACT_SUPPORT = "Contact TabNine Support";
var CPU_NOT_SUPPORTED = "TabNine Local Deep completions cannot work on your current hardware setup, This will decrease the quality of the TabNine suggestions. You can enable TabNine Deep Cloud from the TabNine settings page";
var DOWNLOAD_COMPLETED = "TabNine local model was downloaded successfully";
var status = {
    Finished: "Finished",
    NotStarted: "NotStarted",
    InProgress: "InProgress"
};
var downloadProgress = {
    Downloading: "Downloading",
    RetrievingMetadata: "RetrievingMetadata",
    VerifyingChecksum: "VerifyingChecksum",
};
var isInProgress = false;
function setProgressBar(tabNine) {
    var _this = this;
    if (isInProgress) {
        return;
    }
    isInProgress = true;
    var pollingInterval = setInterval(function () { return __awaiter(_this, void 0, void 0, function () {
        var _a, download_state, local_enabled, cloud_enabled, is_cpu_supported;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0: return [4 /*yield*/, tabNine.request(TabNine_1.API_VERSION, { State: {} })];
                case 1:
                    _a = _b.sent(), download_state = _a.download_state, local_enabled = _a.local_enabled, cloud_enabled = _a.cloud_enabled, is_cpu_supported = _a.is_cpu_supported;
                    if (!local_enabled) {
                        clearPolling();
                        isInProgress = false;
                        return [2 /*return*/];
                    }
                    if (local_enabled && !is_cpu_supported && !cloud_enabled) {
                        notificationsHandler_1.handleErrorMessage(tabNine, CPU_NOT_SUPPORTED, notificationsHandler_1.onEnableCloudAction, CPU_NOT_SUPPORTED);
                        clearPolling();
                        isInProgress = false;
                        return [2 /*return*/];
                    }
                    if (download_state.status === status.Finished) {
                        clearPolling();
                        isInProgress = false;
                        return [2 /*return*/];
                    }
                    if (download_state.status === status.NotStarted && download_state.last_failure) {
                        clearPolling();
                        showErrorNotification(tabNine);
                        isInProgress = false;
                        return [2 /*return*/];
                    }
                    if (download_state.status === status.InProgress && download_state.kind === downloadProgress.Downloading) {
                        clearPolling();
                        handleDownloadingInProgress(tabNine);
                    }
                    return [2 /*return*/];
            }
        });
    }); }, FOUR_SECONDS);
    var pollingTimeout = setTimeout(function () {
        clearInterval(pollingInterval);
    }, ONE_MINUTE);
    function clearPolling() {
        clearInterval(pollingInterval);
        clearTimeout(pollingTimeout);
    }
}
exports.setProgressBar = setProgressBar;
function handleDownloadingInProgress(tabNine) {
    var _a;
    var _this = this;
    tabNine.setState((_a = {}, _a[TabNine_1.StatePayload.message] = { message_type: TabNine_1.StateType.progress }, _a));
    vscode_1.window.withProgress({
        location: vscode_1.ProgressLocation.Notification,
        title: PROGRESS_BAR_TITLE
    }, function (progress) {
        progress.report({ increment: 0 });
        statusBar_1.startSpinner();
        return new Promise(function (resolve) {
            var progressInterval = setInterval(function () { return __awaiter(_this, void 0, void 0, function () {
                var download_state;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, tabNine.request(TabNine_1.API_VERSION, { State: {} })];
                        case 1:
                            download_state = (_a.sent()).download_state;
                            if (download_state.status == status.Finished) {
                                completeProgress(progressInterval, resolve);
                                return [2 /*return*/];
                            }
                            if (download_state.last_failure) {
                                showErrorNotification(tabNine);
                                completeProgress(progressInterval, resolve);
                                return [2 /*return*/];
                            }
                            handleDownloading(download_state, progress, tabNine);
                            return [2 /*return*/];
                    }
                });
            }); }, FOUR_SECONDS);
        });
    });
}
function completeProgress(progressInterval, resolve) {
    statusBar_1.stopSpinner();
    clearInterval(progressInterval);
    resolve();
    isInProgress = false;
}
function handleDownloading(download_state, progress, tabNine) {
    if (download_state.kind == downloadProgress.Downloading) {
        var increment = Math.floor((download_state.crnt_bytes / download_state.total_bytes) * 10);
        var percentage = Math.floor((download_state.crnt_bytes / download_state.total_bytes) * 100);
        progress.report({ increment: increment, message: percentage + "%. " + os_1.EOL + PROGRESS_BAR_MESSAGE });
    }
    if (download_state.kind == downloadProgress.VerifyingChecksum) {
        progress.report({ increment: 100, message: download_state.kind });
        notificationsHandler_1.handleInfoMessage(tabNine, DOWNLOAD_COMPLETED);
    }
}
function showErrorNotification(tabNine) {
    notificationsHandler_1.handleErrorMessage(tabNine, DOWNLOAD_FAILED, function (action) {
        if (action === CONTACT_SUPPORT) {
            vscode_1.commands.executeCommand('vscode.open', vscode_1.Uri.parse('mailto:support@tabnine.com'));
        }
    }, CONTACT_SUPPORT);
}
//# sourceMappingURL=progressBar.js.map