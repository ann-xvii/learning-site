from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone
from courses.models import Course, Step
# Create your tests here.


class CourseModelTests(TestCase):
    """
    our tests all have to start with the word 'test'
    """

    def test_course_creation(self):
        course = Course.objects.create(
            title="Python Regular Expressions",
            description="Learn to write regular expressions in Python"
        )
        now = timezone.now()
        self.assertLess(course.created_at, now)


class StepModelTests(TestCase):
    def test_step_addition_to_course(self):
        course = Course.objects.create(
            title="Otherworldly beings",
            description="George Tsoukalos' hair presents ancient secrets and new lies?"
        )
        step = Step.objects.create(
            title='Photogrammetry and you',
            description="It should be fairly self-explanatory.",
            course=course
        )

        self.assertEqual(course.id, step.course_id)


class StepModelTests2(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title="Python Testing",
            description="Learn to write tests in Python"
        )

    def test_step_creation(self):
        step = Step.objects.create(
            title="Introduction to Doctests",
            description="Learn to write tests in your docstrings.",
            course=self.course
        )

        self.assertIn(step, self.course.step_set.all())


class CourseViewsTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title="Python Testing",
            description="Learn to write tests in Python"
        )

        self.course2 = Course.objects.create(
            title="New Course",
            description="A new course"
        )

        self.step = Step.objects.create(
            title="Introduction to Doctest",
            description="Learn to write tests in your docstrings",
            course=self.course
        )

    def test_course_list_view(self):
        """
        self.client is kind of like a web browser, sends request to url, gives back
        :return:
        """
        resp = self.client.get(reverse('courses:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.course, resp.context['courses'])
        self.assertIn(self.course2, resp.context['courses'])
        self.assertTemplateUsed(resp, 'courses/course_list.html')
        self.assertTemplateUsed(resp, 'layout.html')
        self.assertContains(resp, self.course.title)

    def test_course_detail_view(self):
        resp = self.client.get(reverse('courses:detail',
                                       kwargs={'pk': self.course.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.course, resp.context['course'])
        self.assertTemplateUsed(resp, 'courses/course_detail.html')
        self.assertTemplateUsed(resp, 'layout.html')

    def test_step_detail_view(self):
        resp = self.client.get(reverse('courses:step', kwargs={
                    'course_pk': self.course.pk,
                    'step_pk': self.step.pk
        }))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.step, resp.context['step'])
        self.assertTemplateUsed(resp, 'courses/step_detail.html')
        self.assertTemplateUsed(resp, 'layout.html')


class CourseListViewTestCase(TestCase):
    """
    Tests for the Course list view
    """
    def setUp(self):
        self.course3 = Course.objects.create(
            title="Python Django Reinhardt Appreciation Course 0",
            description="Course 0 is pretty self explanatory."
        )

        for x in range(1,5):
            Course.objects.create(
                title="Python Django Reinhardt Appreciation Course {}".format(x),
                description="Course {} is pretty self explanatory.".format(x)
            )

    def test_new_course_list_view(self):
        resp = self.client.get(reverse('courses:list'))
        self.assertIn(self.course3, resp.context['courses'])
