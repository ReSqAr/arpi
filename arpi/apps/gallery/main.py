import os
import pathlib
import csv

from PyQt5.QtCore import QCoreApplication, QUrl, Qt

from arpi.lib.showlistmodel import ShowListModel

translate = QCoreApplication.translate

class App:
    app_name = lambda: translate("app name", "Photos")
    app_description = lambda: translate("app description", "Show photos.")

    SUPPORTED_SUFFIXES = [".jpeg", ".jpg", ".png"]

    def __init__(self, view, leave_app, global_config):
        """
            Start the app by loading the QML file.
        """

        # save variables
        self._view = view
        self._global_config = global_config
        self._leave_app = leave_app

    def __call__(self):
        # activate main page
        self.activate_main(self._leave_app)


    def activate_main(self, back):
        """
            Load folder overview page.
        """
        # load gallery path
        gallery_path = self._global_config.config['gallery']['path']
        if not gallery_path:
            self._global_config.say(translate("gallery app", "There are no galleries to display."), blocking=True)
            self._leave_app()
            return

        gallery_path = pathlib.Path(gallery_path)
        print("DEBUG: gallery path: {}".format(gallery_path))

        # read sub directories
        galleries = [gallery for gallery in gallery_path.iterdir() if gallery.is_dir()]

        # nothing to show if there are no galleries
        if not galleries:
            self._global_config.say(translate("gallery app", "There are no galleries to display."), blocking=True)
            self._leave_app()
            return

        # sort
        galleries.sort(key=lambda gallery: gallery.stat().st_mtime, reverse=True)

        # delegate view to ShowListModel which lists all galleries
        ShowListModel(
                        self._view,
                        # displayed text
                        [g.name for g in galleries],
                        # activation action
                        lambda index: self.activate_show(lambda: self.activate_main(back),galleries[index]),
                        # selection action: read name
                        lambda index: self._global_config.say(galleries[index].name),
                        back,
                    )()


    def activate_show(self, back, gallery):
        """
            Show the gallery
        """
        print('DEBUG: showing gallery: {}'.format(gallery))

        # list photos
        photos = [
                    photo
                    for photo in gallery.iterdir()
                    if photo.is_file() and photo.suffix.lower() in self.SUPPORTED_SUFFIXES
                ]

        # read comments if possible
        comments = {}
        comments_file = gallery / 'comments.csv'

        print('DEBUG: testing comment file: {}'.format(comments_file))
        if comments_file.is_file():
            print('DEBUG: opening comments file')
            with comments_file.open(newline='') as csvfile:
                try:
                    reader = csv.DictReader(csvfile)
                    print('DEBUG: opening comments csv reader')
                    for row in reader:
                        print("DEBUG: reading comments row: {}".format(row))
                        filename = row['filename']
                        filecomment = row['comment']
                        comments[filename] = filecomment
                except:
                    # if there are no comments, there are no comments
                    pass

        # nothing to show if there are no galleries
        if not photos:
            self._global_config.say(translate("gallery app", "There are no photos to display."), blocking=True)
            back()
            return

        # sort
        photos.sort(key=lambda photo: photo.name)

        # set source and set photos property
        filename = os.path.dirname(__file__) + '/res/gallery.qml'
        self._view.setSource(QUrl(filename))
        root = self._view.rootObject()
        root.setProperty("photos", [str(p) for p in photos])

        def read(keyid):
            # announce index
            current_index = keyid+1
            total_number = len(photos)
            self._global_config.say(translate('gallery app', 'Photo {current_index} out of {total_number}.').format(current_index=current_index,total_number=total_number))
            
            # read out comment
            comment = comments.get( photos[keyid].name )
            print('DEBUG: comment for file {}: {}'.format(photos[keyid].name,comment))
            if comment is not None:
                self._global_config.say(comment)

        # connect signals
        root.back.connect(lambda: back(), Qt.QueuedConnection)
        root.selected.connect(lambda keyid: read(keyid), Qt.QueuedConnection)
        
        # call signal for first item
        read(0)
