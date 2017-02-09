import pathlib

from PyQt5.QtCore import QCoreApplication, QUrl, Qt

import arpi.lib.showlistmodel as showlistmodel


SUPPORTED_SUFFIXES = [".jpeg",".jpg",".png"]


translate = QCoreApplication.translate

app_name = lambda: translate("app name", "Photos")
app_description = lambda: translate("app description", "Show photos.")


def activate( view, exit, globalconfig ):
    """
        Load folder overview page.
    """
    activate_here = lambda: activate( view, exit, globalconfig )

    # load gallery path
    gallery_path = globalconfig.config['gallery']['path']
    if not gallery_path:
        globalconfig.say( translate("gallery app","There are no galleries to display."), blocking=True )
        exit()
        return
        
    gallery_path = pathlib.Path( gallery_path )
    print( "DEBUG: gallery path: {}".format(gallery_path) )

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
    print( "DEBUG: showing gallery: {}".format(gallery) )
    
    # list photos
    photos = [ photo for photo in gallery.iterdir() if photo.is_file() and photo.suffix.lower() in SUPPORTED_SUFFIXES]
    
    # nothing to show if there are no galleries
    if not photos:
        globalconfig.say( translate("gallery app","There are no photos to display."), blocking=True )
        back()
        return
    
    # sort
    photos.sort(key=lambda photo: photo.name)
    
    # set source and set photos property
    view.setSource(QUrl('arpi/apps/gallery/res/gallery.qml'))
    root = view.rootObject()
    root.setProperty("photos",[str(p) for p in photos])

    # connect signals
    root.back.connect(lambda: back(), Qt.QueuedConnection)

