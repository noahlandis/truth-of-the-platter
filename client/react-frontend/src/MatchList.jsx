import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useSearchParams } from 'react-router-dom';
import { Card, CardContent, Typography } from '@mui/material';

function MatchList() {
  const [matches, setMatches] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  // Get search parameters (name and location) from the URL
  const [searchParams] = useSearchParams();
  const name = searchParams.get('name') || '';
  const location = searchParams.get('location') || '';

  useEffect(() => {
    const fetchMatches = async () => {
      setLoading(true);
      try {
        // Check if data exists in localStorage
        const cachedMatches = localStorage.getItem(`matches_${name}_${location}`);
        if (cachedMatches) {
          setMatches(JSON.parse(cachedMatches));
          console.log('Data loaded from localStorage');
          setLoading(false);
        } else {
          const response = await axios.get('http://127.0.0.1:5000/search', {
            params: { name, location },
            
          });
          console.log('Data loaded from server');

          setMatches(response.data); 
          localStorage.setItem(`matches_${name}_${location}`, JSON.stringify(response.data)); // Save the data in localStorage
        }
        setError(null); 
      } catch (err) {
        if (err.response) {
          setError(err.response.data.error); 
        } else {
          setError('An unexpected error occurred');
        }
      } finally {
        setLoading(false);
      }
    };

    if (name || location) {
      fetchMatches();
    }
  }, [name, location]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="flex flex-col items-center justify-center">
      {matches.length > 0 ? (
        matches.map((data, index) => (
          <div key={index} className="w-full mb-4">
            <Card sx={{ width: '100%' }}>
              <div className="flex items-center">
                {data.imageUrl && (
                  <div>
                    <img
                      src={data.imageUrl}
                      alt={`${data.name} example`}
                      style={{ width: 100, height: 100 }}
                    />
                  </div>
                )}
                <div>
                  <CardContent>
                    <Typography variant="h5" component="div">
                      {data.name}
                    </Typography>
                    <Typography variant="body1" color="textSecondary">
                      {data.location}
                    </Typography>
                  </CardContent>
                </div>
              </div>
            </Card>
          </div>
        ))
      ) : (
        <Typography>No matches found</Typography>
      )}
    </div>
  );
}

export default MatchList;
