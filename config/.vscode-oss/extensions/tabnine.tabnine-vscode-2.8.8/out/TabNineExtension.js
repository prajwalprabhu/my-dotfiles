"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var vscode = require("vscode");
var EXTENSION_SUBSTRING = "tabnine-vscode";
var TabNineExtension = /** @class */ (function () {
    function TabNineExtension(ext) {
        this.extension = ext;
    }
    Object.defineProperty(TabNineExtension.prototype, "extensionPath", {
        get: function () {
            return this.extension.extensionPath;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(TabNineExtension.prototype, "version", {
        get: function () {
            return this.extension.packageJSON.version;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(TabNineExtension.prototype, "name", {
        get: function () {
            return EXTENSION_SUBSTRING + "-" + this.version;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(TabNineExtension.prototype, "vscodeVersion", {
        get: function () {
            return vscode.version;
        },
        enumerable: true,
        configurable: true
    });
    TabNineExtension.getInstance = function () {
        if (!TabNineExtension.instance) {
            var extension = vscode.extensions.all.find(function (x) { return x.id.includes(EXTENSION_SUBSTRING); });
            TabNineExtension.instance = new TabNineExtension(extension);
        }
        return TabNineExtension.instance;
    };
    return TabNineExtension;
}());
exports.TabNineExtension = TabNineExtension;
//# sourceMappingURL=TabNineExtension.js.map