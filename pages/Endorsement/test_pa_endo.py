import pytest
from tips_endo import endorsement

def test_pa(page, request):
    try:
        endorsement(page, request)



    finally:
        page.bring_to_front()
        page.get_by_text("playwright", exact=True).click()
        page.get_by_text("Sign Out", exact=True).click()
        page.wait_for_timeout(15000)