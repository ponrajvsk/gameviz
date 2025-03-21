import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import {
  Card,
  Tabs,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  Paper,
  Button,
  Box,
  CircularProgress,
  Link
} from '@mui/material';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  LineChart, Line, PieChart, Pie, Cell
} from 'recharts';

const MatchScorecard = ({ matchData, onBack, onPlayerClick }) => {
  const [currentInnings, setCurrentInnings] = useState(0);
  const [inningsData, setInningsData] = useState([null, null]);
  const [loading, setLoading] = useState(false);

  const fetchInningsData = async (inningsId, index) => {
    try {
      setLoading(true);
      const response = await fetch(`http://127.0.0.1:8000/cricket/scoreboard/${inningsId}`);
      const data = await response.json();
      setInningsData(prev => {
        const newData = [...prev];
        newData[index] = data;
        return newData;
      });
    } catch (error) {
      console.error('Error fetching innings data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (matchData.innings[0]) {
      fetchInningsData(matchData.innings[0], 0);
    }
  }, [matchData.innings]);

  const handleInningsChange = (event, newValue) => {
    setCurrentInnings(newValue);
    if (newValue === 1 && !inningsData[1] && matchData.innings[1]) {
      fetchInningsData(matchData.innings[1], 1);
    }
  };

  const handlePlayerClick = (playerId) => {
    if (onPlayerClick && playerId) {
      onPlayerClick(playerId);
    }
  };

  const renderBattingScorecard = (innings) => (
    <TableContainer component={Paper}>
      <Typography variant="h6" sx={{ p: 2 }}>
        Batting ({innings.total_runs}/{innings.total_wickets})
      </Typography>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Batsman</TableCell>
            <TableCell align="right">Runs</TableCell>
            <TableCell align="right">Balls</TableCell>
            <TableCell align="right">4s</TableCell>
            <TableCell align="right">6s</TableCell>
            <TableCell align="right">SR</TableCell>
            <TableCell>Dismissal</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {Object.entries(innings.batters).map(([name, stats]) => (
            <TableRow key={name}>
              <TableCell>
                <Link
                  component="button"
                  variant="body2"
                  onClick={() => {
      console.log("Batting player ID:", stats.player_id); // Debug log
      handlePlayerClick(stats.player_id);
    }}
                  sx={{ textDecoration: 'none', cursor: 'pointer' }}
                >
                  {name}
                </Link>
              </TableCell>
              <TableCell align="right">{stats.runs}</TableCell>
              <TableCell align="right">{stats.balls}</TableCell>
              <TableCell align="right">{stats.fours}</TableCell>
              <TableCell align="right">{stats.sixes}</TableCell>
              <TableCell align="right">{stats.strike_rate}</TableCell>
              <TableCell>
                {stats.wicket ? (
                  `${stats.wicket.wicket_type} ${
                    stats.wicket.fielder_involved.length > 0
                      ? `c ${stats.wicket.fielder_involved[0]} `
                      : ''
                  }b ${stats.wicket.bowler}`
                ) : 'not out'}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );

  const renderBowlingStats = (innings) => (
    <TableContainer component={Paper} sx={{ mt: 2 }}>
      <Typography variant="h6" sx={{ p: 2 }}>Bowling</Typography>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Bowler</TableCell>
            <TableCell align="right">O</TableCell>
            <TableCell align="right">M</TableCell>
            <TableCell align="right">R</TableCell>
            <TableCell align="right">W</TableCell>
            <TableCell align="right">Econ</TableCell>
            <TableCell align="right">Dots</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {Object.entries(innings.bowlers).map(([name, stats]) => (
            <TableRow key={name}>
              <TableCell>
                <Link
                  component="button"
                  variant="body2"
                  onClick={() => handlePlayerClick(stats.player_id)}
                  sx={{ textDecoration: 'none', cursor: 'pointer' }}
                >
                  {name}
                </Link>
              </TableCell>
              <TableCell align="right">{stats.overs}</TableCell>
              <TableCell align="right">{stats.maiden_overs}</TableCell>
              <TableCell align="right">{stats.runs_conceded}</TableCell>
              <TableCell align="right">{stats.wickets}</TableCell>
              <TableCell align="right">{stats.economy_rate}</TableCell>
              <TableCell align="right">{stats.dot_balls}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );

  const renderFallOfWickets = (innings) => (
    <Card sx={{ mt: 2, p: 2 }}>
      <Typography variant="h6">Fall of Wickets</Typography>
      <Typography variant="body1">
        {innings.fall_of_wickets.map((fow, index) => (
          `${fow.runs_at_wicket}-${index + 1} (${fow.batter_out})`
        )).join(' | ')}
      </Typography>
    </Card>
  );

  const renderPartnerships = (innings) => (
    <Card sx={{ mt: 2, p: 2 }}>
      <Typography variant="h6">Partnerships</Typography>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Players</TableCell>
            <TableCell align="right">Runs</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {innings.partnerships.map((partnership, index) => (
            <TableRow key={index}>
              <TableCell>
                {partnership.batters.map((batter, idx) => (
                  <React.Fragment key={batter.player_id}>
                    <Link
                      component="button"
                      variant="body2"
                      onClick={() => handlePlayerClick(batter.player_id)}
                      sx={{ textDecoration: 'none', cursor: 'pointer' }}
                    >
                      {batter.name}
                    </Link>
                    {idx === 0 ? ' & ' : ''}
                  </React.Fragment>
                ))}
              </TableCell>
              <TableCell align="right">{partnership.runs}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Card>
  );

  const renderExtras = (innings) => (
    <Card sx={{ mt: 2, p: 2 }}>
      <Typography variant="h6">Extras</Typography>
      <Typography variant="body1">
        {`Wide: ${innings.extras.wides} | `}
        {`No Balls: ${innings.extras.no_balls} | `}
        {`Byes: ${innings.extras.byes} | `}
        {`Leg Byes: ${innings.extras.leg_byes} | `}
        {`Penalties: ${innings.extras.penalties}`}
      </Typography>
    </Card>
  );

  const renderPartnershipChart = (innings) => {
    const data = innings.partnerships.map((p, index) => ({
      name: `${index + 1}`,
      runs: p.runs,
      partners: p.batters.map(b => b.name).join(' & ')
    }));

    return (
      <Card sx={{ mt: 2, p: 2 }}>
        <Typography variant="h6">Partnership Analysis</Typography>
        <BarChart width={600} height={300} data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip content={({ payload, label }) => {
            if (payload && payload.length) {
              return (
                <div style={{ background: 'white', padding: '10px', border: '1px solid #ccc' }}>
                  <p>{`Partnership ${label}: ${payload[0].value} runs`}</p>
                  <p>{payload[0].payload.partners}</p>
                </div>
              );
            }
            return null;
          }} />
          <Bar dataKey="runs" fill="#8884d8" />
        </BarChart>
      </Card>
    );
  };

  const renderRunsProgressionChart = (innings) => {
    const data = innings.fall_of_wickets.map((fow) => ({
      wicket: fow.batter_out,
      runs: fow.runs_at_wicket
    }));

    return (
      <Card sx={{ mt: 2, p: 2 }}>
        <Typography variant="h6">Runs Progression</Typography>
        <LineChart width={600} height={300} data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="wicket" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="runs" stroke="#82ca9d" />
        </LineChart>
      </Card>
    );
  };

  const renderScoringDistribution = (innings) => {
    const data = [
      { name: 'Singles', value: 0 },
      { name: 'Boundaries', value: 0 },
      { name: 'Sixes', value: 0 },
      { name: 'Extras', value: 0 }
    ];

    Object.values(innings.batters).forEach(batter => {
      data[0].value += (batter.runs - (batter.fours * 4) - (batter.sixes * 6));
      data[1].value += (batter.fours * 4);
      data[2].value += (batter.sixes * 6);
    });

    data[3].value = Object.values(innings.extras).reduce((a, b) => a + b, 0);

    const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

    return (
      <Card sx={{ mt: 2, p: 2 }}>
        <Typography variant="h6">Scoring Distribution</Typography>
        <PieChart width={400} height={400}>
          <Pie
            data={data}
            cx={200}
            cy={200}
            labelLine={false}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
        </PieChart>
      </Card>
    );
  };

  return (
    <Card sx={{ margin: 2, padding: 2 }}>
      <Button onClick={onBack}>Back to Matches</Button>
      <Typography variant="h5" gutterBottom>
        {matchData.name}
      </Typography>
      <Typography variant="subtitle1">
        {matchData.date} at {matchData.venue}
      </Typography>

      <Tabs
        value={currentInnings}
        onChange={handleInningsChange}
      >
        <Tab label="1st Innings" />
        <Tab label="2nd Innings" />
      </Tabs>

      <Box sx={{ mt: 2 }}>
        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
            <CircularProgress />
          </Box>
        ) : (
          inningsData[currentInnings] && (
            <>
              {renderBattingScorecard(inningsData[currentInnings])}
              {renderBowlingStats(inningsData[currentInnings])}
              {renderFallOfWickets(inningsData[currentInnings])}
              {renderPartnerships(inningsData[currentInnings])}
              {renderExtras(inningsData[currentInnings])}

              <Box sx={{ mt: 4 }}>
                <Typography variant="h5" gutterBottom>Match Analytics</Typography>
                {renderPartnershipChart(inningsData[currentInnings])}
                {renderRunsProgressionChart(inningsData[currentInnings])}
                {renderScoringDistribution(inningsData[currentInnings])}
              </Box>
            </>
          )
        )}
      </Box>
    </Card>
  );
};

MatchScorecard.propTypes = {
  matchData: PropTypes.object.isRequired,
  onBack: PropTypes.func.isRequired,
  onPlayerClick: PropTypes.func.isRequired
};

export default MatchScorecard;