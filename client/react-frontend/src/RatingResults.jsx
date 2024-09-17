import { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { CircularProgress, Rating, Box, Typography } from '@mui/material';
import { useSearchParams } from "react-router-dom";
import { useNavigate } from 'react-router-dom';
import yelp from './assets/yelp.svg'; // Adjust the path based on your folder structure
import tripAdvisor from './assets/trip_advisor.png'; // Adjust the path based on your folder structure
import google from './assets/google.svg'; // Adjust the path based on your folder structure
import StarIcon from '@mui/icons-material/Star'; // Import the star icon

function RatingResults() {
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

    // Function to map website name to corresponding logo
    const getLogoForWebsite = (website) => {
        switch (website.toLowerCase()) {
            case 'yelp':
                return yelp;
            case 'tripadvisor':
                return tripAdvisor;
            case 'google':
                return google;
            default:
                return null; // Return null or a default placeholder logo if website is unrecognized
        }
    };

    useEffect(() => {
        // Redirect to /search if no data is available (opened directly from a link)
        if (!data && nameParam && locationParam) {
            navigate(`/search?name=${nameParam}&location=${locationParam}`);
        }
        if (!data) {
            navigate('/');
        }
    }, [data, nameParam, locationParam, navigate]);

    useEffect(() => {
        // Clear localStorage when new data (restaurant) is selected
        if (data) {
            localStorage.removeItem('siteRatings');
            localStorage.removeItem('starAverage');
            localStorage.removeItem('totalReviewCount');
        }

        const fetchRatings = async () => {
            setLoading(true);
            try {
                const response = await fetch('http://127.0.0.1:5000/select', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data), // Send the entire data object
                });

                if (!response.ok) {
                    throw new Error('Error fetching ratings');
                }

                const result = await response.json();
                setSiteRatings(result.site_ratings);
                setStarAverage(result.star_average);
                setTotalReviewCount(result.total_review_count);

                // Save the fetched data to localStorage
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
        return (
            <div className="flex items-center justify-center mt-20">
                <CircularProgress style={{ color: 'black' }} />
            </div>
        );
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

    return (
        <div>
            <h1 className="items-start mb-4 text-3xl font-bold">
                Showing results for <em>{data?.name} - {data?.location}</em>
            </h1>

            {siteRatings.length > 0 ? (
                <div>
                    <ul className="space-y-12 text-2xl font-semibold ">
                        {siteRatings.map(([website, rating, reviews], index) => (
                            <li key={index}>
                                {rating ? (
                                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                        <div className="flex items-center w-full">
                                            {/* Fixed width container for the logo */}
                                            <div className="flex-shrink-0 w-[150px] h-[100px">
                                                <img
                                                    src={getLogoForWebsite(website)}
                                                    alt={`${website} Logo`}
                                                    className="object-contain w-full h-full align-middle"
                                                />
                                            </div>
                                            {/* Flexible container for the rating and review count */}
                                            <div className="flex items-center flex-grow ml-4">
                                                <Rating
                                                    value={rating}
                                                    precision={0.5}
                                                    readOnly
                                                    icon={<StarIcon style={{ color: '#FFF700' }} />} // Bright yellow stars
                                                    emptyIcon={<StarIcon style={{ color: 'rgba(255, 255, 255, 0.5)' }} />} // Semi-transparent white stars
                                                />
                                                <Typography sx={{ marginLeft: '5px' }}>
                                                    {rating} ({reviews} reviews)
                                                </Typography>
                                            </div>
                                        </div>
                                    </Box>
                                ) : (
                                    <Typography>{website} - Ratings could not be found for this site</Typography>
                                )}
                            </li>
                        ))}
                    </ul>

                    <div className="mt-20 text-2xl font-semibold">
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                            <Typography sx={{ marginRight: '5px' }} variant="h3" className="mt-10 text-3xl font-semibold">
                                Overall
                            </Typography>
                            <Rating
                                value={starAverage}
                                precision={0.5}
                                readOnly
                                icon={<StarIcon style={{ color: '#FFF700' }} />} // Bright yellow stars for overall rating
                                emptyIcon={<StarIcon style={{ color: 'rgba(255, 255, 255, 0.5)' }} />} // Semi-transparent white stars
                            />
                            <Typography sx={{ marginLeft: '5px' }}>
                                {starAverage} ({totalReviewCount} reviews)
                            </Typography>
                        </Box>
                    </div>

                </div>
            ) : (
                <p>No ratings found.</p>
            )}
        </div>
    );
}

export default RatingResults;
