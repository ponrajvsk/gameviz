import React, { useState, useEffect } from 'react';
import {
  Card,
  Typography,
  Box,
  CircularProgress,
  Button,
  Grid,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper
} from '@mui/material';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  LineChart, Line, PieChart, Pie, Cell,
  RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis
} from 'recharts';

const PlayerStats = ({ playerId, onBack }) => {
  const [playerData, setPlayerData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPlayerData();
  }, [playerId]);

  const fetchPlayerData = async () => {
    try {
      setLoading(true);
      const response = await fetch(`http://127.0.0.1:8000/cricket/player/${playerId}`);
      const data = await response.json();
      setPlayerData(data);
    } catch (error) {
      console.error('Error fetching player data:', error);
    } finally {
      setLoading(false);
    }
  };

  const renderBasicInfo = () => (
    <Card sx={{ p: 2, mb: 2 }}>
      <Grid container spacing={2}>
      <Grid item xs={12} md={3}>
        <Box
          component="img"
          sx={{
            width: '100%',
            maxWidth: 300,
            height: 'auto',
            borderRadius: 2,
            boxShadow: 3
          }}
          src={playerData.personal_info.image_url}
          alt={playerData.personal_info.full_name}
          onError={(e) => {
            e.target.src = '/default-player.png'; // Fallback image
          }}
        />
      </Grid>
        <Grid item xs={12} md={4}>
          <Typography variant="h6">Basic Information</Typography>
          <Typography>Full Name: {playerData.personal_info.full_name}</Typography>
          <Typography>Born: {playerData.personal_info.date_of_birth}</Typography>
          <Typography>Role: {playerData.personal_info.role}</Typography>
          <Typography>Batting Style: {playerData.personal_info.batting_style}</Typography>
          <Typography>Bowling Style: {playerData.personal_info.bowling_style}</Typography>
        </Grid>
        <Grid item xs={12} md={8}>
          <Typography variant="h6">Career Statistics</Typography>
          <Grid container spacing={2}>
            <Grid item xs={4}>
              <Typography variant="h3">{playerData.career_stats.matches}</Typography>
              <Typography>Matches</Typography>
            </Grid>
            <Grid item xs={4}>
              <Typography variant="h3">{playerData.career_stats.runs}</Typography>
              <Typography>Runs</Typography>
            </Grid>
            <Grid item xs={4}>
              <Typography variant="h3">{playerData.career_stats.wickets}</Typography>
              <Typography>Wickets</Typography>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </Card>
  );

  const renderBattingStats = () => (
    <Card sx={{ p: 2, mb: 2 }}>
      <Typography variant="h6" gutterBottom>Batting Statistics</Typography>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Format</TableCell>
              <TableCell align="right">Matches</TableCell>
              <TableCell align="right">Runs</TableCell>
              <TableCell align="right">Average</TableCell>
              <TableCell align="right">Strike Rate</TableCell>
              <TableCell align="right">100s</TableCell>
              <TableCell align="right">50s</TableCell>
              <TableCell align="right">Highest</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {playerData.career_stats.batting.map((stat) => (
              <TableRow key={stat.format}>
                <TableCell>{stat.format}</TableCell>
                <TableCell align="right">{stat.matches}</TableCell>
                <TableCell align="right">{stat.runs}</TableCell>
                <TableCell align="right">{stat.average}</TableCell>
                <TableCell align="right">{stat.strikeRate}</TableCell>
                <TableCell align="right">{stat.hundreds}</TableCell>
                <TableCell align="right">{stat.fifties}</TableCell>
                <TableCell align="right">{stat.highest}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Card>
  );

  const renderPerformanceChart = () => {
    const data = playerData.recent_performances.map(perf => ({
      match: perf.matchDate,
      runs: perf.runs,
      wickets: perf.wickets
    }));

    return (
      <Card sx={{ p: 2, mb: 2 }}>
        <Typography variant="h6" gutterBottom>Recent Performances</Typography>
        <LineChart width={800} height={300} data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="match" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="runs" stroke="#8884d8" />
          <Line type="monotone" dataKey="wickets" stroke="#82ca9d" />
        </LineChart>
      </Card>
    );
  };

  const renderFormatDistributionChart = () => {
  const data = [
    { name: 'Tests', value: playerData.career_stats.batting[0].matches },
    { name: 'ODIs', value: playerData.career_stats.batting[1].matches },
    { name: 'T20Is', value: playerData.career_stats.batting[2].matches }
  ];

  return (
    <Card sx={{ p: 2, mb: 2 }}>
      <Typography variant="h6" gutterBottom>Matches by Format</Typography>
      <PieChart width={400} height={300}>
        <Pie
          data={data}
          cx={200}
          cy={150}
          labelLine={false}
          outerRadius={100}
          fill="#8884d8"
          dataKey="value"
          label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={['#0088FE', '#00C49F', '#FFBB28'][index]} />
          ))}
        </Pie>
        <Tooltip />
        <Legend />
      </PieChart>
    </Card>
  );
};

  const renderAverageComparisonChart = () => {
  const data = playerData.career_stats.batting.map(format => ({
    name: format.format,
    average: format.average,
    strikeRate: format.strikeRate
  }));

  return (
    <Card sx={{ p: 2, mb: 2 }}>
      <Typography variant="h6" gutterBottom>Average & Strike Rate Comparison</Typography>
      <BarChart width={600} height={300} data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="average" fill="#8884d8" name="Average" />
        <Bar dataKey="strikeRate" fill="#82ca9d" name="Strike Rate" />
      </BarChart>
    </Card>
  );
};

  const renderMilestoneChart = () => {
  const data = playerData.career_stats.batting.map(format => ({
    name: format.format,
    hundreds: format.hundreds,
    fifties: format.fifties
  }));

  return (
    <Card sx={{ p: 2, mb: 2 }}>
      <Typography variant="h6" gutterBottom>Centuries & Half-centuries</Typography>
      <BarChart width={600} height={300} data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="hundreds" fill="#ff7300" name="Centuries" />
        <Bar dataKey="fifties" fill="#82ca9d" name="Half-centuries" />
      </BarChart>
    </Card>
  );
};

  const renderPerformanceRadar = () => {
  const data = [
    {
      subject: 'Average',
      value: playerData.career_stats.batting[1].average, // Using ODI stats
      fullMark: 60
    },
    {
      subject: 'Strike Rate',
      value: playerData.career_stats.batting[1].strikeRate / 2, // Normalized
      fullMark: 100
    },
    {
      subject: 'Centuries',
      value: playerData.career_stats.batting[1].hundreds,
      fullMark: 50
    },
    {
      subject: 'Matches',
      value: playerData.career_stats.batting[1].matches / 3, // Normalized
      fullMark: 100
    },
    {
      subject: 'Highest Score',
      value: playerData.career_stats.batting[1].highest / 2, // Normalized
      fullMark: 100
    }
  ];

  return (
    <Card sx={{ p: 2, mb: 2 }}>
      <Typography variant="h6" gutterBottom>Player Performance Radar</Typography>
      <RadarChart width={500} height={400} data={data}>
        <PolarGrid />
        <PolarAngleAxis dataKey="subject" />
        <PolarRadiusAxis />
        <Radar
          name="Player Stats"
          dataKey="value"
          stroke="#8884d8"
          fill="#8884d8"
          fillOpacity={0.6}
        />
        <Tooltip />
      </RadarChart>
    </Card>
  );
};


  return (
  <Box sx={{ m: 2 }}>
    <Button onClick={onBack} sx={{ mb: 2 }}>Back to Scorecard</Button>
    {loading ? (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
        <CircularProgress />
      </Box>
    ) : playerData && (
      <>
        {renderBasicInfo()}
        {renderBattingStats()}
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            {renderFormatDistributionChart()}
          </Grid>
          <Grid item xs={12} md={6}>
            {renderPerformanceRadar()}
          </Grid>
        </Grid>
        {renderAverageComparisonChart()}
        {renderMilestoneChart()}
        {renderPerformanceChart()}
      </>
    )}
  </Box>
);
};

export default PlayerStats;










