import { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { CircularProgress, Rating, Box, Typography } from '@mui/material';

function RatingResults() {
    const location = useLocation();
    const { data } = location.state || {}; // Get the entire data object from location.state

    const [siteRatings, setSiteRatings] = useState([]);
    const [starAverage, setStarAverage] = useState(null);
    const [totalReviewCount, setTotalReviewCount] = useState(null);
    const [loading, setLoading] = useState(false);  // Update loading state
    const [error, setError] = useState(null);

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
                    <ul className="space-y-4 text-2xl font-semibold">
                        {siteRatings.map(([website, rating, reviews], index) => (
                            <li key={index}>
                                {rating ? (
                                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                        <Typography sx={{ marginRight: '5px' }}>{website} - </Typography>
                                        <Rating
                                            value={rating}
                                            precision={0.5}
                                            readOnly

                                        />
                                        <Typography sx={{ marginLeft: '5px' }}>
                                            {rating} ({reviews} reviews)
                                        </Typography>
                                    </Box>
                                ) : (
                                    <Typography>{website} - Ratings could not be found for this site</Typography>
                                )}
                            </li>
                        ))}

                    </ul>
                    <h3 className="mt-10 text-3xl font-semibold underline">Overall</h3>
<div className="text-2xl font-semibold">
    <Box sx={{ display: 'flex', alignItems: 'center' }}>
        <Rating value={starAverage} precision={0.5} readOnly />
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
