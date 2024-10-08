import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useSearchParams } from 'react-router-dom';
import { Card, CardContent, CardMedia, CardActionArea, Typography, CircularProgress, useMediaQuery, useTheme } from '@mui/material';
import { useNavigate } from 'react-router-dom';

function MatchList() {
  const apiUrl = import.meta.env.VITE_API_BASE_URL;
  const navigate = useNavigate();

  const [matches, setMatches] = useState([]);
  const [error, setErrorType] = useState(null);
  const [loading, setLoading] = useState(true);

  // Get search parameters (name and location) from the URL
  const [searchParams] = useSearchParams();
  const name = searchParams.get('name') || '';
  const location = searchParams.get('location') || '';

  const theme = useTheme();
  const isXs = useMediaQuery(theme.breakpoints.only('xs'));
  const isSm = useMediaQuery(theme.breakpoints.only('sm'));
  const isMd = useMediaQuery(theme.breakpoints.only('md'));

  const getTruncateLength = () => {
    if (isXs) return 30;
    if (isSm) return 35;
    if (isMd) return 45;
    return 60; // for larger screens
  };

  useEffect(() => {
    const fetchMatches = async () => {
      setLoading(true);
      try {
        // Check if data exists in sessionStorage
        const cachedMatches = sessionStorage.getItem(`matches_${name}_${location}`);
        if (cachedMatches) {
          setMatches(JSON.parse(cachedMatches));
          console.log('Data loaded from sessionStorage');
          setLoading(false);
        } else {
          const response = await axios.get(`${apiUrl}/api/search`, {
            params: { name, location },
          });
          console.log(response.data);
          console.log('Data loaded from server');

          setMatches(response.data); 
          
          sessionStorage.setItem(`matches_${name}_${location}`, JSON.stringify(response.data)); // Save the data in sessionStorage
        }
        setErrorType(null); 
      } catch (err) {
        if (err.response && err.response.data && err.response.data.error_code) {
          setErrorType(err.response.data.error_code);
        }
        else {
          setErrorType('UNKNOWN_ERROR');
        }
      } finally {
        setLoading(false);
      }
    };

    if (name && location) {
      fetchMatches();
    }
    else {
      setLoading(false);
      setErrorType('MISSING_PARAMS');
    }
  }, [name, location]);

  const handleCardClick = (data) => {
    navigate(`/ratings?name=${name}&location=${location}`, { state: { data } });
  };

  const truncateText = (text, maxLength) => {
    return text.length > maxLength ? text.slice(0, maxLength - 3) + '...' : text;
  };

  if (loading) {
    return <div className='flex items-center justify-center mt-20 '>
      <CircularProgress style={{ color: 'black' }} />
    </div>;
  }

  if (error === 'UNKNOWN_LOCATION') {
    return (
      <div className="space-y-4">
        <h1 className="text-3xl font-bold">Sorry, we couldn't recognize the location you entered.</h1>
        <p className="text-xl font-semibold">Please use one of the following formats:</p>
        <div className="space-y-2 text-lg font-semibold">
          <p>706 Mission St, San Francisco, CA</p>
          <p>San Francisco, CA</p>
          <p>San Francisco, CA 94103</p>
          <p>94103</p>
        </div>
      </div>
    );
  }

  if (error === 'NO_RESULTS') {
    return <h1 className="items-start mb-4 text-3xl font-bold">No results for {name} in {location}. Please try again...</h1>
  }
  if (error === 'MISSING_PARAMS') {
    return <h1 className="items-start mb-4 text-3xl font-bold">Couldn't fetch results. Both the name and location are required.</h1>
  }
  if (error) {
    return <div>An error occurred: {error}</div>;
  }

  return (
    <div className="flex flex-col ">
      <h1 className="items-start mb-2 text-xl font-bold md:mb-4 md:text-3xl">Select the restaurant you want to see ratings for</h1>
      
      {matches.length > 0 ? (
        matches.map((data, index) => (
          <div key={index} className="w-full mb-4">
            <Card
              sx={{ width: '100%', cursor: 'pointer' }}
              onClick={() => handleCardClick(data)}
            >
              <div className="flex">
                {data.imageUrl && (
                  <div className="flex-shrink-0">
                    <img
                      src={data.imageUrl}
                      alt={`${data.name} example`}
                      className="object-cover w-24 h-24"
                    />
                  </div>
                )}
                <CardContent className="flex-grow py-2">
                  <Typography 
                    variant="h5" 
                    component="div" 
                    sx={{
                      fontSize: {
                        xs: '1rem',
                        sm: '1.25rem',
                        md: '1.5rem',
                      },
                    }}
                  >
                    {truncateText(data.name, getTruncateLength())}
                  </Typography>
                  <Typography 
                    variant="body1" 
                    color="textSecondary" 
                    sx={{
                      fontSize: {
                        xs: '0.875rem',
                        sm: '1rem',
                        md: '1rem',
                      },
                    }}
                  >
                    {truncateText(data.location, getTruncateLength())}
                  </Typography>
                </CardContent>
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
