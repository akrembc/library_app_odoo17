import unittest
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo import fields

class TestLibraryCheckout(TransactionCase):

    def setUp(self):
        super(TestLibraryCheckout, self).setUp()
        self.Checkout = self.env['library.checkout']
        self.Member = self.env['library.member']
        self.Stage = self.env['library.checkout.stage']
        self.User = self.env['res.users']

    def test_checkout_creation(self):
        member = self.Member.create({
            'name': 'Test Member',
            'email': 'test@example.com',
            'date_of_birth': '1990-01-01',
        })
        user = self.User.create({
            'name': 'Test Librarian',
            'login': 'test_librarian',
        })
        checkout = self.Checkout.create({
            'member_id': member.id,
            'user_id': user.id,
        })
        self.assertEqual(checkout.state, 'new')
        self.assertEqual(checkout.stage_id.state, 'new')
        self.assertEqual(checkout.request_date, fields.Date.today())
        self.assertEqual(checkout.kanban_state, 'normal')

    def test_checkout_stage_change(self):
        member = self.Member.create({
            'name': 'Test Member',
            'email': 'test@example.com',
            'date_of_birth': '1990-01-01',
        })
        user = self.User.create({
            'name': 'Test Librarian',
            'login': 'test_librarian',
        })
        checkout = self.Checkout.create({
            'member_id': member.id,
            'user_id': user.id,
        })

        done_stage = self.Stage.search([('state', '=', 'done')], limit=1)
        checkout.stage_id = done_stage
        self.assertEqual(checkout.state, 'done')

    def test_checkout_cannot_be_created_in_invalid_state(self):
        done_stage = self.Stage.search([('state', '=', 'done')], limit=1)
        with self.assertRaises(UserError):
            self.Checkout.create({
                'member_id': self.Member.create({}).id,
                'stage_id': done_stage.id,
            })

    def test_compute_count_checkouts(self):
        member1 = self.Member.create({'name': 'Test Member 1'})
        member2 = self.Member.create({'name': 'Test Member 2'})
        checkout1 = self.Checkout.create({'member_id': member1.id})
        checkout2 = self.Checkout.create({'member_id': member1.id})
        checkout3 = self.Checkout.create({'member_id': member2.id})
        checkout1.button_done()
        self.assertEqual(member1.count_checkouts, 1)
        self.assertEqual(member2.count_checkouts, 0)

if __name__ == '__main__':
    unittest.main()
