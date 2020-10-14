"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.registerConfig = void 0;
var statusBar_1 = require("./statusBar");
var vscode_1 = require("vscode");
var progressBar_1 = require("./progressBar");
var notificationsHandler_1 = require("./notificationsHandler");
var IS_OSX = process.platform == 'darwin';
function registerConfig(context, tabNine, config) {
    var panel = vscode_1.window.createWebviewPanel('tabnine.settings', 'TabNine Settings', { viewColumn: vscode_1.ViewColumn.Active, preserveFocus: false }, {
        retainContextWhenHidden: true,
        enableFindWidget: true,
        enableCommandUris: true,
        enableScripts: true,
    });
    panel.iconPath = vscode_1.Uri.parse("../small_logo.png");
    panel.webview.html = "\n        <!DOCTYPE html>\n        <html lang=\"en\">\n            <head>\n                <meta charset=\"UTF-8\">\n                <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n                <title>TabNine Settings</title>\n            </head>\n            <body>\n            <iframe src=" + config.message + " id=\"config\" frameborder=\"0\" style=\"display: block; margin: 0px; overflow: hidden; position: absolute; width: 100%; height: 100%; visibility: visible;\"></iframe>\n                <script>\n                    window.onfocus = config.onload = function() {\n                        setTimeout(function() {\n                            document.getElementById(\"config\").contentWindow.focus();\n                        }, 100);\n                    };\n                    window.addEventListener(\"message\", (e) => {\n                      let data = e.data;\n                      switch (data.type) {\n                        case \"keydown\": {\n                          window.dispatchEvent(new KeyboardEvent('keydown',data.event));\n                          break;\n                        }\n                        case \"link-click\": {\n                          let tempRef = document.createElement(\"a\");\n                          tempRef.setAttribute(\"href\", data.href);\n                          config.appendChild(tempRef);\n                          tempRef.click();\n                          tempRef.parentNode.removeChild(tempRef);\n                          break;\n                        }\n                      }\n                  }, false);\n                  </script>\n            </body>\n        </html>";
    panel.onDidDispose(function () {
        statusBar_1.updateStatusBar(tabNine, null);
        progressBar_1.setProgressBar(tabNine);
        notificationsHandler_1.handleStartUpNotification(tabNine);
    }, null, context.subscriptions);
}
exports.registerConfig = registerConfig;
//# sourceMappingURL=configHandler.js.map