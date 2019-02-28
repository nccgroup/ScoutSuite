#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import asyncio

from ScoutSuite.__main__ import main

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
    sys.exit()
