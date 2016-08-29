This simple python script written in python 3.5 will update your wow addons
to the latest version available on curse on a Windows machine.

-----Instructions-----

1) Place main.py and addons.db in the same folder
2) Update the sqlite database to have the addons you wish to have installed.
    a. Column "name" = An easy name for you to remember
    b. Column "url_partial" = The last part of the URL when on that addon's page
        eg: Deadly Boss Mods curse page is "https://mods.curse.com/addons/wow/deadly-boss-mods"
        so the entry for url_partial on Deadly Boss Mods is "deadly-boss-mods"
    c. Columns v_installed, v_available and up_to_date can be left empty
3) Set "wow_addon_directory" variable in this script before running
4) Run script and play WoW
--------------------
