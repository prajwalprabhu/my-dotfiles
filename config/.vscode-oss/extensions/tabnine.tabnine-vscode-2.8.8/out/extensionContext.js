"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getContext = void 0;
var vscode = require("vscode");
var EXTENSION_SUBSTRING = "tabnine-vscode";
function getContext() {
    var extension = vscode.extensions.all.find(function (x) { return x.id.includes(EXTENSION_SUBSTRING); });
    var configuration = vscode.workspace.getConfiguration();
    var isJavaScriptAutoImports = configuration.get("javascript.suggest.autoImports");
    var isTypeScriptAutoImports = configuration.get("typescript.suggest.autoImports");
    var autoImportConfig = 'tabnine.experimentalAutoImports';
    var isTabNineAutoImportEnabled = configuration.get(autoImportConfig);
    if (isTabNineAutoImportEnabled !== false) {
        isTabNineAutoImportEnabled = true;
        configuration.update(autoImportConfig, isTabNineAutoImportEnabled, true);
    }
    return {
        get extensionPath() {
            return extension.extensionPath;
        },
        get version() {
            return extension.packageJSON.version;
        },
        get id() {
            return extension.id;
        },
        get name() {
            return EXTENSION_SUBSTRING + "-" + this.version;
        },
        get vscodeVersion() {
            return vscode.version;
        },
        get isTabNineAutoImportEnabled() {
            return isTabNineAutoImportEnabled;
        },
        get isJavaScriptAutoImports() {
            return isJavaScriptAutoImports;
        },
        get isTypeScriptAutoImports() {
            return isTypeScriptAutoImports;
        }
    };
}
exports.getContext = getContext;
//# sourceMappingURL=extensionContext.js.map