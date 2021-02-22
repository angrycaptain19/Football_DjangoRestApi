from rest_framework import serializers
from .models import Player, Manager, Club


class PlayerSerializer(serializers.ModelSerializer):

    manager = serializers.SerializerMethodField('get_manager')
    club = serializers.SerializerMethodField('get_club')

    class Meta:
        model = Player
        fields = ['player_id', 'first_name', 'last_name', 'birth_date',
                  'best_position', 'manager', 'club', 'last_modified']

    def get_manager(self, player):
        return player.manager_id.__str__()

    def get_club(self, player):
        return player.club_id.__str__()


class PlayerCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = '__all__'

    def save(self):
        try:
            first_name = self.validated_data['first_name']
            last_name = self.validated_data['last_name']
            birth_date = self.validated_data['birth_date']
            best_position = self.validated_data['best_position']
            manager_id = self.validated_data['manager_id']
            club_id = self.validated_data['club_id']

            player = Player(
                first_name=first_name,
                last_name=last_name,
                birth_date=birth_date,
                best_position=best_position,
                manager_id=manager_id,
                club_id=club_id,
            )

            player.save()
            return player
        except KeyError:
            raise serializers.ValidationError({"response": "Data is not valid."})


class PlayerUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = '__all__'

    def validate(self, player):

        try:
            if Manager.objects.get(manager_id=player['manager_id']).DoesNotExist:
                raise serializers.ValidationError({"response": "That manager does not exist"})

            if Club.objects.get(club_id=player['club_id']).DoesNotExist:
                raise serializers.ValidationError({"response": "That club does not exist"})
        except KeyError:
            pass

        return player
