#!/bin/sh
multipass delete -vv testVM --purge
multipass launch -vv -c 4 -m 4G -d 65G -n testVM
