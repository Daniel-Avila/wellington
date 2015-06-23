__author__ = 'sparky'
import os

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Create a new report app'

    def add_arguments(self, parser):
        parser.add_argument('name', nargs='+', type=str)

    def handle(self, *args, **options):
        try:
            os.makedirs(os.path.join(options['name'][0], 'templates', options['name'][0]), 0755)
        except OSError:
            msg = 'Report App "{0}" already exists.'.format(options['name'][0])
            raise CommandError(msg)
        write_files = [{'src': '_report.py', 'dst': 'report.py'},
                       {'src': '_report.yaml', 'dst': 'report.yaml'},
                       {'src': '_models.py', 'dst': 'models.py'},
                       {'src': '_views.py', 'dst': 'views.py'},
                       {'src': '_urls.py', 'dst': 'urls.py'},
                       {'src': '_tests.py', 'dst': 'tests.py'},
                       {'src': '_README', 'dst': 'README'},
                       ]
        files = ['__init__.py']

        for wf in write_files:
            target = os.path.join(os.path.dirname(os.path.realpath(__file__)), '_skel', wf['src'])
            dest_dir = '{0}{1}{2}'.format(os.getcwd(), os.sep, options['name'][0])
            dest = os.path.join(dest_dir, wf['dst'])
            open(dest, 'a').writelines(open(target).readlines())

        for f in files:
            dest_dir = '{0}{1}{2}'.format(os.getcwd(), os.sep, options['name'][0])
            dest = os.path.join(dest_dir, f)
            open(dest, 'a').close()
        msg = 'Report App "{0}" created. Please add it to INSTALLED_APPS in your settings file.'
        self.stdout.write(msg.format(options['name'][0]))
