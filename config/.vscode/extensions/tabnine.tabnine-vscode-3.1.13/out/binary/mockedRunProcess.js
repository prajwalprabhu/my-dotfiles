"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.stdoutMock = exports.stdinMock = exports.readLineMock = exports.spawnedProcessMock = void 0;
// eslint-disable-next-line import/no-extraneous-dependencies
const TypeMoq = require("typemoq");
const capabilities_1 = require("../capabilities");
exports.spawnedProcessMock = TypeMoq.Mock.ofType();
exports.readLineMock = TypeMoq.Mock.ofType();
exports.stdinMock = TypeMoq.Mock.ofType();
exports.stdoutMock = TypeMoq.Mock.ofType();
function mockedRunProcess() {
    exports.spawnedProcessMock.setup((x) => x.killed).returns(() => false);
    exports.spawnedProcessMock.setup((x) => x.stdin).returns(() => exports.stdinMock.object);
    exports.spawnedProcessMock.setup((x) => x.stdout).returns(() => exports.stdoutMock.object);
    setCapabilities({
        enabled_features: [capabilities_1.Capability.ALPHA_CAPABILITY]
    });
    return {
        proc: exports.spawnedProcessMock.object,
        readLine: exports.readLineMock.object,
    };
}
exports.default = mockedRunProcess;
function setCapabilities(capabilities) {
    let requestHappened = false;
    exports.stdinMock.setup((x) => x.write(TypeMoq.It.is((request) => {
        var _a;
        const capabilitiesRequest = JSON.parse(request);
        if ((_a = capabilitiesRequest === null || capabilitiesRequest === void 0 ? void 0 : capabilitiesRequest.request) === null || _a === void 0 ? void 0 : _a.Features) {
            requestHappened = true;
            return true;
        }
        return false;
    }), "utf8"));
    exports.readLineMock
        .setup((x) => x.once("line", TypeMoq.It.isAny()))
        .callback((x, callback) => {
        if (!requestHappened) {
            callback("null");
        }
        else {
            callback(JSON.stringify(capabilities));
        }
    });
}
//# sourceMappingURL=mockedRunProcess.js.map