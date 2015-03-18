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
        all_metas = {}
        relative_readme_path = "README.rst"
        relative_meta_path = os.path.join("meta", "main.yml")

        role_names = th.create_roles_with_dependencies(self.test_path)

        # ----------------------------------------------------------------
        # add meta files to the roles
        # ----------------------------------------------------------------
        for i, role in enumerate(role_names):
            defaults_path = os.path.join(self.test_path, role,
                                         "defaults", "main.yml")
            tasks_path = os.path.join(self.test_path, role,
                                      "tasks", "main.yml")
            utils.string_to_file(defaults_path, th.DEFAULTS_TEMPLATE)
            utils.string_to_file(tasks_path, th.TASKS_TEMPLATE)

        # ----------------------------------------------------------------
        # test role that doens't exists
        # ----------------------------------------------------------------
        (out, err) = utils.capture_shell(
            "ansigenome reverse_dependencies {0} -r test1".format(
                self.test_path))

        if os.path.exists(relative_meta_path):
            th.populate_dict_with_files(self.test_path, role_names, all_metas,
                                        relative_readme_path)

        th.print_out("test role that doens't exists:", out)
        self.assertIn("No role named 'test1' was found in the path", out)

        # ----------------------------------------------------------------
        # test role that exists but has no reverse dependency
        # ----------------------------------------------------------------

        (out, err) = utils.capture_shell(
            "ansigenome reverse_dependencies {0} -r role1".format(
                self.test_path))

        if os.path.exists(relative_meta_path):
            th.populate_dict_with_files(self.test_path, role_names, all_metas,
                                        relative_readme_path)

        th.print_out("test role that exists but has no reverse dependency:",
                     out)
        self.assertIn("['role1']", out)

        # ----------------------------------------------------------------
        # test role that exists and have reverse dependency
        # ----------------------------------------------------------------

        (out, err) = utils.capture_shell(
            "ansigenome reverse_dependencies {0} -r role2".format(
                self.test_path))

        if os.path.exists(relative_meta_path):
            th.populate_dict_with_files(self.test_path, role_names, all_metas,
                                        relative_readme_path)

        th.print_out("test role that exists and have reverse dependency:", out)
        self.assertIn("'role1'", out)
        self.assertIn("'role2'", out)
        self.assertNotIn("'role3'", out)

if __name__ == "__main__":
    unittest.main()
