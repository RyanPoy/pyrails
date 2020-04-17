# coding: utf8
from __init__ import TestCase, UserForTest
import unittest
import os
from template import Template, FormatError


class TagFormDateFieldTest(TestCase):

    def test_form_with_url_and_date_field_tag(self):
        t = Template("""
<%= using form(url="/user/new") do f %>
    <%= f.date_field('name') %>
<% end %>
""")
        self.assertEqual("""
<form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="name" name="name" type="date" />
</form>
""", t.render())

        t = Template("""
<%= using form(url="/user/new") do f %>
    <%= f.date_field('date', '2020-01-01') %>
<% end %>
""")
        self.assertEqual("""
<form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="date" name="date" type="date" value="2020-01-01" />
</form>
""", t.render())

        t = Template("""
<%= using form(url="/user/new") do f %>
    <%= f.date_field('date', _class='special_input') %>
<% end %>
""")
        self.assertEqual("""
<form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="date" name="date" type="date" class="special_input" />
</form>
""", t.render())

        t = Template("""
<%= using form(url="/user/new") do f %>
    <%= f.date_field('date', '2020-01-01', disabled=True, _class='special_input') %>
<% end %>
""")
        self.assertEqual("""
<form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="date" name="date" type="date" value="2020-01-01" disabled="disabled" class="special_input" />
</form>
""", t.render())

if __name__ == '__main__':
    unittest.main()
