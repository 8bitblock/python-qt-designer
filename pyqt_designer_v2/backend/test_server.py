import sys
import os
import time
import urllib.request
import threading
from pyqt_designer_v2.backend.server import start_server

def test_cors_header():
    port = 9005
    root_dir = os.path.dirname(os.path.abspath(__file__))

    # Start the server in a thread
    t = threading.Thread(target=start_server, args=(port, root_dir), daemon=True)
    t.start()

    # Wait for the server to spin up
    time.sleep(1)

    # Perform a request to the server
    url = f"http://127.0.0.1:{port}/"
    response = urllib.request.urlopen(url)

    # Check the CORS header
    allow_origin = response.headers.get("Access-Control-Allow-Origin")

    # Assert that the overly permissive '*' is no longer there
    assert allow_origin != "*", "Vulnerability: CORS header allows all origins (*)."

    # Assert that it matches the expected restricted local origin
    expected_origin = f"http://127.0.0.1:{port}"
    assert allow_origin == expected_origin, f"Expected CORS header '{expected_origin}', but got '{allow_origin}'"
