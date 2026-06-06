Feature: Master Data Management

  Scenario: Edit and verify item description from MDM task

    Given user is authenticated for MDM

    When user opens view modify records from control panel

    And user edits the item description online

    Then the updated item description should be visible in task status

  Scenario: Edit configuration code and validate that it can't be editable

    Given user is authenticated for MDM

    When user opens view modify records from control panel

    And user edit the configuration code and save

    Then the error message of invalid request should come