import pytest
from bs4 import BeautifulSoup
from ckan.tests import factories


@pytest.mark.ckan_config(
    "scheming.dataset_schemas", "ckanext.fluent:fluent_scheming.yaml")
@pytest.mark.usefixtures("clean_db", "with_plugins")
def test_only_first_title_input_is_slug_preview_target(app):
    user = factories.SysadminWithToken()
    headers = {"Authorization": user["token"]}
    html = app.get("/fluent-test/new", headers=headers).get_data(as_text=True)
    soup = BeautifulSoup(html, "html.parser")
    assert soup.find("input", attrs={"name": "title_translated-en"})
    assert soup.find("input", attrs={"name": "title_translated-fr"})
    targets = [
        i["name"] for i in soup.find_all("input")
        if "slug-preview-target" in i.get("data-module", "").split()
    ]
    assert targets == ["title_translated-en"]
