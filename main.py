import json
import sys
from functools import partial
from typing import List, Tuple

from helpers import form_teams
from models import (Member, Roles, SkillMembers, Team, get_members_by_age,
                    get_members_for_city)

EXPERIENCE = "Experience"


def create_members_from_dataset(data_set: List) -> List[Member]:
    '''
        Create Member objects from the representation in input
        @param data_set: List of dictionaries (json) each representing a member
        @return: List of Member objects
    '''
    return [Member(**member) for member in data_set]

def get_teams(data_set: List[Member]) -> Tuple[List[Team], Team]:
    '''
        Create teams from the input data
        @param data_set: List of Member objects
        @return: Tuple of List[Team], the possible teams that can be formed and the members 
              that can not be part of any team
    '''
    locations = set([member.location for member in data_set])
    teams = []
    non_team_members = []
    for location in locations:
        members = get_members_for_city(data_set, location)
        location_teams, location_non_team_members = form_teams_for_location(members)
        teams.extend(location_teams)
        non_team_members.extend(location_non_team_members)
    
    return teams, non_team_members


def form_teams_for_location(members: List[Member]) -> List[Team]:
    '''
        Create teams for a given location. Team formation for a location is independent of other locations.
        @param members: List of Member objects
        @return: List of Teams

        Algorithm:
        1. Create a list of Members for each role separated by the age/experience
        2. Find the limiting skill for the location and form teams with that limiting skill given first preference
        3. While picking other team members, keep the conditions of team formation satisfied
    '''
    skill_members = []
    functions = [partial(get_members_by_age, role) for role in Roles]  # Using partial functions for extensibility
    for function in functions:
        elder, younger = function(members)
        skill_members.append(SkillMembers(role = function.args[0], elder_members = elder, younger_members = younger))
    
    return form_teams(skill_members)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <data_file.json>")
        sys.exit(1)
    elif len(sys.argv) > 2:
      raise Exception("Invalid number of arguments")

    data_file = sys.argv[1]
    with open(data_file, "r") as data_file:
        data_set = json.loads(data_file.read())
    members = create_members_from_dataset(data_set)
    teams, non_team_members = get_teams(members)
    
    print(f"Teams formed: {teams} \n\n")
    print(f"Non team members: {non_team_members}")
