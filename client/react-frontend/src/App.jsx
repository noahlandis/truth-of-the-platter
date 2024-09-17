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
      label: 'Search for Restaurants',
      description: 'Start by entering a restaurant name and location to find places near you.',
      icon: <SearchIcon sx={{ fontSize: 50, color: '#1976d2' }} />,
    },
    {
      label: 'Select a Restaurant',
      description: 'Choose a restaurant from the list of search results to view detailed ratings.',
      icon: <RestaurantIcon sx={{ fontSize: 50, color: '#1976d2' }} />,
    },
    {
      label: 'Check Ratings',
      description: 'View aggregated ratings and reviews from different sites to help you decide.',
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