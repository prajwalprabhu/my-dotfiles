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
exports.TabNine = exports.StatePayload = exports.StateType = exports.API_VERSION = void 0;
var await_semaphore_1 = require("await-semaphore");
var child_process = require("child_process");
var semver = require("semver");
var fs = require("fs");
var path = require("path");
var readline = require("readline");
exports.API_VERSION = "1.0.7";
exports.StateType = {
    error: "error",
    info: "info",
    progress: "progress",
    status: "status",
    pallette: "pallette",
    notification: "notification",
};
exports.StatePayload = {
    message: "Message",
    state: "State",
};
var TabNine = /** @class */ (function () {
    function TabNine(context) {
        this.context = context;
        this.numRestarts = 0;
        this.mutex = new await_semaphore_1.Mutex();
    }
    TabNine.prototype.request = function (version, any_request) {
        return __awaiter(this, void 0, void 0, function () {
            var release;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, this.mutex.acquire()];
                    case 1:
                        release = _a.sent();
                        _a.label = 2;
                    case 2:
                        _a.trys.push([2, , 4, 5]);
                        return [4 /*yield*/, this.requestUnlocked(version, any_request)];
                    case 3: return [2 /*return*/, _a.sent()];
                    case 4:
                        release();
                        return [7 /*endfinally*/];
                    case 5: return [2 /*return*/];
                }
            });
        });
    };
    TabNine.prototype.setState = function (state) {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                return [2 /*return*/, this.request(exports.API_VERSION, { "SetState": { state_type: state } })];
            });
        });
    };
    TabNine.prototype.getCapabilities = function () {
        return __awaiter(this, void 0, void 0, function () {
            var result, error_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        _a.trys.push([0, 2, , 3]);
                        return [4 /*yield*/, this.request(exports.API_VERSION, { "Features": {} })];
                    case 1:
                        result = _a.sent();
                        if (!result["enabled_features"] || !Array.isArray(result["enabled_features"])) {
                            console.error("could not get enabled capabilities");
                            return [2 /*return*/, { enabled_features: [] }];
                        }
                        return [2 /*return*/, result];
                    case 2:
                        error_1 = _a.sent();
                        console.error(error_1);
                        return [2 /*return*/, { enabled_features: [] }];
                    case 3: return [2 /*return*/];
                }
            });
        });
    };
    TabNine.prototype.requestUnlocked = function (version, any_request) {
        var _this = this;
        any_request = {
            "version": version,
            "request": any_request
        };
        var unregisterFunctions = [];
        var request = JSON.stringify(any_request) + '\n';
        var response = new Promise(function (resolve, reject) {
            try {
                if (!_this.isChildAlive()) {
                    _this.restartChild();
                }
                if (!_this.isChildAlive()) {
                    reject(new Error("TabNine process is dead."));
                }
                var onResponse_1 = function (response) {
                    var any_response = JSON.parse(response.toString());
                    resolve(any_response);
                };
                _this.rl.once('line', onResponse_1);
                unregisterFunctions.push(function () { return _this.rl.removeListener('line', onResponse_1); });
                _this.proc.stdin.write(request, "utf8");
            }
            catch (e) {
                console.log("Error interacting with TabNine: " + e);
                reject(e);
            }
        });
        var timeout = new Promise(function (_resolve, reject) {
            var timeout = setTimeout(function () { return reject('request timed out'); }, 1000);
            unregisterFunctions.push(function () { return clearTimeout(timeout); });
        });
        var procExit = new Promise(function (_resolve, reject) {
            var onClose = function () { return reject('Child process exited'); };
            _this.proc.once('exit', onClose);
            unregisterFunctions.push(function () { return _this.proc.removeListener('exit', onClose); });
        });
        var unregister = function () {
            unregisterFunctions.forEach(function (f) { return f(); });
        };
        return Promise.race([response, timeout, procExit]).then(function (value) {
            unregister();
            return value;
        }, function (err) {
            unregister();
            throw err;
        });
    };
    TabNine.prototype.isChildAlive = function () {
        return this.proc && !this.childDead;
    };
    TabNine.runTabNine = function (context, additionalArgs, inheritStdio) {
        if (additionalArgs === void 0) { additionalArgs = []; }
        if (inheritStdio === void 0) { inheritStdio = false; }
        var args = __spreadArrays([
            "--client=vscode",
            "--client-metadata",
            "clientVersion=" + (context === null || context === void 0 ? void 0 : context.vscodeVersion),
            "pluginVersion=" + (context === null || context === void 0 ? void 0 : context.version),
            "t9-vscode-AutoImportEnabled=" + (context === null || context === void 0 ? void 0 : context.isTabNineAutoImportEnabled),
            "t9-vscode-TSAutoImportEnabled=" + (context === null || context === void 0 ? void 0 : context.isTypeScriptAutoImports),
            "t9-vscode-JSAutoImportEnabled=" + (context === null || context === void 0 ? void 0 : context.isJavaScriptAutoImports)
        ], additionalArgs);
        var binary_root = path.join(__dirname, "..", "binaries");
        var command = TabNine.getBinaryPath(binary_root);
        return child_process.spawn(command, args, { stdio: inheritStdio ? 'inherit' : 'pipe' });
    };
    TabNine.prototype.onChildDeath = function () {
        var _this = this;
        this.childDead = true;
        setTimeout(function () {
            if (!_this.isChildAlive()) {
                _this.restartChild();
            }
        }, 10000);
    };
    TabNine.prototype.restartChild = function () {
        var _this = this;
        if (this.numRestarts >= 10) {
            return;
        }
        this.numRestarts += 1;
        if (this.proc) {
            this.proc.kill();
        }
        this.proc = TabNine.runTabNine(this.context, ["ide-restart-counter=" + this.numRestarts]);
        this.childDead = false;
        this.proc.on('exit', function (code, signal) {
            _this.onChildDeath();
        });
        this.proc.stdin.on('error', function (error) {
            console.log("stdin error: " + error);
            _this.onChildDeath();
        });
        this.proc.stdout.on('error', function (error) {
            console.log("stdout error: " + error);
            _this.onChildDeath();
        });
        this.proc.unref(); // AIUI, this lets Node exit without waiting for the child
        this.rl = readline.createInterface({
            input: this.proc.stdout,
            output: this.proc.stdin
        });
    };
    TabNine.getBinaryPath = function (root) {
        var arch;
        if (process.arch == 'x32' || process.arch == 'ia32') {
            arch = 'i686';
        }
        else if (process.arch == 'x64') {
            arch = 'x86_64';
        }
        else {
            throw new Error("Sorry, the architecture '" + process.arch + "' is not supported by TabNine.");
        }
        var suffix;
        if (process.platform == 'win32') {
            suffix = 'pc-windows-gnu/TabNine.exe';
        }
        else if (process.platform == 'darwin') {
            suffix = 'apple-darwin/TabNine';
        }
        else if (process.platform == 'linux') {
            suffix = 'unknown-linux-musl/TabNine';
        }
        else {
            throw new Error("Sorry, the platform '" + process.platform + "' is not supported by TabNine.");
        }
        var versions = fs.readdirSync(root);
        TabNine.sortBySemver(versions);
        var tried = [];
        for (var _i = 0, versions_1 = versions; _i < versions_1.length; _i++) {
            var version = versions_1[_i];
            var full_path = root + "/" + version + "/" + arch + "-" + suffix;
            tried.push(full_path);
            if (fs.existsSync(full_path)) {
                return full_path;
            }
        }
        throw new Error("Couldn't find a TabNine binary (tried the following paths: versions=" + versions + " " + tried + ")");
    };
    TabNine.sortBySemver = function (versions) {
        versions.sort(TabNine.cmpSemver);
    };
    TabNine.cmpSemver = function (a, b) {
        var a_valid = semver.valid(a);
        var b_valid = semver.valid(b);
        if (a_valid && b_valid) {
            return semver.rcompare(a, b);
        }
        else if (a_valid) {
            return -1;
        }
        else if (b_valid) {
            return 1;
        }
        else if (a < b) {
            return -1;
        }
        else if (a > b) {
            return 1;
        }
        else {
            return 0;
        }
    };
    TabNine.reportUninstalled = function () {
        return TabNine.reportUninstall("--uninstalled");
    };
    TabNine.reportUninstalling = function (context) {
        return TabNine.reportUninstall("--uninstalling", context);
    };
    TabNine.reportUninstall = function (uninstallType, context) {
        var _this = this;
        if (context === void 0) { context = null; }
        return new Promise(function (resolve, reject) {
            var proc = _this.runTabNine(context, [uninstallType], true);
            proc.on('exit', function (code, signal) {
                if (signal) {
                    return reject("TabNine aborted with " + signal + " signal");
                }
                resolve(code);
            });
            proc.on('error', function (err) {
                reject(err);
            });
        });
    };
    return TabNine;
}());
exports.TabNine = TabNine;
//# sourceMappingURL=TabNine.js.map