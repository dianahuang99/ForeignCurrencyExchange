from unittest import TestCase
from app import app
from flask import Flask, request, render_template, redirect, flash

app.config["TESTING"] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
        
class FlaskTests(TestCase):
    
    def test_home_page(self):
        with app.test_client() as client:
            # can now make requests to flask via `client`
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Foreign Currency Exchange</h1>', html)

    def test_result(self):
        with app.test_client() as client:
            resp = client.post('/result',
                               data={'converting_from': 'USD', 'converting_to': 'GBP', 'amount': '10'})
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('The result is £8.32.', html)
            
    def test_redirection_with_invalid_entry(self):
        with app.test_client() as client:
            resp = client.post('/result',
                               data={'converting_from': 'USDDd', 'converting_to': 'GBP', 'amount': '10'})

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/")
            
    def test_redirection_followed_with_flash_messages(self):
        with app.test_client() as client:
            resp = client.post('/result',
                               data={'converting_from': 'USDDd', 'converting_to': 'GBP', 'amount': '10'}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Foreign Currency Exchange</h1>', html)
            self.assertIn('Not a valid 3 letter currency: USDDd', html)