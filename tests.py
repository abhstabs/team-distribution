import json
import unittest

from main import create_members_from_dataset, get_teams


class TestTeamFormationScript(unittest.TestCase):
    def test_data_load(self):
        '''
            Test data load works properly
        '''
        with open('test_data/test_data_load.json') as data_file:
            data_set = json.load(data_file)
            result = create_members_from_dataset(data_set)
            self.assertEqual(len(result), 2)
    
    def test_limiting_skill_experience(self):
        '''
            Test algorithm with limiting skill experience
        '''

        with open('test_data/test_limited_experience.json') as data_file:
            data_set = json.load(data_file)
            members = create_members_from_dataset(data_set)
            teams, non_team_members = get_teams(members)
            self.assertEqual(len(teams), 1)
            self.assertEqual(len(non_team_members), 3)
    
    def test_all_skills_equal(self):
        '''
            Test algorithm will all skills in equal numbers
        '''

        with open('test_data/test_all_skills_equal.json') as data_file:
            data_set = json.load(data_file)
            members = create_members_from_dataset(data_set)
            teams, non_team_members = get_teams(members)
            self.assertEqual(len(teams), 2)
            self.assertEqual(len(non_team_members), 0)
    
    def test_all_experienced(self):
        '''
            Test algorithm with everyone having desired experience
        '''
        with open('test_data/test_all_experienced.json') as data_file:
            data_set = json.load(data_file)
            members = create_members_from_dataset(data_set)
            teams, non_team_members = get_teams(members)
            self.assertEqual(len(teams), 2)
            self.assertEqual(len(non_team_members), 0)
    
    def test_multiple_locations_members(self):
        '''
            Test algorithm with multiple locations 
        '''

        with open('test_data/test_multiple_locations_members.json') as data_file:
            data_set = json.load(data_file)
            members = create_members_from_dataset(data_set)
            teams, non_team_members = get_teams(members)
            self.assertEqual(len(teams), 2)
            self.assertEqual(len(non_team_members), 0)

    def test_no_team_formation_possible(self):
        '''
            Test algorithm with no team formation possible
        '''

        with open('test_data/test_no_team_formation_possible.json') as data_file:
            data_set = json.load(data_file)
            members = create_members_from_dataset(data_set)
            teams, non_team_members = get_teams(members)
            self.assertEqual(len(teams), 0)
            self.assertEqual(len(non_team_members), 6)
    
    def test_multiple_locations_multiple_teams(self):
        '''
            Test algorithm with multiple teams and multiple locations 
        '''
        with open('test_data/test_multiple_locations_multiple_teams.json') as data_file:
            data_set = json.load(data_file)
            members = create_members_from_dataset(data_set)
            teams, non_team_members = get_teams(members)
            self.assertEqual(len(teams), 3)
            self.assertEqual(len(non_team_members), 4)
    
    def test_skewed_skillset_distribution(self):
        '''
            Test algorithm with a skewed skillset distribution 
        '''
        with open('test_data/test_skewed_skillset_distribution.json') as data_file:
            data_set = json.load(data_file)
            members = create_members_from_dataset(data_set)
            teams, non_team_members = get_teams(members)
            self.assertEqual(len(teams), 3)
            self.assertEqual(len(non_team_members), 4)






if __name__ == '__main__':
    unittest.main()
