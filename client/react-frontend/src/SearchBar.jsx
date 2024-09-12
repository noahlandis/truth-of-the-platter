import React, { useState } from 'react';
import { Paper, InputBase, IconButton, Box } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import ClearIcon from '@mui/icons-material/Clear';

function SearchBar() {
  const [name, setName] = useState('');
  const [location, setLocation] = useState('');

  const handleClearName = () => setName('');
  const handleClearLocation = () => setLocation('');

  return (
    <Paper
      component="form"
      sx={{
        display: 'flex',
        alignItems: 'center',
        width: '100%',
        maxWidth: 1100,
        borderRadius: '8px',
        backgroundColor: '#fff',
        boxShadow: '0px 4px 12px rgba(0, 0, 0, 0.1)',
        border: '1px solid #ccc',
      }}
    >
      <Box sx={{ position: 'relative', flex: 1 }}>
        <InputBase
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Name"
          sx={{
            ml: 2,
            width: '100%',
            flex: 1,
          }}
          inputProps={{ 'aria-label': 'name' }}
        />
        {name && (
          <IconButton
            onClick={handleClearName}
            sx={{
              position: 'absolute',
              right: 0,
              top: '50%',
              transform: 'translateY(-50%)',
              padding: 0,
            }}
            aria-label="clear name"
          >
            <ClearIcon fontSize="small" />
          </IconButton>
        )}
      </Box>
      
      <Box
        sx={{
          height: '40px',
          width: '1px',
          backgroundColor: '#ccc',
          mx: 2,
        }}
      />

      <Box sx={{ position: 'relative', flex: 1 }}>
        <InputBase
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          placeholder="Location"
          
          sx={{
            flex: 1,
            width: '100%',

            
          }}
          inputProps={{ 'aria-label': 'location' }}
        />
        {location && (
          <IconButton
            onClick={handleClearLocation}
            sx={{
              position: 'absolute',
              right: 20,
              top: '50%',
              transform: 'translateY(-50%)',
              padding: 0,
            }}
            aria-label="clear location"
          >
            <ClearIcon fontSize="small" />
          </IconButton>
        )}
      </Box>

      <IconButton
        type="submit"
        sx={{
          p: '10px',
          backgroundColor: '#1976d2',
          borderRadius: '0 8px 8px 0',
          color: '#fff',
        }}
        aria-label="search"
      >
        <SearchIcon />
      </IconButton>
    </Paper>
  );
}

export default SearchBar;
