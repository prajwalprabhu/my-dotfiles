"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getRootPath = exports.versionPath = void 0;
const consts_1 = require("../consts");
const ARCHITECTURE = getArch();
const SUFFIX = getSuffix();
function versionPath(version) {
    return `${consts_1.BINARY_ROOT_PATH}/${version}/${ARCHITECTURE}-${SUFFIX}`;
}
exports.versionPath = versionPath;
function getRootPath() {
    return consts_1.BINARY_ROOT_PATH;
}
exports.getRootPath = getRootPath;
function getSuffix() {
    switch (process.platform) {
        case "win32":
            return "pc-windows-gnu/TabNine.exe";
        case "darwin":
            return "apple-darwin/TabNine";
        case "linux":
            return "unknown-linux-musl/TabNine";
        default:
            throw new Error(`Sorry, the platform '${process.platform}' is not supported by TabNine.`);
    }
}
function getArch() {
    if (process.arch === "x32" || process.arch === "ia32") {
        return "i686";
    }
    if (process.arch === "x64") {
        return "x86_64";
    }
    throw new Error(`Sorry, the architecture '${process.arch}' is not supported by TabNine.`);
}
//# sourceMappingURL=paths.js.map