Feature: Sales Clearance Portal

  Scenario: Verify that a saved sales order line is visible in Design

    Given user is authenticated for Sales

    When user opens the sales clearance portal and save

    Then the saved sales order line should be visible in Design


  