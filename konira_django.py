from django.test.simple import DjangoTestSuiteRunner

class Spec(DjangoTestSuiteRunner):

    def _before_all(self):
        """ before all """
        self.setup_django_test_environment()

    def setup_django_test_environment(self):
        self.setup_test_environment()
        self.old_config = self.setup_databases()
        

    def _before_each(self):
        pass


    def _after_each(self):
        pass

    def teardown_django_test_environment(self):
        self.teardown_databases(self.old_config)
        self.teardown_test_environment()

    def _after_all(self):
        self.teardown_django_test_environment()
