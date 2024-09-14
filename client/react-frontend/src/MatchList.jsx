import React, { useState, useEffect } from 'react';
import axios from 'axios'; // Add this import to use axios
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
      try {
        setLoading(true); // Set loading to true when the request starts
        const response = await axios.get('http://127.0.0.1:5000/search', {
          params: { name, location },
        });
        console.log(response.data);
        setMatches(response.data); // Store the results in state
        setError(null); // Clear any previous errors
      } catch (err) {
        if (err.response) {
          setError(err.response.data.error); // Handle the error message
        } else {
          setError('An unexpected error occurred');
        }
      } finally {
        setLoading(false); // Set loading to false once the request finishes
      }
    };

    if (name || location) {
      fetchMatches();
    }
  }, [name, location]);

  if (loading) {
    return <div>Loading...</div>; // Show loading state
  }

  if (error) {
    return <div>Error: {error}</div>; // Show error message
  }

  return (
    <div className="flex flex-col items-center justify-center">
      {matches.length > 0 ? (
        matches.map((data, index) => (
          <div key={index} className="w-full mb-4">
            <Card sx={{ width: '100%' }}>
              <div className="flex items-center">
                {/* Left side: Image */}
                {data.imageUrl && (
                  <div>
                    <img
                      src={data.imageUrl}
                      alt={`${data.name} example`}
                      style={{ width: 100, height: 100 }}
                    />
                  </div>
                )}
                {/* Right side: Card content */}
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
