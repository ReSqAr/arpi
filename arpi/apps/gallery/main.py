import pathlib

from PyQt5.QtCore import QCoreApplication, QUrl

import arpi.lib.showlistmodel as showlistmodel


translate = QCoreApplication.translate

app_name = translate("app name", "Gallery")
app_description = translate("app description", "Example.")



def activate( view, exit, globalconfig ):
    """
        Load folder overview page.
    """
    activate_here = lambda: activate( view, exit, globalconfig )

    # load gallery path
    gallery_path_file = globalconfig.configpath / 'gallery_path'
    
    if not gallery_path_file.is_file():
        globalconfig.say( translate("gallery app","There are no galleries to display."), blocking=True )
        exit()
        return
     
    with gallery_path_file.open(encoding="utf8") as gallery_path_f:
        gallery_path = gallery_path_f.readline().strip()
        gallery_path = pathlib.Path( gallery_path )
    
    print( "gallery path: {}".format(gallery_path) )

    # read sub directories
    galleries = [ gallery for gallery in gallery_path.iterdir() if gallery.is_dir() ]
    
    # nothing to show if there are no galleries
    if not galleries:
        globalconfig.say( translate("gallery app","There are no galleries to display."), blocking=True )
        exit()
        return
    
    # sort
    galleries.sort(key=lambda gallery: gallery.stat().st_mtime, reverse=True)
    
    # setup QML
    showlistmodel.setup( view,
                            [g.name for g in galleries], # displayed text
                            lambda index: activate_show( view, activate_here, globalconfig, galleries[index]), # activation action
                            lambda index: globalconfig.say(galleries[index].name), # selection action: read name
                            exit
                        )

def activate_show( view, back, globalconfig, gallery ):
    """
        Show the gallery
    """
    back()
