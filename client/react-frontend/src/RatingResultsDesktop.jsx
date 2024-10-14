import { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { CircularProgress, Rating, Box, Typography, Grid2, Card, CardContent, CardMedia, Divider } from '@mui/material';
import { useSearchParams } from "react-router-dom";
import { useNavigate } from 'react-router-dom';

import google from './assets/logos_png/google_logo.png'
import tripAdvisor from './assets/logos_png/trip_advisor_logo.png'
import yelp from './assets/logos_png/yelp_logo.png'

import StarIcon from '@mui/icons-material/Star'; // Import the star icon

function RatingResultsDesktop() {
    const apiUrl = import.meta.env.VITE_API_BASE_URL;
    const navigate = useNavigate();
    const location = useLocation();
    const { data } = location.state || {}; // Get the entire data object from location.state

    const [siteRatings, setSiteRatings] = useState([]);
    const [starAverage, setStarAverage] = useState(null);
    const [totalReviewCount, setTotalReviewCount] = useState(null);
    const [loading, setLoading] = useState(false);  // Update loading state
    const [error, setError] = useState(null);
    const [searchParams] = useSearchParams();
    const nameParam = searchParams.get('name') || '';
    const locationParam = searchParams.get('location') || '';

    const getLogoForWebsite = (website) => {
        switch (website.toLowerCase()) {
            case 'yelp':
                return yelp;
            case 'tripadvisor':
                return tripAdvisor;
            case 'google':
                return google;
            default:
                return null;
        }
    };

    useEffect(() => {
        if (!data && nameParam && locationParam) {
            navigate(`/search?name=${nameParam}&location=${locationParam}`);
        }
        if (!data) {
            navigate('/');
        }
    }, [data, nameParam, locationParam, navigate]);

    useEffect(() => {
        if (data) {
            localStorage.removeItem('siteRatings');
            localStorage.removeItem('starAverage');
            localStorage.removeItem('totalReviewCount');
        }

        const fetchRatings = async () => {
            setLoading(true);
            try {
                const response = await fetch(`${apiUrl}/api/select`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data),
                });

                if (!response.ok) {
                    throw new Error('Error fetching ratings');
                }

                const result = await response.json();
                setSiteRatings(result.site_ratings);
                setStarAverage(result.star_average);
                setTotalReviewCount(result.total_review_count);

                localStorage.setItem('siteRatings', JSON.stringify(result.site_ratings));
                localStorage.setItem('starAverage', JSON.stringify(result.star_average));
                localStorage.setItem('totalReviewCount', JSON.stringify(result.total_review_count));
            } catch (error) {
                setError(error.message);
            } finally {
                setLoading(false);
            }
        };

        if (data) {
            fetchRatings();
        }
    }, [data]);

    if (loading) {
        return <div className='flex items-center justify-center mt-20 '>
          <CircularProgress style={{ color: 'black' }} />
        </div>;
      }

      
    if (error) {
        return <div>Error: {error}</div>;
    }

    return (
        <Card sx={{ display: 'flex', flexDirection: 'column', padding: 2, boxShadow: 3, marginBottom: 4 }}>
            <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, justifyContent: 'space-between', width: '100%' }}>
                {/* Left Column: Photo, Name, Location */}
                <Box sx={{ flex: 1, marginRight: { md: 2 }, marginBottom: { xs: 2, md: 0 } }}>
                    <CardMedia
                        component="img"
                        sx={{ width: '100%', height: 250, borderRadius: '8px' }}
                        image={data?.imageUrl || google} // Replace with actual photo
                        alt={`${data?.name}`}
                    />
                    <CardContent>
                        <Typography variant="h5" component="div" gutterBottom>
                            {data?.name}
                        </Typography>
                        <Typography variant="body1" color="text.secondary">
                            {data?.location}
                        </Typography>
                    </CardContent>
                </Box>

                {/* Divider */}
                <Divider orientation="vertical" flexItem sx={{ display: { xs: 'none', md: 'block' }, marginRight: 2 }} />
                <Divider orientation="horizontal" flexItem sx={{ display: { xs: 'block', md: 'none' }, marginBottom: 2 }} />

                {/* Right Column: Ratings and Reviews */}
                <Box sx={{ flex: 1 }}>
                    {siteRatings.length > 0 ? (
                        <div>
                            <ul>
                                {siteRatings.map(([website, rating, reviews], index) => (
                                    <li key={index} style={{ marginBottom: '16px' }}>
                                        {rating ? (
                                            <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                                <img
                                                    src={getLogoForWebsite(website)}
                                                    alt={`${website} Logo`}
                                                    style={{ width: '150px', minWidth: '150px', marginRight: '16px' }} // Added minWidth
                                                />
                                                <Rating
                                                    value={rating}
                                                    precision={0.5}
                                                    readOnly
                                                    icon={<StarIcon style={{ color: '#FFD700' }} />}
                                                    sx={{ marginLeft: '8px' }}
                                                />
                                                <Typography sx={{ marginLeft: '8px' }}>
                                                    <span style={{ color: 'black' }}>{rating}</span>
                                                    <span style={{ color: 'gray' }}> ({reviews} reviews)</span>
                                                </Typography>
                                            </Box>
                                        ) : (
                                            <Typography>No ratings for {website}</Typography>
                                        )}
                                    </li>
                                ))}
                            </ul>

                            <Box sx={{ display: 'flex', alignItems: 'center', marginTop: 6.3 }}>
                                <Typography 
                                variant="h5" // make h6 if mobile
                                component="div" sx={{ marginRight: '16px', minWidth: '150px', }}> {/* Added minWidth */}
                                    Overall Rating:
                                </Typography>
                                <Rating
                                    value={starAverage}
                                    precision={0.5}
                                    readOnly
                                    icon={<StarIcon style={{ color: '#FFD700' }} />}
                                />
                                <Typography sx={{ marginLeft: '8px' }}>
                                    <span style={{ color: 'black' }}>{starAverage}</span>
                                    <span style={{ color: 'gray' }}> ({totalReviewCount} reviews)</span>
                                </Typography>
                            </Box>
                        </div>
                    ) : (
                        <Typography>No ratings found.</Typography>
                    )}
                </Box>
            </Box>
        </Card>
    );
}

export default RatingResultsDesktop;