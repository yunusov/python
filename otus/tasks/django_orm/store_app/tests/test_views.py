import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_index_view(client):
    url = reverse("index")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_product_view(client, product_3):
    url = reverse("product_detail", kwargs={"pk": product_3.id})
    response = client.get(url)
    assert response.status_code == 200
    assert product_3.name in response.content.decode()
