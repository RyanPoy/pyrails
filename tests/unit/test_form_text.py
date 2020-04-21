# coding: utf8
from sweet.tests.unit import TestCase
import unittest
from sweet.template import Template


class TextTest(TestCase):

    def test_for_tag(self):

        t = Template("""
<%= using form(action="/user/new") do f %>
    <%= f.text('name') %>
<% end %>
""")
        self.assertEqual("""
<form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="name" name="name" type="text" />
</form>
""", t.render())

        t = Template("""
<%= using form(action="/user/new") do f %>
    <%= f.text('query', 'Enter your search query here') %>
<% end %>
""")
        self.assertEqual("""
<form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="query" name="query" type="text" value="Enter your search query here" />
</form>
""", t.render())

        t = Template("""
<%= using form(action="/user/new") do f %>
    <%= f.text('search', placeholder='Enter search term...') %>
<% end %>
""")
        self.assertEqual("""
<form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="search" name="search" type="text" placeholder="Enter search term..." />
</form>
""", t.render())

        t = Template("""
<%= using form(action="/user/new") do f %>
    <%= f.text('request', _class='special_input') %>
<% end %>
""")
        self.assertEqual("""
<form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="request" name="request" type="text" class="special_input" />
</form>
""", t.render())

        t = Template("""
<%= using form(action="/user/new") do f %>
    <%= f.text('address', '', size=75) %>
<% end %>
""")
        self.assertEqual("""
<form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="address" name="address" type="text" value="" size="75" />
</form>
""", t.render())

        t = Template("""
<%= using form(action="/user/new") do f %>
    <%= f.text('zip', maxlength=5) %>
<% end %>
""")
        self.assertEqual("""
<form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="zip" name="zip" type="text" maxlength="5" />
</form>
""", t.render())

        t = Template("""
<%= using form(action="/user/new") do f %>
    <%= f.text('payment_amount', '$0.00', disabled=True) %>
<% end %>
""")
        self.assertEqual("""
<form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="payment_amount" name="payment_amount" type="text" value="$0.00" disabled="disabled" />
</form>
""", t.render())

        t = Template("""
<%= using form(action="/user/new") do f %>
    <%= f.text('ip', '0.0.0.0', maxlength=15, size=20, _class="ip-input") %>
<% end %>
""")
        self.assertEqual("""
<form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="ip" name="ip" type="text" value="0.0.0.0" size="20" maxlength="15" class="ip-input" />
</form>
""", t.render())
        

if __name__ == '__main__':
    import unittest
    unittest.main()
