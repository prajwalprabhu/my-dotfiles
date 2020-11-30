"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
const vscode = require("vscode");
const errorState_1 = require("./binary/errorState");
const pollDownloadProgress_1 = require("./binary/pollDownloadProgress");
const requests_1 = require("./binary/requests/requests");
const capabilities_1 = require("./capabilities");
const commandsHandler_1 = require("./commandsHandler");
const consts_1 = require("./consts");
const extensionContext_1 = require("./extensionContext");
const handleUninstall_1 = require("./handleUninstall");
const provideCompletionItems_1 = require("./provideCompletionItems");
const selectionHandler_1 = require("./selectionHandler");
const statusBar_1 = require("./statusBar/statusBar");
const ValidatorClient_1 = require("./validator/ValidatorClient");
const pollNotifications_1 = require("./notifications/pollNotifications");
const alphaInstaller_1 = require("./alphaInstaller");
const pollStatusBar_1 = require("./statusBar/pollStatusBar");
function activate(context) {
    requests_1.initBinary();
    handleSelection(context);
    handleUninstall_1.default();
    statusBar_1.registerStatusBar(context);
    // Do not await on this function as we do not want VSCode to wait for it to finish
    // before considering TabNine ready to operate.
    void backgroundInit(context);
    return Promise.resolve();
}
exports.activate = activate;
async function backgroundInit(context) {
    // Goes to the binary to fetch what capabilities enabled:
    await capabilities_1.fetchCapabilitiesOnFocus();
    if (capabilities_1.isCapabilityEnabled(capabilities_1.Capability.ALPHA_CAPABILITY)) {
        void alphaInstaller_1.default(context);
        pollNotifications_1.default(context);
        pollStatusBar_1.default(context);
    }
    statusBar_1.setDefaultStatus();
    commandsHandler_1.registerCommands(context);
    pollDownloadProgress_1.default();
    vscode.languages.registerCompletionItemProvider({ pattern: "**" }, {
        provideCompletionItems: provideCompletionItems_1.default,
    }, ...consts_1.COMPLETION_TRIGGERS);
    // if (isCapabilityEnabled(Capability.VALIDATOR_CAPABILITY)) {
    //   setImmediate(() => {
    //     initValidator(context, pasteDisposable);
    //   });
    // }
    if (capabilities_1.isCapabilityEnabled(capabilities_1.Capability.ON_BOARDING_CAPABILITY)) {
        errorState_1.default();
    }
}
async function deactivate() {
    void ValidatorClient_1.closeValidator();
    pollNotifications_1.cancelNotificationsPolling();
    pollStatusBar_1.disposeStatus();
    return requests_1.deactivate();
}
exports.deactivate = deactivate;
function handleSelection(context) {
    if (extensionContext_1.tabnineContext.isTabNineAutoImportEnabled) {
        context.subscriptions.push(vscode.commands.registerTextEditorCommand(selectionHandler_1.COMPLETION_IMPORTS, selectionHandler_1.selectionHandler));
    }
}
//# sourceMappingURL=extension.js.map