import unittest
from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Listing

class SimpleTest(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()
        u = User.objects.create_user(username='test', password='test')
        u2 = User.objects.create_user(username='someone_else', password='test')
        # create at least one listing
        l = Listing.objects.create(money_price=1.00, int_inventory = 100, owner_user=u)
        
    # A sanity test that gets all the GETtable urls in listings
    def test_get_gettables(self):
        self.client.login(username='test', password='test')
        gettables = ['/listings/', '/listings/new', '/listings/view/1', '/listings/edit/1', '/listings/delete/1']
        print("getting all gettables in listings")
        for g in gettables:
            response = self.client.get(g)
            if response.status_code != 200:
                print("Yikes! GET failed for " + g)
            self.assertEqual(response.status_code, 200)

    def test_listings_new(self):
        print("trying to create a new listing")
        self.client.login(username='test', password='test')
        # Issue a POST request.
        l = Listing.objects.last()
        id = l.id+1
        response = self.client.post('/listings/new', {
            'title_text': 'Good title',
            'desc_text': 'good description',
            'money_price': '1.00',
            'int_inventory': '20'
        })


        # Check that the redirect is ok.
        self.assertRedirects(response, '/listings/view/' + str(id))
    def test_listings_edit(self):
        self.client.login(username='test', password='test')
        # Issue a POST request.
        newResponse = self.client.post('/listings/new', {
            'title_text': 'Good title',
            'desc_text': 'good description',
            'money_price': '1.00',
            'int_inventory': '20'
        })

        l = Listing.objects.last()
        id = l.id
        edit_response = self.client.post('/listings/edit/' + str(id), {
            'title_text': 'edited title',
            'desc_text': 'good description',
            'money_price': '1.00',
            'int_inventory': '20'
        })
        edited_listing = Listing.objects.get(id=id)

        self.assertEqual(edited_listing.title_text, 'edited title')


