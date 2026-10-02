"""Kata04: Data Munging - Weather and Soccer Data Parsing with DRY Fusion

This module implements the Data Munging kata in three parts:
1. Parse weather data to find day with smallest temperature spread
2. Parse soccer data to find team with smallest goal difference
3. DRY Fusion - shared parsing infrastructure

Source: http://codekata.com/kata/kata04-data-munging/
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Protocol, Iterator
from abc import ABC, abstractmethod
import re


# =============================================================================
# Value Objects
# =============================================================================

@dataclass(frozen=True)
class WeatherRecord:
    """Single day's weather data."""
    day: int
    max_temp: int
    min_temp: int
    spread: int
    
    def __str__(self) -> str:
        return f"Day {self.day}: max={self.max_temp}, min={self.min_temp}, spread={self.spread}"


@dataclass(frozen=True)
class SoccerRecord:
    """Single team's soccer data."""
    team: str
    played: int
    won: int
    lost: int
    drawn: int
    goals_for: int
    goals_against: int
    goal_diff: int
    points: int
    
    def __str__(self) -> str:
        return f"{self.team}: GF={self.goals_for}, GA={self.goals_against}, diff={self.goal_diff}"


# =============================================================================
# Repository Interfaces
# =============================================================================

class DataFileRepository(Protocol):
    """Repository for reading data files."""
    
    def read_lines(self, file_path: Path) -> Iterator[str]: ...
    
    def exists(self, file_path: Path) -> bool: ...


class LocalFileRepository:
    """Local filesystem implementation."""
    
    def read_lines(self, file_path: Path) -> Iterator[str]:
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        with file_path.open('r') as f:
            for line in f:
                yield line.rstrip('\n\r')
    
    def exists(self, file_path: Path) -> bool:
        return file_path.exists()


# =============================================================================
# Domain Services - Parsing Logic (DRY Fusion)
# =============================================================================

class ColumnParser:
    """Generic column-based parser for fixed-width or whitespace-delimited files."""
    
    def __init__(self, skip_lines: int = 0, header_pattern: Optional[str] = None):
        self.skip_lines = skip_lines
        self.header_pattern = header_pattern
    
    def parse_lines(self, lines: Iterator[str]) -> Iterator[List[str]]:
        """Parse lines into columns, skipping header/blank lines."""
        line_num = 0
        for line in lines:
            line_num += 1
            if line_num <= self.skip_lines:
                continue
            if not line.strip():
                continue
            if self.header_pattern and re.search(self.header_pattern, line):
                continue
            # Split on whitespace
            cols = line.split()
            if cols:
                yield cols


class WeatherParser:
    """Parser for weather.dat format."""
    
    def __init__(self, parser: Optional[ColumnParser] = None):
        self.parser = parser or ColumnParser(skip_lines=0)
    
    def parse(self, lines: Iterator[str]) -> Iterator[WeatherRecord]:
        for cols in self.parser.parse_lines(lines):
            if len(cols) < 3:
                continue
            try:
                day = int(cols[0])
                max_temp = int(cols[1])
                min_temp = int(cols[2])
                if day <= 0:  # Skip invalid days
                    continue
                spread = max_temp - min_temp
                yield WeatherRecord(day, max_temp, min_temp, spread)
            except (ValueError, IndexError):
                continue


class SoccerParser:
    """Parser for football.dat format."""
    
    def __init__(self, parser: Optional[ColumnParser] = None):
        self.parser = parser or ColumnParser(skip_lines=1, header_pattern=r'^\s*Team')
    
    def parse(self, lines: Iterator[str]) -> Iterator[SoccerRecord]:
        for cols in self.parser.parse_lines(lines):
            if len(cols) < 9:  # Need at least Team, P, W, L, D, GF, GA, GD, Pts
                continue
            try:
                team = cols[0]
                # Skip if it's a header row or totals
                if team.lower() in ('team', 'totals'):
                    continue
                played = int(cols[1])
                won = int(cols[2])
                lost = int(cols[3])
                drawn = int(cols[4])
                goals_for = int(cols[5])
                goals_against = int(cols[6])
                goal_diff = goals_for - goals_against
                points = int(cols[8]) if len(cols) > 8 else won * 3 + drawn
                
                yield SoccerRecord(
                    team=team,
                    played=played,
                    won=won,
                    lost=lost,
                    drawn=drawn,
                    goals_for=goals_for,
                    goals_against=goals_against,
                    goal_diff=goal_diff,
                    points=points
                )
            except (ValueError, IndexError):
                continue


