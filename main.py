import requests
import re
import sqlite3
import zipfile as zip
import os
import wget


class addonUpdater():

    wow_addon_directory = r"F:\World of Warcraft\Interface\AddOns\\"
    path = os.getcwd()
    wow_path = wow_addon_directory[:-1]

    def download_path(self):
        dloads_path = "{0}\\dloads".format(self.path)
        if os.path.exists(dloads_path):
            os.chdir(dloads_path)
        else:
            os.mkdir(dloads_path)
            os.chdir(dloads_path)
        self.db_file = "{0}\\addons.db".format(os.path.dirname(os.getcwd()))

    def main(self):
        self.download_path()
        self.db_connect()
        self.db_select_all_data()
        self.select_out_of_date()
        self.unzip_addons()
        self.set_all_versions_current()
        self.db_close_connection()

    def db_connect(self):
        self.conn = sqlite3.connect(self.db_file)

    def db_select_all_data(self):
        cursor = self.conn.execute("SELECT * FROM info")
        for row in cursor:
            self.name = row[0]
            self.url_partial = row[1]
            self.installed_version = row[2]
            self.cur_version = row[3]
            self.needs_updating = row[4]
            self.version_update()
            self.addon_update_db()

    def set_all_versions_current(self):
        update_query = "UPDATE info SET v_installed = v_available"
        self.conn.execute(update_query)
        second_update_query = "UPDATE info SET up_to_date = '1'"
        self.conn.execute(second_update_query)
        self.commit_db_changes()

    def select_out_of_date(self):
        cursor = self.conn.execute("SELECT * FROM info WHERE up_to_date = '0'")
        for row in cursor:
            self.url_partial = row[1]
            self.download_zip_file_page()

    def download_zip_file_page(self):
        url = "https://mods.curse.com/addons/wow/{0}/download".format(self.url_partial)
        r = requests.get(url)
        page_text = r.text
        link = re.findall("http://.*\.zip", page_text)[0]
        print("Downloading: {0}".format(self.name))
        wget.download(link)

    def version_update(self):
        url = "https://mods.curse.com/addons/wow/{0}".format(self.url_partial)
        r = requests.get(url)
        data = r.text
        self.newest_version = re.sub("Newest File: ", "", re.findall("Newest File:.*\<", data)[0][:-1])
        if self.newest_version != self.cur_version:
            self.db_version_update()

    def db_version_update(self):
        update_query = "UPDATE info SET v_available = '{0}' WHERE url_partial = '{1}'".format(self.newest_version, self.url_partial)
        self.conn.execute(update_query)
        self.commit_db_changes

    def addon_update_db(self):
        if self.installed_version == self.cur_version and self.needs_updating != "1":
            up_to_date_query = "UPDATE info SET up_to_date = '1' WHERE name = '{0}'".format(self.name)
            self.conn.execute(up_to_date_query)
        elif self.installed_version != self.cur_version and self.needs_updating != "0":
            not_up = "UPDATE info SET up_to_date = '0' WHERE name = '{0}'".format(self.name)
            self.conn.execute(not_up)
        self.commit_db_changes()

    def unzip_addons(self):
        for dirName, subdirlist, filelist in os.walk(self.path):
            for fname in filelist:
                if fname.endswith(".zip") is True:
                    src_path = "\\".join((dirName, fname))
                    zipcheck = zip.is_zipfile(src_path)
                    if zipcheck is True:
                        with zip.ZipFile(src_path) as zf:
                            zf.extractall(self.wow_path)
                        os.remove(src_path)

    def commit_db_changes(self):
        self.conn.commit()

    def db_close_connection(self):
        self.conn.close()

if __name__ == "__main__":
    addonUpdater().main()
