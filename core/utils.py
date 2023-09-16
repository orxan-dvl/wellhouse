#
def get_slug2(page):
    return (str(page.content_type)).split("|")[1].strip().replace(" ", "").lower()
