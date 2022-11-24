import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
def test_home_page_url(client):
    response = client.get("/")
    assert response.status_code == 200

@pytest.mark.django_db
def test_home_page_url_by_name(client):
    response = client.get(reverse("home"))
    assert response.status_code == 200

@pytest.mark.django_db
def test_home_page_template_name(client):
    response = client.get(reverse("home"))
    assertTemplateUsed(response, "pages/home.html")

@pytest.mark.django_db
def test_about_page_url(client):
    response = client.get("/about/")
    assert response.status_code == 200

@pytest.mark.django_db
def test_about_page_url_by_name(client):
    response = client.get(reverse("about"))
    assert response.status_code == 200

@pytest.mark.django_db
def test_about_page_template_name(client):
    response = client.get(reverse("about"))
    assertTemplateUsed(response, "pages/about.html")