class DataMungingService:
    """Domain service for data munging operations (DRY Fusion)."""
    
    def __init__(self, repository: DataFileRepository):
        self._repository = repository
        self._weather_parser = WeatherParser()
        self._soccer_parser = SoccerParser()
    
    # Part One: Weather
    def find_min_spread_day(self, file_path: Path) -> Optional[WeatherRecord]:
        """Find day with smallest temperature spread."""
        lines = self._repository.read_lines(file_path)
        records = list(self._weather_parser.parse(lines))
        if not records:
            return None
        return min(records, key=lambda r: r.spread)
    
    def get_all_weather(self, file_path: Path) -> List[WeatherRecord]:
        lines = self._repository.read_lines(file_path)
        return list(self._weather_parser.parse(lines))
    
    # Part Two: Soccer
    def find_min_goal_diff_team(self, file_path: Path) -> Optional[SoccerRecord]:
        """Find team with smallest goal difference."""
        lines = self._repository.read_lines(file_path)
        records = list(self._soccer_parser.parse(lines))
        if not records:
            return None
        return min(records, key=lambda r: abs(r.goal_diff))
    
    def get_all_soccer(self, file_path: Path) -> List[SoccerRecord]:
        lines = self._repository.read_lines(file_path)
        return list(self._soccer_parser.parse(lines))
    
    # Part Three: DRY Fusion - Shared functionality
    def find_min_spread_generic(self, file_path: Path, 
                                 parser,
                                 key_func) -> Optional[object]:
        """Generic min-finding function (DRY principle)."""
        lines = self._repository.read_lines(file_path)
        records = list(parser.parse(lines))
        if not records:
            return None
        return min(records, key=key_func)


# =============================================================================
# Commands (CQRS)
# =============================================================================

@dataclass
class ParseWeatherCommand:
    file_path: Path


@dataclass
class ParseSoccerCommand:
    file_path: Path


class DataMungingCommandHandler:
    """Command handler for data munging operations."""
    
    def __init__(self, service: DataMungingService):
        self._service = service
    
    def handle_weather(self, cmd: ParseWeatherCommand) -> Optional[WeatherRecord]:
        return self._service.find_min_spread_day(cmd.file_path)
    
    def handle_soccer(self, cmd: ParseSoccerCommand) -> Optional[SoccerRecord]:
        return self._service.find_min_goal_diff_team(cmd.file_path)


# =============================================================================
# Queries (CQRS)
# =============================================================================

@dataclass
class WeatherQuery:
    file_path: Path


@dataclass
class SoccerQuery:
    file_path: Path


@dataclass
class DataMungingResult:
    weather: Optional[WeatherRecord] = None
    soccer: Optional[SoccerRecord] = None


class DataMungingQueryHandler:
    """Query handler for data munging."""
    
    def __init__(self, service: DataMungingService):
        self._service = service
    
    def handle_weather(self, query: WeatherQuery) -> Optional[WeatherRecord]:
        return self._service.find_min_spread_day(query.file_path)
    
    def handle_soccer(self, query: SoccerQuery) -> Optional[SoccerRecord]:
        return self._service.find_min_goal_diff_team(query.file_path)
    
    def handle_all(self, weather_path: Path, soccer_path: Path) -> DataMungingResult:
        return DataMungingResult(
            weather=self._service.find_min_spread_day(weather_path),
            soccer=self._service.find_min_goal_diff_team(soccer_path)
        )


# =============================================================================
# Facade
# =============================================================================

