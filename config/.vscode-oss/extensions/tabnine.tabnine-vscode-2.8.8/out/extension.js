/*---------------------------------------------------------
 * Copyright (C) Microsoft Corporation. All rights reserved.
 *--------------------------------------------------------*/
'use strict';
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
exports.activate = void 0;
var vscode = require("vscode");
var TabNine_1 = require("./TabNine");
var importsHandler_1 = require("./importsHandler");
var fs = require("fs");
var path = require("path");
var extensionContext_1 = require("./extensionContext");
var statusBar_1 = require("./statusBar");
var progressBar_1 = require("./progressBar");
var notificationsHandler_1 = require("./notificationsHandler");
var commandsHandler_1 = require("./commandsHandler");
var once = require('lodash.once');
var CHAR_LIMIT = 100000;
var MAX_NUM_RESULTS = 5;
var ON_BOARDING_CAPABILITY = "vscode.onboarding";
var NOTIFICATIONS_CAPABILITY = "vscode.user-notifications";
var DEFAULT_DETAIL = "TabNine";
var initHandlers = once(function (tabNine, context) {
    notificationsHandler_1.handleStartUpNotification(tabNine);
    statusBar_1.registerStatusBar(context, tabNine);
    progressBar_1.setProgressBar(tabNine);
});
function activate(context) {
    return __awaiter(this, void 0, void 0, function () {
        function showFew(response, document, position) {
            for (var _i = 0, _a = response.results; _i < _a.length; _i++) {
                var entry = _a[_i];
                if (entry.kind || entry.documentation) {
                    return false;
                }
            }
            var leftPoint = position.translate(0, -response.old_prefix.length);
            var tail = document.getText(new vscode.Range(document.lineAt(leftPoint).range.start, leftPoint));
            return tail.endsWith('.') || tail.endsWith('::');
        }
        function makeCompletionItem(args) {
            var item = new vscode.CompletionItem(args.entry.new_prefix);
            item.sortText = new Array(args.index + 2).join("0");
            item.insertText = new vscode.SnippetString(escapeTabStopSign(args.entry.new_prefix));
            if (tabNineExtensionContext.isTabNineAutoImportEnabled) {
                item.command = {
                    arguments: [{ completion: args.entry.new_prefix }],
                    command: importsHandler_1.COMPLETION_IMPORTS,
                    title: "accept completion",
                };
            }
            if (args.entry.new_suffix) {
                item.insertText
                    .appendTabstop(0)
                    .appendText(escapeTabStopSign(args.entry.new_suffix));
            }
            item.range = new vscode.Range(args.position.translate(0, -args.old_prefix.length), args.position.translate(0, args.entry.old_suffix.length));
            if (args.entry.documentation) {
                item.documentation = formatDocumentation(args.entry.documentation);
            }
            if (isCapability(NOTIFICATIONS_CAPABILITY)) {
                item.detail = args.entry.detail;
            }
            else {
                if (args.entry.detail) {
                    if (args.detailMessage === DEFAULT_DETAIL || args.detailMessage.includes("Your project contains")) {
                        item.detail = args.entry.detail;
                    }
                    else {
                        item.detail = args.detailMessage;
                    }
                }
                else {
                    item.detail = args.detailMessage;
                }
            }
            item.preselect = (args.index === 0);
            item.kind = args.entry.kind;
            return item;
        }
        function formatDocumentation(documentation) {
            if (isMarkdownStringSpec(documentation)) {
                if (documentation.kind == "markdown") {
                    return new vscode.MarkdownString(documentation.value);
                }
                else {
                    return documentation.value;
                }
            }
            else {
                return documentation;
            }
        }
        function escapeTabStopSign(value) {
            return value.replace(new RegExp("\\$", 'g'), "\\$");
        }
        function isMarkdownStringSpec(x) {
            return x.kind;
        }
        function completionIsAllowed(document, position) {
            var configuration = vscode.workspace.getConfiguration();
            var disable_line_regex = configuration.get('tabnine.disable_line_regex');
            if (disable_line_regex === undefined) {
                disable_line_regex = [];
            }
            var line = undefined;
            for (var _i = 0, disable_line_regex_1 = disable_line_regex; _i < disable_line_regex_1.length; _i++) {
                var r = disable_line_regex_1[_i];
                if (line === undefined) {
                    line = document.getText(new vscode.Range(position.with({ character: 0 }), position.with({ character: 500 })));
                }
                if (new RegExp(r).test(line)) {
                    return false;
                }
            }
            var disable_file_regex = configuration.get('tabnine.disable_file_regex');
            if (disable_file_regex === undefined) {
                disable_file_regex = [];
            }
            for (var _a = 0, disable_file_regex_1 = disable_file_regex; _a < disable_file_regex_1.length; _a++) {
                var r = disable_file_regex_1[_a];
                if (new RegExp(r).test(document.fileName)) {
                    return false;
                }
            }
            return true;
        }
        var tabNineExtensionContext, tabNine, enabled_features, isCapability, triggers;
        var _a;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    tabNineExtensionContext = extensionContext_1.getContext();
                    tabNine = new TabNine_1.TabNine(tabNineExtensionContext);
                    return [4 /*yield*/, tabNine.getCapabilities()];
                case 1:
                    enabled_features = (_b.sent()).enabled_features;
                    isCapability = function (capability) { return enabled_features.includes(capability); };
                    handleAutoImports(tabNineExtensionContext, context);
                    handleUninstall(tabNineExtensionContext);
                    if (isCapability(ON_BOARDING_CAPABILITY)) {
                        initHandlersOnFocus(tabNine, context);
                    }
                    else {
                        commandsHandler_1.registerConfigurationCommand(tabNine, context);
                    }
                    triggers = [
                        ' ',
                        '.',
                        '(',
                        ')',
                        '{',
                        '}',
                        '[',
                        ']',
                        ',',
                        ':',
                        '\'',
                        '"',
                        '=',
                        '<',
                        '>',
                        '/',
                        '\\',
                        '+',
                        '-',
                        '|',
                        '&',
                        '*',
                        '%',
                        '=',
                        '$',
                        '#',
                        '@',
                        '!',
                    ];
                    (_a = vscode.languages).registerCompletionItemProvider.apply(_a, __spreadArrays([{ pattern: '**' }, {
                            provideCompletionItems: function (document, position, token, context) {
                                return __awaiter(this, void 0, void 0, function () {
                                    var offset, before_start_offset, after_end_offset, before_start, after_end, before, after, request, response, completionList, results, detailMessage, _i, _a, msg, limit, index, _b, _c, entry, e_1;
                                    return __generator(this, function (_d) {
                                        switch (_d.label) {
                                            case 0:
                                                _d.trys.push([0, 2, , 3]);
                                                offset = document.offsetAt(position);
                                                before_start_offset = Math.max(0, offset - CHAR_LIMIT);
                                                after_end_offset = offset + CHAR_LIMIT;
                                                before_start = document.positionAt(before_start_offset);
                                                after_end = document.positionAt(after_end_offset);
                                                before = document.getText(new vscode.Range(before_start, position));
                                                after = document.getText(new vscode.Range(position, after_end));
                                                request = tabNine.request(TabNine_1.API_VERSION, {
                                                    "Autocomplete": {
                                                        "filename": document.fileName,
                                                        "before": before,
                                                        "after": after,
                                                        "region_includes_beginning": (before_start_offset === 0),
                                                        "region_includes_end": (document.offsetAt(after_end) !== after_end_offset),
                                                        "max_num_results": MAX_NUM_RESULTS,
                                                    }
                                                });
                                                if (!completionIsAllowed(document, position)) {
                                                    return [2 /*return*/, undefined];
                                                }
                                                return [4 /*yield*/, request];
                                            case 1:
                                                response = _d.sent();
                                                completionList = void 0;
                                                if (response.results.length === 0) {
                                                    completionList = [];
                                                }
                                                else {
                                                    results = [];
                                                    detailMessage = "";
                                                    if (isCapability(NOTIFICATIONS_CAPABILITY)) {
                                                        notificationsHandler_1.handleUserMessage(tabNine, response);
                                                    }
                                                    else {
                                                        for (_i = 0, _a = response.user_message; _i < _a.length; _i++) {
                                                            msg = _a[_i];
                                                            if (detailMessage !== "") {
                                                                detailMessage += "\n";
                                                            }
                                                            detailMessage += msg;
                                                        }
                                                        if (detailMessage === "") {
                                                            detailMessage = DEFAULT_DETAIL;
                                                        }
                                                    }
                                                    limit = undefined;
                                                    if (showFew(response, document, position)) {
                                                        limit = 1;
                                                    }
                                                    index = 0;
                                                    for (_b = 0, _c = response.results; _b < _c.length; _b++) {
                                                        entry = _c[_b];
                                                        results.push(makeCompletionItem({
                                                            document: document,
                                                            index: index,
                                                            position: position,
                                                            detailMessage: detailMessage,
                                                            old_prefix: response.old_prefix,
                                                            entry: entry,
                                                        }));
                                                        index += 1;
                                                        if (limit !== undefined && index >= limit) {
                                                            break;
                                                        }
                                                    }
                                                    completionList = results;
                                                }
                                                return [2 /*return*/, new vscode.CompletionList(completionList, true)];
                                            case 2:
                                                e_1 = _d.sent();
                                                console.log("Error setting up request: " + e_1);
                                                return [3 /*break*/, 3];
                                            case 3: return [2 /*return*/];
                                        }
                                    });
                                });
                            }
                        }], triggers));
                    return [2 /*return*/];
            }
        });
    });
}
exports.activate = activate;
function initHandlersOnFocus(tabNine, context) {
    commandsHandler_1.registerCommands(tabNine, context);
    if (vscode.window.state.focused) {
        initHandlers(tabNine, context);
    }
    else {
        vscode.window.onDidChangeWindowState(function (_a) {
            var focused = _a.focused;
            focused && initHandlers(tabNine, context);
        });
    }
}
function handleAutoImports(tabNineExtensionContext, context) {
    if (tabNineExtensionContext.isTabNineAutoImportEnabled) {
        context.subscriptions.push(vscode.commands.registerTextEditorCommand(importsHandler_1.COMPLETION_IMPORTS, importsHandler_1.importsHandler));
    }
}
function handleUninstall(context) {
    var _this = this;
    try {
        var extensionsPath_1 = path.dirname(context.extensionPath);
        var uninstalledPath_1 = path.join(extensionsPath_1, '.obsolete');
        var isFileExists_1 = function (curr, prev) { return curr.size != 0; };
        var isModified_1 = function (curr, prev) { return new Date(curr.mtimeMs) >= new Date(prev.atimeMs); };
        var isUpdating_1 = function (files) { return files.filter(function (f) { return f.toLowerCase().includes(context.id.toLowerCase()); }).length != 1; };
        var watchFileHandler_1 = function (curr, prev) {
            if (isFileExists_1(curr, prev) && isModified_1(curr, prev)) {
                fs.readFile(uninstalledPath_1, function (err, uninstalled) {
                    try {
                        if (err) {
                            console.error("failed to read .obsolete file:", err);
                            throw err;
                        }
                        fs.readdir(extensionsPath_1, function (err, files) { return __awaiter(_this, void 0, void 0, function () {
                            return __generator(this, function (_a) {
                                switch (_a.label) {
                                    case 0:
                                        if (err) {
                                            console.error("failed to read " + extensionsPath_1 + " directory:", err);
                                            throw err;
                                        }
                                        if (!(!isUpdating_1(files) && uninstalled.includes(context.name))) return [3 /*break*/, 2];
                                        return [4 /*yield*/, TabNine_1.TabNine.reportUninstalling(context)];
                                    case 1:
                                        _a.sent();
                                        fs.unwatchFile(uninstalledPath_1, watchFileHandler_1);
                                        _a.label = 2;
                                    case 2: return [2 /*return*/];
                                }
                            });
                        }); });
                    }
                    catch (error) {
                        console.error("failed to report uninstall:", error);
                    }
                });
            }
        };
        fs.watchFile(uninstalledPath_1, watchFileHandler_1);
    }
    catch (error) {
        console.error("failed to invoke uninstall:", error);
    }
}
//# sourceMappingURL=extension.js.map