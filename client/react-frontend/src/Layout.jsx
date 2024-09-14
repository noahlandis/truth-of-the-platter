import Header from './Header';

function Layout({ children }) {
  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-b from-white to-red-500">
      {/* Common Header */}
      <div className="p-4 mt-10">
      <Header />
      </div>

      {/* Page Content */}
     
      {/* Page Content */}
      <main className="flex justify-center flex-grow p-4"> {/* Added flex and justify-center */}
        <div className="w-full max-w-7xl"> {/* This div ensures a max width to center the content */}
          {children} {/* This is where the routed page content will go */}
        </div>
        </main>

    </div>
  );
}

export default Layout;