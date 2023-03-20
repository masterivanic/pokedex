from abc import ABC
from abc import abstractmethod


class IPokemonTeam(ABC):
    @abstractmethod
    def get_team_id(self):
        """get team's trainer ids"""
        pass

    @abstractmethod
    def get_teams_info(self, user, id_team: int):
        """get team and pokemon of team"""
        pass

    @abstractmethod
    def assign_pokemon_team(self, user, id_team, id_pokemon):
        """assign a pokemon team of a train"""
        pass

    @abstractmethod
    def remove_pokemon_from_team(self, user, id_team, id_pokemon):
        """remove a pokemon from a trainer team"""
        pass
