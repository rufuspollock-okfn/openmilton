from ConfigParser import SafeConfigParser

import pkg_resources

import shakespeare.cli

class LoadTexts(shakespeare.cli.BaseCommand):
    '''Load Milton texts.
    '''
    summary = __doc__.split('\n')[0]
    usage = __doc__
    max_args = None
    min_args = 0

    def command(self):
        self._load_config()
        self.load_texts()
        print 'Loaded successfully'

    @classmethod
    def load_texts(self):
        import shakespeare.model as model
        pkg = 'miltondata'
        fileobj = pkg_resources.resource_stream(pkg, '/texts/metadata.txt')
        def locator(section):
            return u'%s::/texts/%s.txt' % (pkg, section)

        model.load_texts(fileobj, locator)

