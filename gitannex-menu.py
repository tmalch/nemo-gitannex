import sys
sys.path.append("/home/cloud/projects/bin/nemo-gitannex/")

from gi.repository import Nemo, GObject
import gitannex_utils as utils
import urllib
import os.path


class GitAnnexMenuProvider(GObject.GObject, Nemo.MenuProvider):
    def __init__(self):
        pass
    def menu_get_cb(self, menu, path_list):
        for path in path_list:
            utils.getPath(path)
    def menu_lock_cb(self, menu, path_list):
        for path in path_list:
            utils.lockPath(path)
    def menu_unlock_cb(self, menu, path_list):
        for path in path_list:
            utils.unlockPath(path)
    def menu_drop_cb(self, menu, path_list):
        for path in path_list:
            utils.dropPath(path)
    def menu_sync_cb(self, menu, path):
        utils.sync(path)

    def get_file_items(self, window, files):
        files = [file for file in files if file.get_uri_scheme() == 'file']
        if len(files) < 1:
            return
        file_paths = []
        for file in files:
            file_paths.append(urllib.unquote(file.get_uri()[7:]))

        file = files[0]
        file_path = file_paths[0]
        dir_path = os.path.dirname(file_path)

        if not utils.isGitAnnex(dir_path):
            return

        submenulist = []
        lock_menuitem = Nemo.MenuItem(name='GitAnnexMenuProvider::lock', label='lock', tip='',icon='')
        unlock_menuitem = Nemo.MenuItem(name='GitAnnexMenuProvider::unlock', label='unlock', tip='',icon='')
        get_menuitem = Nemo.MenuItem(name='GitAnnexMenuProvider::get', label='get', tip='',icon='')
        drop_menuitem = Nemo.MenuItem(name='GitAnnexMenuProvider::drop', label='drop', tip='',icon='')
        lock_menuitem.connect('activate', self.menu_lock_cb, file_paths)
        unlock_menuitem.connect('activate', self.menu_unlock_cb, file_paths)
        get_menuitem.connect('activate', self.menu_get_cb, file_paths)
        drop_menuitem.connect('activate', self.menu_drop_cb, file_paths)
        if file.is_directory() or len(files) > 1:
            submenulist.append(get_menuitem)
            submenulist.append(lock_menuitem)
            submenulist.append(unlock_menuitem)
            submenulist.append(drop_menuitem)
        else:
            if utils.isFileLocalAvailable(file_path):
                if utils.isFileModifyable(file_path):
                    submenulist.append(lock_menuitem)
                else:
                    submenulist.append(unlock_menuitem)
                    submenulist.append(drop_menuitem)
            else:
                submenulist.append(get_menuitem)

        top_menuitem = Nemo.MenuItem(name='GitAnnexMenuProvider::GitAnnex', 
                                         label='GitAnnex', 
                                         tip='',
                                         icon='')
        submenu = Nemo.Menu()
        top_menuitem.set_submenu(submenu)

        for sub_menuitem in submenulist:
          submenu.append_item(sub_menuitem)

        return top_menuitem,

    def get_background_items(self, window, file):

        if file.get_uri_scheme() != 'file':
            return
        dir_path = urllib.unquote(file.get_uri()[7:])
        if not file.is_directory():
            dir_path = os.path.dirname(dir_path)
        if not utils.isGitAnnex(dir_path):
            return

        sync_menuitem = Nemo.MenuItem(name='GitAnnexMenuProvider::sync', label='sync', tip='', icon='')
        sync_menuitem.connect('activate', self.menu_sync_cb, dir_path)

        submenu = Nemo.Menu()
        submenu.append_item(sync_menuitem)
        menuitem = Nemo.MenuItem(name='GitAnnexMenuProvider::GitAnnex',
                                         label='GitAnnex',
                                         tip='',
                                         icon='')
        menuitem.set_submenu(submenu)

        return menuitem,

