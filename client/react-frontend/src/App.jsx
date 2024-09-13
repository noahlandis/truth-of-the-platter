import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Layout from './Layout';  // Import your Layout component

function Home() {
  return <h1>Home</h1>;
}

function Search() {
  return <h1>Search</h1>;
}

function Result() {
  return <h1>Result</h1>;
}

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/search" element={<Search />} />
          <Route path="/result" element={<Result />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
