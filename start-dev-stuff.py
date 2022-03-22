#!/usr/bin/env python3.7

import iterm2
# This script was created with the "basic" environment which does not support adding dependencies
# with pip.

async def main(connection):
    cxr_window = await iterm2.Window.async_create(connection, "Default", "cd ~/repo/airkit/node/cxr && ~/Documents/dotfiles/set_iterm_badge.sh CXR")
    nsg_window = await iterm2.Window.async_create(connection, "Default", "cd ~/repo/airkit/node/session-gateway && ~/Documents/dotfiles/set_iterm_badge.sh 'SESSION GATEWAY'")
    ksm_window = await iterm2.Window.async_create(connection, "Default", "cd ~/repo/airkit/kotlin/session-manager && ~/Documents/dotfiles/set_iterm_badge.sh 'SESSION MANAGER'")
    nwb_window = await iterm2.Window.async_create(connection, "Default", "cd ~/repo/airkit/node/web-builder && ~/Documents/dotfiles/set_iterm_badge.sh 'WEB BUILDER'")

iterm2.run_forever(main)