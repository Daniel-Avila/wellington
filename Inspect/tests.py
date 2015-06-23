from model_mommy import mommy
from Inspect import models

__author__ = 'sparky'

import os
import shutil
import random
from django.core.management import call_command, CommandError
from django.test import TestCase
from django.utils.six import StringIO
from report import BaseReport

class TestMakeReport(TestCase):
    def setUp(self):

        self.name = str(random.randint(20, 500))
        p = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.target = os.path.join(p, self.name)
        try:
            shutil.rmtree(self.target)
        except OSError:
            pass

    def tearDown(self):
        try:
            shutil.rmtree(self.target)
        except OSError:
            pass

    def test_newreport(self):
        '''Can we make a new report app?'''
        out = StringIO()
        name = self.name

        call_command('newreport', name, stdout=out)
        expected = 'Report App "{0}" created. Please add it to INSTALLED_APPS in your settings file.'.format(name)
        self.assertIn(expected, out.getvalue())
        self.assertTrue(os.path.isdir(self.target))
        files = ['report.py', 'report.yaml', '__init__.py',
                 'models.py', 'views.py', 'tests.py', 'urls.py',
                 'README']
        for f in files:
            target_file = os.path.join(self.target, f)
            msg = 'Expected file "{0}" does not exist'.format(target_file)
            self.assertTrue(os.path.exists(target_file), msg=msg)

    def test_raises_command_error(self):
        '''Do we raise a command error if there is already a report of that name?'''

        out = StringIO()
        name = self.name
        call_command('newreport', name, stdout=out)
        with self.assertRaises(CommandError) as context:

            call_command('newreport', name, stdout=out)
        expected = 'Report App "{0}" already exists'.format(name)

        self.assertIn(expected, context.exception.message)

    def test_makes_templatedir(self):
        '''Do we set up the template directory for our report app?'''
        out = StringIO()
        name = self.name
        call_command('newreport', name, stdout=out)
        expected = '{0}{1}{2}{3}{4}'.format(self.target, os.sep, 'templates', os.sep, name)
        self.assertTrue(os.path.exists(expected))

    def test_specify_path(self):
        '''Do we throw an exception if path is not specified?'''

        class FooReport(BaseReport):
            def generate_report(self):
                pass
        with self.assertRaises(ValueError) as context:
            FooReport()
        self.assertIn('Please specify the location of the yaml file', context.exception.message)

    def test_implement_generate_report(self):
        '''Do we force the developer to implement generate report?'''
        class FooReport(BaseReport):
            path = 'bobo/is/a/dog.yaml'
        with self.assertRaises(TypeError) as context:
            FooReport()
        expected = "Can't instantiate abstract class FooReport with abstract methods generate_report"
        self.assertIn(expected, context.exception.message)


