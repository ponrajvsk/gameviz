import React, { useState, useEffect } from 'react';
import {
  Card,
  List,
  ListItem,
  ListItemText,
  Typography,
  Divider,
  CircularProgress,
  Box
} from '@mui/material';

const SeriesList = ({ onSeriesSelect }) => {
  const [series, setSeries] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchSeries();
  }, []);

  const fetchSeries = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://127.0.0.1:8000/cricket/series');
      const data = await response.json();
      setSeries(data);
    } catch (error) {
      console.error('Error fetching series:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card sx={{ margin: 2, padding: 2 }}>
      <Typography variant="h5" gutterBottom>Cricket Series</Typography>
      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
          <CircularProgress />
        </Box>
      ) : (
        <List>
          {series.map((item) => (
            <React.Fragment key={item.id}>
              <ListItem button onClick={() => onSeriesSelect(item)}>
                <ListItemText
                  primary={item.name}
                  secondary={`${item.season}`}
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

export default SeriesList;