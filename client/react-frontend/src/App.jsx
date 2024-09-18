import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Layout from './Layout';  // Import your Layout component
import MatchList from './MatchList';  // Import your MatchList component
import RatingResults from './RatingResults';  // Import your RatingResults component

import { Box, Typography, Paper, Stepper, Step, StepLabel } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import RestaurantIcon from '@mui/icons-material/Restaurant';
import StarRateIcon from '@mui/icons-material/StarRate';

function Home() {
  const steps = [
    {
      label: 'Find Restaurants Near RANDOM NAME',
      description: 'Enter a restaurant name or use automatic location detection to discover places around you.',
      icon: <SearchIcon sx={{ fontSize: 50, color: '#1976d2' }} />,
    },
    {
      label: 'Choose a Restaurant',
      description: 'Browse through search results and select a restaurant to see detailed ratings from Yelp, Google, and TripAdvisor.',
      icon: <RestaurantIcon sx={{ fontSize: 50, color: '#1976d2' }} />,
    },
    {
      label: 'View Aggregated Ratings',
      description: 'Check the weighted average rating and review counts from all platforms to make an informed decision.',
      icon: <StarRateIcon sx={{ fontSize: 50, color: '#1976d2' }} />,
    },
  ];
  
  

  return (
    <Box sx={{ display: 'flex', justifyContent: 'center' }}>
      <Paper elevation={3} sx={{ padding: 5, width: '80%', maxWidth: 600 }}>

        <Stepper orientation="vertical">
          {steps.map((step, index) => (
            <Step key={index} active>
              <StepLabel
                icon={step.icon}
                sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}
              >
                <Typography variant="h6">{step.label}</Typography>
              </StepLabel>
              <Typography sx={{ mb: 2, ml: 6 }}>{step.description}</Typography>
            </Step>
          ))}
        </Stepper>
      </Paper>
    </Box>
  );
}

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/search" element={<MatchList />} />
          <Route path="/ratings" element={<RatingResults />} />
          <Route path="*" element={<Home />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;