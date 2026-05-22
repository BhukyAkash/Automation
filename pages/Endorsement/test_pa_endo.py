from tips_endo import endorsement


#Run Command: pytest -s endorsement\test_pa_endo.py --product=pa
def test_pa(page, request):
    try:
        endorsement(page, request)



    finally:
        page.bring_to_front()
        page.get_by_text("playwright", exact=True).click()
        page.get_by_text("Sign Out", exact=True).click()
        page.wait_for_timeout(15000)