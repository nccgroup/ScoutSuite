#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import asyncio

from concurrent.futures import ThreadPoolExecutor

from ScoutSuite.__main__ import main

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    # TODO: make max_workers parameterizable (through the thread_config cli argument)
    loop.set_default_executor(ThreadPoolExecutor(max_workers=10))
    loop.run_until_complete(main())
    loop.close()
    sys.exit()
