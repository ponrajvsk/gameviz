import React, { useState, useEffect } from 'react';
import {
  Card,
  List,
  ListItem,
  ListItemText,
  Typography,
  Divider,
  Button,
  CircularProgress,
  Box
} from '@mui/material';

const MatchesList = ({ seriesData, onMatchSelect, onBack }) => {
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchMatches();
  }, [seriesData.id]);

  const fetchMatches = async () => {
    try {
      setLoading(true);
      const response = await fetch(`http://127.0.0.1:8000/cricket/series/${seriesData.id}/matches`);
      const data = await response.json();
      setMatches(data);
    } catch (error) {
      console.error('Error fetching matches:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card sx={{ margin: 2, padding: 2 }}>
      <Button onClick={onBack} sx={{ mb: 2 }}>Back to Series</Button>
      <Typography variant="h5" gutterBottom>{seriesData.name}</Typography>
      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
          <CircularProgress />
        </Box>
      ) : (
        <List>
          {matches.map((match) => (
            <React.Fragment key={match.id}>
              <ListItem button onClick={() => onMatchSelect(match)}>
                <ListItemText
                  primary={match.name}
                  secondary={`${match.date} at ${match.venue}`}
                />
              </ListItem>
              <Divider />
            </React.Fragment>
          ))}
        </List>
      )}
    </Card>
  );
};

export default MatchesList;