"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const fs = require("fs");
const paths_1 = require("./paths");
const semverUtils_1 = require("../semverUtils");
function fetchBinaryPath() {
    const versions = semverUtils_1.default(fs.readdirSync(paths_1.getRootPath())).map(paths_1.versionPath);
    const selectedVersion = versions.find(fs.existsSync);
    if (!selectedVersion) {
        throw new Error(`Couldn't find a TabNine binary (tried the following paths: ${versions.join(", ")})`);
    }
    return selectedVersion;
}
exports.default = fetchBinaryPath;
//# sourceMappingURL=fetchBinaryPath.js.map