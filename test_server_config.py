import os
import subprocess
import sys
import unittest


class ServerConfigTests(unittest.TestCase):
    def test_supabase_url_missing_leading_h_is_normalized_on_import(self):
        env = os.environ.copy()
        env["SUPABASE_URL"] = "ttps://example.supabase.co/"
        env["SUPABASE_SERVICE_ROLE_KEY"] = "test-service-role-key"

        result = subprocess.run(
            [
                sys.executable,
                "-c",
                "import server; print(server.SUPABASE_URL)",
            ],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            env=env,
            text=True,
            capture_output=True,
            check=True,
        )

        self.assertEqual(result.stdout.strip(), "https://example.supabase.co")


if __name__ == "__main__":
    unittest.main()