class DataMunging:
    """Main facade for data munging operations."""
    
    def __init__(self, repository: Optional[DataFileRepository] = None):
        self._repository = repository or LocalFileRepository()
        self._service = DataMungingService(self._repository)
        self._command_handler = DataMungingCommandHandler(self._service)
        self._query_handler = DataMungingQueryHandler(self._service)
    
    # Part One
    def find_min_spread_day(self, file_path: Path) -> Optional[int]:
        """Find day with smallest temperature spread. Returns day number."""
        record = self._service.find_min_spread_day(file_path)
        return record.day if record else None
    
    def get_weather_record(self, file_path: Path) -> Optional[WeatherRecord]:
        return self._service.find_min_spread_day(file_path)
    
    # Part Two
    def find_min_goal_diff_team(self, file_path: Path) -> Optional[str]:
        """Find team with smallest goal difference. Returns team name."""
        record = self._service.find_min_goal_diff_team(file_path)
        return record.team if record else None
    
    def get_soccer_record(self, file_path: Path) -> Optional[SoccerRecord]:
        return self._service.find_min_goal_diff_team(file_path)
    
    # Part Three - DRY Fusion
    def find_min_generic(self, file_path: Path, parser, key_func) -> Optional[object]:
        """Generic min-finding (DRY Fusion)."""
        return self._service.find_min_spread_generic(file_path, parser, key_func)
    
    # Full analysis
    def analyze(self, weather_path: Path, soccer_path: Path) -> DataMungingResult:
        return self._query_handler.handle_all(weather_path, soccer_path)


# =============================================================================
# Functional Alternative
# =============================================================================

def find_min_spread_day(weather_data: str) -> int:
    """Functional interface: parse weather data string, return day with min spread."""
    lines = weather_data.strip().split('\n')
    parser = WeatherParser()
    records = list(parser.parse(iter(lines)))
    if not records:
        return -1
    return min(records, key=lambda r: r.spread).day


def find_min_goal_diff_team(soccer_data: str) -> str:
    """Functional interface: parse soccer data string, return team with min goal diff."""
    lines = soccer_data.strip().split('\n')
    parser = SoccerParser()
    records = list(parser.parse(iter(lines)))
    if not records:
        return ""
    return min(records, key=lambda r: abs(r.goal_diff)).team


def parse_weather_data(data: str) -> List[WeatherRecord]:
    """Parse weather data string into records."""
    parser = WeatherParser()
    return list(parser.parse(iter(data.strip().split('\n'))))


def parse_soccer_data(data: str) -> List[SoccerRecord]:
    """Parse soccer data string into records."""
    parser = SoccerParser()
    return list(parser.parse(iter(data.strip().split('\n'))))


# =============================================================================
# Sample Data for Testing
# =============================================================================

SAMPLE_WEATHER = """ 1  88  59  74  53.8  0.00  280  9.6  270  17  1.6  93  23  1004.5
 2  79  63  71  46.5  0.00  330  8.7  340  23  3.3  70  28  1004.5
 3  77  55  66  49.5  0.00  290  5.6  300  13  2.1  80  25  1004.5
 4  77  59  68  51.5  0.00  300  7.2  310  15  1.8  85  26  1004.5
 5  90  66  78  55.5  0.00  280  8.2  290  18  2.2  95  28  1004.5
 6  81  61  71  49.0  0.00  290  9.1  300  20  1.9  90  27  1004.5
 7  73  57  65  48.0  0.00  280  6.5  290  22  2.0  88  26  1004.5
 8  69  55  62  47.5  0.00  290  4.3  280  24  1.7  82  25  1004.5
 9  82  60  71  52.0  0.00  300  11.2 310  25  1.5  92  27  1004.5
10  85  62  74  54.5  0.00  310  13.1 320  27  1.4  95  28  1004.5
11  88  65  76  56.0  0.00  300  9.8  300  29  1.3  98  29  1004.5
12  90  68  79  57.5  0.00  290  8.7  290  31  1.2  99  30  1004.5
13  92  69  80  58.0  0.00  280  7.6  280  33  1.1  100 31  1004.5
14  95  70  82  59.5  0.00  270  6.5  270  35  1.0  102 32  1004.5
15  97  72  84  60.5  0.00  280  5.4  280  37  0.9  105 33  1004.5
16  99  74  86  61.5  0.00  290  4.3  290  39  0.8  108 34  1004.5
17  98  75  86  61.0  0.00  280  3.2  280  41  0.7  110 35  1004.5
18  95  73  84  59.0  0.00  270  2.1  270  43  0.6  112 36  1004.5
19  93  71  82  57.0  0.00  280  1.0  280  45  0.5  115 37  1004.5
20  90  68  79  55.5  0.00  290  0.0  290  47  0.4  118 38  1004.5
21  88  65  76  53.5  0.00  280  0.0  280  49  0.3  120 39  1004.5
22  85  63  74  51.5  0.00  270  0.0  270  51  0.2  122 40  1004.5
23  82  61  71  49.5  0.00  280  0.0  280  53  0.1  125 41  1004.5
24  80  59  69  47.5  0.00  290  0.0  290  55  0.0  128 42  1004.5
25  78  57  67  45.5  0.00  280  0.0  280  57  0.0  130 43  1004.5
26  76  55  65  43.5  0.00  270  0.0  270  59  0.0  132 44  1004.5
27  74  53  63  41.5  0.00  280  0.0  280  61  0.0  135 45  1004.5
28  72  51  61  39.5  0.00  270  0.0  270  63  0.0  138 46  1004.5
29  70  49  59  37.5  0.00  280  0.0  280  65  0.0  140 47  1004.5
30  68  47  57  35.5  0.00  290  0.0  290  67  0.0  142 48  1004.5"""

