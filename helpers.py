from typing import List, Tuple

from models import Roles, SkillMembers, Team


def form_teams(skill_members: List[SkillMembers]) -> Tuple[List[Team], Team]:
    '''
        Form teams with experienced members first to satisfy the team formation condition
        @param skill_members: List of SkillMembers
        @return: Tuple of list of teams that can be formed and list of members that can't be part of a team
    '''
    sales, marketing, engineers = [members for members in skill_members]
    teams = []
    non_team_members = []
    
    while len(engineers.elder_members)> 0:
        members = [engineers.elder_members.pop()]

        # Add members to the Team
        if len(marketing.younger_members) > 0:
            members.append(marketing.younger_members.pop())
        elif len(marketing.elder_members) > 0:
            members.append(marketing.elder_members.pop())
        
        if len(sales.younger_members) > 0:
            members.append(sales.younger_members.pop())
        elif len(sales.elder_members) > 0:
            members.append(sales.elder_members.pop())
        
        # Check if the team obtained is valid
        if len(members) == 3:
            teams.append(Team(members=members))
        else:
            non_team_members += members
    
    while len(marketing.elder_members)> 0:
        members = [marketing.elder_members.pop()]
        if len(engineers.younger_members) > 0:
            members.append(engineers.younger_members.pop())
        
        if len(sales.younger_members) > 0:
            members.append(sales.younger_members.pop())
        elif len(sales.elder_members) > 0:
            members.append(sales.elder_members.pop())
        
        if len(members) == 3:
            teams.append(Team(members=members))
        else:
            non_team_members += members

    while len(sales.elder_members)> 0:
        members = [sales.elder_members.pop()]
        if len(marketing.younger_members) > 0:
            members.append(marketing.younger_members.pop())
        
        if len(engineers.younger_members) > 0:
            members.append(engineers.younger_members.pop())
        
        if len(members) == 3:
            teams.append(Team(members=members))
        else:
            non_team_members += members
    
    non_team_members += engineers.younger_members + marketing.younger_members + sales.younger_members

    return teams, non_team_members
