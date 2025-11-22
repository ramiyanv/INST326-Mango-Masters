import re

def parse_game(line):
    """
    TODO: Implement this function.
    Instructions:
    1. Each line in the NBA results text file looks like this:
    Oklahoma City Thunder 125 - 124 Houston Rockets (Paycom Center, October 21,
    2025)
    2. Use a regular expression (regex) to extract the following six groups:
    - team1: the first team's name
    - score1: the first team's score (integer)
    - score2: the second team's score (integer)
    - team2: the second team's name
    - location: the arena name
    - date: the full date (e.g., "October 21, 2025")
    3. Return a dictionary with those six keys and their values.
    Example:
    {
    "team1": "Oklahoma City Thunder",
    "score1": 125,
    "score2": 124,
    "team2": "Houston Rockets",
    "location": "Paycom Center",
    "date": "October 21, 2025"
    }
    4. If you can't parse the line correctly, raise an appropriate exception.
    """
    pattern = r'^(.*?)\s+(\d+)\s*-\s*(\d+)\s+(.*?)\s+\((.*?),\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})\)$'
    match = re.match(pattern, line)

    if not match:
        raise ValueError(f"Could not parse line: {line}")

    team1, score1, score2, team2, location, date = match.groups()

    return {
        "team1": team1.strip(),
        "score1": int(score1),
        "score2": int(score2),
        "team2": team2.strip(),
        "location": location.strip(),
        "date": date.strip()
    }


def load_games(filename):
    games = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            games.append(parse_game(line))
    return games
