SECRET_KEY = '-8j@cxj^72z4ku=o1@hep1cr6&v^70421us$o-+)cs(36#y)hr'
DEBUG = True

def get(setting, default=None):
    return globals().get(setting, default)
