from arpi.apps.phonebook import main as phone_book
from arpi.apps.gallery import main as gallery
from arpi.apps.email import main as email
# from arpi.apps.newspaper import main as newspaper
from arpi.apps.call import main as call

loaded_apps = [
    phone_book,
    gallery,
    email,
    # newspaper,
    call,
]

loaded_apps = [app.App for app in loaded_apps]