SAMPLE_SOCCER = """                            F     A
Team            P   W   L   D  GF  GA  GD  Pts
Arsenal        38  26   9   3  79  36  43   87
Liverpool      38  24   8   6  67  30  37   80
Manchester_Utd 38  24   5   7  87  45  42   79
Newcastle      38  21   8   9  74  52  22   71
Leeds          38  18  12   8  53  37  16   66
Chelsea        38  17  13   8  66  41  25   59
West_Ham       38  15   8  15  48  57  -9   53
Aston_Villa    38  12  14  12  46  47  -1   48
Sunderland     38  10  10  18  29  51  -22  40
Middlesbrough  38   9  11  18  35  54  -19  38
Fulham         38   8  15  15  35  49  -14  39
Charlton       38   8  15  15  31  46  -15  39
Everton        38   7  14  17  30  50  -20  35
Bolton         38   6  15  17  28  51  -23  33
Blackburn      38   7  13  18  34  55  -21  34
Southampton    38   6  13  19  32  50  -18  31
Tottenham      38   6  14  18  30  48  -18  30
Leicester      38   5  15  18  28  58  -30  23
Ipswich        38   4  16  18  24  56  -32  20
Derby          38   1  20  17  18  71  -53  10"""

if __name__ == "__main__":
    print("=== Kata04: Data Munging - Demo ===\n")
    
    # Parse sample data
    weather_records = parse_weather_data(SAMPLE_WEATHER)
    soccer_records = parse_soccer_data(SAMPLE_SOCCER)
    
    # Part One: Min spread day
    min_spread = min(weather_records, key=lambda r: r.spread)
    print(f"Part One - Min Spread Day: {min_spread.day} (spread: {min_spread.spread})")
    
    # Part Two: Min goal diff team
    min_goal_diff = min(soccer_records, key=lambda r: abs(r.goal_diff))
    print(f"Part Two - Min Goal Diff Team: {min_goal_diff.team} (diff: {min_goal_diff.goal_diff})")
    
    # Part Three: DRY Fusion - generic finder
    from kata04_data_munging import DataMunging, LocalFileRepository
    from pathlib import Path
    
    # Using generic finder (DRY Fusion)
    dm = DataMunging()
    # We can't run file-based without actual files, but the DRY function works:
    # min_spread_generic = dm.find_min_generic(weather_path, weather_parser, lambda r: r.spread)
    # min_goal_generic = dm.find_min_generic(soccer_path, soccer_parser, lambda r: abs(r.goal_diff))
    
    print("\n=== Kata Questions ===")
    print("1. Design decisions impact DRY: Using shared ColumnParser made fusion easy")
    print("2. Second program influenced by first: Yes, recognized common parsing pattern")
    print("3. DRY not always good: Over-abstraction can hurt readability if domains differ significantly")