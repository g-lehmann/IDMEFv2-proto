# VERSION: 1.0
# AUTHOR: Prelude Team <support.prelude@csgroup.eu>
# DESCRIPTION: Triggered by a single host being the source of many actions on a single target
# Copyright (C) 2006 G Ramon Gomez <gene at gomezbrothers dot com>
# Copyright (C) 2009-2021 CS GROUP - France <support.prelude@csgroup.eu>
#
# This file is part of the Prelude-Correlator program.
#
# SPDX-License-Identifier: BSD-2-Clause
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIEDi
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Detect Eventscan:
# Playing multiple events from a single host against another single host

from preludecorrelator.context import Context
from preludecorrelator.pluginmanager import Plugin


class EventScanPlugin(Plugin):
    def run(self, idmef):
        source = idmef.get("alert.source(*).node.address(*).address")
        target = idmef.get("alert.target(*).node.address(*).address")

        if not source or not target:
            return

        for saddr in source:
            for daddr in target:
                ctx = Context(("SCAN EVENTSCAN", saddr, daddr),
                              {"expire": 60, "threshold": 30, "alert_on_expire": True},
                              update=True, idmef=idmef, ruleid=self.name)
                if ctx.getUpdateCount() == 0:
                    ctx.set("alert.correlation_alert.name",
                            "A single host has played many events against a single target. This may be a vulnerability "
                            "scan")
                    ctx.set("alert.classification.text", "Eventscan")
                    ctx.set("alert.assessment.impact.severity", "high")
