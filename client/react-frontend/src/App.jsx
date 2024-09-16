import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Layout from './Layout';  // Import your Layout component
import MatchList from './MatchList';  // Import your MatchList component
import RatingResults from './RatingResults';  // Import your RatingResults component

function Home() {
  return <h1>Home</h1>;
}

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/search" element={<MatchList />} />
          <Route path="/ratings" element={<RatingResults />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;