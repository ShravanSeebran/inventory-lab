import os
from pathlib import Path
import socket
import subprocess
import sys
import time
from urllib.request import urlopen

import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture
def page(tmp_path):
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    env = {**os.environ, "DATABASE_URL": f"sqlite:///{tmp_path / 'browser.db'}"}
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", str(port)],
        cwd=Path(__file__).resolve().parents[2], env=env,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    base_url = f"http://127.0.0.1:{port}"
    try:
        for _ in range(100):
            if process.poll() is not None:
                pytest.fail("Application exited before the browser could connect")
            try:
                urlopen(base_url, timeout=1).close()
                break
            except OSError:
                time.sleep(0.1)
        else:
            pytest.fail("Application did not start")
        with sync_playwright() as playwright:
            channel = os.environ.get("BROWSER_CHANNEL")
            browser = playwright.chromium.launch(channel=channel)
            context = browser.new_context(base_url=base_url)
            browser_page = context.new_page()
            yield browser_page
            context.close()
            browser.close()
    finally:
        process.terminate()
        process.wait(timeout=10)


def register(page, username="kea"):
    page.goto("/register")
    page.get_by_label("First name").fill("Kea")
    page.get_by_label("Last name").fill("Nhlapo")
    page.get_by_label("Username", exact=True).fill(username)
    page.get_by_label("Email", exact=True).fill(f"{username}@example.com")
    page.get_by_label("Password", exact=True).fill("a-long-password")
    page.get_by_role("button", name="Create account").click()


def test_registration_form_submits_and_shows_duplicate_error(page):
    from playwright.sync_api import expect

    register(page)
    expect(page.get_by_role("status")).to_contain_text("Account created")
    register(page)
    expect(page.get_by_role("alert")).to_contain_text("already registered")


def test_login_persists_across_reload_and_logout_clears_session(page):
    from playwright.sync_api import expect

    register(page)
    expect(page.get_by_role("status")).to_contain_text("Account created")
    page.goto("/login")
    page.get_by_label("Username", exact=True).fill("kea")
    page.get_by_label("Password", exact=True).fill("wrong-password")
    page.get_by_role("button", name="Sign in", exact=True).click()
    expect(page.get_by_role("alert")).to_contain_text("Invalid username or password")
    page.get_by_label("Password", exact=True).fill("a-long-password")
    page.get_by_role("button", name="Sign in", exact=True).click()
    expect(page.get_by_role("status")).to_contain_text("Signed in as Kea Nhlapo")
    page.reload()
    expect(page.get_by_role("status")).to_contain_text("Signed in as Kea Nhlapo")
    page.get_by_role("button", name="Sign out").click()
    expect(page.get_by_role("button", name="Sign in", exact=True)).to_be_visible()
    assert page.request.get("/users/me").status == 401
