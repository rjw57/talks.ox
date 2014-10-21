import unittest
from operator import attrgetter

from django.test import TestCase

from . import forms, models, factories


class TestEventForm(TestCase):

    def test_empty(self):
        form = forms.EventForm({})
        self.assertEquals(form.is_valid(), False, "empty form should not validate")
        errors = form.errors.as_data()
        self.assertEquals(len(errors), 2)
        self.assertIn('title', errors)
        self.assertIn('description', errors)

    def test_all_fields_blanked(self):
        data = {
            'description': u'',
            'title': u'',
            'location': u'',
            'department_suggest': u'',
            'start': u'',
            'topics': u'',
            'speaker_suggest': u'',
            'location_suggest': u'',
            'department_organiser': u'',
            'speakers': u'',
            'topic_suggest': u'',
            'end': u'',
        }
        form = forms.EventForm(data)
        self.assertEquals(form.is_valid(), False, "blanked form should not validate")
        errors = form.errors.as_data()
        self.assertEquals(len(errors), 2)
        self.assertIn('title', errors)
        self.assertIn('description', errors)

    def test_invalid_date(self):
        data = {
            'description': u'',
            'title': u'',
            'location': u'',
            'department_suggest': u'',
            'start': u'94872394',
            'topics': u'',
            'speaker_suggest': u'',
            'location_suggest': u'',
            'department_organiser': u'',
            'speakers': u'',
            'topic_suggest': u'',
            'end': u'',
        }
        form = forms.EventForm(data)
        self.assertEquals(form.is_valid(), False, "blanked form should not validate")
        errors = form.errors.as_data()
        self.assertEquals(len(errors), 3)
        self.assertIn('title', errors)
        self.assertIn('description', errors)
        self.assertIn('start', errors)


class TestEventGroupForm(TestCase):

    def test_empty(self):
        form = forms.EventGroupForm({})
        self.assertEquals(form.is_valid(), True, "empty form should validate")

    @unittest.skip("not actually true")
    def test_enabled(self):
        form = forms.EventGroupForm({
            'enabled': False,
            'foo': 'fldsjhfdsff',
            'title': 32434,
            'event_group_select': 'this is not a valid pk of event group',
            'select_create': 'definitely invalid choice'
        })
        self.assertEquals(form.is_valid(), {}, "if enabled is set the form should accept anything")

    def test_all_fields_blanked(self):
        return
        data = {
            'description': u'',
            'title': u'',
            'location': u'',
            'department_suggest': u'',
            'start': u'',
            'topics': u'',
            'speaker_suggest': u'',
            'location_suggest': u'',
            'department_organiser': u'',
            'speakers': u'',
            'topic_suggest': u'',
            'end': u'',
        }
        form = forms.EventGroupForm(data)
        self.assertEquals(form.is_valid(), False, "blanked form should not validate")
        errors = form.errors.as_data()
        self.assertEquals(len(errors), 2)
        self.assertIn('title', errors)
        self.assertIn('description', errors)




class TestCreateEventView(TestCase):

    def test_get_happy_no_group_id(self):
        response = self.client.get('/events/new')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/create_event.html')
        self.assertContains(response, "Oxford Talks")
        self.assertContains(response, "Add Talk")
        self.assertIn('event_form', response.context)
        self.assertIn('event_group_form', response.context)
        self.assertIn('speaker_form', response.context)

    def test_get_nonexistent_group(self):
        response = self.client.get('/events/groups/8475623/new')
        self.assertEquals(response.status_code, 404)
        self.assertTemplateNotUsed(response, 'events/create_event.html')

    def test_get_happy_for_existing_group(self):
        group = factories.EventGroupFactory.create()
        response = self.client.get('/events/groups/%s/new' % group.pk)
        self.assertEquals(response.status_code, 200)
        self.assertIn('event_group_form', response.context)
        self.assertEquals(response.context['event_group_form']['event_group_select'].value(), group.pk)

    def test_post_valid_save_and_continue_no_group_id(self):
        title = u'cjwnf887y98fw'
        description = u'kfjdnsf'
        data = {
            'event-description ': description,
            'another': u'true',
            'event-title': title,
            'event-location ': u'',
            'event-department_suggest ': u'',
            'email_address ': u'',
            'event-start': u'',
            'event-topics ': u'',
            'event-speaker_suggest ': u'',
            'event-group-description': u'',
            'event-location_suggest ': u'',
            'event-department_organiser ': u'',
            'event-group-event_group_select ': u'',
            'event-speakers ': u'',
            'event-group-group_type ': u'',
            'csrfmiddlewaretoken': u'3kHyJXv0HDO8sJPLlpvQhnBqM04cIJAM',
            'event-group-select_create ': u'CRE',
            'event-topic_suggest': u'',
            'event-end ': u'',
            'event-group-title ': u'',
            'name ': u'',
        }

        response = self.client.post('/events/new', data)
        self.assertRedirects(response, '/events/new')
        count = models.Event.objects.filter(title=title, description=description).count()
        self.assertEquals(count, 1, msg="Event instance was not saved")

    def test_post_valid_save_and_continue_with_group_id(self):
        title = u'cjwnf887y98fw'
        description = u'kfjdnsf'
        group = factories.EventGroupFactory.create()
        group_id = group.pk
        data = {
            'event-description ': description,
            'another': u'true',
            'event-title': title,
            'event-location ': u'',
            'event-department_suggest ': u'',
            'email_address ': u'',
            'event-start': u'',
            'event-topics ': u'',
            'event-speaker_suggest ': u'',
            'event-group-description': u'',
            'event-location_suggest ': u'',
            'event-department_organiser ': u'',
            'event-group-event_group_select ': u'',
            'event-speakers ': u'',
            'event-group-group_type ': u'',
            'csrfmiddlewaretoken': u'3kHyJXv0HDO8sJPLlpvQhnBqM04cIJAM',
            'event-group-select_create ': u'SEL',
            'event-topic_suggest': u'',
            'event-end ': u'',
            'event-group-title ': u'',
            'name ': u'',
        }

        response = self.client.post('/events/groups/%s/new' % group_id, data)
        self.assertRedirects(response, '/events/groups/%s/new' % group_id)
        count = models.Event.objects.filter(title=title, description=description, group_id=group_id).count()
        self.assertEquals(count, 1, msg="Event instance was not saved")

    def test_post_valid(self):
        title = u'cjwnf887y98fw'
        description = u'kfjdnsf'
        data = {
            'event-description ': description,
            'event-title': title,
            'event-location ': u'',
            'event-department_suggest ': u'',
            'email_address ': u'',
            'event-start': u'',
            'event-topics ': u'',
            'event-speaker_suggest ': u'',
            'event-group-description': u'',
            'event-location_suggest ': u'',
            'event-department_organiser ': u'',
            'event-group-event_group_select ': u'',
            'event-speakers ': u'',
            'event-group-group_type ': u'',
            'csrfmiddlewaretoken': u'3kHyJXv0HDO8sJPLlpvQhnBqM04cIJAM',
            'event-group-select_create ': u'CRE',
            'event-topic_suggest': u'',
            'event-end ': u'',
            'event-group-title ': u'',
            'name ': u'',
        }
        response = self.client.post('/events/new', data)
        try:
            event = models.Event.objects.get(title=title, description=description)
        except models.Event.DoesNotExist:
            self.fail("Event instance was not saved")
        self.assertRedirects(response, event.get_absolute_url())
