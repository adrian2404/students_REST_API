from rest_framework import status
from rest_framework.test import APITestCase
from studentsAPI.models.groups import Group
from django.core.urlresolvers import reverse
from studentsAPI.models.students import Student
from studentsAPI.serializers import GroupSerializer, StudentSerializer


class CreateGroupTest(APITestCase):
    def setUp(self):
        self.student = Student.objects.create(first_name='Adrian',
                                              last_name='Yavorski',
                                              ticket=12312)
        self.data = {'title': 'TestGroup', 'leader': 1, 'notes': 'Blabla'}

    def test_can_create_group(self):
        """
        Ensure we can or can not create a new group object.
        """
        response = self.client.post(reverse('groups-list'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.data['title'] = ''
        response = self.client.post(reverse('groups-list'), self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ReadGroupTest(APITestCase):
    def setUp(self):
        self.student = Student.objects.create(
            first_name='Adrian', last_name='Yavorski', ticket=12312)
        self.group = Group.objects.create(
            title='TestGroup1', leader=self.student, notes='Blabla')
        Group.objects.create(title='TestGroup2', leader=None, notes='Blabla')
        Group.objects.create(title='TestGroup3', leader=None, notes='Blabla')

    def test_can_read_groups_list(self):
        """
        Tests if list of groups is received.
        """
        response = self.client.get(reverse('groups-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_read_group_detail(self):
        """
        Tests if we can get info about specific group.
        """
        response = self.client.get(
            reverse('groups-detail', args=[self.group.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_not_read_group_detail(self):
        """
        Tests to get group info for unexisting group.
        """
        response = self.client.get(reverse('groups-detail', args=[2]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateGroupTest(APITestCase):
    def setUp(self):
        self.group = Group.objects.create(
            title='TestGroup', leader=None, notes='Blabla')
        self.data = GroupSerializer(self.group).data
        self.data.update({'title': 'NewGroup', 'leader': ''})

    def test_can_update_group(self):
        """
        Tests if we can successfuly update group info.
        """
        response = self.client.put(
            reverse('groups-detail', args=[self.group.id]), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_not_update_group(self):
        """
        Tests if we can get info about specific group.
        """
        self.student = Student.objects.create(
            first_name='Adrian', last_name='Yavorski',
            ticket=12312, student_group=self.group)
        self.group = Group.objects.create(
            title='TestGroup', leader=self.student, notes='Blabla')
        self.data = GroupSerializer(self.group).data
        self.data.update({'title': 'NewGroup1'})
        response = self.client.put(
            reverse('groups-detail', args=[self.group.id]), self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteGroupTest(APITestCase):
    def setUp(self):
        self.group = Group.objects.create(
            title='TestGroup', leader=None, notes='Blabla')

    def test_can_delete_group(self):
        """
        Testing group deletion functional.
        """
        response = self.client.delete(
            reverse('groups-detail', args=[self.group.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_can_not_delete_group(self):
        """
        Testing deletion of group with students in it.
        """
        self.student = Student.objects.create(
            first_name='Adrian', last_name='Yavorski',
            ticket=12312, student_group=self.group)
        response = self.client.delete(
            reverse('groups-detail', args=[self.group.id]))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
