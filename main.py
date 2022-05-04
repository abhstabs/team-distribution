import json
import sys
from functools import partial
from typing import List, Tuple

from helpers import form_teams_with_experience, form_teams_with_limiting_skill
from models import (Member, Roles, SkillMembers, Team, get_members_by_age,
                    get_members_for_city)

EXPERIENCE = "Experience"

# data_set = json.loads(open("data.json", "r").read())

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
    
    limiting_skill = find_the_limiting_skill(skill_members)
    if limiting_skill == EXPERIENCE:
        # if the limiting skill is experience, then form teams with experienced members on priority
        return form_teams_with_experience(skill_members)
    
    # if the limiting skill is not experience, then form teams with members with the limiting skill on priority
    return form_teams_with_limiting_skill(skill_members, limiting_skill)

        
def find_the_limiting_skill(skill_members: List[SkillMembers]) -> str:
    '''
        Find the limiting skill from the list of SkillMembers (Members distributed on their skills and experience)
        @param skill_members: List of SkillMembers
        @return: The limiting skill
    '''
    skill_count = {role : 0 for role in Roles}
    skill_count[EXPERIENCE] = 0
    for skill_member in skill_members:
        skill_count[skill_member.role] += skill_member.total_members
        skill_count[EXPERIENCE] += len(skill_member.elder_members)

    limiting_skill_count = 100_000_000_000 #initialize with a large number
    limiting_skill = None

    # finding the limiting skill
    for skill in skill_count: 
      if skill_count[skill] < limiting_skill_count:
        limiting_skill_count = skill_count[skill]
        limiting_skill = skill
    return limiting_skill



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
