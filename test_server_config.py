import os
import subprocess
import sys
import unittest
from unittest.mock import patch


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

    def test_supabase_mode_does_not_preconnect_during_startup_init(self):
        import server

        with patch.object(server, "use_supabase", return_value=True), \
                patch.object(server, "load_json", side_effect=RuntimeError("dns failed")):
            server.init_files()


if __name__ == "__main__":
    unittest.main()
