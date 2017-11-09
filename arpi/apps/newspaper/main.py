from PyQt5.QtCore import QCoreApplication

import arpi.lib.showlistmodel as showlistmodel
import arpi.lib.showparagraphedtext as showparagraphedtext

translate = QCoreApplication.translate

app_name = lambda: translate("app name", "Newspaper")
app_description = lambda: translate("app description", "Read newspapers.")

# newspaper extractor
available_newspaper = []


def zeit():
    articles = []

    return articles


available_newspaper.append({"name": "Zeit", "extractor": zeit})


def activate(view, exit, globalconfig):
    """
        Show the last x emails.
    """
    activate_here = lambda: activate(view, exit, globalconfig)

    # load selected newspaper
    selected_newspaper = globalconfig.config['newspaper']['selected']  # comma separated list
    print("DEBUG: selected newspaper (raw):", selected_newspaper)
    selected_newspaper = [n.strip().lower() for n in selected_newspaper.split(",")]  # normalise
    selected_newspaper = [n for n in available_newspaper if n["name"].strip().lower() in selected_newspaper]

    print("DEBUG: selected newspaper:", ",".join(n["name"] for n in selected_newspaper))

    if not selected_newspaper:
        globalconfig.say(translate("newspaper app", "There are no newspaper to display."), blocking=True)
        exit()
        return

    # delegate view to ShowListModel which lists all selected newspaper
    showlistmodel.setup(view,
                        [newspaper["name"] for newspaper in selected_newspaper],  # displayed text
                        lambda index: activate_newspaper(view, activate_here, globalconfig, selected_newspaper[index]),
                        # activation action
                        lambda index: globalconfig.say(selected_newspaper[index]["name"]),
                        # selection action: read name
                        exit
                        )


def activate_newspaper(view, back, globalconfig, newspaper):
    """
        Show the newspaper
    """
    activate_here = lambda: activate(view, back, globalconfig)

    articles = newspaper["extractor"]()

    if not articles:
        globalconfig.say(translate("newspaper app", "There are no articles to display."), blocking=True)
        back()
        return

    # delegate view to ShowListModel which lists all articles
    showlistmodel.setup(view,
                        [article.title for article in articles],  # displayed text
                        lambda index: activate_article(view, activate_here, globalconfig, articles[index]),
                        # activation action
                        lambda index: globalconfig.say(articles[index].title),  # selection action: read name
                        exit
                        )


def activate_article(view, back, globalconfig, article):
    # extract text
    text = article.text

    # split into lines
    lines = text.split('\n')

    # create list of paragraphs (between paragraphs is an empty line)
    paragraphs = []
    current_paragraph = []
    for line in lines:
        if not line:
            # 'flush' current paragraph
            if current_paragraph:
                paragraphs.append(' '.join(current_paragraph))
                current_paragraph = []
        else:
            # add to current paragraph
            current_paragraph.append(line)
    # commit last paragraph
    if current_paragraph:
        paragraphs.append(' '.join(current_paragraph))

    # add information
    text = translate("newspaper app", "Title: {title}").format(title=article.title)
    paragraphs.insert(0, text)

    text = translate("newspaper app", "Summary: {summary}").format(summary=article.summary)
    paragraphs.insert(1, text)

    text = translate("newspaper app", "End of article")
    paragraphs.append(text)

    # show paragraphs
    showparagraphedtext.setup(view,
                              paragraphs,
                              lambda index: globalconfig.say(paragraphs[index]),
                              lambda index: globalconfig.say(paragraphs[index]),
                              back
                              )
