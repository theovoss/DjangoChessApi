import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

# from myproject.apps.core.models import Account
from DjangoChessApi.Chess.models import GameType


@pytest.mark.django_db
class ConfigurationTests(APITestCase):
    def test_get_movements(self):
        url = reverse('movements-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 4)
        print(response)
        print(response.data)
        self.assertContains(response, "ends_on_enemy")
        self.assertContains(response, "directional")
        self.assertContains(response, "distance_of_one")
        self.assertContains(response, "doesnt_land_on_own_piece")

    def test_get_directions(self):
        url = reverse('directions-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 4)
        self.assertContains(response, "vertical")
        self.assertContains(response, "horizontal")
        self.assertContains(response, "diagonal")
        self.assertContains(response, "L")

    def test_get_capture_actions(self):
        url = reverse('capture-actions-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 2)
        self.assertContains(response, "explode")
        self.assertContains(response, "captures_destination")
        self.assertContains(response, "becomes_piece")

    def test_get_standard_chess_pieces(self):
        url = reverse('standard-chess-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('pieces', response.data)
        self.assertIn('queen', response.data['pieces'])
        self.assertIn('pawn', response.data['pieces'])
        self.assertIn('bishop', response.data['pieces'])
        self.assertIn('rook', response.data['pieces'])
        self.assertIn('king', response.data['pieces'])

    def test_post_directions_success(self):
        game_type = GameType(name="name", description="description")
        game_type.save()
        pk = game_type.id

        key = 'directions'
        expected = ['vertical', 'horizontal']
        data = {'piece': 'king', 'index': '0', 'key': key, 'value': expected}

        url = reverse('chess-configuration-checkmark', args=[game_type.id])
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 200)

        game_type = GameType.objects.get(pk=pk)
        self.assertEqual(game_type.rules['pieces']['king']['moves'][0][key], expected)

        game_type.delete()

    def test_post_directions_success_when_rules_is_empty(self):
        game_type = GameType(name="name", description="description", rules={})
        game_type.save()
        pk = game_type.id

        self.assertEqual(game_type.rules, {})

        key = 'directions'
        expected = ['vertical', 'horizontal']
        data = {'piece': 'king', 'index': '0', 'key': key, 'value': expected}

        url = reverse('chess-configuration-checkmark', args=[game_type.id])
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 200)

        game_type = GameType.objects.get(pk=pk)
        self.assertEqual(game_type.rules['pieces']['king']['moves'][0][key], expected)

        game_type.delete()

    def test_post_conditions_success(self):
        game_type = GameType(name="name", description="conditions")
        game_type.save()
        pk = game_type.id

        key = 'conditions'
        expected = ['doesnt_land_on_piece', 'directional', 'cant_jump_pieces']
        data = {'piece': 'king', 'index': '0', 'key': key, 'value': expected}

        url = reverse('chess-configuration-checkmark', args=[game_type.id])
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 200)

        game_type = GameType.objects.get(pk=pk)
        self.assertEqual(game_type.rules['pieces']['king']['moves'][0][key], expected)

        game_type.delete()

    def test_post_capture_actions_success(self):
        game_type = GameType(name="name", description="conditions")
        game_type.save()
        pk = game_type.id

        key = 'capture_actions'
        expected = ['becomes_piece', 'explode', 'captures_destination']
        data = {'piece': 'king', 'index': '0', 'key': key, 'value': expected}

        url = reverse('chess-configuration-checkmark', args=[game_type.id])
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 200)

        game_type = GameType.objects.get(pk=pk)
        self.assertEqual(game_type.rules['pieces']['king']['moves'][0][key], expected)

        game_type.delete()

    def test_post_post_move_action_success(self):
        game_type = GameType(name="name", description="conditions")
        game_type.save()
        pk = game_type.id

        key = 'post_move_actions'
        expected = ['increment_move_count', 'promotable']
        data = {'piece': 'king', 'index': '0', 'key': key, 'value': expected}

        url = reverse('chess-configuration-checkmark', args=[game_type.id])
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 200)

        game_type = GameType.objects.get(pk=pk)
        self.assertEqual(game_type.rules['pieces']['king']['moves'][0][key], expected)

        game_type.delete()

    def test_post_limits_directions(self):
        game_type = GameType(name="name", description="description")
        game_type.save()
        pk = game_type.id

        data = {
            'piece': 'king',
            'index': '0',
            'key': 'directions',
            'value': ['thor', 'horizontal'],
        }

        url = reverse('chess-configuration-checkmark', args=[game_type.id])
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 400)

        game_type = GameType.objects.get(pk=pk)
        game_type.delete()

    def test_post_limits_conditions(self):
        game_type = GameType(name="name", description="description")
        game_type.save()
        pk = game_type.id

        data = {'piece': 'king', 'index': '0', 'key': 'conditions', 'value': ['thor']}

        url = reverse('chess-configuration-checkmark', args=[game_type.id])
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 400)

        game_type = GameType.objects.get(pk=pk)
        game_type.delete()

    def test_post_limits_capture_actions(self):
        game_type = GameType(name="name", description="description")
        game_type.save()
        pk = game_type.id

        data = {
            'piece': 'king',
            'index': '0',
            'key': 'capture_actions',
            'value': ['thor'],
        }

        url = reverse('chess-configuration-checkmark', args=[game_type.id])
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 400)

        game_type = GameType.objects.get(pk=pk)
        game_type.delete()

    def test_post_limits_post_move_actions(self):
        game_type = GameType(name="name", description="description")
        game_type.save()
        pk = game_type.id

        data = {
            'piece': 'king',
            'index': '0',
            'key': 'post_move_actions',
            'value': ['thor'],
        }

        url = reverse('chess-configuration-checkmark', args=[game_type.id])
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 400)

        game_type = GameType.objects.get(pk=pk)
        game_type.delete()

    def test_post_limits_unsupported_key(self):
        game_type = GameType(name="name", description="description")
        game_type.save()
        pk = game_type.id

        data = {
            'piece': 'king',
            'index': '0',
            'key': 'unsupported_key',
            'value': ['thor'],
        }

        url = reverse('chess-configuration-checkmark', args=[game_type.id])
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 400)

        game_type = GameType.objects.get(pk=pk)
        game_type.delete()
