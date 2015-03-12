import os
import unittest

import ansigenome.constants as c
import ansigenome.test_helpers as th
import ansigenome.utils as utils


class TestReverseDependencies(unittest.TestCase):
    """
    Integration tests for the genmeta command.
    """
    def setUp(self):
        self.test_path = os.getenv("ANSIGENOME_TEST_PATH", c.TEST_PATH)

        if not os.path.exists(self.test_path):
            os.makedirs(self.test_path)

    def tearDown(self):
        th.rmrf(self.test_path)

    def test_reverse_dependencies(self):
        th.create_roles_with_dependencies(self.test_path)

        # ----------------------------------------------------------------
        # test role that doens't exists
        # ----------------------------------------------------------------
        (out, err) = utils.capture_shell(
            "ansigenome reverse_dependencies {0} -r test1".format(
                self.test_path))
        th.print_out("test role that doens't exists:", out)
        self.assertIn("No role named 'test1' was found in the path", out)

        # ----------------------------------------------------------------
        # test role that exists but has no reverse dependency
        # ----------------------------------------------------------------

        (out, err) = utils.capture_shell(
            "ansigenome reverse_dependencies {0} -r role1".format(
                self.test_path))

        th.print_out("test role that exists but has no reverse dependency:",
                     out)
        self.assertIn("['role1']", out)

        # ----------------------------------------------------------------
        # test role that exists and have reverse dependency
        # ----------------------------------------------------------------

        (out, err) = utils.capture_shell(
            "ansigenome reverse_dependencies {0} -r role2".format(
                self.test_path))

        th.print_out("test role that exists and have reverse dependency:", out)
        self.assertIn("'role1'", out)
        self.assertIn("'role2'", out)
        self.assertNotIn("'role3'", out)

if __name__ == "__main__":
    unittest.main()