class TestReports(TestCase):

    class TestReport(BaseReport):
        path = '{0}/report.yaml'.format(os.path.dirname(os.path.realpath(__file__)))

        def generate_report(self):
            return self.data[0]

    def setUp(self):
        self.acct = mommy.make(models.RvAccounts, account_name='Foobar', m2m_password='wallet')
        for i in range(4):
            self.auditid = mommy.make(models.RvAudit, account_id=self.acct.account_id).auditid


    def test_filter_by_model_attribute(self):
        '''Can we filter based on data put into the yaml file?

        similar to
        Select <values> from <table> where ID==( select id from <othertable> where name==<value> )
        '''
        my_report = self.TestReport()
        data = my_report.generate_report()
        self.assertEqual(len(data), 4)

    def test_gte_filter(self):
        '''Can we filter on gte? (>=)'''
        my_report = self.TestReport()
        my_yaml = ['RvAudit:\n', '  account_id: RvAccounts.account_id:account_name=Foobar\n',
                   '  auditid: gte {0}\n'.format(self.auditid - 1), '  username: null\n']
        path = '{0}/lt.yaml'.format(os.path.dirname(os.path.realpath(__file__)))
        open(path, 'w').writelines(my_yaml)
        my_report.load_yaml(path)
        data = my_report.generate_report()
        self.assertEqual(len(data), 2)

    def test_gt_filter(self):
        '''Can we filter on gt? (>)'''
        my_report = self.TestReport()
        my_yaml = ['RvAudit:\n', '  account_id: RvAccounts.account_id:account_name=Foobar\n',
                   '  auditid: gt {0}\n'.format(self.auditid - 1), '  username: null\n']
        path = '{0}/lt.yaml'.format(os.path.dirname(os.path.realpath(__file__)))
        open(path, 'w').writelines(my_yaml)
        my_report.load_yaml(path)
        data = my_report.generate_report()
        self.assertEqual(len(data), 1)

    def test_lte_filter(self):
        '''Can we filter on lte? (=<)'''
        my_report = self.TestReport()
        my_yaml = ['RvAudit:\n', '  account_id: RvAccounts.account_id:account_name=Foobar\n',
                   '  auditid: lte {0}\n'.format(self.auditid - 1), '  username: null\n']
        path = '{0}/lt.yaml'.format(os.path.dirname(os.path.realpath(__file__)))
        open(path, 'w').writelines(my_yaml)
        my_report.load_yaml(path)
        data = my_report.generate_report()
        self.assertEqual(len(data), 3)

    def test_lt_filter(self):
        '''Can we filter on lt? (<)'''
        my_report = self.TestReport()
        my_yaml = ['RvAudit:\n', '  account_id: RvAccounts.account_id:account_name=Foobar\n',
                   '  auditid: lt {0}\n'.format(self.auditid - 1), '  username: null\n']
        path = '{0}/lt.yaml'.format(os.path.dirname(os.path.realpath(__file__)))
        open(path, 'w').writelines(my_yaml)
        my_report.load_yaml(path)
        data = my_report.generate_report()
        self.assertEqual(len(data), 2)

    def test_exact_filter(self):
        '''Can we filter for exact?

        NOTE: exact is the default but we can also pass a filter
        '''
        my_report = self.TestReport()
        my_yaml = ['RvAudit:\n', '  account_id: RvAccounts.account_id:account_name=Foobar\n',
                   '  auditid: exact {0}\n'.format(self.auditid - 1), '  username: null\n']
        path = '{0}/lt.yaml'.format(os.path.dirname(os.path.realpath(__file__)))
        open(path, 'w').writelines(my_yaml)
        my_report.load_yaml(path)
        data = my_report.generate_report()
        self.assertEqual(len(data), 1)

    def test_iexact_filter(self):
        my_report = self.TestReport()
        my_yaml = ['RvAccounts:\n', '  account_id: null\n',
                   '  account_name: iexact foobar']
        path = '{0}/lt.yaml'.format(os.path.dirname(os.path.realpath(__file__)))
        open(path, 'w').writelines(my_yaml)
        my_report.load_yaml(path)
        data = my_report.generate_report()
        self.assertEqual(len(data), 1)

    def test_contains_filter(self):
        my_report = self.TestReport()
        my_yaml = ['RvAccounts:\n', '  account_id: null\n',
                   '  account_name: contains bar']
        path = '{0}/lt.yaml'.format(os.path.dirname(os.path.realpath(__file__)))
        open(path, 'w').writelines(my_yaml)
        my_report.load_yaml(path)
        data = my_report.generate_report()
        self.assertEqual(len(data), 1)

    def test_icontains_filter(self):
        my_report = self.TestReport()
        my_yaml = ['RvAccounts:\n', '  account_id: null\n',
                   '  account_name: icontains BAR']
        path = '{0}/lt.yaml'.format(os.path.dirname(os.path.realpath(__file__)))
        open(path, 'w').writelines(my_yaml)
        my_report.load_yaml(path)
        data = my_report.generate_report()
        self.assertEqual(len(data), 1)

    def test_in_filter(self):
        my_report = self.TestReport()
        my_yaml = ['RvAccounts:\n', '  account_id: null\n',
                   '  account_name: in ["Foobar", "Bob"]' ]
        path = '{0}/lt.yaml'.format(os.path.dirname(os.path.realpath(__file__)))
        open(path, 'w').writelines(my_yaml)
        my_report.load_yaml(path)
        data = my_report.generate_report()
        self.assertEqual(len(data), 1)

    def test_startswith_filter(self):
        my_report = self.TestReport()
        my_yaml = ['RvAccounts:\n', '  account_id: null\n',
                   '  account_name: startswith Foo']
        path = '{0}/lt.yaml'.format(os.path.dirname(os.path.realpath(__file__)))
        open(path, 'w').writelines(my_yaml)
        my_report.load_yaml(path)
        data = my_report.generate_report()
        self.assertEqual(len(data), 1)

    def test_istartswith_filter(self):
        my_report = self.TestReport()
        my_yaml = ['RvAccounts:\n', '  account_id: null\n',
                   '  account_name: istartswith foo']
        path = '{0}/lt.yaml'.format(os.path.dirname(os.path.realpath(__file__)))
        open(path, 'w').writelines(my_yaml)
        my_report.load_yaml(path)
        data = my_report.generate_report()
        self.assertEqual(len(data), 1)

    def test_endswith_filter(self):
        my_report = self.TestReport()
        my_yaml = ['RvAccounts:\n', '  account_id: null\n',
                   '  account_name: endswith bar']
        path = '{0}/lt.yaml'.format(os.path.dirname(os.path.realpath(__file__)))
        open(path, 'w').writelines(my_yaml)
        my_report.load_yaml(path)
        data = my_report.generate_report()
        self.assertEqual(len(data), 1)

    def test_iendswith_filter(self):
        my_report = self.TestReport()
        my_yaml = ['RvAccounts:\n', '  account_id: null\n',
                   '  account_name: iendswith bAr']
        path = '{0}/lt.yaml'.format(os.path.dirname(os.path.realpath(__file__)))
        open(path, 'w').writelines(my_yaml)
        my_report.load_yaml(path)
        data = my_report.generate_report()
        self.assertEqual(len(data), 1)

    def test_range_filter(self):
        my_report = self.TestReport()
        self.failIf(models.RvAudit.objects.count() < 2, 'Not enough audit objects got created')
        lower = self.auditid - 2
        my_yaml = ['RvAudit:\n', '  auditid: range {0}, {1}\n'.format(self.auditid - 2, self.auditid),
                   '  actionid: null\n', '  context: null']

        path = '{0}/lt.yaml'.format(os.path.dirname(os.path.realpath(__file__)))
        open(path, 'w').writelines(my_yaml)
        my_report.load_yaml(path)
        data = my_report.generate_report()
        self.assertEqual(len(data), 3)


    def test_isnull_filter(self):

        mommy.make(models.RvAccounts, account_name='Foobar', m2m_password=None)
        my_report = self.TestReport()
        my_yaml = ['RvAccounts:\n', '  account_id: null\n',
                   '  account_name: null\n', '  m2m_password: isnull True']

        path = '{0}/lt.yaml'.format(os.path.dirname(os.path.realpath(__file__)))
        open(path, 'w').writelines(my_yaml)
        my_report.load_yaml(path)
        data = my_report.generate_report()
        self.assertEqual(len(data), 1)

    def test_search_filter(self):
        self.fail('Test not implemented')

    def test_regex_filter(self):
        my_report = self.TestReport()
        my_yaml = ['RvAccounts:\n', '  account_id: null\n',
                   "  account_name: regex (^Fo.*)"]
        path = '{0}/lt.yaml'.format(os.path.dirname(os.path.realpath(__file__)))
        open(path, 'w').writelines(my_yaml)
        my_report.load_yaml(path)
        data = my_report.generate_report()
        self.assertEqual(len(data), 1)

    def test_iregex_filter(self):
        my_report = self.TestReport()
        my_yaml = ['RvAccounts:\n', '  account_id: null\n',
                   "  account_name: iregex (^fo.*)"]
        path = '{0}/lt.yaml'.format(os.path.dirname(os.path.realpath(__file__)))
        open(path, 'w').writelines(my_yaml)
        my_report.load_yaml(path)
        data = my_report.generate_report()
        self.assertEqual(len(data), 1)

    # Date filters
    def test_year_filter(self):
        self.fail('Test not implemented')

    def test_month_filter(self):
        self.fail('Test not implemented')

    def test_day_filter(self):
        self.fail('Test not implemented')

    def test_week_day_filter(self):
        self.fail('Test not implemented')

    def test_hour_filter(self):
        self.fail('Test not implemented')

    def test_minute_filter(self):
        self.fail('Test not implemented')

    def test_second_filter(self):
        self.fail('Test not implemented')
