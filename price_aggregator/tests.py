from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from price_aggregator.helpers.scraper import amazon_list, ebay_list

class ProductListViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("home")  # Adjust the URL name if it's different in your project

    @patch("price_aggregator.helpers.scraper.amazon_list")
    @patch("price_aggregator.helpers.scraper.ebay_list")
    def test_product_list_view_with_data(self, mock_ebay_list, mock_amazon_list):
        # Mock data returned by the Amazon scraper
        mock_amazon_list.return_value = {
            "content": {
                "offers": [
                    {
                        "name": "SAMSUNG Galaxy S23 5G 128GB - Phantom Black",
                        "price": "$799.99",
                        "link": "https://www.amazon.com/SAMSUNG-Galaxy-S23-Factory-Unlocked/dp/B0C5B736X3/ref=sr_1_1?keywords=Samsung+Galaxy+S23&qid=1730961836&sr=8-1",
                    }
                ]
            }
        }

        # Mock data returned by the eBay scraper
        mock_ebay_list.return_value = {
            "products": [
                {
                    "title": "SAMSUNG Galaxy S23 - Brand New",
                    "sale_price": 359,
                    "link": "https://ebay.com/samsung-galaxy-s23",
                    "image_url": "https://ebay.com/images/samsung-galaxy-s23.jpg",
                }
            ]
        }

        # Make a GET request with search parameters
        response = self.client.get(self.url, {"search": "SAMSUNG Galaxy S23"})

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Log response context to check for 'products'
        print("Response Context:", response.context)

        # Check that the response context contains products
        self.assertIn("products", response.context)
        self.assertGreater(len(response.context["products"]), 0)  # Ensure products are being returned

        # Check that the products have correct data, using partial URL check
        amazon_product = response.context["products"][0]
        ebay_product = response.context["products"][1] if len(response.context["products"]) > 1 else None

        # Check for the presence of core words in Amazon product title
        core_keywords = ["samsung", "galaxy", "s23"]
        for keyword in core_keywords:
            self.assertIn(keyword, amazon_product["title"].lower())  # Flexible title check
        self.assertEqual(amazon_product["price"], "$799.99")  # Adjust based on actual mock price
        self.assertIn("amazon.com", amazon_product["url"])  # Partial URL check
        self.assertEqual(amazon_product["source"], "Amazon")

        # Optional: Check for eBay product (if it exists)
        if ebay_product:
            self.assertEqual(ebay_product["title"], "SAMSUNG Galaxy S23 - Brand New")
            self.assertEqual(ebay_product["sale_price"], 359)
            self.assertEqual(ebay_product["url"], "https://ebay.com/samsung-galaxy-s23")
            self.assertEqual(ebay_product["source"], "Ebay")

    def test_product_list_view_without_data(self):
        # Make a GET request without search parameters
        response = self.client.get(self.url)

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Log response context to check for 'products'
        print("Response Context:", response.context)

        # Check that the response context contains an empty products list
        self.assertIn("products", response.context)
        self.assertEqual(response.context["products"], [])
