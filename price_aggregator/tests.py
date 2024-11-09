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
        # Mock data returned by the Amazon scraper (2 products)
        mock_amazon_list.return_value = {
            "content": {
                "offers": [
                    {
                        "name": "SAMSUNG Galaxy S23 5G 128GB - Phantom Black",
                        "price": "$799.99",
                        "link": "https://www.amazon.com/SAMSUNG-Galaxy-S23-Factory-Unlocked/dp/B0C5B736X3/ref=sr_1_1?keywords=Samsung+Galaxy+S23&qid=1730961836&sr=8-1",
                    },
                    {
                        "name": "Apple iPhone 14 Pro 128GB - Space Black",
                        "price": "$999.99",
                        "link": "https://www.amazon.com/Apple-iPhone-14-Pro-128GB-Space-Black/dp/B0B5V2XQGH",
                    }
                ]
            }
        }

        # Mock data returned by the eBay scraper (2 products)
        mock_ebay_list.return_value = {
            "products": [
                {
                    "title": "SAMSUNG Galaxy S23 - Brand New",
                    "sale_price": 359,
                    "link": "https://ebay.com/samsung-galaxy-s23",
                    "image_url": "https://ebay.com/images/samsung-galaxy-s23.jpg",
                },
                {
                    "title": "Apple iPhone 14 Pro - Brand New",
                    "sale_price": 899,
                    "link": "https://ebay.com/apple-iphone-14-pro",
                    "image_url": "https://ebay.com/images/iphone-14-pro.jpg",
                }
            ]
        }

        # Make a GET request with search parameters
        response = self.client.get(self.url, {"search": "SAMSUNG Galaxy S23"})

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the response context contains products
        self.assertIn("products", response.context)
        self.assertEqual(len(response.context["products"]), 4)  # We are testing with 4 products

        # Check that the products have correct data, using partial URL check
        amazon_product = response.context["products"][0]
        ebay_product = response.context["products"][2]

        # Check for the presence of core words regardless of extra details
        core_keywords = ["samsung", "galaxy", "s23"]
        for keyword in core_keywords:
            self.assertIn(keyword, amazon_product["title"].lower())  # Flexible title check
        self.assertEqual(amazon_product["price"], 799.99)  # Check the mocked price for the Amazon product
        self.assertIn("amazon.com", amazon_product["url"])  # Partial URL check
        self.assertEqual(amazon_product["source"], "Amazon")

        core_keywords_iphone = ["iphone", "14", "pro"]
        for keyword in core_keywords_iphone:
            self.assertIn(keyword, ebay_product["title"].lower())  # Flexible title check
        self.assertEqual(ebay_product["price"], 899)  # Check the mocked price for the eBay product
        self.assertEqual(ebay_product["url"], "https://ebay.com/apple-iphone-14-pro")
        self.assertEqual(ebay_product["source"], "Ebay")

    def test_product_list_view_without_data(self):
        # Make a GET request without search parameters
        response = self.client.get(self.url)

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the response context contains an empty products list
        self.assertIn("products", response.context)
        self.assertEqual(response.context["products"], [])
