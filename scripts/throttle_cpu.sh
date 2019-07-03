#!/usr/bin/env bash

ps aux | grep run_account | awk '{if($3>90){print $2}}' | xargs -I "%" cputh "%" 70