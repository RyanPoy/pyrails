# coding: utf8
from sweet.tests import TestCase
from sweet.template import Template


class SearchTest(TestCase):

    def test_for_tag(self):
        t = Template("""
<%= using form(action="/user/new") do f %>
    <%= f.search('name') %>
<% end %>
""")
        self.assertEqual("""
<form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="name" name="name" type="search" />
</form>
""", t.render())

        t = Template("""
<%= using form(action="/user/new") do f %>
    <%= f.search('search', 'Enter your search query here') %>
<% end %>
""")
        self.assertEqual("""
<form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="search" name="search" type="search" value="Enter your search query here" />
</form>
""", t.render())

        t = Template("""
<%= using form(action="/user/new") do f %>
    <%= f.search('search', None, _class='special_input') %>
<% end %>
""")
        self.assertEqual("""
<form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="search" name="search" type="search" class="special_input" />
</form>
""", t.render())

        t = Template("""
<%= using form(action="/user/new") do f %>
    <%= f.search('search', 'Enter your search query here', _class='special_input', disabled=True) %>
<% end %>
""")
        self.assertEqual("""
<form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="search" name="search" type="search" value="Enter your search query here" disabled="disabled" class="special_input" />
</form>
""", t.render())


if __name__ == '__main__':
    import unittest
    unittest.main()