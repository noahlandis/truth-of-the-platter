import { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { CircularProgress, Rating, Box, Typography, Grid2, Card, CardContent, CardMedia, Divider } from '@mui/material';
import { useSearchParams } from "react-router-dom";
import { useNavigate } from 'react-router-dom';

import google from './assets/logos_png/google_logo.png'
import tripAdvisor from './assets/logos_png/trip_advisor_logo.png'
import yelp from './assets/logos_png/yelp_logo.png'

import StarIcon from '@mui/icons-material/Star'; // Import the star icon

function RatingResults() {
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
        <Card sx={{ display: 'flex', flexDirection: 'column', padding: 2, boxShadow: 3 }}>
            {/* Top Section: Photo, Name, Location */}
            <Box sx={{ width: '100%', marginBottom: 2 }}>
                <CardMedia
                    component="img"
                    sx={{ width: '100%', height: 250, borderRadius: '8px' }}
                    image={data?.imageUrl || google}
                    alt={`${data?.name}`}
                />
                <CardContent sx={{ paddingBottom: 0 }}> {/* Reduced bottom padding */}
                    <Typography variant="h6" component="div" gutterBottom>
                        {data?.name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                        {data?.location}
                    </Typography>
                </CardContent>
            </Box>

            {/* Horizontal Divider */}
            <Divider sx={{ marginTop: -2, marginBottom: 2 }} /> {/* Added negative top margin */}

            {/* Bottom Section: Ratings and Reviews */}
            <Box>
                {siteRatings.length > 0 ? (
                    <div>
                        <ul style={{ padding: 0, listStyle: 'none' }}>
                            {siteRatings.map(([website, rating, reviews], index) => (
                                <li key={index} style={{ marginBottom: '24px' }}>
                                    {rating ? (
                                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                            <Box sx={{ 
                                                width: '140px', 
                                                marginRight: '16px', 
                                                display: 'flex', 
                                                alignItems: 'center', 
                                                justifyContent: 'flex-start',
                                                height: '48px'
                                            }}>
                                                <img
                                                    src={getLogoForWebsite(website)}
                                                    alt={`${website} Logo`}
                                                    style={{ 
                                                        maxWidth: website.toLowerCase() === 'google' ? '100%' : '85%', 
                                                        maxHeight: '100%', 
                                                        objectFit: 'contain'
                                                    }}
                                                />
                                            </Box>
                                            <Box sx={{ display: 'flex', flexDirection: 'column' }}>
                                                <Rating
                                                    value={rating}
                                                    precision={0.5}
                                                    readOnly
                                                    icon={<StarIcon style={{ color: '#FFD700' }} />}
                                                />
                                                <Typography variant="body2" sx={{ marginTop: '4px' }}>
                                                    <span style={{ color: 'black' }}>{rating}</span>
                                                    <span style={{ color: 'gray' }}> ({reviews} reviews)</span>
                                                </Typography>
                                            </Box>
                                        </Box>
                                    ) : (
                                        <Typography>No ratings for {website}</Typography>
                                    )}
                                </li>
                            ))}
                        </ul>

                        <Box sx={{ display: 'flex', alignItems: 'center', marginTop: 2 }}>
                            <Box sx={{ 
                                width: '140px', 
                                marginRight: '16px', 
                                display: 'flex', 
                                alignItems: 'center', 
                                justifyContent: 'flex-start',
                                height: '48px'
                            }}>
                                <Typography 
                                    variant="h6"
                                    component="div" 
                                    sx={{ fontWeight: 'bold' }}  // Added this line to make the text bold
                                >
                                    Overall
                                </Typography>
                            </Box>
                            <Box sx={{ display: 'flex', flexDirection: 'column' }}>
                                <Rating
                                    value={starAverage}
                                    precision={0.5}
                                    readOnly
                                    icon={<StarIcon style={{ color: '#FFD700' }} />}
                                />
                                <Typography variant="body2" sx={{ marginTop: '4px' }}>
                                    <span style={{ color: 'black' }}>{starAverage}</span>
                                    <span style={{ color: 'gray' }}> ({totalReviewCount} reviews)</span>
                                </Typography>
                            </Box>
                        </Box>
                    </div>
                ) : (
                    <Typography>No ratings found.</Typography>
                )}
            </Box>
        </Card>
    );
}

export default RatingResults;
