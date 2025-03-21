import React, { useState } from 'react';
import {
  Container,
  AppBar,
  Toolbar,
  Typography
} from '@mui/material';
import SeriesList from './components/SeriesList';
import MatchesList from './components/MatchesList';
import MatchScorecard from './components/MatchScorecard';
import PlayerStats from './components/PlayerStats';

function App() {
  const [selectedSeries, setSelectedSeries] = useState(null);
  const [selectedMatch, setSelectedMatch] = useState(null);
  const [selectedPlayer, setSelectedPlayer] = useState(null);

  const handlePlayerClick = (playerId) => {
    console.log("Player clicked:", playerId); // Debug log
    if (playerId) {
      setSelectedPlayer(playerId);
    }
  };

  const handleBackFromPlayer = () => {
    setSelectedPlayer(null);
  };

  const handleBackFromMatch = () => {
    setSelectedMatch(null);
  };

  const handleBackFromSeries = () => {
    setSelectedSeries(null);
  };

  const renderContent = () => {
    if (selectedPlayer) {
      return (
        <PlayerStats
          playerId={selectedPlayer}
          onBack={() => setSelectedPlayer(null)}
        />
      );
    }
    if (selectedMatch) {
      return (
        <MatchScorecard
          matchData={selectedMatch}
          onBack={() => setSelectedMatch(null)}
          onPlayerClick={handlePlayerClick}
        />
      );
    }
    if (selectedSeries) {
      return (
        <MatchesList
          seriesData={selectedSeries}
          onMatchSelect={setSelectedMatch}
          onBack={handleBackFromSeries}
        />
      );
    }
    return <SeriesList onSeriesSelect={setSelectedSeries} />;
  };

  return (
    <div>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6">
            Cricket Scorecard
          </Typography>
        </Toolbar>
      </AppBar>
      <Container>
        {renderContent()}
      </Container>
    </div>
  );
}

export default App;