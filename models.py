from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple

AGE_CRITERIA = 35 # Age criteria for elder and younger members

class Roles(Enum):
    '''
        Possible roles for the members
    '''
    SALES = "Sales"
    MARKETING = "Marketing"
    ENGINEER = "Engineer"

@dataclass
class Member:
    '''
        Class representation of a member
    '''
    name: str
    age: int
    location: str
    Role: str

@dataclass
class Team:
    '''
        Class representation of a team
    '''
    members: List[Member]

@dataclass
class SkillMembers:
    '''
        Class representation of members divided into age groups for a given role
        Used to easily handle the age groups instead of maintaining multiple arrays for each role
    '''
    role: str
    elder_members: List[Member]
    younger_members: List[Member]

    @property
    def total_members(self) -> int:
        '''
            Returns the total number of members for a given role
        '''
        return len(self.elder_members) + len(self.younger_members)


def get_members_for_city(queryset: List[Member], city: str) -> List[Member]:
    '''
        @param queryset: List of members
        @param city: City for which the members are to be returned
        @return List of members for the given city
    '''
    return [member for member in queryset if member.location == city]

def get_members_by_age(role: str, queryset: List[Member]) -> Tuple[List[Member], List[Member]]:
    '''
        @param role: Role for which the members are to be returned
        @param queryset: List of members
        @return Tuple of list of elder and younger members for the given role
    '''
    elder_members = []
    younger_members = []
    for member in queryset:
        if member.Role == role.value:
            if member.age > AGE_CRITERIA:
                elder_members.append(member)
            else:
                younger_members.append(member)
    
    return elder_members, younger_members
