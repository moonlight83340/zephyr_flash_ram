# SPDX-License-Identifier: Apache-2.0

"""west "flash-ram" command"""

import os
import sys
from pathlib import Path

ZEPHYR_BASE = os.environ.get("ZEPHYR_BASE")
if not ZEPHYR_BASE:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "zephyr").is_dir():
            ZEPHYR_BASE = str(parent / "zephyr")
            break
    else:
        print("ZEPHYR_BASE not set and zephyr directory not found.")
        sys.exit(1)

sys.path.insert(0, os.path.join(ZEPHYR_BASE, "scripts", "west_commands"))

from west.commands import WestCommand
from run_common import add_parser_common
from flash import Flash


class FlashRam(WestCommand):
    def __init__(self):
        super().__init__(
            "flash-ram",
            "Flash binary to RAM using OpenOCD",
            "Load an ELF file into RAM (instead of flashing to flash).",
            accepts_unknown_args=True,
        )

        self.flash_cmd = Flash()

    def do_add_parser(self, parser_adder):
        return add_parser_common(self, parser_adder)

    def do_run(self, my_args, runner_args):
        self.flash_cmd.manifest = getattr(self, "manifest", None)
        self.flash_cmd.topdir = getattr(self, "topdir", None)
        self.flash_cmd._logger = getattr(self, "_logger", None)
        runner_args = list(runner_args)
        runner_args.append("--use-elf")
        return self.flash_cmd.do_run(my_args, runner_args)
