#!/usr/bin/env bash
py.test authentication.py businesses.py categories.py my_account.py offers.py management.py search.py tags.py special_categories.py combined_tags.py breadcrumbs.py --html=report.html --junitxml results.xml
