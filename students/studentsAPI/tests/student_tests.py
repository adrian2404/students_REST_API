from rest_framework import status
from rest_framework.test import APITestCase
from studentsAPI.models.groups import Group
from django.core.urlresolvers import reverse
from studentsAPI.models.students import Student
from studentsAPI.serializers import GroupSerializer, StudentSerializer


class CreateStudentTest(APITestCase):
    def setUp(self):
        self.data = {'first_name': 'Adrian',
                     'last_name': 'Yavorski', 'ticket': 123}

    def test_can_create_student(self):
        """
        Ensure we can create a new student object.
        """
        response = self.client.post(reverse('students-list'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_can_not_create_student(self):
        """
        Tests creation with invalid parameters.
        """
        self.data = {'first_name': 'Adrian', 'last_name': 'Yavorski'}
        response = self.client.post(reverse('students-list'), self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ReadStudentTest(APITestCase):
    def setUp(self):
        self.group = Group.objects.create(title='TestGroup', notes='Blabla')
        self.student = Student.objects.create(
            first_name='Adrian', last_name='Yavorski', ticket=12312)
        Student.objects.create(
            first_name='Andri', last_name='Pirat', ticket=122,
            student_group=self.group)
        Student.objects.create(
            first_name='Ben', last_name='Big', ticket=1212,
            student_group=self.group)

    def test_can_read_students_list(self):
        """
        Tests if list of students is received.
        """
        response = self.client.get(reverse('students-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_read_student_detail(self):
        """
        Tests if we can get info about specific student.
        """
        response = self.client.get(
            reverse('students-detail', args=[self.student.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_not_read_student_detail(self):
        """
        Tests reading info of unexisting student.
        """
        response = self.client.get(reverse('students-detail', args=[2]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_filter_students(self):
        """
        Test for student's filtering.
        """
        response = self.client.get('/students?group={}'.format(self.group.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UpdateStudentTest(APITestCase):
    def setUp(self):
        self.group = Group.objects.create(
            title='TestGroup', leader=None, notes='Blabla')
        self.student = Student.objects.create(
            first_name='Adrian', last_name='Yavorski', ticket=12312,
            student_group=self.group)
        self.data = StudentSerializer(self.student).data
        self.data.update({'first_name': 'Andrii', 'birthday': '1992-12-12'})

    def test_can_update_student(self):
        """
        Tests whether a student info is updated.
        """
        response = self.client.put(
            reverse('students-detail', args=[self.student.id]), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_not_update_student(self):
        """
        Tests whether a student info is updated.
        """
        self.data.update({'first_name': ''})
        response = self.client.put(
            reverse('students-detail', args=[self.student.id]), self.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteStudentTest(APITestCase):
    def setUp(self):
        self.student = Student.objects.create(
            first_name='Adrian', last_name='Yavorski', ticket=12312)

    def test_can_delete_student(self):
        """
        Testing student's deletion functional.
        """
        response = self.client.delete(
            reverse('students-detail', args=[self.student.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_can_not_delete_student(self):
        """
        Testing student's deletion functional.
        """
        response = self.client.delete(reverse('students-detail', args=[2]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
