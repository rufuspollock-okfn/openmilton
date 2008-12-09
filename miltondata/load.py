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
        cfgp = SafeConfigParser()
        cfgp.readfp(fileobj)
        for section in cfgp.sections():
            work = model.Work.by_name(section)
            if work is None:
                work = model.Work(name=section)
            item = model.Material.by_name(section)
            if item is None:
                item = model.Material(name=section)
            assert item is not None
            for key, val in cfgp.items(section):
                if key in ['title', 'creator']:
                    setattr(work, key, val)
                setattr(item, key, val)
            item.work = work
            item.src_pkg = pkg
            item.src_locator = '/texts/%s.txt' % section
            model.Session.flush()


