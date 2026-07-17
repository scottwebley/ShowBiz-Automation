#!/bin/zsh

cd /Users/scottwebley/ShowBiz-Automation-Production-Backup || exit 1

exec /Library/Frameworks/Python.framework/Versions/3.14/bin/python3 showbiz_daily.py
