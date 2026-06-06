Feature: User Management

  Scenario: Create and Verify User

    Given user is authenticated

    When user creates a new user

    And user searches for the created user

    Then the user should be visible in the user management table

  Scenario: New user with duplicate mobile number

    Given user is authenticated

    When user creates a new user with duplicate mobile number

    Then the user creation should fail with duplicate mobile error

  Scenario: New user with duplicate email

    Given user is authenticated

    When user creates a new user with duplicate email

    Then the user creation should fail with duplicate mobile error

