from typing import List, Tuple

from models import Roles, SkillMembers, Team


def form_teams_with_experience(skill_members: List[SkillMembers]) -> Tuple[List[Team], Team]:
    '''
        Form teams with experienced members first since experienced members are limiting factor
        @param skill_members: List of SkillMembers
        @return: Tuple of list of teams that can be formed and list of members that can't be part of a team
    '''
    sales, marketing, engineers = [members for members in skill_members]
    teams = []
    non_team_members = []

    while len(engineers.elder_members)> 0:
      members = [engineers.elder_members.pop(), marketing.younger_members.pop(), sales.younger_members.pop()]
      teams.append(Team(members=members))
    
    while len(marketing.elder_members)> 0:
      members = [marketing.elder_members.pop(), sales.younger_members.pop(), engineers.younger_members.pop()]
      teams.append(Team(members=members))
    
    while len(sales.elder_members)> 0:
      members = [sales.elder_members.pop(), engineers.younger_members.pop(), marketing.younger_members.pop()]
      teams.append(Team(members=members))
    
    # Add remaining members to non_team_members
    non_team_members += sales.younger_members + marketing.younger_members + engineers.younger_members
    
    return teams, non_team_members

def form_teams_with_limiting_skill(skill_members: List[SkillMembers], skill: str) -> Tuple[List[Team], Team]:
    '''
        Form teams with members with the limiting skill first
        @param skill_members: List of SkillMembers
        @param skill: The limiting skill
        @return: Tuple of list of teams that can be formed and list of members that can't be part of a team

        Assign the variables as follows:
        1. limiting_skill: The SkillMembers of the limiting skill
        2. non_limiting_skill_1 : The SkillMembers of the first non-limiting skill
        3. non_limiting_skill_2 : The SkillMembers of the second non-limiting skill
    '''
    sales, marketing, engineers = [members for members in skill_members]
    teams = []
    if skill == Roles.SALES:
        limiting_skill = sales
        non_limiting_skill_1 = marketing
        non_limiting_skill_2 = engineers
    elif skill == Roles.ENGINEER:
        limiting_skill = engineers
        non_limiting_skill_1 = marketing
        non_limiting_skill_2 = sales
    elif skill == Roles.MARKETING:
        limiting_skill = marketing
        non_limiting_skill_1 = engineers
        non_limiting_skill_2 = sales
    else:
        raise Exception("Incorrect Limiting Skill provided")
    

    # Team formation based on the experience of limiting skill members
    while len(limiting_skill.elder_members)> 0:
        members = [limiting_skill.elder_members.pop()]
        if len(non_limiting_skill_1.younger_members) > 0:
            members.append(non_limiting_skill_1.younger_members.pop())
        else:
            members.append(non_limiting_skill_1.elder_members.pop())

        if len(non_limiting_skill_2.younger_members) > 0:
            members.append(non_limiting_skill_2.younger_members.pop())
        else:
            members.append(non_limiting_skill_2.elder_members.pop())
        teams.append(Team(members=members))
    
    # Team formation based on the experience of non-limiting skill members
    # Priority is given to experienced members first from other skills
    while len(limiting_skill.younger_members)> 0:
        members = [limiting_skill.younger_members.pop()]
        if len(non_limiting_skill_1.elder_members) > 0:
            members.append(non_limiting_skill_1.elder_members.pop())
            if len(non_limiting_skill_2.younger_members) > 0:
                members.append(non_limiting_skill_2.younger_members.pop())
            else:
                members.append(non_limiting_skill_2.elder_members.pop())
        else:
            members.append(non_limiting_skill_1.younger_members.pop())
            members.append(non_limiting_skill_2.elder_members.pop())
        teams.append(Team(members=members))

    # Add remaining members to non_team_members
    non_team_members = non_limiting_skill_1.elder_members + non_limiting_skill_1.younger_members + \
                        non_limiting_skill_2.elder_members + non_limiting_skill_2.younger_members
    return teams, non_team_members
        

        

    

