"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const vscode_1 = require("vscode");
const requests_1 = require("./requests/requests");
const statusBar_1 = require("../statusBar/statusBar");
const FIRST_EXECUTION_DELAY = 4000;
let currentFilename = null;
function handleErrorState() {
    vscode_1.workspace.onDidOpenTextDocument(({ fileName }) => {
        const firstExecutionDelay = currentFilename ? 0 : FIRST_EXECUTION_DELAY;
        currentFilename = fileName.replace(/[.git]+$/, "");
        setTimeout(() => {
            void requests_1.getState({ filename: currentFilename }).then((state) => {
                if (isInErrorState(state)) {
                    return; // Currently decided that errors will be supressed, until we can provide guidance in the config page.
                    statusBar_1.setErrorStatus("TODO: ERROR HERE");
                }
            });
        }, firstExecutionDelay);
    });
}
exports.default = handleErrorState;
function isInErrorState(state) {
    return (((state === null || state === void 0 ? void 0 : state.local_enabled) && !(state === null || state === void 0 ? void 0 : state.is_cpu_supported)) ||
        ((state === null || state === void 0 ? void 0 : state.cloud_enabled) && !(state === null || state === void 0 ? void 0 : state.is_authenticated)));
}
//# sourceMappingURL=errorState.js.map