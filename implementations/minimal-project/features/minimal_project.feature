Feature: Minimal Project

  Scenario: Check a java client (plantuml)
    Given MIT Plantuml is downloaded
    When run Plantuml client with `-author` argument
    Then success command output match regexp
    """
    PlantUML version .+ \(.+\)\n\(MIT source distribution\)\n
    """

  Scenario: Check spring-boot-hello-world
    Given spring-boot-hello-world server is up
    When fetch root hello-world endpoint
    Then get http 200:Success code
    And requests response content match regexp
     """
     ^Hello World v.+ \[.+\]$
     """
