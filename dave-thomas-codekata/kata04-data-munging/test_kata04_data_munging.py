"""Tests for Kata04: Data Munging - Weather and Soccer Data Parsing."""

import pytest
from pathlib import Path
from kata04_data_munging import (
    DataMunging,
    find_min_spread_day,
    find_min_goal_diff_team,
    parse_weather_data,
    parse_soccer_data,
    WeatherRecord,
    SoccerRecord,
    WeatherParser,
    SoccerParser,
    ColumnParser,
    LocalFileRepository,
    DataMungingService,
)


class TestDataMunging:
    """Test cases for Kata04: Data Munging."""

    def setup_method(self):
        """Create a fresh DataMunging instance for each test."""
        self.dm = DataMunging()

    # =========================================================================
    # Sample Data Constants
    # =========================================================================

    SAMPLE_WEATHER = """ 1  88  59  74  53.8  0.00  280  9.6  270  17  1.6  93  23  1004.5
 2  79  63  71  46.5  0.00  330  8.7  340  23  3.3  70  28  1004.5
 3  77  55  66  49.5  0.00  290  5.6  300  13  2.1  80  25  1004.5
 4  77  59  68  51.5  0.00  300  7.2  310  15  1.8  85  26  1004.5
 5  90  66  78  55.5  0.00  280  8.2  290  18  2.2  95  28  1004.5"""

    SAMPLE_SOCCER = """                            F     A
Team            P   W   L   D  GF  GA  GD  Pts
Arsenal        38  26   9   3  79  36  43   87
Liverpool      38  24   8   6  67  30  37   80
Manchester_Utd 38  24   5   7  87  45  42   79
Leeds          38  18  12   8  53  37  16   66
Chelsea        38  17  13   8  66  41  25   59
Aston_Villa    38  12  14  12  46  47  -1   48"""

    # =========================================================================
    # Part One: Weather Data - Min Temperature Spread
    # =========================================================================

    def test_parse_weather_data(self):
        """Parse weather data into WeatherRecord objects."""
        records = parse_weather_data(self.SAMPLE_WEATHER)
        assert len(records) == 5
        assert records[0].day == 1
        assert records[0].max_temp == 88
        assert records[0].min_temp == 59
        assert records[0].spread == 29
        # Day 2 should have min spread
        spreads = [r.spread for r in records]
        assert min(spreads) == 16  # Day 2: 79-63=16

    def test_find_min_spread_day_functional(self):
        """Functional interface: find day with min spread."""
        # Day 3: 77-55=22, Day 2: 79-63=16, Day 1: 88-59=29
        # Min is Day 2 with spread 16
        day = find_min_spread_day(self.SAMPLE_WEATHER)
        assert day == 2

    def test_find_min_spread_day_class(self):
        """Class-based interface: find day with min spread."""
        dm = DataMunging()
        # We'll test with the functional version since we don't have files
        # The class method uses file-based, so we test the parser directly
        parser = WeatherParser()
        records = list(parser.parse(iter(self.SAMPLE_WEATHER.split('\n'))))
        min_record = min(records, key=lambda r: r.spread)
        assert min_record.day == 2
        assert min_record.spread == 16

    def test_weather_record_properties(self):
        """WeatherRecord should have correct properties."""
        record = WeatherRecord(day=1, max_temp=88, min_temp=59, spread=29)
        assert record.day == 1
        assert record.max_temp == 88
        assert record.min_temp == 59
        assert record.spread == 29
        assert str(record) == "Day 1: max=88, min=59, spread=29"

    def test_weather_parser_skips_invalid_lines(self):
        """Parser should skip invalid/malformed lines."""
        bad_data = """ 1  88
 2  79  abc
 3  77  55
invalid line
 4  79  59"""
        records = parse_weather_data(bad_data)
        # Should only parse valid lines (day 1 has only 2 cols, day 2 has invalid temp, day 3 valid, day 4 valid)
        assert len(records) == 2
        assert records[0].day == 3
        assert records[1].day == 4

    # =========================================================================
    # Part Two: Soccer Data - Min Goal Difference
    # =========================================================================

    def test_parse_soccer_data(self):
        """Parse soccer data into SoccerRecord objects."""
        records = parse_soccer_data(self.SAMPLE_SOCCER)
        assert len(records) == 6  # 6 teams in sample
        assert records[0].team == "Arsenal"
        assert records[0].goals_for == 79
        assert records[0].goals_against == 36
        assert records[0].goal_diff == 43

    def test_find_min_goal_diff_functional(self):
        """Functional interface: find team with min goal difference."""
        # Aston_Villa has diff -1 (abs=1), smallest absolute diff
        team = find_min_goal_diff_team(self.SAMPLE_SOCCER)
        assert team == "Aston_Villa"

    def test_soccer_record_properties(self):
        """SoccerRecord should have correct properties."""
        record = SoccerRecord(
            team="Arsenal", played=38, won=26, lost=9, drawn=3,
            goals_for=79, goals_against=36, goal_diff=43, points=87
        )
        assert record.team == "Arsenal"
        assert record.goal_diff == 43
        assert record.points == 87
        assert "GF=79" in str(record)

    def test_soccer_parser_skips_headers(self):
        """Parser should skip header and totals lines."""
        data_with_header = self.SAMPLE_SOCCER + "\nTotals  100  50  50  0  200  200  0  150"
        records = parse_soccer_data(data_with_header)
        team_names = [r.team for r in records]
        assert "Totals" not in team_names
        assert "Team" not in team_names

    def test_soccer_parser_handles_various_formats(self):
        """Parser should handle different team name formats."""
        custom_data = """Team  P  W  L  D  GF  GA  GD  Pts
Man_City      38  28  5  5  90  30  60  89
Tottenham     38  20  10 8  65  40  25  68"""
        records = parse_soccer_data(custom_data)
        assert len(records) == 2
        assert records[0].team == "Man_City"
        assert records[1].team == "Tottenham"

    # =========================================================================
    # Part Three: DRY Fusion - Shared Functionality
    # =========================================================================

    def test_dry_generic_finder_weather(self):
        """DRY: Generic finder works for weather."""
        # Test the DRY concept: same min-finding logic works for both weather and soccer
        records = parse_weather_data(self.SAMPLE_WEATHER)
        min_record = min(records, key=lambda r: r.spread)
        assert min_record.day == 2
        assert min_record.spread == 16

    def test_dry_generic_finder_soccer(self):
        """DRY: Generic finder works for soccer."""
        records = parse_soccer_data(self.SAMPLE_SOCCER)
        min_record = min(records, key=lambda r: abs(r.goal_diff))
        assert min_record.team == "Aston_Villa"

    def test_shared_column_parser(self):
        """ColumnParser is shared between weather and soccer parsers."""
        weather_parser = WeatherParser()
        soccer_parser = SoccerParser()
        
        # Both use ColumnParser internally
        assert isinstance(weather_parser.parser, ColumnParser)
        assert isinstance(soccer_parser.parser, ColumnParser)

    # =========================================================================
    # Column Parser Tests
    # =========================================================================

    def test_column_parser_basic(self):
        """ColumnParser splits lines on whitespace."""
        lines = ["1 2 3", "4 5 6", "7 8 9"]
        parser = ColumnParser()
        cols = list(parser.parse_lines(lines))
        assert len(cols) == 3
        assert cols[0] == ['1', '2', '3']

    def test_column_parser_skip_lines(self):
        """ColumnParser skips specified number of lines."""
        lines = ["header1", "header2", "1 2 3", "4 5 6"]
        parser = ColumnParser(skip_lines=2)
        cols = list(parser.parse_lines(lines))
        assert len(cols) == 2
        assert cols[0] == ['1', '2', '3']

    def test_column_parser_header_pattern(self):
        """ColumnParser skips lines matching header pattern."""
        lines = ["Team  P  W", "Arsenal 38 26", "Liverpool 38 24"]
        parser = ColumnParser(skip_lines=0, header_pattern=r'^Team')
        cols = list(parser.parse_lines(lines))
        assert len(cols) == 2
        assert cols[0] == ['Arsenal', '38', '26']

    def test_column_parser_skips_empty(self):
        """ColumnParser skips empty lines."""
        lines = ["1 2 3", "", "4 5 6", "   ", "7 8 9"]
        parser = ColumnParser()
        cols = list(parser.parse_lines(lines))
        assert len(cols) == 3

    # =========================================================================
    # Domain Services Tests
    # =========================================================================

    def test_weather_parser_service(self):
        """WeatherParser service parses correctly."""
        parser = WeatherParser()
        lines = iter(self.SAMPLE_WEATHER.split('\n'))
        records = list(parser.parse(lines))
        assert len(records) == 5
        assert records[0].day == 1

    def test_soccer_parser_service(self):
        """SoccerParser service parses correctly."""
        parser = SoccerParser()
        lines = iter(self.SAMPLE_SOCCER.split('\n'))
        records = list(parser.parse(lines))
        assert len(records) == 6

    def test_data_munging_service(self):
        """DataMungingService coordinates parsing."""
        repo = LocalFileRepository()
        service = DataMungingService(repo)
        
        # Test with sample data (using string-based parsers)
        weather_parser = WeatherParser()
        soccer_parser = SoccerParser()
        
        weather_records = list(weather_parser.parse(iter(self.SAMPLE_WEATHER.split('\n'))))
        soccer_records = list(soccer_parser.parse(iter(self.SAMPLE_SOCCER.split('\n'))))
        
        min_weather = min(weather_records, key=lambda r: r.spread)
        min_soccer = min(soccer_records, key=lambda r: abs(r.goal_diff))
        
        assert min_weather.day == 2
        assert min_soccer.team == "Aston_Villa"

    # =========================================================================
    # Repository Pattern Tests
    # =========================================================================

    def test_local_file_repository(self, tmp_path):
        """LocalFileRepository reads files correctly."""
        repo = LocalFileRepository()
        test_file = tmp_path / "test.dat"
        test_file.write_text("line1\nline2\nline3")
        
        lines = list(repo.read_lines(test_file))
        assert lines == ["line1", "line2", "line3"]
        assert repo.exists(test_file)
        assert not repo.exists(tmp_path / "nonexistent.dat")

    def test_repository_missing_file(self):
        """Repository raises FileNotFoundError for missing files."""
        repo = LocalFileRepository()
        with pytest.raises(FileNotFoundError):
            list(repo.read_lines(Path("/nonexistent/file.dat")))

    # =========================================================================
    # Architecture Pattern Tests
    # =========================================================================

    def test_cqrs_separation(self):
        """Commands and queries are separated."""
        dm = DataMunging()
        # Query - doesn't modify state (using string-based parsers)
        # The facade has command and query handlers internally
        assert hasattr(dm, '_command_handler')
        assert hasattr(dm, '_query_handler')
        # Verify CQRS structure: commands modify state, queries read state
        # We test the structure without file I/O
        assert hasattr(dm._query_handler, 'handle_all')
        assert hasattr(dm._command_handler, 'handle_weather')
        assert hasattr(dm._command_handler, 'handle_soccer')

    def test_repository_pattern(self):
        """Repository abstracts data access."""
        repo = LocalFileRepository()
        service = DataMungingService(repo)
        assert service._repository is repo

    def test_value_objects_immutable(self):
        """Value objects should be immutable."""
        weather = WeatherRecord(day=1, max_temp=88, min_temp=59, spread=29)
        with pytest.raises(AttributeError):
            weather.day = 2
        
        soccer = SoccerRecord(team="Arsenal", played=38, won=26, lost=9, drawn=3,
                              goals_for=79, goals_against=36, goal_diff=43, points=87)
        with pytest.raises(AttributeError):
            soccer.team = "Chelsea"

    # =========================================================================
    # TDD Progression (from README)
    # =========================================================================

    def test_tdd_step_1_weather_min_spread(self):
        """Step 1: Find day with smallest temperature spread."""
        # Day 2 has spread 16 (79-63), which is the minimum
        day = find_min_spread_day(self.SAMPLE_WEATHER)
        assert day == 2

    def test_tdd_step_2_soccer_min_goal_diff(self):
        """Step 2: Find team with smallest goal difference."""
        team = find_min_goal_diff_team(self.SAMPLE_SOCCER)
        assert team == "Aston_Villa"

    def test_tdd_step_3_dry_fusion(self):
        """Step 3: DRY fusion - shared parsing logic."""
        # Both parsers use shared ColumnParser
        # Both use shared min-finding logic
        records = parse_soccer_data(self.SAMPLE_SOCCER)
        min_soccer = min(records, key=lambda r: abs(r.goal_diff))
        assert min_soccer.team == "Aston_Villa"

    # =========================================================================
    # Edge Cases
    # =========================================================================

    def test_empty_weather_data(self):
        """Empty weather data returns -1."""
        assert find_min_spread_day("") == -1

    def test_empty_soccer_data(self):
        """Empty soccer data returns empty string."""
        assert find_min_goal_diff_team("") == ""

    def test_single_weather_record(self):
        """Single weather record returns that day."""
        data = "1  88  59  74  53.8  0.00  280  9.6  270  17  1.6  93  23  1004.5"
        assert find_min_spread_day(data) == 1

    def test_single_soccer_record(self):
        """Single soccer record returns that team."""
        data = """Team  P  W  L  D  GF  GA  GD  Pts
TestTeam  38  20  10  8  60  40  20  68"""
        assert find_min_goal_diff_team(data) == "TestTeam"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])