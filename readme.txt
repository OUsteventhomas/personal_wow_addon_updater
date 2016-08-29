This simple python script written in python 3.5 will update your wow addons
to the latest version available on curse on a Windows machine.

-----Instructions-----

1) Place main.py and addons.db in the same folder
2) Create dloads directory in same folder where main.py and addons.db exist
3) Update the sqlite database to have the addons you wish to have installed.
    a. Column "name" = An easy name for you to remember
    b. Column "url_partial" = The last part of the URL when on that addon's page
        eg: Deadly Boss Mods curse page is "https://mods.curse.com/addons/wow/deadly-boss-mods"
        so the entry for url_partial on Deadly Boss Mods is "deadly-boss-mods"
    c. Columns v_installed, v_available and up_to_date can be left empty
4) Set one variables in this script before running
    a. wow_addon_directory

5) Run script and play WoW
--------------------
