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
exports.importsHandler = exports.COMPLETION_IMPORTS = void 0;
var vscode_1 = require("vscode");
var importStatement = /Import ([\S]*) from module [\S]*/;
var existingImportStatement = /Add ([\S]*) to existing import declaration from [\S]*/;
var importDefaultStatement = /Import default ([\S]*) from module [\S]*/;
var existingDefaultImportStatement = /Add default import ([\S]*) to existing import declaration from [\S]*/;
var importStatements = [importStatement, existingImportStatement, importDefaultStatement, existingDefaultImportStatement];
var DELAY_FOR_CODE_ACTION_PROVIDER = 400;
exports.COMPLETION_IMPORTS = 'tabnine-completion-imports';
function importsHandler(editor, edit, _a) {
    var completion = _a.completion;
    return __awaiter(this, void 0, void 0, function () {
        var selection, completionSelection_1;
        var _this = this;
        return __generator(this, function (_b) {
            try {
                selection = editor.selection;
                completionSelection_1 = new vscode_1.Selection(selection.active.translate(0, -completion.length), selection.active);
                setTimeout(function () { return __awaiter(_this, void 0, void 0, function () {
                    var codeActionCommands, importCommands, distinctImports, firstCommand, error_1;
                    return __generator(this, function (_a) {
                        switch (_a.label) {
                            case 0:
                                _a.trys.push([0, 5, , 6]);
                                return [4 /*yield*/, vscode_1.commands.executeCommand('vscode.executeCodeActionProvider', editor.document.uri, completionSelection_1, vscode_1.CodeActionKind.QuickFix)];
                            case 1:
                                codeActionCommands = _a.sent();
                                importCommands = findImportCommands(codeActionCommands);
                                distinctImports = filterSameImportFromDifferentModules(importCommands);
                                if (!distinctImports.length) return [3 /*break*/, 4];
                                firstCommand = distinctImports[0];
                                return [4 /*yield*/, vscode_1.workspace.applyEdit(firstCommand.edit)];
                            case 2:
                                _a.sent();
                                return [4 /*yield*/, vscode_1.commands.executeCommand(exports.COMPLETION_IMPORTS, { completion: completion })];
                            case 3:
                                _a.sent();
                                _a.label = 4;
                            case 4: return [3 /*break*/, 6];
                            case 5:
                                error_1 = _a.sent();
                                console.error(error_1);
                                return [3 /*break*/, 6];
                            case 6: return [2 /*return*/];
                        }
                    });
                }); }, DELAY_FOR_CODE_ACTION_PROVIDER);
            }
            catch (error) {
                console.error(error);
            }
            return [2 /*return*/];
        });
    });
}
exports.importsHandler = importsHandler;
function findImportCommands(codeActionCommands) {
    return codeActionCommands.filter(function (_a) {
        var title = _a.title;
        return importStatements.some(function (statement) { return statement.test(title); });
    });
}
/*
 filter imports with same name from different modules
 for example if there are multiple modules with same exported name:
 Import {foo} from './a' and Import {foo} from './b'
 in this case we will ignore and not auto import it
*/
function filterSameImportFromDifferentModules(importCommands) {
    var importNames = importCommands.map(getImportName);
    return importCommands.filter(function (command) { return importNames.filter(function (name) { return name == getImportName(command); }).length <= 1; });
}
function getImportName(_a) {
    var title = _a.title;
    var statement = importStatements.map(function (statement) { return title.match(statement); }).find(Boolean);
    return statement[1];
}
//# sourceMappingURL=importsHandler.js.map