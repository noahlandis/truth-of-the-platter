import Header from './Header';

function Layout({ children }) {
  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-b from-white to-red-500">
      {/* Common Header */}
      <div className="p-4 mt-8">
      <Header />
      </div>

      {/* Page Content */}
      <main className="flex-grow p-4">
        {children} {/* This is where the routed page content will go */}
      </main>

    </div>
  );
}

export default Layout;