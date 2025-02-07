from bs4 import BeautifulSoup
from django.test import TestCase


class SoupTestMixin:
    def get_doc(self, *args, **kwargs):
        response = self.client.get(*args, **kwargs)
        return BeautifulSoup(response.render().content, 'lxml')

    def post_doc(self, *args, **kwargs):
        kwargs['follow'] = True
        response = self.client.post(*args, **kwargs)
        try:
            return BeautifulSoup(response.render().content, 'lxml')
        except AttributeError:
            return BeautifulSoup(response.content, 'lxml')


class SoupTest(SoupTestMixin, TestCase):
    pass


def extract_form_fields(soup):
    """
    Turn a BeautifulSoup form in to a dict of fields and default values
    Inspiration: https://gist.github.com/simonw/104413
    """
    data = {}
    for field in soup.find_all('input'):
        # ignore submit/image with no name attribute
        if field['type'] in ('submit', 'image') and not field.has_attr('name'):
            continue

        if field['type'] in ('checkbox', 'radio'):
            if field.has_attr('checked') and field.has_attr('name'):
                if field['name'] in data:
                    if not isinstance(data[field['name']], list):
                        data[field['name']] = [data[field['name']]]
                    data[field['name']].append(field.get('value', 'on'))
                else:
                    data[field['name']] = field.get('value', 'on')
            continue
        elif field.has_attr('name'):
            # single element name/value fields
            value = field.get('value', '')
            if field['name'] in data:
                if not isinstance(data[field['name']], list):
                    data[field['name']] = [data[field['name']]]
                data[field['name']].append(value)
            else:
                data[field['name']] = value
            continue

    # textareas
    for textarea in soup.findAll('textarea'):
        if textarea['name'] in data:
            if not isinstance(data[textarea['name']], list):
                data[textarea['name']] = [data[textarea['name']]]
            data[textarea['name']].append(textarea.text or '')
        else:
            data[textarea['name']] = textarea.text or ''

    # select fields
    for select in soup.find_all('select'):
        value = ''
        options = select.find_all('option')
        is_multiple = select.has_attr('multiple')
        selected_options = [option for option in options if option.has_attr('selected')]

        # If no select options, go with the first one
        if not selected_options and options:
            selected_options = [options[0]]

        if not is_multiple:
            assert len(selected_options) < 2
            if len(selected_options) == 1:
                value = selected_options[0]['value']
        else:
            value = [option['value'] for option in selected_options]

        if select['name'] in data:
            if not isinstance(data[select['name']], list):
                data[select['name']] = [data[select['name']]]
            data[select['name']].append(value)
        else:
            data[select['name']] = value

    return data
