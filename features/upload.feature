Feature: Upload CSV
  This is testing for upload of CSV files.
  We use Behave: https://behave.readthedocs.io/en/latest/context_attributes.html#user-attributes

  Scenario: Upload good CSV
    Given I upload CSV with the following rows
      | id   | login   | name              | salary  |
      | ID 0 | LOGIN 0 | Comma'd User 0, 1 | 1000.00 |
      | ID 1 | LOGIN 1 | Comma'd User 1, 1 | 2000.00 |
      | ID 2 | LOGIN 2 | Comma'd User 2, 1 | 3000.00 |
      | ID 3 | LOGIN 3 | Comma'd User 3, 1 | 4000.00 |
    Then I get success
    Then I can find uploaded users

  Scenario: Upload same good CSV twice
    Given I upload CSV with the following rows
      | id   | login   | name              | salary  |
      | ID 0 | LOGIN 0 | Comma'd User 0, 1 | 1000.00 |
      | ID 1 | LOGIN 1 | Comma'd User 1, 1 | 2000.00 |
      | ID 2 | LOGIN 2 | Comma'd User 2, 1 | 3000.00 |
      | ID 3 | LOGIN 3 | Comma'd User 3, 1 | 4000.00 |
    Then I get success
    Then I can find uploaded users
    Then I upload the file with different salary
    Then I get success
    Then I can find uploaded users

  Scenario Outline: Upload CSV with wrong number of columns
    Given I upload CSV with <ncols> instead of 4 columns
    Then I get failure
    Examples:
      | ncols |
      | 1 |
      | 2 |
      | 3 |
      | 5 |

  Scenario: Upload CSV with comments
    Given I upload CSV with the following text
        """
        id,name,login,salary
        # Good file with comments
        id 0,login 0,Ron Weasley,19234.5
        id 1,login 1,Ron Weasley the Imposter,19234.6
        """
    Then I get success

    Scenario: Upload CSV with malformed salary
      Given I upload CSV with the following text
        """
        id,name,login,salary
        # Bad file
        id 0,login 0,Ron Weasley,19234.5
        id 1,login 1,Ron Weasley,19234.5ab
        """
      Then I get failure

