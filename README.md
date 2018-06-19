# Planetary Vegetation


WARNING:
    - Automated use of Twitter can result in account termination.
      Make sure you know what you are doing.
    - This tool may or may not have bugs.  Use at your own risk.


This project is built around an old project that originally stored user info in a MySQL database.
We are transitioning everything to use MongoDB.


Source Files:

    twitter_automation.py   - All of the good twitter stuff is in here.
                            - This also contains a basic CLI for the newer functionality

    accounts_control.py  - This contains functions for managing twitter accounts and other account types.
                           This is old and still uses MySQL.

    green_layer.py - This is the Flask web GUI.  Currently it mostly just works as a front end for accounts_control.py

    feed_source.py - This contains functions to scrape data and automaticlly post it.
                     It is old and needs to be redone.

    main.config - This is the main configuration file.  Currently this controls which MongoDB instance is used.


Terminology:

    account - a twitter account that you own/control ( you )
    user - another twitter user ( someone else )
    friend - someone that you follow
    follower - someone that follows you