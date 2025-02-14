# Zeekctl test plugin that uses plugin state variables.

import ZeekControl.plugin


class StateTest(ZeekControl.plugin.Plugin):
    def __init__(self):
        super().__init__(apiversion=1)

    def name(self):
        return "statetest"

    def pluginVersion(self):
        return 1

    def init(self):
        sv = self.getState("statevar")
        if not sv:
            sv = 0

        self.setState("statevar", sv + 1)

        with open("state.out", "w") as f:
            f.write(f"statevar: {self.getState('statevar')}\n")

        return True
